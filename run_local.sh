#!/bin/sh
source venv/bin/activate
export ENVIRONMENT=local
python manage.py runserver
