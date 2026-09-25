import re
from typing import List

STOP_WORDS = {
    "a", "an", "the", "is", "are", "and", "or", "of", "to", "in", "on", "for", "with",
    "this", "that", "it", "as", "at", "by", "from", "be", "was", "were", "we", "you",
    "your", "their", "they", "them", "he", "she", "his", "her", "its", "do", "does", "did",
    "how", "many", "what", "when", "where", "why", "who", "can", "could", "should", "would",
    "about", "into", "over", "under", "after", "before", "between", "through", "during", "if",
    "then", "than", "not", "no", "yes", "more", "most", "some", "any", "all", "each", "every"
}


def normalize_text(text: str) -> list[str]:
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    words = cleaned.split()
    filtered = []
    for word in words:
        if word and word not in STOP_WORDS and len(word) > 1:
            filtered.append(word)
    return filtered


def retrieve_relevant_documents(question: str, documents: List[dict], top_k: int = 3):
    question_words = set(normalize_text(question))
    if not question_words:
        return []

    scored_docs = []
    for document in documents:
        text = document.get("extractedText", "")
        doc_words = set(normalize_text(text))
        if not doc_words:
            continue
        score = len(question_words.intersection(doc_words))
        if score > 0:
            scored_docs.append({"document": document, "score": score})

    scored_docs.sort(key=lambda item: item["score"], reverse=True)
    ranked = [item["document"] for item in scored_docs[:top_k]]
    return ranked
