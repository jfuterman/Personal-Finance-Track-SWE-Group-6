# Dockerfile runs on build. 
FROM python:3.12

# Set working directory inside container
WORKDIR /Personal-Finance-Track-SWE-Group-6

# Install dependencies from requirements.txt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy project into container
COPY . .

