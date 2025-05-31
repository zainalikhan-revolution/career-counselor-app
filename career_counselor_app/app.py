import streamlit as st

# Set custom page title and icon
st.set_page_config(
    page_title="Career Counselor AI",  # Your custom app title
    page_icon="🎯",  # You can change this emoji or use a URL to a favicon
)

# Hide Streamlit footer and hamburger menu
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}  /* hides the hamburger menu */
    footer {visibility: hidden;}     /* hides the footer */
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import difflib

# -------------------- Page Setup --------------------
st.set_page_config(page_title="AI Career Counselor", layout="centered")
st.markdown(
    "<h1 style='text-align: center; color: #4B8BBE;'>🎓 AI-Powered Career Counselor</h1>"
    "<p style='text-align: center;'>Get smart and personalized career advice based on your interests and skills</p>",
    unsafe_allow_html=True
)

# -------------------- Example Data (for demo) --------------------
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

# -------------------- NLP Matching Logic --------------------
def recommend_careers(user_interest, user_skill):
    recommendations = []
    for row in career_data:
        interest_match = difflib.SequenceMatcher(None, row["interest"].lower(), user_interest.lower()).ratio()
        skill_match = difflib.SequenceMatcher(None, row["skill"].lower(), user_skill.lower()).ratio()
        score = (interest_match + skill_match) / 2
        if score > 0.6:  # threshold
            recommendations.append((row["career"], score))
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in recommendations]

# -------------------- Get Recommendation --------------------
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


