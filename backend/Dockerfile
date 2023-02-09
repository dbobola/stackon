# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Run migrations and start the backend server
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
