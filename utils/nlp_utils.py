import spacy # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from typing import List
from sklearn.metrics.pairwise import cosine_similarity # type: ignore

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text: str) -> str:
    """Clean and lemmatize text"""
    doc = nlp(text.lower())
    return " ".join(token.lemma_ for token in doc if not token.is_stop and token.is_alpha)

def similarity_score(text1: str, text2: str) -> float:
    """Calculate cosine similarity between two texts"""
    vectorizer = TfidfVectorizer(tokenizer=preprocess_text)
    tfidf = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]