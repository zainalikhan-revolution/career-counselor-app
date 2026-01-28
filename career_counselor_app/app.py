
import streamlit as st
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="FutureSeeker Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ ASSETS & STYLE ------------------
logo_path = os.path.join(os.path.dirname(__file__), "logo.png")

st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            font-weight: 600;
        }
        .main-header {
            font-size: 3rem;
            color: #1E3A8A;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #64748B;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stat-card {
            background-color: #f8fafc;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #e2e8f0;
            margin-bottom: 10px;
        }
        .stat-number {
             font-size: 2rem;
             font-weight: bold;
             color: #2563eb;
        }
        .stat-label {
            color: #64748b;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        h1, h2, h3 { color: #0F172A; }
    </style>
""", unsafe_allow_html=True)

# ------------------ CONFIGURATION ------------------
api_key = None
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

if api_key:
    genai.configure(api_key=api_key)

# ------------------ LOAD DATA ------------------
base_dir = os.path.dirname(__file__)
career_path = os.path.join(base_dir, 'career_data.csv')
opp_path = os.path.join(base_dir, 'opportunities.csv')
uni_path = os.path.join(base_dir, 'universities_pakistan.csv')

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def load_data():
    c_df = pd.read_csv(career_path)
    o_df = pd.read_csv(opp_path)
    try:
        u_df = pd.read_csv(uni_path)
    except:
        u_df = pd.DataFrame(columns=["University", "City", "Province", "Sector", "Programs", "Website"])
    return c_df, o_df, u_df

try:
    with st.spinner("Initializing Professional Suite..."):
        embedding_model = load_embedding_model()
        career_df, opp_df, uni_df = load_data()
except Exception as e:
    st.error(f"System Error: {e}")
    st.stop()

# ------------------ HELPER FUNCTIONS ------------------
def semantic_search(query, documents, top_k=5):
    query_vec = embedding_model.encode([query])
    doc_vecs = embedding_model.encode(documents)
    scores = cosine_similarity(query_vec, doc_vecs)[0]
    indices = scores.argsort()[-top_k:][::-1]
    return indices, scores

def ai_assistant(role, prompt):
    if not api_key:
        return None
    try:
        model = genai.GenerativeModel('gemini-pro')
        full_prompt = f"Role: {role}\n\n{prompt}\n\nFormat: Professional Markdown."
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"AI Service Error: {e}"

# ------------------ SIDEBAR ------------------
with st.sidebar:
    if os.path.exists(logo_path):
        st.image(logo_path, use_column_width=True)
    
    st.title("FutureSeeker Pro")
    st.caption("AI-Powered Career Intelligence")
    
    if api_key:
        st.success("✅ AI Online")
    else:
        st.warning("⚠️ AI Offline")
        st.caption("Add key to .streamlit/secrets.toml")
    
    st.markdown("---")
    st.markdown("### 🛠 Navigation")
    tool = st.radio("", ["🏠 Home Dashboard", "🚀 Career Matcher", "🇵🇰 Uni Finder (Pakistan)", "🗺️ Roadmap Generator", "🌍 Global Opportunities"])

# ------------------ HOME DASHBOARD ------------------
if tool == "🏠 Home Dashboard":
    st.markdown('<div class="main-header">FutureSeeker Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your intelligent companion for global career success.</div>', unsafe_allow_html=True)
    
    # Stats Row
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="stat-card"><div class="stat-number">{len(career_df)}+</div><div class="stat-label">Careers Indexed</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-card"><div class="stat-number">{len(uni_df)}+</div><div class="stat-label">Pakistani Universities</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-card"><div class="stat-number">{len(opp_df)}+</div><div class="stat-label">Global Scholarships</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Career Categories")
        # Extract categories crudely if needed, or just show top items
        category_counts = career_df['interest'].value_counts().head(10)
        fig = px.bar(category_counts, orientation='h', title="Top Interest Categories")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("🌍 Opportunity Distribution")
        country_counts = opp_df['Country'].value_counts().head(10)
        fig2 = px.pie(country_counts, values=country_counts.values, names=country_counts.index, title="Opportunities by Region")
        st.plotly_chart(fig2, use_container_width=True)

# ------------------ TAB: CAREER MATCHER ------------------
elif tool == "🚀 Career Matcher":
    st.markdown("## 🚀 Find Your Perfect Profession")
    st.write("Using semantic analysis to match your unique profile with global career paths.")
    
    col1, col2 = st.columns(2)
    with col1:
        interest = st.text_area("What motivates you?", placeholder="e.g. Solving puzzles, designing structures...", height=100)
    with col2:
        skills = st.text_area("What are you good at?", placeholder="e.g. Math, Python, Drawing...", height=100)
    
    if st.button("Analyze Profile", type="primary"):
        if interest or skills:
            query = f"{interest} {skills}"
            
            st.subheader("📊 Data-Backed Recommendations")
            documents = career_df['career'] + " " + career_df['interest'] + " " + career_df['skill']
            indices, scores = semantic_search(query, documents.tolist())
            
            found = False
            for idx in indices:
                if scores[idx] > 0.3: # Higher threshold for better quality
                    found = True
                    row = career_df.iloc[idx]
                    with st.expander(f"💼 {row['career']} (Match: {int(scores[idx]*100)}%)"):
                         st.write(f"**Why**: Matches your interest in *{row['interest']}*.")
                         st.write(f"**Skills Needed**: {row['skill']}")
            
            if not found:
                 st.info("No perfect database matches. Try refining your keywords!")

            if api_key:
                st.subheader("🧠 Deep AI Insight")
                with st.spinner("Consulting AI Expert..."):
                    prompt = f"User Interests: {interest}\nSkills: {skills}\nTask: Suggest 3 specific, modern careers with a 'Day in the Life' summary."
                    response = ai_assistant("Senior Career Strategist", prompt)
                    st.markdown(response)
        else:
            st.error("Please define your interests or skills.")

# ------------------ TAB: UNIVERSITY FINDER ------------------
elif tool == "🇵🇰 Uni Finder (Pakistan)":
    st.markdown("## 🇵🇰 Explore Pakistani Universities")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        city_filter = st.multiselect("City", sorted(uni_df['City'].unique()))
    with col2:
        sector_filter = st.multiselect("Sector", sorted(uni_df['Sector'].unique()))
    with col3:
        search_term = st.text_input("Search Programs", placeholder="e.g. Computer Science")
    
    filtered_df = uni_df.copy()
    if city_filter: filtered_df = filtered_df[filtered_df['City'].isin(city_filter)]
    if sector_filter: filtered_df = filtered_df[filtered_df['Sector'].isin(sector_filter)]
    if search_term: filtered_df = filtered_df[filtered_df['Programs'].str.contains(search_term, case=False, na=False)]
    
    st.success(f"Found {len(filtered_df)} Universities")
    st.dataframe(filtered_df, use_container_width=True, column_config={"Website": st.column_config.LinkColumn()})

# ------------------ TAB: ROADMAP GENERATOR ------------------
elif tool == "🗺️ Roadmap Generator":
    st.markdown("## 🗺️ Career Roadmap Generator")
    st.info("💡 Power Feature: Generates a 5-year step-by-step success plan.")
    
    target_career = st.text_input("Target Career", placeholder="e.g. AI Researcher")
    current_status = st.selectbox("Current Status", ["High School Student", "Undergraduate", "Graduate", "Professional"])
    
    if st.button("Generate Roadmap", type="primary"):
        if api_key:
            with st.spinner(f"Drafting roadmap for {target_career}..."):
                prompt = f"Goal: Become a {target_career}\nCurrent Status: {current_status}\nContext: Pakistan & Global Market\nTask: Detailed 5-year roadmap."
                response = ai_assistant("Strategic Career Coach", prompt)
                st.markdown(response)
        else:
            st.error("Please add your API Key to .streamlit/secrets.toml to use this feature.")

# ------------------ TAB: OPPORTUNITIES ------------------
elif tool == "🌍 Global Opportunities":
    st.markdown("## 🌍 Scholarships & Free Programs")
    
    filter_text = st.text_input("Filter opportunities", placeholder="e.g. UK, Engineering, Fully Funded")
    
    if filter_text:
        opp_documents = opp_df['Name'] + " " + opp_df['Field'] + " " + opp_df['Country'] + " " + opp_df['Description']
        indices, scores = semantic_search(filter_text, opp_documents.tolist())
        display_df = opp_df.iloc[indices]
    else:
        display_df = opp_df
        
    for _, row in display_df.iterrows():
        with st.expander(f"🎓 {row['Name']} ({row['Country']}) - {row['Type']}"):
            st.write(f"**Field**: {row['Field']}")
            st.write(f"_{row['Description']}_")
            st.markdown(f"**[Apply Here]({row['URL']})**")
