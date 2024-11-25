#!/usr/bin/env bash

# Remove unused packages and configuration files
apt-get clean && apt-get autoremove && apt-get autopurge 

# Update package list and install Tesseract OCR
apt-get update && apt-get install -y tesseract-ocr

# Install dependencies from requirements.txt
pip install -r requirements.txt
