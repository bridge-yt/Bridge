FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gunicorn

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=api.bridge:app
ENV FLASK_ENV=production

# Initialize and migrate the database
RUN flask db init || true  # Initialize migrations if not already done
RUN flask db migrate -m "Initial migration." || true  # Migrate database schema
RUN flask db upgrade || true  # Apply migrations

# Expose the port
EXPOSE 8000

# Set the command to run the application
CMD ["gunicorn", "api.bridge:app", "--bind", "0.0.0.0:8000"]
