import streamlit as st
from vector_store import MovieVectorStore
from guardrails import age_filter
from debate_agents import run_debate


st.set_page_config(page_title="🎬 Movie Court", layout="wide")

st.title("🎬 Movie Court: AI Debate Edition")
st.write("Describe your mood. Watch AI critics fight. Get a verdict.")

age = st.number_input("Enter your age:", min_value=1, max_value=100, value=18)
mood = st.text_area("Describe your mood:")

if st.button("Start Debate"):

    if not mood:
        st.warning("Tell us your mood first.")
    else:
        with st.spinner("Loading movie database..."):
            store = MovieVectorStore("data/IMDb movies.csv")
            store.ensure_index()

            candidates = store.search(mood, k=20)
            safe_candidates = age_filter(candidates, age)
            final_candidates = safe_candidates.head(6)

        def format_candidates(df):
            text = ""
            for _, row in df.iterrows():
                text += f"""
Title: {row['Series_Title']}
Genre: {row['Genre']}
Rating: {row['IMDB_Rating']}
Overview: {row['Overview']}
---
"""
            return text

        candidates_text = format_candidates(final_candidates)

        st.subheader("Debate Begins!")

        # Capture debate output
        debate_output = run_debate(mood, age, candidates_text)

        st.markdown(debate_output)