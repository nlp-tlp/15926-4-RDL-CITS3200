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

# Use Node.js version 22
echo "Switching to Node.js version 22..."
nvm install 22
nvm use 22

# Install Python dependencies
echo "Installing Python dependencies..."
pip install black

# Navigate to the client directory and install Node.js dependencies
echo "Installing Node.js dependencies..."
cd src/client || exit
npm install

echo "Setup complete."
