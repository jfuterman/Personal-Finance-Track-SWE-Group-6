FROM python:3.12

WORKDIR /app

COPY . /app/.

RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1


# Only needed for production:
ENV PORT=80
EXPOSE 80
# Copy entrypoint script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
# Set the entrypoint script as the command to run when the container starts
ENTRYPOINT ["/app/entrypoint.sh"]