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

# Configure Google Gemini API Key
GOOGLE_API_KEY = "YOUR_GOOGLE_GENAI_API_KEY"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

# Function to convert an image to Base64 format
def image_to_base64(image):
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

# Function to run OCR on an image
def run_ocr(image):
    return pytesseract.image_to_string(image).strip()

# Function to analyze the image using Gemini
def analyze_image(image, prompt):
    try:
        image_base64 = image_to_base64(image)
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
            ]
        )
        response = llm.invoke([message])
        return response.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.getvalue()

# Main app function
def main():
    # Set Streamlit page configuration
    st.set_page_config(page_title="AI Assistant", layout="wide", page_icon="💡")
    st.title('AI Assistive Tool for Visually Impaired')
    st.write('Empowering accessibility through AI-powered assistive tools')

    # File uploader for images
    st.sidebar.header("Upload Image")
    uploaded_file = st.sidebar.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

    # Sidebar options for instructions
    st.sidebar.header("Instructions")
    st.sidebar.markdown(
    """
    1. Upload an image.
    2. Choose a function: 
        - Scene Description, 
        - Text Extraction, 
        - Obstacle Detection, or 
        - Personalized Assistance.
    3. Listen to the audio playback of the results.""")

    # Check if an image is uploaded
    if uploaded_file:
        if 'last_uploaded_file' in st.session_state and st.session_state.last_uploaded_file != uploaded_file:
            st.session_state.extracted_text = None
            st.session_state.summarized_text = None
            st.session_state.summarize_enabled = False

        # Update last uploaded file
        st.session_state.last_uploaded_file = uploaded_file
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Tabs for different functionalities
        tabs = st.tabs(["1-Describe Scene", "2-Extract Text (Summarize)", "3-Detect Objects & Obstacles", "4-Personalized Assistance"])

        # Describe Scene Tab
        with tabs[0]:
            if st.button("Generate Scene Description"):
                with st.spinner("Generating scene description..."):
                    scene_prompt = "Describe this image briefly."
                    scene_description = analyze_image(image, scene_prompt)
                    st.write("Scene Description:")
                    st.success(scene_description)
                    st.audio(text_to_speech(scene_description), format='audio/mp3')

        # Extract Text Tab
        with tabs[1]:
            if st.button("Extract Text"):
                with st.spinner("Extracting text..."):
                    extracted_text = run_ocr(image)
                    if extracted_text:
                        st.session_state.extracted_text = extracted_text
                        st.write("Extracted Text:")
                        st.info(extracted_text)
                        st.audio(text_to_speech(extracted_text), format='audio/mp3')
                        st.session_state.summarize_enabled = True
                    else:
                        st.warning("No text detected in the image.")

            if st.button("Summarize Text", disabled=not st.session_state.get('summarize_enabled', False)):
                with st.spinner("Summarizing text..."):
                    template = "Tell what the following text is about and summarize it briefly:\n\n{text}"
                    prompt = PromptTemplate(input_variables=["text"], template=template)
                    chain = LLMChain(llm=llm, prompt=prompt)
                    summary = chain.run(text=st.session_state.extracted_text)
                    st.session_state.summarized_text = summary
                    st.write("Summary of Extracted Text:")
                    st.success(summary)
                    st.audio(text_to_speech(summary), format='audio/mp3')

        # Detect Objects & Obstacles Tab
        with tabs[2]:
            if st.button("Detect Objects & Obstacles"):
                with st.spinner("Identifying objects and obstacles..."):
                    obstacle_prompt = "Identify objects or obstacles in this image and provide their positions for safe navigation in brief."
                    obstacle_description = analyze_image(image, obstacle_prompt)
                    st.write("Objects & Obstacles Detection:")
                    st.success(obstacle_description)
                    st.audio(text_to_speech(obstacle_description), format='audio/mp3')

        # Personalized Assistance Tab
        with tabs[3]:
            if st.button("Personalized Assistance"):
                with st.spinner("Providing personalized guidance..."):
                    task_prompt = "Provide task-specific guidance based on the content of this image in brief. Include item recognition, label reading, and any relevant context."
                    assistance_description = analyze_image(image, task_prompt)
                    st.write("Personalized Assistance:")
                    st.success(assistance_description)
                    st.audio(text_to_speech(assistance_description), format='audio/mp3')

if __name__ == "__main__":
    main()
