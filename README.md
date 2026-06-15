# Smart Resume Job Matcher

A polished Streamlit app that compares a resume with a job description, calculates a match score, highlights matched and missing skills, and generates practical resume improvement suggestions.

This project is designed as a real-world portfolio app for students, developers, and job seekers.

## Features

- Beautiful two-column Resume vs Job Description UI
- Overall match score with progress indicators
- Skill match analysis
- Keyword overlap analysis
- Missing skill recommendations
- ATS-style formatting warnings
- Downloadable JSON and text reports
- Built-in sample resume and job description
- Lightweight Python matching engine
- Unit tests for the core matcher

## Tech Stack

- Python
- Streamlit
- Standard-library text processing
- Pytest for tests

## Project Structure

```text
smart-resume-job-matcher/
├── app.py
├── matcher.py
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── sample_data/
│   ├── sample_resume.txt
│   └── sample_job_description.txt
├── tests/
│   └── test_matcher.py
└── .github/
    └── workflows/
        └── python-tests.yml
```

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Run Tests

```bash
pytest
```

## How It Works

The matcher extracts normalized skills and important keywords from both texts. It combines skill overlap, keyword overlap, and resume completeness checks into an overall match score. The result includes a structured report with matched skills, missing skills, important job keywords, and improvement suggestions.

## Portfolio Notes

This project is intentionally easy to run and explain. It shows UI design, Python programming, text processing, scoring logic, report generation, and GitHub project structure in one practical application.
