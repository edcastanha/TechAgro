#!/bin/sh
set -e

# Executa o mock para popular models
PYTHONPATH=. 
python manage.py migrate &&
python manage.py popular_mock &&
python manage.py collectstatic --noinput &&


