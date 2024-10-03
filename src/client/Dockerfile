# Base image
FROM node:20-slim

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

RUN npm install -g serve

# Development run
CMD ["serve", "-s", "dist", "-l", "5173"]