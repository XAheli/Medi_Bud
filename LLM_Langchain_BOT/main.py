import streamlit as st
from PIL import Image

# Custom CSS with medical theme
custom_css = """
<style>
/* Main theme colors */
:root {
    --primary-blue: #4a90e2; /* Softer blue for a professional look */
    --secondary-blue: #7ab1f2; /* Complementary lighter blue */
    --neutral-gray: #f7f9fc; /* Lighter gray for a cleaner background */
    --dark-gray: #3c3c3c; /* Darker gray for contrast */
    --doctor-white: #ffffff;
    --alert-red: #e74c3c;
    --text-gray: #5a5a5a; /* Soft text color */
}

/* Main container styling */
.main-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 2rem;
}

/* Header styling */
.medical-header {
    background: var(--neutral-gray);
    padding: 2rem;
    text-align: center;
    margin-bottom: 2rem;
    border-radius: 10px;
    border: 2px solid var(--primary-blue);
}

.medical-header h1 {
    color: var(--primary-blue);
    font-size: 2.2rem;
    font-weight: bold;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Sidebar styling */
.css-1d391kg {
    background-color: var(--neutral-gray);
    border-right: 2px solid var(--secondary-blue);
    padding: 1.5rem;
}

.css-1d391kg h2 {
    color: var(--primary-blue);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* File uploader styling */
.upload-container {
    border: 2px dashed var(--primary-blue);
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
    transition: all 0.3s ease;
    text-align: center;
    background-color: rgba(127, 146, 255, 0.05);
}

.upload-container:hover {
    border-color: var(--secondary-blue);
    background-color: rgba(74, 144, 226, 0.1);
}

/* Button styling */
.medical-button {
    background-color: var(--primary-blue);
    color: white;
    border: none;
    padding: 0.75rem 2.5rem;
    border-radius: 25px;
    font-weight: 600;
    transition: all 0.3s ease;
    cursor: pointer;
    margin-top: 1rem;
}

.medical-button:hover {
    background-color: var(--secondary-blue);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Warning card styling */
.warning-card {
    display: flex;
    align-items: center;
    background: var(--neutral-gray);
    border-left: 5px solid var(--alert-red);
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.warning-icon {
    font-size: 2rem;
    color: var(--alert-red);
    margin-right: 0.5rem;
}

.warning-text h4 {
    color: var(--alert-red);
    margin: 0;
}

.warning-text ul {
    margin: 0;
    padding-left: 1.2rem;
    color: var(--dark-gray);
}


/* Card styling for features */
.feature-card {
    background-color: var(--doctor-white);
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-left: 4px solid var(--primary-blue);
}

.feature-card h3 {
    color: var(--primary-blue);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.feature-card p, .feature-card ul {
    color: var(--text-gray);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 2rem;
    padding: 1rem;
    color: var(--text-gray);
    font-size: 0.8rem;
}

.footer p {
    margin: 0;
}
</style>
"""

# Page configuration
st.set_page_config(
    page_title="AI-Powered Medical Chatbot - Medi Bud",
    page_icon="⚕",
    layout="wide",
)

# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<h2>Medi Bud ⚕️</h2>', unsafe_allow_html=True)
    st.markdown("### Your AI Health Companion")
    
    # File Upload
    st.markdown('<div class="upload-container">📄 Upload Medical Documents</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Attach your medical files (PDF, JPG, PNG)", 
        type=["pdf", "jpg", "png"]
    )
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

# Main Content
st.markdown('<div class="medical-header"><h1>Welcome to Medi Bud ⚕️!</h1></div>', unsafe_allow_html=True)
st.image("logo-no-background.png", width=700)
st.markdown('</div>', unsafe_allow_html=True)

# Author Details
st.write("""
<div align="center" style="display: flex; flex-direction: column; align-items: center; gap: 8px;">
    <div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
        <a href="https://github.com/XAheli/Medi_Bud" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-Repository-%23181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Repository" style="height: 24px;">
        </a>
        <a href="https://www.linkedin.com/in/ahelipoddar/" target="_blank">
            <img src="https://img.shields.io/badge/Aheli%20Poddar-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="Aheli Poddar LinkedIn" style="height: 24px;">
        </a>
        <a href="https://www.linkedin.com/in/sourabh-dey/" target="_blank">
            <img src="https://img.shields.io/badge/Sourabh%20Dey-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="Sourabh Dey LinkedIn" style="height: 24px;">
        </a>
    </div>
    <div style="display: flex; justify-content: center; align-items: center; gap: 5px; margin-top: 8px;">
        <span style="font-size: 15px; color: #dfdfdf;">𝗬𝗼𝘂 𝗮𝗿𝗲 𝘃𝗶𝘀𝗶𝘁𝗼𝗿</span>
        <img src="https://profile-counter.glitch.me/Medi_Bud_Streamlit/count.svg" alt="visitor count" style="height: 24px;"/>
    </div>
</div>
""", unsafe_allow_html=True)


# Features Section
st.markdown("""
<div class="feature-card">
    <h3>🏥 Key Features</h3>
    <ul>
        <li>24/7 availability for health-related queries</li>
        <li>Secure document upload for context-aware consultations</li>
        <li>Multiple AI model options for diverse healthcare needs</li>
        <li>Clear, accessible medical information</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Caution Section with enhanced warning card
st.markdown("""
<div class="warning-card">
    <div class="warning-icon">⚠</div>
    <div class="warning-text">
        <h4>Important Medical Disclaimer</h4>
        <ul>
            <li>This AI chatbot provides preliminary guidance only and is not a substitute for professional medical advice.</li>
            <li>Always consult qualified healthcare providers for medical conditions.</li>
            <li>In case of emergency, contact your local emergency services immediately.</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)


# Start Conversation Section
st.markdown("""
<div class="feature-card">
    <h3>🩺 Ready to Start Your Consultation?</h3>
    <p>Click below to begin your conversation with Medi Bud.</p>
</div>
""", unsafe_allow_html=True)


# Navigation Buttons
if st.button("🧠 Med Bud With Memory"):
    st.switch_page("pages/1 🧠 Med_Bud_With_Memory.py")
if st.button("🌐 Med Bud With Web Access"):
    st.switch_page("pages/2 🌐 Med_Bud_With_Web_Access.py")
if st.button("💊 Prescription Decoder"):
    st.switch_page("pages/3 💊 Prescription_Decoder.py")


# Footer
st.markdown("""
<div class="footer">
    <p>Medi Bud - Your Trusted AI Health Assistant</p>
    <p>Version 1.0.0 | © 2024 Medi Bud. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
