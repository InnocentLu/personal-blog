web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn my_blog.wsgi --bind 0.0.0.0:${PORT:-8000}
