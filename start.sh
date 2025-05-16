#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Prompt for Google API Key
read -sp "Please enter your GOOGLE_API_KEY: " GOOGLE_API_KEY
echo # Add a newline after the hidden input

# Create .env file
echo "Creating .env file with your API_KEY..."
echo "GOOGLE_API_KEY=${GOOGLE_API_KEY}" > .env
echo ".env file created."
echo ""

# Virtual environment setup reminder
echo "--------------------------------------------------------------------------------"
echo "PYTHON VIRTUAL ENVIRONMENT SETUP"
echo "--------------------------------------------------------------------------------"

# Check if .venv directory exists
if [ ! -d ".venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv .venv
  if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment. Please ensure python3 and venv are installed."
    exit 1
  fi
else
  echo "Virtual environment .venv already exists."
fi

echo "Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
  echo "Error: Failed to activate virtual environment."
  exit 1
fi

echo "Virtual environment is active."
echo ""

# Install dependencies
echo "--------------------------------------------------------------------------------"
echo "INSTALLING DEPENDENCIES"
echo "--------------------------------------------------------------------------------"

# Check for uv and install if not present
if ! command -v uv &> /dev/null
then
    echo "uv not found. Attempting to install uv using pip..."
    pip install uv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install uv. Please install it manually and re-run the script."
        exit 1
    fi
    echo "uv installed successfully."
fi

if command -v uv &> /dev/null
then
    echo "uv found. Installing dependencies using 'uv pip sync uv.lock'..."
    uv pip sync uv.lock
else
    echo "uv not found. Attempting to install dependencies using pip..."
    if [ -f "requirements.txt" ]; then
        echo "requirements.txt found. Installing with 'pip install -r requirements.txt'..."
        pip install -r requirements.txt
    elif [ -f "pyproject.toml" ]; then
        echo "pyproject.toml found. You might need to install dependencies using a tool like pip or poetry."
        echo "For example: pip install ."
        echo "This script will try 'pip install .', but please ensure this is appropriate for your project setup."
        pip install .
    else
        echo "No uv.lock, requirements.txt, or pyproject.toml found. Cannot automatically install dependencies."
        echo "Please install dependencies manually."
        exit 1
    fi
fi
echo "Dependencies installed."
echo ""

# Prepare sample data and database
echo "--------------------------------------------------------------------------------"
echo "PREPARING SAMPLE DATA AND DATABASE"
echo "--------------------------------------------------------------------------------"
if [ -f "scripts/prepare_sql_mcp_db.sh" ]; then
    echo "Running 'bash scripts/prepare_sql_mcp_db.sh'..."
    bash scripts/prepare_sql_mcp_db.sh
    echo "Data and database preparation complete."
else
    echo "Error: scripts/prepare_sql_mcp_db.sh not found!"
    echo "Please ensure this script exists and is executable."
    exit 1
fi
echo ""

# Run the agent demo
echo "--------------------------------------------------------------------------------"
echo "STARTING THE AGENT DEMO"
echo "--------------------------------------------------------------------------------"
if [ -d "src" ]; then
    echo "Changing directory to src/ and running 'adk web'..."
    cd src
    adk web
else
    echo "Error: src/ directory not found!"
    echo "Cannot start the agent demo."
    exit 1
fi

echo "--------------------------------------------------------------------------------"
echo "Script finished. If 'adk web' started successfully, your demo should be accessible."
echo "--------------------------------------------------------------------------------" 