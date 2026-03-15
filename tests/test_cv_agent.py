import sys
import tempfile
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.cv_parser import extract_text_from_pdf
from src.feature_extraction import parse_cv
from src.scoring import score_candidate


def test_parse_cv_basic():
    text = """John Doe\n5 years experience in Python, SQL and Machine Learning.\nMaster degree in Computer Science.\nSpeaks English and French.\nWorked at Acme and Beta Corp."""
    features = parse_cv(text)
    assert features["years_experience"] >= 5
    assert "master" in features["education_level"]
    assert "python" in features["technical_skills"]
    assert "english" in features["languages"]


def test_score_candidate_relevance():
    cv_text = "Experienced data engineer with Python, SQL, ETL and AWS."  
    features = parse_cv(cv_text)
    job_description = "Looking for a Python and SQL engineer experienced in AWS."  
    score = score_candidate(features, job_description)
    assert score["relevance"] > 0.1
    assert score["score"] > 0


def test_extract_text_from_pdf_dummy():
    # create a small PDF in tmp using pure bytes for compatibility
    pdf_data = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 0/Kids[]>>endobj\nxref\n0 3\n0000000000 65535 f \n0000000010 00000 n \n0000000053 00000 n \ntrailer<</Size 3/Root 1 0 R>>\nstartxref\n94\n%%EOF"
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmpf:
        tmpf.write(pdf_data)
        tmpf_path = tmpf.name

    extracted = extract_text_from_pdf(tmpf_path)
    assert isinstance(extracted, str)
    Path(tmpf_path).unlink(missing_ok=True)
