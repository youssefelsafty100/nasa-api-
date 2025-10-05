#!/bin/bash

# Unzip the static assets first
unzip -o deepzoom_output.zip

# Install dependencies using specific python version
python3.9 -m pip install -r requirements.txt

# Run migrations
python3.9 manage.py migrate --noinput

# Collect static files using specific python version
python3.9 manage.py collectstatic --noinput

# Initialize database with data
python3.9 manage.py init_data