# -------------------- MUST BE FIRST: Import & Page Config --------------------
import streamlit as st

st.set_page_config(
    page_title="Career Counselor AI",
    page_icon="🎯",
    layout="centered"
)
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
        padding: 2rem;
    }
    h1 {
        color: #2a9d8f;
    }
    .stButton>button {
        background-color: #e76f51;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #d35400;
    }
    </style>
    """,
    unsafe_allow_html=True
)
col1, col2 = st.columns([1, 2])

with col1:
    st.image("career_image.png", width=200)  # Add an image in your folder

with col2:
    st.title("🎯 AI-Powered Career Counselor")
    st.write("Helping you discover the best career paths based on your interests.")
age = st.slider("Your Age", 10, 60, 18)
experience = st.radio("Do you have any work experience?", ("Yes", "No"))

# -------------------- Other Imports --------------------
import pandas as pd
import difflib

# -------------------- Hide Streamlit footer & menu --------------------
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# -------------------- Header --------------------
st.markdown(
    "<h1 style='text-align: center; color: #4B8BBE;'>🎓 AI-Powered Career Counselor</h1>"
    "<p style='text-align: center;'>Get smart and personalized career advice based on your interests and skills</p>",
    unsafe_allow_html=True
)

# -------------------- Example Data --------------------
career_data = [
    {"career": "Data Scientist", "interest": "Science", "skill": "Mathematics"},
    {"career": "Journalist", "interest": "Arts", "skill": "Writing"},
    {"career": "Doctor", "interest": "Science", "skill": "Biology"},
    {"career": "Accountant", "interest": "Commerce", "skill": "Accounting"},
    {"career": "Teacher", "interest": "Education", "skill": "Teaching"},
    {"career": "Agricultural Scientist", "interest": "Agriculture", "skill": "Biology"},
    {"career": "Economist", "interest": "Commerce", "skill": "Mathematics"},
    {"career": "Author", "interest": "Arts", "skill": "Writing"},
]

interests_list = sorted(list(set([row["interest"] for row in career_data])))
skills_list = sorted(list(set([row["skill"] for row in career_data])))

# -------------------- User Input --------------------
st.subheader("👤 Tell us about yourself")

col1, col2 = st.columns(2)
with col1:
    interest = st.selectbox("Choose your main interest", options=[""] + interests_list)
with col2:
    skill = st.selectbox("Choose your main skill", options=[""] + skills_list)

# -------------------- Recommendation Logic --------------------
def recommend_careers(user_interest, user_skill):
    recommendations = []
    for row in career_data:
        interest_match = difflib.SequenceMatcher(None, row["interest"].lower(), user_interest.lower()).ratio()
        skill_match = difflib.SequenceMatcher(None, row["skill"].lower(), user_skill.lower()).ratio()
        score = (interest_match + skill_match) / 2
        if score > 0.6:
            recommendations.append((row["career"], score))
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in recommendations]

# -------------------- Show Results --------------------
if st.button("🔍 Get Career Recommendations"):
    if interest and skill:
        results = recommend_careers(interest, skill)
        if results:
            st.success("✅ Based on your interest and skill, you may enjoy these careers:")
            for career in results:
                st.markdown(f"- 🎯 **{career}**")
        else:
            st.error("❌ Sorry, we couldn't find a good match. Try different inputs.")
    else:
        st.warning("⚠️ Please select both interest and skill to continue.")

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 13px;'>Built by Zain • Powered by Streamlit & AI ✨</p>", unsafe_allow_html=True)







