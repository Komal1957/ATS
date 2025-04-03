import os
import platform
import base64
import streamlit as st
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Automatically detect OS and set Poppler path
if platform.system() == "Windows":
    POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"
else:
    POPPLER_PATH = "/usr/bin"  # Default path for Poppler on Linux (Streamlit Cloud)

# Configure Gemini API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    """Generate response from Google Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    """Convert the uploaded PDF to an image and encode it."""
    if uploaded_file is not None:
        # Convert PDF to images
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=POPPLER_PATH)

        first_page = images[0]

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded") 

## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Job description input
input_text = st.text_area("Job Description:", key="input")

# Resume upload
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

# Buttons
submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Percentage Match")

# Prompts for AI analysis
input_prompt1 = """
You are an experienced HR with Tech Experience in the field of Data Science, Full Stack, Web Development, Big Data Engineering, DevOps, Data Analysis, or any Computer Science domain.
Your task is to review the provided resume against the job description for these profiles.
Please provide a professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the application in relation to the specified job requirements.
"""  

input_prompt3 = """
You are a skilled ATS (Application Tracking System) scanner with deep knowledge of ATS functionality in various Computer Science fields (Data Science, Full Stack, Web Development, Big Data, DevOps, etc.).
Your task is to evaluate the resume against the provided job description and provide:
1. The percentage match between the resume and job description.
2. Missing keywords.
3. Final thoughts on how to improve the resume.
"""

# Process and analyze resume
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.warning("Please upload a resume.")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.warning("Please upload a resume.")
