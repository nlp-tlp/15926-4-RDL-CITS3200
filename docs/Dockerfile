# Use an official Python image as a base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /docs

# Copy the current directory contents into the container at /docs
COPY . /docs

# Install MkDocs and any necessary plugins
RUN pip install mkdocs mkdocs-material

# Expose the port MkDocs will serve on
EXPOSE 8000

# Run MkDocs when the container launches
CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]
