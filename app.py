from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai 
# from pdf2image import convert_from_path
# images = convert_from_path("sample.pdf", poppler_path="C:\\Program Files (x86)\\poppler\\Library\\bin")

# Automatically detect OS and set Poppler path
if platform.system() == "Windows":
    POPPLER_PATH = "C:\\Program Files (x86)\\poppler\\Library\\bin"
else:
    POPPLER_PATH = "/usr/bin"  # Default path for Poppler on Linux (Streamlit Cloud)
# POPPLER_PATH = ""  # Poppler is installed in this directory on Windows (Streamlit Cloud)




genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
    ##Convert the PDF to Image
        images=pdf2image.convert_from_bytes(uploaded_file.read(),  poppler_path=POPPLER_PATH)

        first_page=images[0]

        #Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
           {
                "mime_type":"image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded") 

##Streamlit App
st.set_page_config(page_title= "ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description:", key="input")
uploaded_file=st.file_uploader("Uploaded your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF uploaded Succeccfully")

submit1 = st.button("Tell Me About the Resume")

##submit2 = st.button("How Can I Improve my Skills")

#submit3 = st.button("What are the Keywords That are Missing")

submit2 = st.button("Percentage match")

input_prompt1 = """
You are an experienced HR with Tech Experience in the feild of any one job role from  Data Science, Full Stack, Web development, Big Data Engineering, DEVOPS, Data Analyst, and Any Computer Science field, your task is to review
the provided resume against the job description for these profiles.
Please share your professional evalution on whether the candidate's profile aligns with the role.
Highlight the strengths and weakness of the application in relation to the specified job requirements.
"""  
input_prompt3 = """" 
You are an skilled ATS (Application Tracking System) scanner with a deep understanding of any one job role Data Science, Full Stack, Web development, Big Data Engineering, DEVOPS, Data Analyst, and Any Computer Science field,
and  deep ATS functionality.
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches job description.
First the output should come as percentage and then keywords missing and last final thoughts.
""" 

if submit1:
    if uploaded_file is not None :
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)

    else:
        st.write("Please upload the resume")  

elif submit2:
    if uploaded_file is not None :
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)

    else:
        st.write("Please upload the resume")              