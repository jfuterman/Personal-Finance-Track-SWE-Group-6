#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

if [ "$PIPELINE" = "development" ]; then
  echo "Starting Django development server..."
  exec python manage.py runserver 0.0.0.0:$PORT
else
    echo "Collecting static files..."
    # Collect static files - use --noinput to prevent prompts
    python manage.py collectstatic --noinput
    
    echo "Starting Gunicorn..."
    exec gunicorn wealthwise.wsgi:application --bind 0.0.0.0:$PORT
fi
