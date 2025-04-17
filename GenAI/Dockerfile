# Use an official Ubuntu image as the base
FROM ubuntu:22.04

# Disable interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install required packages
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama using the installer script
RUN curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama in the background, wait, then pull the model and kill the background process
RUN ollama serve & \
    sleep 5 && \
    ollama pull smollm2:135m && \
    pkill -f "ollama serve"

# Expose the port Ollama uses (11434 is used in this example)
EXPOSE 11434

# At runtime, start Ollama server as the main process
CMD ["ollama", "serve"]
