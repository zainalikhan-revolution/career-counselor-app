import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Career & Opportunity Finder", page_icon="🎓", layout="centered")

# Hide Streamlit branding
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load Models and Data
@st.cache_data
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def load_career_data():
    return pd.read_csv("career_data.csv")

@st.cache_data
def load_opportunities():
    return pd.read_csv("opportunities.csv")

model = load_model()
career_df = load_career_data()
opp_df = load_opportunities()

# UI Tabs
tab1, tab2 = st.tabs(["🎯 Career Recommender", "🌍 Scholarships & Opportunities"])

# ============ Tab 1: Career Recommender ============
with tab1:
    st.header("🎯 Find Careers Based on Your Interests")
    interests = sorted(career_df['interest'].dropna().unique())
    skills = sorted(career_df['skill'].dropna().unique())

    col1, col2 = st.columns(2)
    with col1:
        selected_interest = st.selectbox("Your Interest", options=[""] + interests)
    with col2:
        selected_skill = st.selectbox("Your Skill", options=[""] + skills)

    def match_careers(user_interest, user_skill):
        from difflib import SequenceMatcher
        matches = []
        for _, row in career_df.iterrows():
            i_score = SequenceMatcher(None, row['interest'], user_interest).ratio()
            s_score = SequenceMatcher(None, row['skill'], user_skill).ratio()
            avg_score = (i_score + s_score) / 2
            if avg_score >= 0.6:
                matches.append((row['career'], avg_score))
        matches = sorted(matches, key=lambda x: x[1], reverse=True)
        return [m[0] for m in matches]

    if st.button("🔍 Get Career Matches"):
        if selected_interest and selected_skill:
            results = match_careers(selected_interest, selected_skill)
            if results:
                st.success("Here are some careers you may like:")
                for r in results:
                    st.markdown(f"- ✅ **{r}**")
            else:
                st.error("No strong matches found. Try different inputs.")
        else:
            st.warning("Please select both interest and skill.")

# ============ Tab 2: Opportunities ============
with tab2:
    st.header("🌍 Find Scholarships, Internships, and Free Programs")
    st.write("This tool recommends global programs for rural & underserved students using AI.")

    user_field = st.text_input("What field are you interested in? (e.g., AI, Biology, Engineering)")
    user_group = st.text_input("Who are you? (e.g., rural student, low-income, youth)")
    user_query = f"{user_field} {user_group}"

    if st.button("🎓 Find Opportunities"):
        with st.spinner("Finding the best matches for you..."):
            query_embedding = model.encode([user_query])
            combined_text = (opp_df["Field"] + " " + opp_df["Target Group"] + " " + opp_df["Description"]).tolist()
            data_embeddings = model.encode(combined_text)
            sims = cosine_similarity(query_embedding, data_embeddings)[0]
            opp_df["score"] = sims
            top_matches = opp_df.sort_values(by="score", ascending=False).head(5)

            for _, row in top_matches.iterrows():
                st.subheader(f"{row['Type']} — {row['Name']}")
                st.write(f"🌐 Field: **{row['Field']}** | 🎯 Group: *{row['Target Group']}* | 🌍 Country: {row['Country']}")
                st.write(f"📝 {row['Description']}")
                st.markdown(f"[🔗 Learn more]({row['URL']})")
                st.markdown("---")








