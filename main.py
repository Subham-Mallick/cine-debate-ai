from vector_store import MovieVectorStore
from guardrails import age_filter
from debate_agents import run_debate


def format_candidates(df):
    text = ""
    for _, row in df.iterrows():
        text += f"""
        Title: {row['Series_Title']}
        Year: {row['Released_Year']}
        Certificate: {row['Certificate']}
        Genre: {row['Genre']}
        IMDB Rating: {row['IMDB_Rating']}
        Overview: {row['Overview']}
        ---
        """
    return text


def main():
    age = int(input("Enter your age: "))
    mood = input("Describe your mood: ")

    store = MovieVectorStore("data/IMDb movies.csv")
    store.ensure_index()

    candidates = store.search(mood, k=20)

    safe_candidates = age_filter(candidates, age)
    final_candidates = safe_candidates.head(6)

    candidates_text = format_candidates(final_candidates)

    run_debate(mood, age, candidates_text)


if __name__ == "__main__":
    main()