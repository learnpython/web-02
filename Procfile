web: gunicorn -b 0.0.0.0:$PORT -b [::1]:$PORT -k ${GUNICORN_WORKER_TYPE:-sync} -t ${GUNICORN_TIMEOUT:-30} --graceful-timeout=${GUNICORN_TIMEOUT:-30} --keep-alive=${GUNICORN_KEEP_ALIVE:-4} -w ${GUNICORN_WORKERS:-4} chitatel.wsgi:application
dev: python manage.py runserver_plus 0.0.0.0:$PORT
