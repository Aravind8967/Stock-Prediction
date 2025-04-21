# Use an official Ubuntu image as the base
FROM ubuntu:22.04

# Disable interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY . /app

# Install required packages
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    gnupg \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama using the installer script
RUN curl -fsSL https://ollama.com/install.sh | sh


RUN pip3 install -r requirements.txt

# Start Ollama in the background, wait, then pull the model and kill the background process
RUN ollama serve & \
    sleep 5 && \
    ollama pull smollm2:135m && \
    pkill -f "ollama serve"


RUN chmod 755 *

# Expose the port Ollama uses (11434 is used in this example)
EXPOSE 80

# At runtime, start Ollama server as the main process
CMD ["sh", "StartApp.sh"]
