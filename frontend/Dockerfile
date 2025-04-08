# This is the Dockerfile for the frontend service.
FROM node:18

WORKDIR /app

# Find the dependencies
COPY package*.json ./

# Import the dependencies
RUN npm install

COPY . .

# Run the server
CMD ["npm", "start"]
