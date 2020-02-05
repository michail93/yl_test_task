echo "The running of app"
python manage.py migrate
python manage.py test
python manage.py runserver 0.0.0.0:8000