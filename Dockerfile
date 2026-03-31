# Use Python base image
FROM python:3.10
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy files
COPY . .

#install Newman
RUN npm install -g newman

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pymongo requests

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]