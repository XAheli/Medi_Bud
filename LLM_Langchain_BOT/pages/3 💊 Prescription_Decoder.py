import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
#from dotenv import load_dotenv

# Load environment variables
#load_dotenv()

# Configure Google API
GOOGLE_API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Streamlit page configuration
st.set_page_config(page_title="Medi Bud Prescription Solver", page_icon="💊")

st.title("💊 Prescription Decoder Bot")
st.caption("Upload a prescription image and ask questions about it!")
st.caption("Try not to ask irrelevant questions and keep in mind the size of the image file to be less than or equal to 3MB")
st.write('[![View Source Code](https://img.shields.io/badge/View%20Source%20Code-%2300A7E1.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/XAheli/Medi_Bud)')

@st.cache_resource
def load_gemini_model():
    return genai.GenerativeModel('gemini-1.5-flash')

model = load_gemini_model()

def analyze_prescription(image, prompt):
    try:
        # Use the PIL image directly
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"An error occurred while generating the response, may be the prompt or image is not relevant!"


# File uploader
uploaded_file = st.file_uploader("Upload a prescription image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Prescription", use_column_width=True)

    # Text input for user's question
    user_question = st.text_input("Ask a question about the prescription:")

    if user_question:
        if st.button("Analyze"):
            with st.spinner("Analyzing the prescription..."):
                answer = analyze_prescription(image, user_question)  # Pass the image object here
                st.write(answer)

    # Predefined questions
    st.subheader("Or try these predefined questions:")
    if st.button("List all medications"):
        with st.spinner("Analyzing medications..."):
            medications = analyze_prescription(image, "List all medications or causes mentioned in this prescription with their dosages or remedies or else tell me something about the image.")
            st.write(medications)
    
    if st.button("Identify potential side effects or something that might happen to the patient if taken in wrong way at wrong time"):
        with st.spinner("Analyzing potential side effects..."):
            side_effects = analyze_prescription(image, "What are the potential side effects of the medications in this prescription? or tell me something about this image")
            st.write(side_effects)
    
    if st.button("Explain usage instructions"):
        with st.spinner("Analyzing usage instructions... and tell me the time at which the patient should consume the medication or dosage as mentioned in prescription, else tell me something about the image"):
            instructions = analyze_prescription(image, "Explain the usage instructions for each medication in this prescription.")
            st.write(instructions)

    st.warning("Please note: This bot is for informational purposes only. Always consult with a healthcare professional for medical advice.")

else:
    st.info("Please upload a prescription image to start.")

st.markdown("---")
st.caption("Powered by Google Gemini and Streamlit")
