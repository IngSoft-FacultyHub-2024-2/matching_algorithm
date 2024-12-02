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

# Expose the port that FastAPI will run on
EXPOSE 8000

# Set the command to run FastAPI app using uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]

# Set the entrypoint to bash
# ENTRYPOINT ["/bin/bash"]

