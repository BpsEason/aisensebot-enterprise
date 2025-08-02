# Stage 1: Build the Vue application
FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine
# Copy the built files from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html
# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
