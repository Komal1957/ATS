from dotenv import load_dotenv
load_dotenv()

import base64
import streamlit as st
import os
import io
import time
import fitz  # ✅ Replaces pdf2image
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Function to interact with Gemini with debug and error handling
def get_gemini_response(input, pdf_content, prompt):
    st.write("🔍 Calling Gemini API...")
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        start = time.time()
        response = model.generate_content([input, pdf_content[0], prompt])
        duration = round(time.time() - start, 2)
        st.write(f"✅ Gemini responded in {duration} seconds.")
        return response.text
    except Exception as e:
        st.error(f"❌ Gemini API call failed: {str(e)}")
        return "⚠️ There was a problem getting a response from Gemini."

# ✅ Updated to use fitz (PyMuPDF) with logging
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            st.write("📄 Reading PDF...")
            pdf_data = uploaded_file.read()
            doc = fitz.open(stream=pdf_data, filetype="pdf")

            st.write("🖼 Rendering first page as image...")
            pix = doc[0].get_pixmap()
            img_byte_arr = pix.tobytes("jpeg")  # Directly get JPEG bytes

            st.write("📦 Encoding image to base64...")
            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()
                }
            ]
            st.success("✅ PDF processing complete.")
            return pdf_parts
        except Exception as e:
            st.error(f"❌ Error reading PDF: {str(e)}")
            return None
    else:
        raise FileNotFoundError("No file uploaded")

# ✅ Streamlit UI setup
st.set_page_config(page_title="ATS Resume Expert")
st.header("📊 ATS Tracking System")

input_text = st.text_area("📌 Paste the Job Description:", key="input")
uploaded_file = st.file_uploader("📎 Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("📄 PDF Uploaded Successfully")

# ✅ Define prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as a percentage, then keywords missing, and last final thoughts.
"""

# ✅ Buttons
submit1 = st.button("📋 Tell Me About the Resume")
submit3 = st.button("📈 Percentage Match")

# ✅ Submit 1 - Resume review
if submit1:
    if uploaded_file is not None:
        with st.spinner("🔍 Analyzing resume..."):
            pdf_content = input_pdf_setup(uploaded_file)
            if pdf_content:
                response = get_gemini_response(input_prompt1, pdf_content, input_text)
                st.subheader("💬 The Response is")
                st.write(response)
    else:
        st.warning("⚠️ Please upload your resume.")

# ✅ Submit 3 - Match percentage
elif submit3:
    if uploaded_file is not None:
        with st.spinner("📊 Evaluating match percentage..."):
            pdf_content = input_pdf_setup(uploaded_file)
            if pdf_content:
                response = get_gemini_response(input_prompt3, pdf_content, input_text)
                st.subheader("📌 The Response is")
                st.write(response)
    else:
        st.warning("⚠️ Please upload your resume.")