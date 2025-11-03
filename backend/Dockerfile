# ------------ Dockerfile (backend) ------------
# Use an official Python image
FROM python:3.12-slim

# Create working directory inside container
WORKDIR /app

# Prevent .pyc files and use unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements first, then install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Expose Flask port
EXPOSE 5002

# Set the default command
CMD ["python", "app.py"]