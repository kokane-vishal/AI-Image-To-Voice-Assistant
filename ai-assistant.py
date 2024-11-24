import streamlit as st
from PIL import Image
import pytesseract
from transformers import BlipProcessor, BlipForConditionalGeneration
from gtts import gTTS
import os

# Load the BLIP model for Scene Understanding
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Define a function for real-time scene understanding (object detection)
def describe_image(image):
    # Prepare the image for the BLIP model
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)
    return description

# Define a function for Text-to-Speech Conversion
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    # Save the speech to a file
    tts.save("output.mp3")
    # Play the speech using a streamlit audio player
    st.audio("output.mp3", format='audio/mp3')
    os.remove("output.mp3")  # Cleanup the saved file after playing

# Define a function for OCR text extraction from an image
def extract_text_from_image(image):
    # Convert the image to text using Tesseract OCR
    text = pytesseract.image_to_string(image)
    return text.strip()

# Streamlit UI for the app
def main():
    st.title("AI-Powered Assistive Tool")
    st.write("Upload an image to analyze and convert its content into audio")

    # Upload an image
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        # Load the image with PIL
        image = Image.open(uploaded_image)

        # Display the uploaded image
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Button for Scene Understanding (Image Description)
        if st.button("Describe Image"):
            # Generate and display a description of the image using BLIP model
            description = describe_image(image)
            st.subheader("Image Description:")
            st.write(description)
            text_to_speech(description)  # Convert the description to speech

        # Button for Text-to-Speech (Text in Image)
        if st.button("Extract Text and Convert to Speech"):
            # Extract text from the image using OCR
            extracted_text = extract_text_from_image(image)
            if extracted_text:
                st.subheader("Extracted Text:")
                st.write(extracted_text)
                text_to_speech(extracted_text)  # Convert the extracted text to speech
            else:
                st.write("No text found in the image.")

if __name__ == "__main__":
    main()
