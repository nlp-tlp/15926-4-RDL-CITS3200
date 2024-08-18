#!/bin/bash

echo -e "\nSetting up the project..."

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

# Create Python virtual environment and install dependencies from requirements.txt
echo -e "\n\nSetting up Python virtual environment and installing dependencies..."
python3 -m venv src/server/venv
source src/server/venv/bin/activate
pip install -r src/server/requirements.txt

# Install Node.js dependencies in src/client
echo -e "\n\nInstalling Node.js dependencies in src/client..."
npm install --prefix src/client

# Create a .env file for Docker Compose in /src
echo -e "\n\nCreating .env file for Docker Compose in /src..."
cat <<EOF > src/.env
# Environment variables for Docker Compose
COMPOSE_PROJECT_NAME=iso-visualiser

# For client service
CLIENT_PORT=5173

# For server service
SERVER_PORT=5000
FLASK_ENV=development
FLASK_APP=server.py

# Add other environment variables as needed
EOF

echo -e "\n\nSetup complete."
