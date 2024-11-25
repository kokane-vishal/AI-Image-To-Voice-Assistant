#!/usr/bin/env bash

# Update package list and install Tesseract OCR
apt-get update && apt-get install -y tesseract-ocr

# Install dependencies from requirements.txt
pip install -r requirements.txt
