#!/bin/bash

sleep 3
python manage.py makemigrations --settings=core.settings.production
python manage.py migrate --settings=core.settings.production
python manage.py generate_dummy_teachers --settings=core.settings.production
python manage.py generate_dummy_students --settings=core.settings.production
python manage.py generate_super_user --settings=core.settings.production
python manage.py runserver 0.0.0.0:8080 --settings=core.settings.production
