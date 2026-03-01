import faiss
import numpy as np
import pandas as pd
import pickle
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DIM = 1536


class MovieVectorStore:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.index_path = "data/movie_index.faiss"
        self.meta_path = "data/movie_metadata.pkl"
        self.index = None
        self.df = None

    def embed(self, text):
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        vec = np.array(response.data[0].embedding, dtype="float32")
        return vec / np.linalg.norm(vec)

    def build_and_save(self):
        print("Building embeddings (one-time process)...")

        self.df = pd.read_csv(self.csv_path)
        index = faiss.IndexFlatIP(DIM)
        vectors = []

        for i, (_, row) in enumerate(self.df.iterrows(), start=1):
            text = f"""
            Title: {row['Series_Title']}
            Genre: {row['Genre']}
            Overview: {row['Overview']}
            Director: {row['Director']}
            Cast: {row['Star1']}, {row['Star2']}, {row['Star3']}, {row['Star4']}
            IMDB Rating: {row['IMDB_Rating']}
            """
            vec = self.embed(text)
            vectors.append(vec)

            if i % 50 == 0:
                print(f"Embedded {i}/{len(self.df)} movies")

        vectors = np.array(vectors)
        index.add(vectors)

        faiss.write_index(index, self.index_path)

        with open(self.meta_path, "wb") as f:
            pickle.dump(self.df, f)

        print("Index built and saved.")

    def load_index(self):
        print("Loading existing index...")
        self.index = faiss.read_index(self.index_path)
        with open(self.meta_path, "rb") as f:
            self.df = pickle.load(f)

    def ensure_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.load_index()
        else:
            self.build_and_save()
            self.load_index()

    def search(self, query, k=20):
        q_vec = self.embed(query)
        D, I = self.index.search(np.array([q_vec]), k)
        return self.df.iloc[I[0]]