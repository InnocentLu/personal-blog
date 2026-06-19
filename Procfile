build: python manage.py collectstatic --noinput && python manage.py migrate --noinput
web: gunicorn my_blog.wsgi --bind 0.0.0.0:${PORT:-8000} --log-file -
