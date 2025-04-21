# Stage 1: Build the React app using Node
FROM node:18 AS builder

# Set working directory
WORKDIR /app

# Copy dependency files and install dependencies
COPY package*.json ./
RUN npm install

# Copy all source files into the container
COPY . .

# Build the production files (this will create the /app/dist directory)
RUN npm run build

# Stage 2: Serve the app using Nginx
FROM nginx

RUN apt-get update ; apt-get install -y vim sudo nano

# Remove the default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy your custom Nginx configuration file into the container
COPY nginx.conf /etc/nginx/conf.d

RUN rm -rf /usr/share/nginx/html/*

# Copy the built files from the builder stage to Nginx’s HTML directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 where the app will be served
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]