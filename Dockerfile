# The Dockerfile runs on the web service build command. It imports the requirements, 
# establishes listening ports, and runs entrypoint.sh.  
FROM python:3.12

WORKDIR /app

COPY . /app/.

RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENV PORT=80
EXPOSE 80
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]