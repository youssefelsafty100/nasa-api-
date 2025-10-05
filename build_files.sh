#!/bin/bash

echo "--- Starting Build Process ---"

# Install dependencies
pip install -r requirements.txt
    
# Run database migrations to create tables
echo "--- Running Migrations ---"
python manage.py migrate
    
# Populate the database with data
echo "--- Populating Database ---"
python manage.py init_data
    
echo "--- Build Process Finished ---"