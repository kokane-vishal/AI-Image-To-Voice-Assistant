# AI Assistive Tool for Visually Impaired

An AI-powered web application designed to assist visually impaired individuals by providing image analysis, text extraction, and audio feedback capabilities.

## Features

- **Scene Description**: Generates detailed descriptions of uploaded images
- **Text Extraction & Summarization**: Extracts text from images and provides summarized versions
- **Object & Obstacle Detection**: Identifies objects and their positions for safe navigation
- **Personalized Assistance**: Offers task-specific guidance based on image content
- **Audio Feedback**: Converts all text outputs to speech for better accessibility

## Prerequisites

- Python 3.7+
- Tesseract OCR
- Google API Key for Gemini AI

## Installation

1. Install system dependencies (Linux):

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```
3. Set up environment variables:

- Create a .env file in the project root
- Add your Google Gemini API key

## Usage

1. Start the application:

```bash
streamlit run app.py
```
2. Access the web interface through your browser at
[http://localhost:8501](http://localhost:8501)

3. Use the application to analyze images, extract text, and receive audio feedback.

## Technology Stack

- Streamlit: Web interface
- Google Gemini AI: Image analysis and text generation
- Tesseract OCR: Text extraction from images
- gTTS: Text-to-speech conversion
- Langchain: AI chain management
- PIL: Image processing
