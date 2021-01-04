
FROM python:3.8-slim

# define environments
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Bundle app source
COPY . .

EXPOSE 8080
CMD ./start.sh
