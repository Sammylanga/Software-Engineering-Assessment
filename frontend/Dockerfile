# Use the official Node.js image
FROM node:14-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the React app
RUN npm run build

# Expose the port the app runs on
EXPOSE 3000
# Set the startup command to run the React app
CMD ["npm", "start"]