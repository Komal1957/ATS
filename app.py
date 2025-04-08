from dotenv import load_dotenv
load_dotenv()

import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai 

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Set the correct Poppler path here
POPPLER_PATH = r"C:\Program Files (x86)\poppler\Library\bin"
  # <- Change only if your path differs

# Function to generate Gemini response
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# Function to handle PDF to image conversion
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # ✅ Convert the PDF to images using Poppler
        images = pdf2image.convert_from_bytes(
            uploaded_file.read(),
            poppler_path=POPPLER_PATH
        )

        # Use the first page
        first_page = images[0]

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Encode to base64 for Gemini input
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# ---------------- Streamlit App ---------------- #

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Job description input
input_text = st.text_area("Job Description:", key="input")

# File uploader
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

# Confirm upload
if uploaded_file is not None:
    st.write("✅ PDF uploaded successfully")

# Buttons for user actions
submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Percentage match")

# Prompt for analysis
input_prompt1 = """
You are an experienced HR with Tech Experience in the field of any one job role from Data Science, Full Stack, Web development, Big Data Engineering, DEVOPS, Data Analyst, and Any Computer Science field.
Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the application in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Application Tracking System) scanner with a deep understanding of any one job role in Data Science, Full Stack, Web development, Big Data Engineering, DEVOPS, Data Analyst, and Any Computer Science field.
Evaluate the resume against the provided job description.
First give the percentage match, then list keywords that are missing, and finally provide your thoughts on the overall alignment.
"""

# Resume Analysis
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("⚠ Please upload a resume.")

# Percentage Match
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("⚠ Please upload a resume.")
    