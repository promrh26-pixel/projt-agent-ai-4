"""Model-based relevance scoring."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_relevance_score(cv_text: str, job_description: str) -> float:
    """Calculate a relevance score between CV text and job description using TF-IDF cosine similarity."""
    if not cv_text or not job_description:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")
    corpus = [cv_text, job_description]
    tfidf_matrix = vectorizer.fit_transform(corpus)
    sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return float(sim)
