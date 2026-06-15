from matcher import analyze_match, extract_skills, tokenize


def test_tokenize_keeps_words():
    assert tokenize("Python, Streamlit, and SQL!") == ["python", "streamlit", "and", "sql"]


def test_extract_skills_finds_aliases():
    text = "Built Python dashboards with natural language processing and GitHub."
    skills = extract_skills(text)
    assert "python" in skills
    assert "nlp" in skills
    assert "git" in skills


def test_analyze_match_scores_resume_against_job():
    resume = "Python developer with Streamlit, SQL, machine learning, NLP, GitHub, projects, education, and experience. Email: test@example.com https://github.com/example 30% faster reports."
    job = "Need Python, Streamlit, SQL, machine learning, NLP, GitHub, testing, and communication."
    report = analyze_match(resume, job)
    assert report.overall_score > 40
    assert "python" in report.matched_skills
    assert "testing" in report.missing_skills
