# Base image
FROM node:20-slim AS build

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy project files
COPY . .

# Build the project
RUN npm run build

# Production image for nginx
FROM nginx:alpine

# Copy the nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built files from the previous build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for nginx
EXPOSE 80

# Start nginx server
CMD ["nginx", "-g", "daemon off;"]