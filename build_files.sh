#!/bin/bash

# Unzip the static assets first
unzip -o deepzoom_output.zip

# Install dependencies using specific python version
python3.9 -m pip install -r requirements.txt

# Collect static files using specific python version
python3.9 manage.py collectstatic --noinput