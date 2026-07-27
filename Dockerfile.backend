# Base image
FROM python:3.12-slim

# Prevent Python from buffering output
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Port info
EXPOSE 8000

# Start application
CMD ["uvicorn", "src.api.api:app", "--host", "0.0.0.0", "--port", "8000"]