import streamlit as st
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Career & Opportunity Finder",
    page_icon="🎓",
    layout="centered"
)

# ✅ Try to load the logo safely
logo_path = os.path.join(os.path.dirname(__file__), "logo.png")

# If logo exists, show it
if os.path.exists(logo_path):
    with st.sidebar:
        st.image(logo_path, width=150)
        st.markdown("## 🌟 Welcome to AI Finder")
        st.markdown("Discover opportunities powered by AI")

    st.image(logo_path, width=200)
else:
    with st.sidebar:
        st.markdown("## 🌟 Welcome to AI Finder")
        st.markdown("Discover opportunities powered by AI")
    st.warning("⚠️ 'logo.png' not found. Please upload it to the same folder as app.py")

# ------------------ UI ------------------
st.title("🎓 AI Opportunity Finder for Rural Students")
st.markdown("Helping rural students find careers, scholarships, and AI programs.")

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

# ------------------ LOAD DATA ------------------
career_data_path = os.path.join(os.path.dirname(__file__), 'career_data.csv')
opportunities_path = os.path.join(os.path.dirname(__file__), 'opportunities.csv')

@st.cache_data
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def load_career_data():
    return pd.read_csv(career_data_path)

@st.cache_data
def load_opportunities():
    return pd.read_csv(opportunities_path)

model = load_model()
career_df = load_career_data()
opp_df = load_opportunities()

# ------------------ TABS ------------------
career_tab, opportunity_tab = st.tabs(["💼 Career Guidance", "🌍 Scholarships & Opportunities"])

# ------------------ TAB 1 ------------------
with career_tab:
    st.subheader("🎯 Get Personalized Career Recommendations")

    interests_list = sorted(career_df["interest"].dropna().unique())
    skills_list = sorted(career_df["skill"].dropna().unique())

    col1, col2 = st.columns(2)
    selected_interest = col1.selectbox("Your Main Interest", [""] + list(interests_list))
    selected_skill = col2.selectbox("Your Main Skill", [""] + list(skills_list))

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

# ------------------ TAB 2 ------------------
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










