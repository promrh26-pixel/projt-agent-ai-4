"""Candidate scoring module."""
from typing import Dict, List

from .feature_extraction import EDUCATION_LEVELS
from .model import calculate_relevance_score

EDUCATION_WEIGHT = 20
EXPERIENCE_WEIGHT = 30
SKILLS_WEIGHT = 25
LANGUAGE_WEIGHT = 10
STABILITY_WEIGHT = 15

EDUCATION_VALUE = {
    "phd": 5,
    "doctorate": 5,
    "master": 4,
    "bac+5": 4,
    "bachelor": 3,
    "licence": 3,
    "bac+3": 3,
    "associate": 2,
    "high school": 1,
    "unknown": 0,
}


def education_score(level: str) -> int:
    return EDUCATION_VALUE.get(level.lower(), 0)


def stability_score(previous_companies: int) -> float:
    if previous_companies <= 1:
        return 1.0
    if previous_companies <= 3:
        return 0.8
    if previous_companies <= 5:
        return 0.5
    return 0.2


def score_candidate(candidate_features: Dict, job_description: str) -> Dict[str, object]:
    exp = candidate_features.get("years_experience", 0)
    edu = education_score(candidate_features.get("education_level", "unknown"))
    skills = candidate_features.get("technical_skills", [])
    langs = candidate_features.get("languages", [])
    prev_companies = candidate_features.get("previous_companies", 0)

    skill_match_gained = len(skills)
    languages_gained = len(langs)
    stability = stability_score(prev_companies)

    relevance = calculate_relevance_score(candidate_features.get("normalized_text", ""), job_description)

    raw_score = (
        EXPERIENCE_WEIGHT * min(exp / 15, 1.0)
        + EDUCATION_WEIGHT * (edu / 5)
        + SKILLS_WEIGHT * min(skill_match_gained / 10, 1.0)
        + LANGUAGE_WEIGHT * min(languages_gained / 3, 1.0)
        + STABILITY_WEIGHT * stability
        + 20 * relevance
    )

    final_score = round(raw_score, 2)

    return {
        "experience": exp,
        "education": edu,
        "skill_matches": skill_match_gained,
        "language_matches": languages_gained,
        "stability": stability,
        "relevance": round(relevance, 3),
        "score": final_score,
    }


def rank_candidates(candidates: List[Dict], job_description: str) -> List[Dict]:
    scored = []
    for candidate in candidates:
        scoring = score_candidate(candidate, job_description)
        candidate_record = {**candidate, **scoring}
        scored.append(candidate_record)

    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)
    for idx, c in enumerate(ranked, 1):
        c["rank"] = idx
    return ranked
