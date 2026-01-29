FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Pillow
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and other files
COPY . .

# Expose Streamlit port
EXPOSE 3004

# Run streamlit
CMD ["streamlit", "run", "src/app.py", "--server.port", "3004", "--server.address", "0.0.0.0"]
