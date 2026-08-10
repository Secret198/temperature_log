FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py models.py ./
COPY templates/ ./templates/

# Expose Flask port
EXPOSE 5000

# Run with Gunicorn production server bound to 0.0.0.0
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]