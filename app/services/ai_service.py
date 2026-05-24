from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
import os
import json
from fastapi import HTTPException

env_path = Path(__file__).resolve().parent.parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

# Prevent startup crashes on platforms like Railway if GROQ_API_KEY is not yet configured
api_key = os.getenv("GROQ_API_KEY") or "placeholder_key"
client = Groq(
    api_key=api_key
)

def call_groq(prompt, temperature=0.3, response_format=None):
    if api_key == "placeholder_key":
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY environment variable is not configured. Please add GROQ_API_KEY to your Railway service variables."
        )
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format=response_format or {"type": "text"},
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        err_str = str(e)
        if "api_key" in err_str or "401" in err_str or "unauthorized" in err_str.lower():
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY is invalid or unauthorized. Please verify your Groq API key in your Railway service variables."
            )
        raise HTTPException(
            status_code=500,
            detail=f"Groq AI error: {err_str}"
        )

def generate_summary(repo_data):
    prompt = f"""
    You are a strict senior technical recruiter.

    Analyze the GitHub repositories honestly and realistically.

    IMPORTANT RULES:
    - Do NOT exaggerate skills.
    - Do NOT overhype beginner projects.
    - Do NOT label someone as "advanced" unless the repositories genuinely demonstrate advanced engineering.
    - A simple CRUD app, static website, or beginner ML notebook should NOT be described as production-grade or enterprise-level.
    - Avoid flashy LinkedIn-style wording.
    - Keep summaries concise, realistic, and professional.
    - Infer skills only from clear evidence in repositories, READMEs, technologies used, and project complexity.
    - If projects are beginner/intermediate level, state that honestly.
    - Focus on accuracy over praise.

    Return ONLY valid JSON.

    Format:

    {{
        "professional_summary": "max 3 concise realistic sentences",

        "key_skills": {{
            "languages": [],
            "frameworks": [],
            "ml_tools": [],
            "devtools": []
        }},

        "top_company_matches": [
            {{
                "company": "",
                "role": "",
                "match_pct": 0
            }}
        ],

        "resume_bullets": [
            "",
            "",
            ""
        ]
    }}

    Repository Data:
    {repo_data}
    """

    content = call_groq(prompt, temperature=0.5, response_format={"type": "json_object"})
    return json.loads(content)

def analyze_readme(readme_content):

    prompt = f"""
    Analyze this GitHub README.

    IMPORTANT:
    - Keep output concise
    - Do NOT exaggerate
    - Return ONLY valid JSON

    Format:

    {{
        "project_summary": "",

        "main_features": [],

        "tech_stack": [],

        "resume_bullets": [],

        "difficulty_level": ""
    }}

    README:
    {readme_content}
    """

    content = call_groq(prompt, temperature=0.3, response_format={"type": "json_object"})
    return json.loads(content)

def match_job_description(
    username,
    job_description
):

    from app.services.github_service import (
        get_user_repositories
    )

    from app.services.analyzer_service import (
        extract_repo_data
    )


    repos = get_user_repositories(username)

    cleaned_data = extract_repo_data(repos)

    prompt = f"""
    You are a strict senior technical recruiter.

    Compare the candidate's GitHub repositories
    with the given job description.

    IMPORTANT RULES:
    - Be realistic.
    - Do NOT exaggerate.
    - Do NOT overrate beginner projects.
    - Judge based on actual project complexity.
    - Keep response concise and structured.
    - Match percentage must be strict and realistic.
    - Beginner/intermediate projects should not exceed 65-75% for senior roles.

    Return ONLY valid JSON.

    Format:

    {{
        "match_percentage": 0,

        "final_verdict": "",

        "strengths": [- Strengths must reference actual demonstrated project work.
                      - Avoid vague statements like "AI-related projects".
                      - Mention concrete technologies or project types.],

        "missing_skills": [],

        "top_matching_repositories": [
            {{
                "repo_name": "",
                "reason": "",
                "match_percentage": 0
            }}
        ]
    }}

    Candidate GitHub Repository Data:
    {cleaned_data}

    Job Description:
    {job_description}
    """

    content = call_groq(prompt, temperature=0.3, response_format={"type": "json_object"})
    return json.loads(content)