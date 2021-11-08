# Wichteln
This project is aiming to make a wichteln draw.

## Dev
Local development can be done in gitpod. To start the app use 

```bash
python manage.py migrate && heroku local
```

It will show a local preview in the sidewindow. 
Deploy does not work from the gitpod right now. But you can clone the repo and use the following on your local machine:

```bash
heroku login
heroku git:remote -a sardinen-panda-wichteln
git push heroku main
```
*There is also this deploy button but I don't know how it works*
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)





# ------------------------ Documentation from forked project -------------------
# Python: Getting Started

A barebones Django app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python 3.10 [installed locally](https://docs.python-guide.org/starting/installation/). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/heroku/python-getting-started.git
$ cd python-getting-started

$ python3 -m venv getting-started
$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku main

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
