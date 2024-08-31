# ./db/Dockerfile

# Use the Virtuoso Open-Source Edition as the base image
FROM openlink/virtuoso-opensource-7:7.2

# Expose the necessary ports
EXPOSE 1111
EXPOSE 8890

# Set the working directory to the database directory
WORKDIR /opt/virtuoso-opensource/database

# Set the volume for the database
VOLUME ["/opt/virtuoso-opensource/database"]

# Set the default command to run Virtuoso
CMD ["virtuoso-t", "+wait", "+foreground"]
