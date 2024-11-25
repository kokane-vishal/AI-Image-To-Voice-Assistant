import streamlit as st
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.messages import HumanMessage
import pytesseract
from gtts import gTTS
import io
import base64

# Configure Google gemini API Key
GOOGLE_API_KEY = "YOUR_GOOGLE_GENAI_API_KEY"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

def image_to_base64(image):
    """Convert PIL Image to Base64 string for Gemini."""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

def run_ocr(image):
    """Run OCR on the uploaded image."""
    return pytesseract.image_to_string(image).strip()

def analyze_image(image, prompt):
    """Send image and prompt to Gemini for analysis."""
    try:
        image_base64 = image_to_base64(image)
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
            ]
        )
        # Synchronous invocation using `invoke`
        response = llm.invoke([message])
        return response.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def text_to_speech(text):
    """Convert text to speech and return MP3 bytes."""
    tts = gTTS(text=text, lang='en')
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.getvalue()

# Main app
def main():
    # Setting layout to "centered"
    st.set_page_config(page_title="AI Assistant", layout="centered")
    
    st.title("AI-Powered Assistive Tool for Visually Impaired")
    st.write("Upload an image to analyze and convert its content into audio")

    # Upload the image
    uploaded_file = st.file_uploader("Upload an image...", type=['jpg', 'jpeg', 'png'])

    # Reset session state when a new image is uploaded
    if uploaded_file:
        if 'last_uploaded_file' in st.session_state and st.session_state.last_uploaded_file != uploaded_file:
            st.session_state.extracted_text = None
            st.session_state.summarized_text = None
            st.session_state.summarize_enabled = False

        # Update last uploaded file
        st.session_state.last_uploaded_file = uploaded_file  

        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Scene Description Button
        if st.button("Scene Description"):
            with st.spinner("Analyzing scene..."):
                scene_prompt = "Describe this image briefly."
                scene_description = analyze_image(image, scene_prompt)
                st.subheader("Scene Description")
                st.write(scene_description)
                st.write("Read aloud:")
                st.audio(text_to_speech(scene_description), format='audio/mp3')

        # Text Extraction Button
        if st.button("Extract & Read Text from Image"):
            with st.spinner("Extracting text..."):
                extracted_text = run_ocr(image)
                st.subheader("Extracted Text from Image")
                
                if extracted_text:
                    # Store extracted text in session state
                    st.session_state.extracted_text = extracted_text
                    st.write(extracted_text)
                    st.write("Read aloud:")
                    st.audio(text_to_speech(extracted_text), format='audio/mp3')

                    # Enable the Summarize Text button only after extraction
                    st.session_state.summarize_enabled = True
                else:
                    st.write("No text detected in the image.")

        # Summarize Text Button, initially disabled
        summarize_button = st.button("Summarize & Read Extracted Text", disabled=not st.session_state.get('summarize_enabled', False))

        if summarize_button and 'extracted_text' in st.session_state:
            with st.spinner("Summarizing text..."):
                template = "Tell what the following text is about and summarize it briefly:\n\n{text}"
                prompt = PromptTemplate(input_variables=["text"], template=template)
                chain = LLMChain(llm=llm, prompt=prompt)
                summary = chain.run(text=st.session_state.extracted_text)

                # Store the summary in session state
                st.session_state.summarized_text = summary
                st.subheader("Summary of Extracted Text from Image")
                st.write(summary)
                st.write("Read aloud:")
                st.audio(text_to_speech(summary), format='audio/mp3')


if __name__ == "__main__":
    main()
