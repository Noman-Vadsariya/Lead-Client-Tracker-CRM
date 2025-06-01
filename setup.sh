#!/bin/bash

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create Django project
django-admin startproject crm_project .

# Create main app
python manage.py startapp crm

# Create necessary directories
mkdir -p crm/templates/crm
mkdir -p crm/static/crm
mkdir -p crm/templates/admin
mkdir -p crm/api

# Create __init__.py files
touch crm/api/__init__.py
touch crm/models/__init__.py
touch crm/views/__init__.py

# Make the script executable
chmod +x setup.sh 