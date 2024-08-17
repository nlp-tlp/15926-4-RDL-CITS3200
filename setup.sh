#!/bin/bash

echo "Setting up the project..."

# Check if nvm is installed
if ! command -v nvm &> /dev/null
then
    echo "nvm not found. Installing nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

    # Load nvm after installation
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
else
    # Load nvm if it's already installed
    echo "nvm found. Loading nvm..."
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
fi

# Use Node.js version 20
echo "Switching to Node.js version 20..."
nvm install 20
nvm use 20

# Check if npm is installed
if ! command -v npm &> /dev/null
then
    echo "npm is not installed. Please install Node.js properly."
    exit 1
else
    echo "npm found. Proceeding with installation..."
fi

# Install Node.js dependencies in the main directory
echo "Installing Node.js dependencies in the main directory..."
npm install

# Set up Husky
echo "Setting up Husky..."
npx husky install

# Install Python dependencies
echo "Installing Python dependencies..."
pip install black

# Navigate to the client directory and install Node.js dependencies
echo "Installing Node.js dependencies in src/client..."
cd src/client || exit
npm install

echo "Setup complete."
