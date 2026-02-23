# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy the application
COPY . .

# Expose the default Gradio port
ENV PORT=7860
EXPOSE $PORT

# Default command — Gradio auto-starts
CMD ["python", "app.py"]