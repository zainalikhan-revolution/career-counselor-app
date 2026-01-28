
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

def test_matching():
    # Load Data
    base_dir = os.path.dirname(__file__)
    career_path = os.path.join(base_dir, 'career_data.csv')
    
    print(f"Loading data from {career_path}...")
    df = pd.read_csv(career_path)
    print(f"Loaded {len(df)} careers.")
    
    # Load Model
    print("Loading model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Test Query
    query = "drawing and painting"
    print(f"\nTesting Query: '{query}'")
    
    # Encode
    query_vec = model.encode([query])
    df['text'] = df['career'] + " " + df['interest'] + " " + df['skill']
    doc_vecs = model.encode(df['text'].tolist())
    
    # Match
    scores = cosine_similarity(query_vec, doc_vecs)[0]
    df['score'] = scores
    top_results = df.sort_values(by='score', ascending=False).head(3)
    
    print("\nTop Matches:")
    for _, row in top_results.iterrows():
        print(f"- {row['career']} (Score: {row['score']:.2f})")
    
    # Verification
    top_career = top_results.iloc[0]['career']
    if "Artist" in top_career or "Designer" in top_career or "Painter" in top_career:
        print("\n✅ SUCCESS: Semantic search identified art-related careers.")
    else:
        print(f"\n❌ FAILURE: Top result was {top_career}, expected something related to Art.")

if __name__ == "__main__":
    try:
        test_matching()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
