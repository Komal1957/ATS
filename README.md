# 📝 ATS Resume Matcher

An AI-powered web application that analyzes resumes against job descriptions to provide recruiter-like feedback and ATS (Applicant Tracking System) match percentages using Google's Gemini API.

---

## 🧩 Problem Statement

Job applicants often submit resumes that fail to align with specific job descriptions. Recruiters and ATS software struggle to efficiently evaluate resumes at scale, leading to missed opportunities for both candidates and employers.

---

## 🌟 Inspiration

Inspired by real-world recruitment challenges and the inefficiencies in manual resume screening, this project aims to assist both job seekers and HR professionals by simulating ATS analysis using AI.

---

## ✅ Solution

Created a web-based application where users can:
- Upload a PDF resume
- Paste a job description
- Get instant feedback including a match score, missing keywords, and improvement suggestions powered by Gemini 1.5 Flash (Google's LLM).

---

## 🔑 Features

- 📄 **Resume Upload**: Accepts PDFs and extracts the first page for evaluation.
- 🧠 **AI Analysis Modes**:
  - *Recruiter Review*: Gives professional feedback on resume strengths and weaknesses.
  - *ATS Match*: Returns a match percentage, missing keywords, and final hiring suggestions.
- ⚙️ **Gemini API Integration**: Uses Google’s LLM to analyze resumes in context.
- 🔐 **.env Configured**: Securely handles API keys with dotenv.
- 📊 **Visual Feedback**: Clean, user-friendly interface built in Streamlit.

---

## 🛠 Tech Stack

- **Frontend**: Streamlit (Python-based UI)
- **AI Integration**: Gemini 1.5 Flash via `google.generativeai`
- **PDF Processing**: PyMuPDF (fitz)
- **Environment Config**: python-dotenv
- **Deployment**: (Optional: Streamlit Sharing, Render, or Local)

---

## ⚙️ Project Setup Guide

```bash
# Clone the repository
git clone https://github.com/Komal1957/ATS-Resume-Matcher.git
cd ATS-Resume-Matcher

# Install dependencies
pip install -r requirements.txt

# Create a .env file and add your Gemini API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py
```
### 📄 Resume Upload Interface
![Resume Upload](![image](https://github.com/user-attachments/assets/6ef3ecb5-825e-49da-bb8f-e9dde91abfbc)
)

### 🧠 Gemini AI Feedback
![Gemini Feedback](![image](https://github.com/user-attachments/assets/8eaeef8d-c7de-48c5-a82c-0088236bfecf)
)

### 📊 Match Percentage Output
![Match Result](![image](https://github.com/user-attachments/assets/4c7a1eae-48a8-438b-8903-d5c07511d675)
)

## 🔗 Live Demo  
🌐 [Click here to view the live site](Coming Soon!!..)
