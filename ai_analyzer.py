"""
CareerPulse AI Resume Analyzer & Job Matching Engine
Parses resumes (PDF, DOCX, TXT), extracts skills, calculates ATS scores,
generates actionable recommendations, and matches candidates with open vacancies.
"""

import os
import re
from pypdf import PdfReader

# Master taxonomy of recognized technical and professional skills
TECH_SKILLS_DB = {
    # Programming Languages
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang",
    "rust", "ruby", "php", "swift", "kotlin", "scala", "dart", "html", "html5",
    "css", "css3", "sql", "bash", "shell", "r", "matlab",
    
    # Web & Backend Frameworks
    "react", "react.js", "angular", "vue", "vue.js", "next.js", "node.js", "express",
    "flask", "django", "fastapi", "spring", "spring boot", "asp.net", ".net",
    "laravel", "ruby on rails", "graphql", "rest", "restful api", "rest api", "grpc",
    
    # Cloud, DevOps & Infrastructure
    "aws", "amazon web services", "azure", "gcp", "google cloud", "docker",
    "kubernetes", "k8s", "terraform", "ansible", "jenkins", "ci/cd", "git",
    "github", "gitlab", "linux", "unix", "nginx", "microservices", "serverless",
    "prometheus", "grafana", "helm",
    
    # Databases & Caching
    "postgresql", "postgres", "mysql", "mongodb", "sqlite", "redis", "elasticsearch",
    "cassandra", "dynamodb", "oracle", "mariadb", "neo4j", "supabase", "firebase",
    
    # Data Science, AI & Machine Learning
    "machine learning", "deep learning", "artificial intelligence", "ai", "nlp",
    "natural language processing", "computer vision", "pytorch", "tensorflow",
    "keras", "scikit-learn", "pandas", "numpy", "scipy", "llm", "large language models",
    "generative ai", "transformers", "huggingface", "data analysis", "data engineering",
    
    # Design, Architecture & Soft Skills
    "figma", "ui/ux", "ui design", "ux design", "wireframing", "prototyping",
    "user research", "design systems", "agile", "scrum", "kanban", "jira",
    "system design", "distributed systems", "oop", "clean architecture",
    "unit testing", "tdd", "leadership", "mentorship", "problem solving"
}

ACTION_VERBS = {
    "architected", "developed", "engineered", "designed", "implemented",
    "led", "spearheaded", "optimized", "scaled", "automated", "built",
    "launched", "created", "reduced", "improved", "increased", "delivered"
}


def extract_text_from_file(file_path):
    """Extract plain text from PDF, TXT or DOC files."""
    if not os.path.exists(file_path):
        return ""

    ext = file_path.rsplit(".", 1)[-1].lower() if "." in file_path else ""

    if ext == "pdf":
        try:
            reader = PdfReader(file_path)
            extracted = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted.append(text)
            return "\n".join(extracted)
        except Exception:
            # Fallback plain read
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read()
            except Exception:
                return ""
    else:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return ""


def extract_skills_from_text(text):
    """Identify skills present in the resume text using exact and token boundaries."""
    text_clean = text.lower()
    found_skills = set()

    for skill in TECH_SKILLS_DB:
        # Match using word boundaries or symbol-safe boundaries
        pattern = r"(?:\b|\W)" + re.escape(skill) + r"(?:\b|\W)"
        if re.search(pattern, text_clean):
            found_skills.add(skill.title() if len(skill) > 3 and not skill.isupper() else skill.upper() if len(skill) <= 3 else skill.title())

    return sorted(list(found_skills))


def estimate_experience_level(text):
    """Estimate experience level from resume content."""
    text_lower = text.lower()

    # Look for numeric years: e.g., "5+ years", "4 years of experience"
    year_matches = re.findall(r"(\d+)\+?\s*years?(?:\s*of)?\s*(?:experience)?", text_lower)
    max_years = 0
    if year_matches:
        try:
            max_years = max([int(y) for y in year_matches if int(y) < 40])
        except ValueError:
            max_years = 0

    if any(k in text_lower for k in ["principal", "staff engineer", "vp", "director", "head of", "architect"]) or max_years >= 8:
        return "Principal / Staff / Lead (8+ years exp)", 95
    elif any(k in text_lower for k in ["senior", "sr."]) or max_years >= 5:
        return "Senior Specialist (5+ years exp)", 88
    elif any(k in text_lower for k in ["mid-level", "intermediate"]) or max_years >= 2:
        return "Mid-Level Professional (2-5 years exp)", 78
    elif any(k in text_lower for k in ["junior", "associate", "entry-level", "intern", "internship"]) or max_years <= 1:
        return "Entry-Level / Junior (0-2 years exp)", 68
    else:
        return "Mid-Level Professional (3+ years exp)", 75


