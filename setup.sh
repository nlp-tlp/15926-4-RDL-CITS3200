#!/bin/bash

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pip install pre-commit
pre-commit install
echo "Setup complete. Pre-commit hooks are installed."

# Other stuff....