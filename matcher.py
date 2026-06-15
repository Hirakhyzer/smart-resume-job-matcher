"""Core matching logic for the Smart Resume Job Matcher app."""
from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, asdict
from typing import Iterable

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "have",
    "in", "is", "it", "of", "on", "or", "our", "that", "the", "their", "this", "to",
    "we", "with", "you", "your", "will", "work", "team", "role", "candidate", "job",
    "experience", "skills", "ability", "strong", "using", "use", "including", "such",
}

SKILL_ALIASES = {
    "python": ["python", "python3"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "java": ["java"],
    "sql": ["sql", "postgresql", "mysql", "sqlite", "mssql"],
    "html": ["html", "html5"],
    "css": ["css", "css3", "tailwind", "bootstrap"],
    "react": ["react", "reactjs", "react.js"],
    "node.js": ["node", "nodejs", "node.js", "express"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "streamlit": ["streamlit"],
    "machine learning": ["machine learning", "ml", "scikit-learn", "sklearn"],
    "deep learning": ["deep learning", "neural network", "neural networks", "tensorflow", "pytorch"],
    "nlp": ["nlp", "natural language processing", "text classification"],
    "data analysis": ["data analysis", "data analytics", "analytics"],
    "data visualization": ["data visualization", "visualization", "dashboard", "plotly", "matplotlib"],
    "git": ["git", "github", "version control"],
    "docker": ["docker", "container", "containers"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "api development": ["api", "rest api", "apis", "backend api"],
    "testing": ["testing", "unit tests", "pytest", "unittest", "test automation"],
    "ci/cd": ["ci/cd", "github actions", "continuous integration", "deployment pipeline"],
    "agile": ["agile", "scrum", "kanban"],
    "communication": ["communication", "collaboration", "stakeholders"],
    "problem solving": ["problem solving", "analytical", "critical thinking"],
}

SECTION_HINTS = {
    "education": ["education", "degree", "university", "college", "bachelor", "master", "phd"],
    "experience": ["experience", "employment", "work history", "internship"],
    "projects": ["projects", "portfolio", "github"],
    "skills": ["skills", "technical skills", "technologies"],
}

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9.+#/-]*")


@dataclass
class MatchReport:
    overall_score: int
    skill_score: int
    keyword_score: int
    section_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    job_keywords: list[str]
    resume_keywords: list[str]
    ats_warnings: list[str]
    suggestions: list[str]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    def to_text(self) -> str:
        lines = [
            "Smart Resume Job Matcher Report",
            "================================",
            f"Overall score: {self.overall_score}%",
            f"Skill score: {self.skill_score}%",
            f"Keyword score: {self.keyword_score}%",
            f"Section score: {self.section_score}%",
            "",
            "Matched skills:",
            *[f"- {item}" for item in self.matched_skills],
            "",
            "Missing skills:",
            *[f"- {item}" for item in self.missing_skills],
            "",
            "Important job keywords:",
            *[f"- {item}" for item in self.job_keywords],
            "",
            "ATS warnings:",
            *[f"- {item}" for item in self.ats_warnings],
            "",
            "Suggestions:",
            *[f"- {item}" for item in self.suggestions],
        ]
        return "\n".join(lines) + "\n"


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def tokenize(text: str) -> list[str]:
    return [token.lower().strip(".,;:()[]{}") for token in TOKEN_RE.findall(text)]


def extract_skills(text: str) -> set[str]:
    normalized = f" {normalize_text(text)} "
    found = set()
    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias.lower()) + r"(?![a-zA-Z0-9])"
            if re.search(pattern, normalized):
                found.add(skill)
                break
    return found


def top_keywords(text: str, limit: int = 12) -> list[str]:
    tokens = [token for token in tokenize(text) if len(token) > 2 and token not in STOPWORDS]
    counts = Counter(tokens)
    return [word for word, _ in counts.most_common(limit)]


def section_coverage(resume_text: str) -> tuple[int, list[str]]:
    normalized = normalize_text(resume_text)
    present = []
    missing = []
    for section, hints in SECTION_HINTS.items():
        if any(hint in normalized for hint in hints):
            present.append(section)
        else:
            missing.append(section)
    score = round(len(present) / len(SECTION_HINTS) * 100)
    return score, missing


def ats_warnings(resume_text: str) -> list[str]:
    warnings = []
    if len(resume_text.strip()) < 500:
        warnings.append("Resume text looks short. Add measurable project or work achievements.")
    if "@" not in resume_text:
        warnings.append("No email address detected. Add clear contact information.")
    if not re.search(r"https?://|github.com|linkedin.com", resume_text.lower()):
        warnings.append("No portfolio, GitHub, or LinkedIn link detected.")
    if not re.search(r"\b\d+%|\b\d+x|\b\d+\+|\b\d+ users|\b\d+ projects", resume_text.lower()):
        warnings.append("Few measurable achievements detected. Add numbers such as percentages, users, speedups, or project counts.")
    return warnings


def make_suggestions(missing_skills: Iterable[str], missing_sections: Iterable[str], job_keywords: list[str]) -> list[str]:
    suggestions = []
    missing_skills = list(missing_skills)
    missing_sections = list(missing_sections)

    if missing_skills:
        suggestions.append("Add relevant evidence for these job skills if you have them: " + ", ".join(missing_skills[:6]) + ".")
    if missing_sections:
        suggestions.append("Add or rename these resume sections for better scanning: " + ", ".join(missing_sections) + ".")
    if job_keywords:
        suggestions.append("Mirror important job language naturally where accurate: " + ", ".join(job_keywords[:6]) + ".")
    suggestions.append("Use bullet points with action verbs, tools used, and measurable outcomes.")
    suggestions.append("Keep the resume truthful. Do not add skills or experience you cannot explain in an interview.")
    return suggestions


def score_overlap(resume_items: set[str], job_items: set[str]) -> int:
    if not job_items:
        return 0
    return round(len(resume_items & job_items) / len(job_items) * 100)


def analyze_match(resume_text: str, job_text: str) -> MatchReport:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)
    matched_skills = sorted(resume_skills & job_skills)
    missing_skills = sorted(job_skills - resume_skills)

    skill_score = score_overlap(resume_skills, job_skills)

    resume_keywords = set(top_keywords(resume_text, limit=25))
    job_keyword_list = top_keywords(job_text, limit=15)
    job_keyword_set = set(job_keyword_list)
    keyword_score = score_overlap(resume_keywords, job_keyword_set)

    section_score, missing_sections = section_coverage(resume_text)
    warnings = ats_warnings(resume_text)
    suggestions = make_suggestions(missing_skills, missing_sections, job_keyword_list)

    overall_score = round((skill_score * 0.50) + (keyword_score * 0.30) + (section_score * 0.20))

    return MatchReport(
        overall_score=overall_score,
        skill_score=skill_score,
        keyword_score=keyword_score,
        section_score=section_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        job_keywords=job_keyword_list,
        resume_keywords=sorted(resume_keywords)[:15],
        ats_warnings=warnings,
        suggestions=suggestions,
    )
