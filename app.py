# ats_resume_app.py

import os
import time
import base64
import fitz  # PyMuPDF
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure Gemini API
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    st.error("❌ GOOGLE_API_KEY not found. Please check your .env file.")
    st.stop()

# Setup Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")
st.title("📄 ATS Resume Matcher")
st.markdown("Upload your **resume** and paste the **job description** to get AI-powered feedback.")

# Job description input
job_description = st.text_area("📝 Paste the Job Description:")

# Resume file upload
uploaded_file = st.file_uploader("📎 Upload your Resume (PDF only)", type=["pdf"])

# Prompts
resume_review_prompt = """
You are an experienced HR Technical Recruiter. Carefully analyze the provided resume and compare it with the job description.
Provide feedback on strengths, weaknesses, and how well the candidate matches the job criteria.
"""

ats_match_prompt = """
You're an ATS (Applicant Tracking System). Compare the resume to the job description and:
1. Give a percentage match.
2. List missing keywords.
3. Provide final recommendations.
"""

# Function to convert first page of PDF to base64 image
def extract_first_page_as_base64(uploaded_file):
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = doc[0]
        pix = first_page.get_pixmap(dpi=150)
        img_bytes = pix.tobytes("jpeg")
        encoded = base64.b64encode(img_bytes).decode("utf-8")
        return [{"mime_type": "image/jpeg", "data": encoded}]
    except Exception as e:
        st.error(f"❌ PDF parsing error: {e}")
        return None

# Function to query Gemini
def query_gemini(prompt, image_parts, job_desc):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        start = time.time()
        response = model.generate_content([prompt, image_parts[0], job_desc])
        end = time.time()
        st.success(f"✅ Gemini responded in {round(end - start, 2)}s.")
        return response.text
    except Exception as e:
        st.error(f"❌ Gemini API error: {e}")
        return None

# Buttons
col1, col2 = st.columns(2)
with col1:
    do_review = st.button("📋 Resume Review")
with col2:
    do_match = st.button("📊 Get Match Percentage")

# Processing on button click
if uploaded_file and (do_review or do_match):
    with st.spinner("🧠 Processing resume..."):
        image_parts = extract_first_page_as_base64(uploaded_file)

        if not image_parts:
            st.error("⚠️ Could not process resume. Try a different file.")
        elif not job_description.strip():
            st.warning("⚠️ Please paste the job description first.")
        else:
            prompt = resume_review_prompt if do_review else ats_match_prompt
            result = query_gemini(prompt, image_parts, job_description)
            if result:
                st.subheader("📬 Result:")
                st.write(result)
else:
    if do_review or do_match:
        st.warning("⚠️ Please upload a resume and paste a job description first.")