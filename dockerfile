
# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY docker_requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r docker_requirements.txt

# Copy the application code (all Python files from src and utils folders)
COPY src /app/src

COPY utils /app/utils/

# Create input and output directories
RUN mkdir -p /data/input_data
RUN mkdir -p /data/output_data


# Expose the port the app runs on (if needed)
EXPOSE 80


# Set the default command to run when starting the container
CMD ["python"]
