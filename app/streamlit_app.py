"""Streamlit app for CV AI screening agent."""
import streamlit as st
import pandas as pd

from src.utils import load_and_parse_cvs
from src.scoring import rank_candidates


def main():
    st.set_page_config(page_title="AI CV Screening Agent", layout="wide")

    st.title("AI-Based CV Screening & Ranking")
    st.markdown("Upload PDF CVs and a job description to analyze candidate fit.")

    uploaded_files = st.file_uploader("Upload one or more CV PDFs", type=["pdf"], accept_multiple_files=True)
    job_description = st.text_area("Job description", height=180)

    if st.button("Analyze"):
        if not uploaded_files:
            st.warning("Please upload at least one CV PDF file.")
            return
        if not job_description.strip():
            st.warning("Please enter a job description.")
            return

        with st.spinner("Processing CVs..."):
            file_paths = []
            for uploaded in uploaded_files:
                file_location = f"/tmp/{uploaded.name}"
                with open(file_location, "wb") as f:
                    f.write(uploaded.getbuffer())
                file_paths.append(file_location)

            candidates = load_and_parse_cvs(file_paths)
            ranked = rank_candidates(candidates, job_description)

        st.success("Analysis complete!")

        df = pd.DataFrame([{
            "Candidate File": c.get("file"),
            "Experience (yrs)": c.get("years_experience"),
            "Education": c.get("education_level"),
            "Skills": ", ".join(c.get("technical_skills", [])),
            "Languages": ", ".join(c.get("languages", [])),
            "Companies": c.get("previous_companies"),
            "Relevance": c.get("relevance"),
            "Final Score": c.get("score"),
            "Rank": c.get("rank"),
        } for c in ranked])

        st.dataframe(df.sort_values(by="Rank"))

        best = ranked[0]
        st.subheader("Top candidate")
        st.write(f"**File:** {best.get('file')}")
        st.write(f"**Score:** {best.get('score')}")
        st.write(f"**Extracted features:**")
        st.json({
            "years_experience": best.get("years_experience"),
            "education_level": best.get("education_level"),
            "tech_skills": best.get("technical_skills"),
            "languages": best.get("languages"),
            "activity_sector": best.get("activity_sector"),
            "previous_companies": best.get("previous_companies"),
        })


if __name__ == "__main__":
    main()
