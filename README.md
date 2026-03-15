# AI-Based CV Screening Agent

This repository provides a complete Python-based AI agent for screening and ranking CVs (PDF format) in a recruitment pre-selection workflow. The system extracts features from CV text, computes candidate scores, and ranks candidates based on matching a job description.

## Features
- Upload and process multiple PDF CVs
- Extract text using `PyPDF2`
- NLP preprocessing (lowercasing, tokenization, stopword removal)
- Feature extraction: experience, education, skills, languages, sector, company count
- Candidate scoring by experience, education, skills, languages, stability, and relevance
- Relevance evaluation with TF-IDF + cosine similarity
- Streamlit demo interface for fast exploration

## Project Structure
```
cv-ai-agent/
├── data/
│   └── sample_cvs/   # sample PDF resumes
├── src/
│   ├── cv_parser.py
│   ├── feature_extraction.py
│   ├── scoring.py
│   ├── model.py
│   └── utils.py
├── app/
│   └── streamlit_app.py
├── notebooks/
│   └── experimentation.ipynb
├── tests/
│   └── test_cv_agent.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation
1. Clone this repository:
```bash
git clone https://github.com/<owner>/projt-agent-ai-4.git
cd projt-agent-ai-4
```
2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. (Optional) Download spaCy English model:
```bash
python -m spacy download en_core_web_sm
```

## Running the app
```bash
streamlit run app/streamlit_app.py
```

## Usage
1. Upload one or more PDF CVs.
2. Paste or type a job description.
3. Click `Analyze`.
4. View features, scores, and ranking.

## Scoring Logic
- Years of experience weighted by 30
- Education level (PhD / Master / Bachelor) weighted by 20
- Technical skills matching count weighted by 25
- Language match weighted by 10
- Stability (company hops) weighted by 15
- Relevance (TF-IDF cosine similarity) adds to score

## Ethical considerations and bias risks
- Automated CV ranking can reinforce unconscious biases, especially across gender, age, ethnicity, or schooling history.
- Always human-review shortlists before hiring decisions.
- Audit feature matching keywords for representational fairness.
- Regularly retrain and validate model behavior using unbiased datasets.
- Use this tool as assistance, not as sole decision-maker.

## Testing
```bash
pytest tests/test_cv_agent.py
```

## Sample dataset
Place anonymized PDF CVs in `data/sample_cvs/` and run the Streamlit app to test.
