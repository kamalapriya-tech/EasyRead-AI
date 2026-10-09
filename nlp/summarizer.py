
import re
from sklearn.feature_extraction.text import TfidfVectorizer


def split_sentences(text):
    """Split normalized document text into sentences."""

    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []

    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if sentence.strip()
    ]


def summarize_text(text, sentence_count=5):
    """Return the highest-ranked sentences in their original reading order."""

    sentences = split_sentences(text)

    if len(sentences) <= sentence_count:
        return sentences

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000
        )

        matrix = vectorizer.fit_transform(sentences)

    except ValueError:
        return sentences[:sentence_count]

    # Average TF-IDF weight per sentence.
    scores = matrix.mean(axis=1).A1

    # Select the most informative sentences, then restore document order.
    ranked_indices = sorted(
        range(len(sentences)),
        key=lambda i: scores[i],
        reverse=True
    )

    selected = sorted(ranked_indices[:sentence_count])

    return [sentences[i] for i in selected]