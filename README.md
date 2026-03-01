# 🎬 CineDebate – AI Movie Court

An interactive multi-agent AI movie recommendation system where AI critics debate before delivering a final verdict.

## 🚀 Features

- Semantic movie retrieval using FAISS vector database
- OpenAI embeddings (text-embedding-3-small)
- Multi-agent debate powered by AutoGen
- Age-based content guardrails
- Cached vector indexing for performance
- Streamlit web interface

## 🏗 Architecture

User Mood → Vector Search → Guardrails → AI Debate → Judge Verdict

## 🛠 Tech Stack

- Python
- AutoGen
- FAISS
- OpenAI API
- Streamlit
- Pandas

## 📦 Setup

1. Clone repo
2. Install dependencies
3. Add `.env` with your OpenAI API key
4. Download IMDb dataset into `/data`
5. Run:
