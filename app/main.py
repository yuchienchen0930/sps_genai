from fastapi import FastAPI
from pydantic import BaseModel
from app.bigram_model import BigramModel
import spacy

app = FastAPI()

# 原本的 bigram model
corpus = [
    "The Count of Monte Cristo is a novel written by Alexandre Dumas.",
    "this is another example sentence",
    "we are generating text based on bigram probabilities",
    "bigram models are simple but effective"
]

bigram_model = BigramModel(corpus)

class TextGenerationRequest(BaseModel):
    start_word: str
    length: int

# ⭐ 新增：載入 Spacy 模型
nlp = spacy.load("en_core_web_md")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/generate")
def generate_text(request: TextGenerationRequest):
    generated_text = bigram_model.generate_text(request.start_word, request.length)
    return {"generated_text": generated_text}

# ⭐ 新增：embedding endpoint
@app.get("/embedding/{word}")
def get_embedding(word: str):
    doc = nlp(word)
    vector = doc.vector.tolist()
    return {
        "word": word,
        "vector_dim": len(vector),
        "vector": vector
    }
