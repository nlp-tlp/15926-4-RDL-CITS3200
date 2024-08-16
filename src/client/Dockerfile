# Base image
FROM node:22-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy project files
COPY . .

# Build the project
RUN npm run build

# Expose port
EXPOSE 5173

# Development run
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]