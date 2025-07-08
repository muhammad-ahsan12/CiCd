# Use official Python image
FROM python:3.10

# Set working dir
WORKDIR /app

# Copy backend code
COPY backend/ /app

# Install deps
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
