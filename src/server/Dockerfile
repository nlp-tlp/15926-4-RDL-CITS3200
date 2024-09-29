# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Setup CLI to be executable
RUN chmod +x /app/cli.py

# Expose port
EXPOSE 5000

# Run the app and bind to all interfaces
CMD ["flask", "run", "--host=0.0.0.0"]
