#!/bin/bash

# Start the admin viewer
python3 -u viewer.py &

# Start the website
FLASK_ENV=production flask run --host 0.0.0.0 --port 5000