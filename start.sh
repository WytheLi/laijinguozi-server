python manage.py celery -A laijinguozi worker --loglevel=info > /opt/logs/django.log &
python manage.py celery beat --loglevel=info > /opt/logs/django.log &
python manage.py runserver 0.0.0.0:8000
