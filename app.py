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

    # Simple label encoding for interest and skills
    data['interests'] = pd.factorize(data['interests'])[0]
    data['skills'] = pd.factorize(data['skills'])[0]

    # Features and target
    X = data[['interest', 'skills']]
    y = data['recommended_career']

    # Train the model
    model = DecisionTreeClassifier()
    model.fit(X, y)

    # Create model directory
    os.makedirs('career_counselor_app/model', exist_ok=True)

    # Save the trained model
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

    st.write("✅ Model trained and saved.")
else:
    # Load existing model
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    st.write("✅ Model loaded successfully.")

# User Input
interest = st.text_input("Enter your main interest:")
skills = st.text_input("Enter your main skills:")

# Predict Button
if st.button("Get Career Recommendation"):
    if interest and skills:
        # Encode user input
        interest_encoded = pd.factorize([interest])[0][0]
        skills_encoded = pd.factorize([skills])[0][0]

        # Make prediction
        prediction = model.predict([[interest_encoded, skills_encoded]])[0]
        st.success(f"🎯 Recommended Career: {prediction}")
    else:
        st.error("❌ Please enter both interest and skills.")
