# This file determines based on the environmental variable for pipeline whether
# this is running in production or development and chooses the appropriate settings 
#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

if [ "$PIPELINE" != "production" ]; then
  echo "Starting Django development server..."
  exec python manage.py runserver 0.0.0.0:8000
else
    echo "Collecting static files..."
    # Collect static files - use --noinput to prevent prompts
    python manage.py collectstatic --noinput
    
    echo "Starting Gunicorn..."
    exec gunicorn wealthwise.wsgi:application --bind 0.0.0.0:$PORT
fi
