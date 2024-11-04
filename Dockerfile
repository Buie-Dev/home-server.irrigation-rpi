# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the Python script into the container


# Install the Paho MQTT library
RUN pip install paho-mqtt
RUN pip install python-dotenv

COPY . .

