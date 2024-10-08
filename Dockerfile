# Use the official Python 3.11 image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . .

# Set the entrypoint to bash
ENTRYPOINT ["/bin/bash"]

# Set the command to run your app
# CMD ["python", "app/main.py"]
