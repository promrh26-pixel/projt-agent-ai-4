"""Feature extraction from CV text."""
import re
from typing import Dict, List

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


DEFAULT_TECH_SKILLS = ["python", "java", "sql", "machine learning", "deep learning", "nlp", "data science", "cloud", "docker", "kubernetes", "aws", "azure", "react", "node.js", "tensorflow", "pytorch"]
DEFAULT_LANGUAGES = ["english", "french", "arabic", "spanish", "german", "chinese"]
DEFAULT_SECTORS = ["it", "finance", "healthcare", "education", "retail", "marketing", "telecom"]

EDUCATION_LEVELS = {
    "phd": 5,
    "doctorate": 5,
    "master": 4,
    "bac+5": 4,
    "bachelor": 3,
    "licence": 3,
    "bac+3": 3,
    "associate": 2,
    "high school": 1,
}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> List[str]:
    return [tok for tok in normalize_text(text).split() if tok and tok not in ENGLISH_STOP_WORDS]


def extract_years_experience(text: str) -> int:
    text_lower = text.lower()
    matches = re.findall(r"(\d+)\s+(?:\+\s*)?(?:years|yrs|year)", text_lower)
    values = [int(v) for v in matches if v.isdigit()]
    if values:
        return max(values)

    matches = re.findall(r"(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s+years", text_lower)
    if matches:
        return int(float(matches[-1][1]))

    # fallback detection by career duration words
    return 0


def extract_education_level(text: str) -> str:
    text_lower = text.lower()
    for keyword in sorted(EDUCATION_LEVELS.keys(), key=lambda k: -len(k)):
        if keyword in text_lower:
            return keyword
    return "unknown"


def extract_technical_skills(text: str, skills_list: List[str] = None) -> List[str]:
    candidate = normalize_text(text)
    skills_list = skills_list or DEFAULT_TECH_SKILLS
    found = [skill for skill in skills_list if skill in candidate]
    return found


def extract_languages(text: str, languages_list: List[str] = None) -> List[str]:
    candidate = normalize_text(text)
    languages_list = languages_list or DEFAULT_LANGUAGES
    found = [lang for lang in languages_list if lang in candidate]
    return found


def extract_activity_sector(text: str, sectors_list: List[str] = None) -> str:
    candidate = normalize_text(text)
    sectors_list = sectors_list or DEFAULT_SECTORS
    for sector in sectors_list:
        if sector in candidate:
            return sector
    return "unknown"


def extract_previous_companies(text: str) -> int:
    text_lower = text.lower()
    matches = re.findall(r"\b(?:worked at|at|from|with)\s+([a-zA-Z0-9 &.,'-]+)", text_lower)
    companies = [c.strip() for c in matches if len(c.strip()) > 2]
    return min(len(set(companies)), 10)


def parse_cv(text: str) -> Dict[str, object]:
    normalized = normalize_text(text)

    return {
        "years_experience": extract_years_experience(text),
        "education_level": extract_education_level(text),
        "technical_skills": extract_technical_skills(text),
        "languages": extract_languages(text),
        "activity_sector": extract_activity_sector(text),
        "previous_companies": extract_previous_companies(text),
        "raw_text": text,
        "tokens": tokenize(text),
        "normalized_text": normalized,
    }
