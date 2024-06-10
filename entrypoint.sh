#!/bin/bash

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser if not exists
echo "from django.contrib.auth import get_user_model; User = get_user_model(); import os; User.objects.filter(email=os.environ['DJANGO_SUPERUSER_EMAIL']).exists() or User.objects.create_superuser(os.environ['DJANGO_SUPERUSER_USERNAME'], os.environ['DJANGO_SUPERUSER_EMAIL'], os.environ['DJANGO_SUPERUSER_PASSWORD'])" | python manage.py shell

# Start server
exec "$@"
