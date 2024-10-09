# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Copy project files
COPY . .

# Setup CLI to be executable
RUN chmod +x /app/cli.py

# Expose port
EXPOSE 5000

# Use Gunicorn to serve the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:flaskApp"]
