#!/bin/bash

# Install dependencies
pip install -r backend/requirements.txt

# Run the application
uvicorn backend.main:app --host 0.0.0.0 --port 8000