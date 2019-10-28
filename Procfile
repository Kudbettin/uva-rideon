release: rm -rf */migrations/0*.py
release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn RideOn.wsgi
