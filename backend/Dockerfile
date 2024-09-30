# Use a multi-stage build to create a smaller final image
FROM node:14 AS build

# Set working directory for frontend
WORKDIR /app/frontend

# Copy frontend files
COPY frontend/bridge-ui/package*.json ./
COPY frontend/bridge-ui/ ./

# Install dependencies and build the React app
RUN npm install
RUN npm run build

FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gunicorn

# Install Python dependencies
COPY backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the backend application code
COPY backend .

# Copy built frontend files from the previous stage
COPY --from=build /app/frontend/build /app/frontend/bridge-ui/build

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
