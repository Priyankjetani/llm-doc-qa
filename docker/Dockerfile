# Start from official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (Docker caches this layer — faster rebuilds)
COPY requirements.txt .

# Install all Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire project into the container
COPY . .

# Expose port 8000
EXPOSE 8000

# Command to run your app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]