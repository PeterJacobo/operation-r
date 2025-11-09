FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y libusb-1.0-0
# Install curl (if not already present)
RUN apt-get update && apt-get install -y curl unzip

# Download and install ngrok binary
RUN curl -s https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-arm.zip -o ngrok.zip \
 && unzip ngrok.zip -d /usr/local/bin \
 && rm ngrok.zip
 

COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
