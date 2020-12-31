
FROM python:3.8

# define environments
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Bundle app source
COPY . .

EXPOSE 8080
CMD python -m http.server 8080
