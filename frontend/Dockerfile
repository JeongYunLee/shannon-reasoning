# Step 1: Build the application
FROM node:20.19-bullseye AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json first
COPY package*.json ./

# Clean install dependencies
RUN rm -rf node_modules package-lock.json && npm install

# Copy the rest of the application files
COPY . .

# Build the application
RUN npm run build

# Step 2: Run the application
FROM node:20.19-bullseye

# Set working directory
WORKDIR /app

# Copy only the necessary files from the build stage
COPY --from=builder /app/.output /app/.output

# Install only production dependencies
COPY package*.json ./
RUN npm install --omit=dev

# Expose the port the app runs on
EXPOSE 3000

# Start the Nuxt application
CMD ["node", ".output/server/index.mjs"]