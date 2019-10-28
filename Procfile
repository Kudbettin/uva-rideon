release: rm -rf */migrations/0*.py
release: python manage.py makemigrations
release: manage.py migrate
web: gunicorn RideOn.wsgi
