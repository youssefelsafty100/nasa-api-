#!/bin/bash

# Unzip the static assets first
unzip -o deepzoom_output.zip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput