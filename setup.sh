#!/bin/bash

# Check if the script is being run with sudo
if [ ! -z "$SUDO_USER" ]; then
    echo -e "\nThis script should not be run with sudo. Please run it as a regular user."
    exit 1
fi

# Check if nvm is installed
if ! command -v nvm &> /dev/null
then
    echo -e "\n\nnvm not found. Installing nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

    # Load nvm after installation
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
else
    # Load nvm if it's already installed
    echo -e "\n\nnvm found. Loading nvm..."
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
fi

# Use Node.js version 20
echo -e "\n\nSwitching to Node.js version 20..."
nvm install 20
nvm use 20

# Check if npm is installed
if ! command -v npm &> /dev/null
then
    echo -e "\n\nnpm is not installed. Please install Node.js properly."
    exit 1
else
    echo -e "\n\nnpm found. Proceeding with installation..."
fi

# Install Node.js dependencies in the main directory
echo -e "\n\nInstalling Node.js dependencies in the main directory..."
npm install

# Set up Husky
echo -e "\n\nSetting up Husky..."
npx husky-init

# Add pre-commit hook
echo -e "\n\nAdding pre-commit hook to Husky..."
sed -i '/npm test/d' .husky/pre-commit
npx husky add .husky/pre-commit \
  "cd src/client && npm run lint:fix && npm run format && npm run type-check && \
  cd ../../src/server && . venv/bin/activate && black . && deactivate"

# Check if python3-venv is installed
if ! dpkg -s python3-venv &> /dev/null
then
    echo -e "\n\npython3-venv is not installed. Please install it with 'sudo apt install python3-venv' and rerun this script."
    exit 1
fi

# Create Python virtual environment and install dependencies from requirements.txt
echo -e "\n\nSetting up Python virtual environment and installing dependencies..."
python3 -m venv src/server/venv
source src/server/venv/bin/activate
pip install -r src/server/requirements.txt

# Install Node.js dependencies in src/client
echo -e "\n\nInstalling Node.js dependencies in src/client..."
npm install --prefix src/client

# Copy .env.example to .env in /src
echo -e "\n\nCopying .env.example to .env in /src..."
cp src/.env.example src/.env

echo -e "\n\nSetup complete."