def analyze_resume_profile(resume_text, profile_skills=""):
    """
    Produce comprehensive AI insights including ATS Score,
    Key Strengths, Improvement Suggestions, and Experience analysis.
    """
    combined_text = (resume_text + " " + (profile_skills or "")).strip()
    extracted_skills = extract_skills_from_text(combined_text)

    # If profile_skills contains additional comma-separated skills, merge them
    if profile_skills:
        for s in profile_skills.split(","):
            s_clean = s.strip()
            if s_clean and not any(s_clean.lower() == es.lower() for es in extracted_skills):
                extracted_skills.append(s_clean)

    exp_label, base_exp_score = estimate_experience_level(combined_text)

    # ATS Scoring Calculation
    score = 40  # baseline
    strengths = []
    recommendations = []

    # 1. Skills Breadth
    skill_count = len(extracted_skills)
    if skill_count >= 10:
        score += 25
        strengths.append(f"Outstanding technical vocabulary: Detected {skill_count} relevant industry competencies and toolsets.")
    elif skill_count >= 5:
        score += 18
        strengths.append(f"Solid skill baseline: Identified {skill_count} key technical competencies.")
    else:
        score += 8
        recommendations.append("Expand technical competencies: Add more industry-standard tools, frameworks, and database technologies.")

    # 2. Action verbs & Impact
    text_lower = combined_text.lower()
    found_verbs = [v for v in ACTION_VERBS if v in text_lower]
    if len(found_verbs) >= 4:
        score += 15
        strengths.append(f"Strong action-driven phrasing: Effectively demonstrates impact using leadership verbs ({', '.join(found_verbs[:3])}).")
    else:
        recommendations.append("Strengthen bullet points with strong action verbs like 'Engineered', 'Optimized', 'Architected', and 'Scaled'.")

    # 3. Measurable Metrics (%, $, numbers)
    has_metrics = bool(re.search(r"\b(?:\d+%(?:|\s*increase|\s*reduction|\s*improvement)|\$\d+|\d+x)\b", text_lower))
    if has_metrics:
        score += 10
        strengths.append("High ATS impact: Contains quantifiable achievements with measurable performance metrics.")
    else:
        recommendations.append("Incorporate quantitative metrics: Quantify results with percentages, speedups (e.g. 'reduced latency by 35%'), or revenue impact.")

    # 4. Education & Contact info
    has_contact = bool(re.search(r"[\w\.-]+@[\w\.-]+", combined_text)) or bool(re.search(r"\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}", combined_text))
    if has_contact:
        score += 5
        strengths.append("Complete contact profile: Clear communication details detected for recruiter outreach.")
    else:
        recommendations.append("Ensure your phone number, email address, and LinkedIn or GitHub links are prominently placed at the top.")

    # 5. Section Organization
    has_sections = any(sec in text_lower for sec in ["experience", "education", "skills", "projects", "summary"])
    if has_sections:
        score += 5

    # Clamp score to reasonable range
    score = min(max(score, 52), 98)

    if not recommendations:
        recommendations.append("Keep resume updated with your most recent projects and certifications to maintain high visibility.")

    return {
        "ats_score": score,
        "experience_level": exp_label,
        "skills": extracted_skills,
        "strengths": strengths,
        "recommendations": recommendations,
        "raw_text_length": len(combined_text)
    }


def match_resume_with_jobs(extracted_skills, resume_text, jobs):
    """
    Rank all open positions according to compatibility with candidate's resume.
    Returns list of jobs with match percentage, matching skills, and missing skills.
    """
    matched_jobs = []
    resume_skills_lower = {s.lower() for s in extracted_skills}
    resume_text_lower = (resume_text or "").lower()

    for job in jobs:
        # Extract required skills from job
        job_skills_raw = (job["skills"] or "").split(",") if job["skills"] else []
        job_skills = [s.strip() for s in job_skills_raw if s.strip()]

        # If job skills field was empty, extract from title and description
        if not job_skills:
            job_full_desc = f"{job['title']} {job['description']} {job['requirements'] or ''}"
            job_skills = extract_skills_from_text(job_full_desc)

        job_skills_lower = {s.lower() for s in job_skills}

        # 1. Direct Skill Matches
        matched_skill_set = []
        missing_skill_set = []

        for js in job_skills:
            if js.lower() in resume_skills_lower or js.lower() in resume_text_lower:
                matched_skill_set.append(js)
            else:
                missing_skill_set.append(js)

        # 2. Text Keyword Overlap (Title / Description)
        title_words = [w for w in re.findall(r"\w+", job["title"].lower()) if len(w) > 3]
        title_matches = sum(1 for w in title_words if w in resume_text_lower)

        # 3. Score Calculation
        if job_skills:
            skill_ratio = len(matched_skill_set) / len(job_skills)
        else:
            skill_ratio = 0.5

        title_boost = min(title_matches * 10, 20)
        match_score = int(round((skill_ratio * 70) + title_boost + 10))
        match_score = min(max(match_score, 35), 98)

        # Categorize Match
        if match_score >= 82:
            fit_tier = "Excellent Match"
            fit_badge = "badge-selected"
            fit_color = "#34d399"
        elif match_score >= 68:
            fit_tier = "Strong Fit"
            fit_badge = "badge-interview"
            fit_color = "#c084fc"
        elif match_score >= 50:
            fit_tier = "Moderate Fit"
            fit_badge = "badge-shortlisted"
            fit_color = "#fbbf24"
        else:
            fit_tier = "Growth Opportunity"
            fit_badge = "badge-type"
            fit_color = "#94a3b8"

        matched_jobs.append({
            "job": job,
            "match_score": match_score,
            "fit_tier": fit_tier,
            "fit_badge": fit_badge,
            "fit_color": fit_color,
            "matched_skills": matched_skill_set,
            "missing_skills": missing_skill_set[:5]  # Top 5 skills to improve
        })

    # Sort descending by match_score
    matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    return matched_jobs
