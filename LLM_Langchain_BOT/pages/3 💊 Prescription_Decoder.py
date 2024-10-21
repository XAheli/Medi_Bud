import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google API
GOOGLE_API_KEY = os.getenv("API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Streamlit page configuration
st.set_page_config(page_title="Med Bud Prescription Solver", page_icon="💊")

st.title("💊 Prescription Uploader Bot")
st.caption("Upload a prescription image and ask questions about it!")

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
        return f"An error occurred: {str(e)}"

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
            medications = analyze_prescription(image, "List all medications mentioned in this prescription with their dosages.")
            st.write(medications)
    
    if st.button("Identify potential side effects"):
        with st.spinner("Analyzing potential side effects..."):
            side_effects = analyze_prescription(image, "What are the potential side effects of the medications in this prescription?")
            st.write(side_effects)
    
    if st.button("Explain usage instructions"):
        with st.spinner("Analyzing usage instructions..."):
            instructions = analyze_prescription(image, "Explain the usage instructions for each medication in this prescription.")
            st.write(instructions)

    st.warning("Please note: This bot is for informational purposes only. Always consult with a healthcare professional for medical advice.")

else:
    st.info("Please upload a prescription image to start.")

st.markdown("---")
st.caption("Powered by Google Gemini and Streamlit")
