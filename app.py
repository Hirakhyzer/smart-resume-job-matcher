from __future__ import annotations

from pathlib import Path

import streamlit as st

from matcher import analyze_match

BASE_DIR = Path(__file__).parent
SAMPLE_RESUME = BASE_DIR / "sample_data" / "sample_resume.txt"
SAMPLE_JOB = BASE_DIR / "sample_data" / "sample_job_description.txt"

st.set_page_config(
    page_title="Smart Resume Job Matcher",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
:root {
    --card-bg: rgba(255,255,255,0.86);
    --border: rgba(120, 130, 155, 0.22);
    --shadow: 0 18px 45px rgba(15, 23, 42, 0.10);
}
.main {
    background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 45%, #fff7ed 100%);
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.hero {
    padding: 2.2rem;
    border-radius: 28px;
    background: radial-gradient(circle at top left, rgba(59,130,246,.20), transparent 34%),
                linear-gradient(135deg, rgba(15,23,42,.96), rgba(30,41,59,.92));
    color: white;
    box-shadow: var(--shadow);
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-size: 3rem;
    line-height: 1.05;
    margin-bottom: .6rem;
}
.hero p {
    font-size: 1.08rem;
    color: rgba(255,255,255,.82);
    max-width: 920px;
}
.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: .55rem;
    margin-top: 1rem;
}
.badge {
    padding: .45rem .75rem;
    border-radius: 999px;
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.20);
    font-size: .86rem;
}
.metric-card {
    padding: 1.2rem;
    border-radius: 22px;
    background: var(--card-bg);
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    min-height: 134px;
}
.metric-label {
    font-size: .88rem;
    color: #64748b;
    margin-bottom: .35rem;
}
.metric-value {
    font-size: 2.3rem;
    font-weight: 800;
    color: #0f172a;
}
.metric-help {
    font-size: .86rem;
    color: #64748b;
}
.panel {
    padding: 1rem;
    border-radius: 24px;
    background: rgba(255,255,255,.72);
    border: 1px solid var(--border);
    box-shadow: 0 10px 30px rgba(15,23,42,.06);
}
.chip {
    display: inline-block;
    padding: .38rem .68rem;
    margin: .18rem;
    border-radius: 999px;
    background: #e0f2fe;
    color: #075985;
    font-size: .85rem;
    font-weight: 600;
}
.chip-missing {
    display: inline-block;
    padding: .38rem .68rem;
    margin: .18rem;
    border-radius: 999px;
    background: #fee2e2;
    color: #991b1b;
    font-size: .85rem;
    font-weight: 600;
}
.small-note {
    color: #64748b;
    font-size: .9rem;
}
.stTextArea textarea {
    border-radius: 18px;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def read_sample(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


with st.sidebar:
    st.title("🎯 Matcher Controls")
    st.caption("Paste your resume and a job post, then generate a structured match report.")
    use_samples = st.button("Load sample resume + job", use_container_width=True)
    st.divider()
    st.markdown("### Score weights")
    st.write("Skills: 50%")
    st.write("Keywords: 30%")
    st.write("Resume sections: 20%")
    st.divider()
    st.markdown("### Tip")
    st.info("For best results, include technical skills, projects, education, links, and measurable achievements.")

if use_samples:
    st.session_state["resume_text"] = read_sample(SAMPLE_RESUME)
    st.session_state["job_text"] = read_sample(SAMPLE_JOB)

st.markdown(
    """
    <div class="hero">
      <h1>Smart Resume Job Matcher</h1>
      <p>Compare a resume against a job description, find missing skills, and generate a clean improvement report for better applications.</p>
      <div class="badge-row">
        <span class="badge">Resume scoring</span>
        <span class="badge">Skill gap analysis</span>
        <span class="badge">ATS-style warnings</span>
        <span class="badge">Downloadable reports</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("📄 Resume Text")
    resume_text = st.text_area(
        "Paste resume text",
        value=st.session_state.get("resume_text", ""),
        height=330,
        label_visibility="collapsed",
        placeholder="Paste the candidate resume here...",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("💼 Job Description")
    job_text = st.text_area(
        "Paste job description",
        value=st.session_state.get("job_text", ""),
        height=330,
        label_visibility="collapsed",
        placeholder="Paste the job description here...",
    )
    st.markdown("</div>", unsafe_allow_html=True)

analyze = st.button("Analyze Match", type="primary", use_container_width=True)

if analyze:
    if not resume_text.strip() or not job_text.strip():
        st.warning("Please add both resume text and job description text.")
    else:
        report = analyze_match(resume_text, job_text)

        st.markdown("## Results")
        c1, c2, c3, c4 = st.columns(4)
        cards = [
            (c1, "Overall Match", report.overall_score, "Combined score"),
            (c2, "Skill Match", report.skill_score, "Skills found in both texts"),
            (c3, "Keyword Match", report.keyword_score, "Important job terms covered"),
            (c4, "Section Score", report.section_score, "Resume structure coverage"),
        ]
        for col, label, value, help_text in cards:
            with col:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}%</div>
                        <div class="metric-help">{help_text}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.progress(value / 100)

        tab1, tab2, tab3, tab4 = st.tabs(["Skills", "Keywords", "Warnings", "Export"])

        with tab1:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Matched Skills")
                if report.matched_skills:
                    st.markdown("".join(f'<span class="chip">{skill}</span>' for skill in report.matched_skills), unsafe_allow_html=True)
                else:
                    st.caption("No matched skills found yet.")
            with col_b:
                st.subheader("Missing Skills")
                if report.missing_skills:
                    st.markdown("".join(f'<span class="chip-missing">{skill}</span>' for skill in report.missing_skills), unsafe_allow_html=True)
                else:
                    st.success("No missing skills found from the current skill catalog.")

        with tab2:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Important Job Keywords")
                st.write(", ".join(report.job_keywords) if report.job_keywords else "No keywords found.")
            with col_b:
                st.subheader("Resume Keywords")
                st.write(", ".join(report.resume_keywords) if report.resume_keywords else "No keywords found.")

        with tab3:
            st.subheader("ATS-Style Warnings")
            if report.ats_warnings:
                for warning in report.ats_warnings:
                    st.warning(warning)
            else:
                st.success("No major ATS-style warnings found.")

            st.subheader("Improvement Suggestions")
            for suggestion in report.suggestions:
                st.write("• " + suggestion)

        with tab4:
            st.subheader("Download Report")
            st.download_button(
                "Download JSON report",
                data=report.to_json(),
                file_name="resume_match_report.json",
                mime="application/json",
                use_container_width=True,
            )
            st.download_button(
                "Download text report",
                data=report.to_text(),
                file_name="resume_match_report.txt",
                mime="text/plain",
                use_container_width=True,
            )
else:
    st.markdown("<p class='small-note'>Load the sample data from the sidebar or paste your own texts, then click Analyze Match.</p>", unsafe_allow_html=True)
