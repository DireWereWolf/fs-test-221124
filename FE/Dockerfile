# Step 1: Build Angular application
FROM node:20 AS builder

# Set the working directory
WORKDIR /app

# Copy only the necessary files to install dependencies
COPY package*.json ./

# Install dependencies (with --legacy-peer-deps for compatibility issues)
RUN npm install --legacy-peer-deps

# Copy the rest of the application source code
COPY . .

# Build the Angular application for production
RUN npm run build:prod

# Step 2: Serve Angular application
FROM node:20-slim AS runtime

# Set the working directory
WORKDIR /app

# Copy only the necessary files to install dependencies
COPY package*.json ./

# Install all dependencies (to ensure compatibility)
RUN npm install --legacy-peer-deps

# Prune development dependencies to reduce image size
RUN npm prune --production

# Copy the built Angular app from the builder stage
COPY --from=builder /app/dist/fe/browser ./dist/fe/browser

# Copy the server.js file for serving the application
COPY server.js ./

# Expose the application's port
EXPOSE 9000

# Start the server
CMD ["node", "server.js"]
