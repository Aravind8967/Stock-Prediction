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
    vim \
    gnupg \
    python3 \
    dos2unix \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama using the installer script
RUN curl -fsSL https://ollama.com/install.sh | sh

RUN dos2unix StartApp.sh \
    && chmod 777 StartApp.sh

RUN pip3 install -r requirements.txt

# Start Ollama in the background, wait, then pull the model and kill the background process
RUN ollama serve & \
    sleep 5 && \
    ollama pull smollm2:135m && \
    pkill -f "ollama serve"

EXPOSE 80

CMD ["sh", "StartApp.sh"]