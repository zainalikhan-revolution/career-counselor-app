import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle
import os

# Set up Streamlit app
st.title("AI-Powered Career Counselor")
st.write("Get personalized career recommendations based on your interests and skills.")

# Load or Train Model
MODEL_PATH = 'career_counselor_app/model/career_model.pkl'

if not os.path.exists(MODEL_PATH):
    st.write("🔧 Training Model... (First Time Setup)")
    # Load your dataset
    data = pd.read_csv('career_data.csv')

    # Encode interest and skills
    data['interests_encoded'] = pd.factorize(data['interests'])[0]
    data['skills_encoded'] = pd.factorize(data['skills'])[0]

    # Features and target
    X = data[['interests_encoded', 'skills_encoded']]
    y = data['career_path']

    # Train the model
    model = DecisionTreeClassifier()
    model.fit(X, y)

    # Save model
    os.makedirs('career_counselor_app/model', exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

    st.write("✅ Model trained and saved.")
else:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    st.write("✅ Model loaded successfully.")

# User Input
interest = st.text_input("Enter your main interest (e.g., Science, Arts, Commerce):")
skills = st.text_input("Enter your main skill (e.g., Mathematics, Writing):")

# Predict Button
if st.button("Get Career Recommendation"):
    if interest and skills:
        # Use same values as used in training
        all_interests = ['Science', 'Arts', 'Agriculture', 'Commerce', 'Education']
        all_skills = ['Mathematics', 'Writing', 'Biology', 'Accounting', 'Teaching']

        if interest in all_interests and skills in all_skills:
            interest_encoded = all_interests.index(interest)
            skills_encoded = all_skills.index(skills)

            prediction = model.predict([[interest_encoded, skills_encoded]])[0]
            st.success(f"🎯 Recommended Career: {prediction}")
        else:
            st.error("❌ Please enter valid interest and skill from the suggestions.")
    else:
        st.error("❌ Please enter both interest and skills.")

