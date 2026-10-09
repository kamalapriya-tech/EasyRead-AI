import math
import re
from collections import Counter


STOP_WORDS = {
    "the", "is", "are", "was", "were", "a", "an", "and",
    "or", "but", "in", "on", "at", "to", "of", "for",
    "with", "by", "from", "as", "it", "this", "that",
    "be", "been", "being", "has", "have", "had", "not",
    "we", "they", "he", "she", "you", "i", "their",
    "its", "our", "can", "will", "would", "should"
}


def tokenize(text):
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9'-]*\b",
                       text.lower())
    return [
        word for word in words
        if word not in STOP_WORDS and len(word) > 1
    ]


def extract_keywords(text, top_n=10):
    """Rank keywords using a pure-Python TF-IDF calculation."""

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    documents = [tokenize(s) for s in sentences if s.strip()]

    if not documents:
        return []

    # Document frequency: number of sentences containing each word.
    document_frequency = Counter()

    for words in documents:
        document_frequency.update(set(words))

    total_documents = len(documents)
    scores = Counter()

    for words in documents:
        frequencies = Counter(words)
        total_words = len(words)

        if not total_words:
            continue

        for word, count in frequencies.items():
            tf = count / total_words
            idf = math.log(
                (1 + total_documents) /
                (1 + document_frequency[word])
            ) + 1

            scores[word] += tf * idf

    ranked = scores.most_common(top_n)

    return [
        {"word": word, "score": round(score, 4)}
        for word, score in ranked
    ]