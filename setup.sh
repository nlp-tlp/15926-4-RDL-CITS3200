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
echo -e "\n\n>>> Switching to Node.js version 20..."
nvm install 20
nvm use 20

# Check if npm is installed
if ! command -v npm &> /dev/null
then
    echo -e "\n\n>>> npm is not installed. Please install Node.js properly."
    exit 1
else
    echo -e "\n\n>>> npm found. Proceeding with installation..."
fi

# Install Node.js dependencies in the main directory
echo -e "\n\n>>> Installing Node.js dependencies in the main directory..."
npm install

# Set up Husky
echo -e "\n\n>>> Setting up Husky..."
npx husky-init

# Add pre-commit hook
echo -e "\n\n>>> Adding pre-commit hook to Husky..."
cp .husky/pre-commit.example .husky/pre-commit

# Check if python3-venv is installed
if ! dpkg -s python3-venv &> /dev/null
then
    echo -e "\n\npython3-venv is not installed. Please install it with 'sudo apt install python3-venv' and rerun this script."
    exit 1
fi

# Create Python virtual environment and install dependencies from requirements.txt
echo -e "\n\n>>> Setting up Python virtual environment and installing dependencies..."
python3 -m venv src/server/venv
source src/server/venv/bin/activate
pip install -r src/server/requirements.txt

# Install Node.js dependencies in src/client
echo -e "\n\n>>> Installing Node.js dependencies in src/client..."
npm install --prefix src/client

# Copy .env.example to .env in /src
echo -e "\n\n>>> Copying .env.example to .env in /src..."
cp src/.env.example src/.env


# Append custom package update logic to the activate scripts
echo -e "\n\n>>> Adding package update logic to activate scripts..."

# Append to the `activate` script
cat << 'EOF' >> src/server/venv/bin/activate
# Automatically update packages upon activation
REQUIREMENTS_FILE="$VIRTUAL_ENV/../requirements.txt"

if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Updating packages based on 'requirements.txt' before activating..."
    pip install --quiet --requirement "$REQUIREMENTS_FILE"
    echo "Packages updated."
else
    echo "Requirements file not found at '$REQUIREMENTS_FILE'"
    echo "Aborting activation."
    deactivate  # Deactivate the virtual environment if it was partially activated
    return 1  # Exit script with an error code
fi
EOF

# Append to the `activate.csh` script
cat << 'EOF' >> src/server/venv/bin/activate.csh
# Automatically update packages upon activation
set REQUIREMENTS_FILE="$VIRTUAL_ENV/../requirements.txt"

if ( -f "$REQUIREMENTS_FILE" ) then
    echo "Updating packages based on 'requirements.txt' before activating..."
    pip install --quiet --requirement "$REQUIREMENTS_FILE"
    echo "Packages updated."
else
    echo "Requirements file not found at '$REQUIREMENTS_FILE'"
    echo "Aborting activation."
    deactivate  # Deactivate the virtual environment if it was partially activated
    exit 1  # Exit script with an error code
endif
EOF

# No support for fish terminal activation

echo -e "\n\nSetup complete."
