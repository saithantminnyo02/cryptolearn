# Dockerfile

# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files (optional, for production)
RUN python manage.py collectstatic --noinput

# Run the Django app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "secureweb.wsgi:application"]