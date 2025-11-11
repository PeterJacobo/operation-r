FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y libusb-1.0-0
# Install curl (if not already present)
RUN apt-get update && apt-get install -y curl unzip

# Download and install ngrok binary (detect architecture)
RUN ARCH=$(dpkg --print-architecture) && \
    if [ "$ARCH" = "arm64" ] || [ "$ARCH" = "armhf" ]; then \
        NGROK_ARCH="linux-arm64"; \
    else \
        NGROK_ARCH="linux-amd64"; \
    fi && \
    curl -s https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-${NGROK_ARCH}.tgz -o ngrok.tgz && \
    tar -xzf ngrok.tgz -C /usr/local/bin && \
    rm ngrok.tgz
 

COPY . .
COPY entrypoint.sh /entrypoint.sh
# Convert line endings from CRLF to LF
RUN sed -i 's/\r$//' /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
