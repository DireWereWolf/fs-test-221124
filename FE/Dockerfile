# Step 1: Build Angular application
FROM node:20 AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json for dependency installation
COPY package*.json ./

# Install dependencies (with --legacy-peer-deps for compatibility issues)
RUN npm install --legacy-peer-deps

# Copy the rest of the application source code
COPY . .

# Build the Angular application for production
RUN npm run build:prod

# Step 2: Serve Angular application
FROM node:20-slim

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json for production dependencies
COPY package*.json ./

# Install production dependencies only (including express)
RUN npm install --legacy-peer-deps --only=production

# Debug: Check if express is installed correctly
RUN ls -l node_modules/express

# Copy the built Angular app from the builder stage
COPY --from=builder /app/dist/fe/browser /app/dist/fe/browser

# Copy the server.js file
COPY server.js ./

# Expose the application's port
EXPOSE 9000

# Run the application
CMD ["node", "server.js"]
