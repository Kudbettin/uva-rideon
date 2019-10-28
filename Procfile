release: rm -rf */migrations/0*.py
python manage.py makemigrations
python manage.py migrate
web: gunicorn RideOn.wsgi
