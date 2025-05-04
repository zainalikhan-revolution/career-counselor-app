import streamlit as st
import pickle
import numpy as np

# Load model and encoders
with open('model/career_model.pkl', 'rb') as f:
    data = pickle.load(f)
    model = data['model']
    le_interests = data['le_interests']
    le_skills = data['le_skills']
    le_environment = data['le_environment']
    le_career = data['le_career']

# Language selection
language = st.selectbox("Select Language / زبان منتخب کریں:", ["English", "اردو"])

# Define labels based on language
if language == "English":
    title = "AI-Powered Career Counselor"
    description = "Helping students in rural areas discover suitable career paths."
    interest_label = "Select your interest:"
    skill_label = "Select your skill:"
    marks_label = "Enter your academic marks (%):"
    environment_label = "Preferred work environment:"
    button_label = "Get Career Recommendation"
    result_label = "Recommended Career Path:"
else:
    title = "اے آئی پر مبنی کیریئر مشیر"
    description = "دیہی علاقوں کے طلباء کو موزوں کیریئر راستے تلاش کرنے میں مدد فراہم کرنا۔"
    interest_label = "اپنی دلچسپی منتخب کریں:"
    skill_label = "اپنی مہارت منتخب کریں:"
    marks_label = "اپنے تعلیمی نمبر درج کریں (%):"
    environment_label = "ترجیحی کام کا ماحول:"
    button_label = "کیریئر کی سفارش حاصل کریں"
    result_label = "تجویز کردہ کیریئر راستہ:"

st.title(title)
st.write(description)

# User inputs
interests = st.selectbox(interest_label, le_interests.classes_)
skills = st.selectbox(skill_label, le_skills.classes_)
marks = st.slider(marks_label, 0, 100, 50)
environment = st.selectbox(environment_label, le_environment.classes_)

if st.button(button_label):
    # Encode inputs
    interests_enc = le_interests.transform([interests])[0]
    skills_enc = le_skills.transform([skills])[0]
    environment_enc = le_environment.transform([environment])[0]

    # Predict
    X = np.array([[interests_enc, skills_enc, marks, environment_enc]])
    career_enc = model.predict(X)[0]
    career = le_career.inverse_transform([career_enc])[0]

    st.success(f"{result_label} {career}")
