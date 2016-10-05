#!/bin/sh

#install machine dependencies
sudo apt-get install virtualenv

#create and activate virtual environment
virtualenv venv
source venv/bin/activate

#install pip dependencies
pip2 install -r requirements.txt

#make the django database
python2 manage.py migrate

#set environment variables
export ENVIRONMENT=local

#run the local environment
python2 manage.py runserver
