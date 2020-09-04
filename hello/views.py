import json
import os
import sqlite3

# Third-party libraries
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

from django.shortcuts import render
from django.http import HttpResponse

# Internal imports
from .models.db import init_db_command
from .models.user import User
from .models.models import Greeting

# Configuration
# GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
# GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_CLIENT_ID = "520031654361-a99671jbjlns0shl3sl224ikvuvbgul3.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "eZIZcRGH_oANx-XFNqKzhZSx"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Make this more robust and add error handling for Google API call in case it returns a failure
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

## ROUTES ##

## HOMEPAGE ##
@app.route("/")
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'

## LOGIN ##
@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

## LOGIN CALLBACK ##
@app.route("/login/callback")
def callback():
	# Get authorization code Google sent back to you
	code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for things on behalf of a user
	google_provider_cfg = get_google_provider_cfg()
	token_endpoint = google_provider_cfg["token_endpoint"]

	# Prepare and send a request to get tokens! Yay tokens!
	token_url, headers, body = client.prepare_token_request(
	    token_endpoint,
	    authorization_response=request.url,
	    redirect_url=request.base_url,
	    code=code
	)
	token_response = requests.post(
	    token_url,
	    headers=headers,
	    data=body,
	    auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
	)

	# Parse the tokens!
	client.parse_request_body_response(json.dumps(token_response.json()))

	# Now that you have tokens (yay) let's find and hit the URL
	# from Google that gives you the user's profile information,
	# including their Google profile image and email
	userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
	uri, headers, body = client.add_token(userinfo_endpoint)
	userinfo_response = requests.get(uri, headers=headers, data=body)

	# You want to make sure their email is verified.
	# The user authenticated with Google, authorized your
	# app, and now you've verified their email through Google!
	if userinfo_response.json().get("email_verified"):
	    unique_id = userinfo_response.json()["sub"]
	    users_email = userinfo_response.json()["email"]
	    picture = userinfo_response.json()["picture"]
	    users_name = userinfo_response.json()["given_name"]
	else:
	    return "User email not available or not verified by Google.", 400

	# Create a user in your db with the information provided
	# by Google
	user = User(
	    id_=unique_id, name=users_name, email=users_email, profile_pic=picture
	)

	# Doesn't exist? Add it to the database.
	if not User.get(unique_id):
	    User.create(unique_id, users_name, users_email, picture)

	# Begin user session by logging the user in
	login_user(user)

	# Send user back to homepage
	return redirect(url_for("index"))

## LOGOUT ##
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
