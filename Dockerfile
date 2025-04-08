# Dockerfile runs on build. It builds the image with
# the settings required.  
FROM python:3.12

# Set working directory inside container
WORKDIR /app

# Install dependencies from requirements.txt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy project into container
COPY . .

