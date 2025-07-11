# Use official Python image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Copy frontend code
COPY frontend/ /app

# Install deps
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
