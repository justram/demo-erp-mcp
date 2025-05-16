#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Run data generation and loading scripts
echo "Generating sample data..."
python scripts/make_samples.py
echo "Loading data into SQLite..."
python scripts/load_to_sql.py

# Define paths
SQL_MCP_DIR="sql_mcp"
SQL_MCP_DATA_DIR="$SQL_MCP_DIR/data"
SOURCE_DB_FILE="erp_demo.db"
SOURCE_SCHEMA_FILE="data/schema.yaml" # Assuming schema.yaml is in the root data directory

# Create sql_mcp/data directory if it doesn't exist
echo "Setting up sql_mcp data directory..."
mkdir -p "$SQL_MCP_DATA_DIR"

# Move database and copy schema
echo "Moving database file to $SQL_MCP_DATA_DIR/$SOURCE_DB_FILE"
mv "$SOURCE_DB_FILE" "$SQL_MCP_DATA_DIR/"

if [ -f "$SOURCE_SCHEMA_FILE" ]; then
    echo "Copying schema file to $SQL_MCP_DATA_DIR/schema.yaml"
    cp "$SOURCE_SCHEMA_FILE" "$SQL_MCP_DATA_DIR/"
else
    echo "Warning: Schema file $SOURCE_SCHEMA_FILE not found. Skipping copy."
fi

echo "SQL MCP database setup complete in $SQL_MCP_DATA_DIR" 