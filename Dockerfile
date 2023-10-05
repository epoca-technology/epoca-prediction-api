# Extend Python's Slim Buster Image - Alpine is not compatible with TensorFlow
FROM python:3.10-slim-buster

# Create App Directory
WORKDIR /usr/src/app

# Add the Requirements File
ADD requirements.txt requirements.txt

# Update apt-get
# Upgrade PIP
# Install Postgres' Requirements & Build Tools
# Install the Project's Requirements
RUN apt-get update && \
    pip install --upgrade pip && \
    apt-get install -y libpq-dev gcc g++ && \
    pip install -r requirements.txt

# Copy the Project Files
ADD . .

# Expose the Port
EXPOSE 5000

# Initialize the API
CMD ["python", "dist/index.py"]