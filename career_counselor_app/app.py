import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Career & Opportunity Finder",
    page_icon="🎓",
    layout="centered"
)

# ------------------ HIDE STREAMLIT DEFAULTS ------------------
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------ LOAD MODEL ------------------
@st.cache_data
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_career_data():
    return pd.read_csv("career_counselor_app/career_data.csv")  # ✅ fixed path

@st.cache_data
def load_opportunities():
    return pd.read_csv("career_counselor_app/opportunities.csv")  # ✅ fixed path

career_df = load_career_data()
opp_df = load_opportunities()

# ------------------ APP TITLE ------------------
st.markdown("<h1 style='text-align: center;'>🎓 AI Opportunity Finder for Rural Students</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Discover personalized careers, scholarships, and free programs using AI</p>", unsafe_allow_html=True)

# ------------------ TABS ------------------
career_tab, opportunity_tab = st.tabs(["💼 Career Guidance", "🌍 Scholarships & Opportunities"])

# ------------------ TAB 1: CAREERS ------------------
with career_tab:
    st.subheader("🎯 Get Personalized Career Recommendations")

    interests_list = sorted(career_df["interest"].dropna().unique())
    skills_list = sorted(career_df["skill"].dropna().unique())

    col1, col2 = st.columns(2)
    with col1:
        selected_interest = st.selectbox("Your Main Interest", [""] + list(interests_list))
    with col2:
        selected_skill = st.selectbox("Your Main Skill", [""] + list(skills_list))

    def match_careers(interest, skill):
        results = []
        for _, row in career_df.iterrows():
            interest_score = SequenceMatcher(None, row["interest"].lower(), interest.lower()).ratio()
            skill_score = SequenceMatcher(None, row["skill"].lower(), skill.lower()).ratio()
            score = (interest_score + skill_score) / 2
            if score >= 0.6:
                results.append((row["career"], score))
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results]

    if st.button("🔍 Find Careers"):
        if selected_interest and selected_skill:
            careers = match_careers(selected_interest, selected_skill)
            if careers:
                st.success("Here are career paths matched to you:")
                for c in careers:
                    st.markdown(f"✅ **{c}**")
            else:
                st.error("Sorry, no strong matches found.")
        else:
            st.warning("Please select both interest and skill.")

# ------------------ TAB 2: OPPORTUNITIES ------------------
with opportunity_tab:
    st.subheader("🌍 Discover Global Scholarships & Free Programs")

    field = st.text_input("What field are you interested in? (e.g. AI, Biology, Health)")
    background = st.text_input("Describe your background or challenges (e.g. rural, low-income)")

    if st.button("🎓 Find Opportunities"):
        if field and background:
            query = f"{field} {background}"
            query_vec = model.encode([query])
            opp_df["text"] = opp_df["Field"] + " " + opp_df["Target Group"] + " " + opp_df["Description"]
            opp_embeddings = model.encode(opp_df["text"].tolist())
            scores = cosine_similarity(query_vec, opp_embeddings)[0]
            opp_df["score"] = scores
            top_opps = opp_df.sort_values(by="score", ascending=False).head(5)

            for _, row in top_opps.iterrows():
                st.markdown(f"### 🎓 {row['Name']}")
                st.write(f"📌 Type: **{row['Type']}**")
                st.write(f"🌐 Field: {row['Field']} | 🎯 Group: {row['Target Group']} | 🌍 Country: {row['Country']}")
                st.write(f"📝 {row['Description']}")
                st.markdown(f"[🔗 Apply or Learn More]({row['URL']})")
                st.markdown("---")
        else:
            st.warning("Please fill in both field and background to get results.")








