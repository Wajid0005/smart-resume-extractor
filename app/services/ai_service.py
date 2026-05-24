from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
import os
import json

env_path = Path(__file__).resolve().parent.parent.parent / ".env"

load_dotenv(dotenv_path=env_path)


# Prevent startup crashes on platforms like Railway if GROQ_API_KEY is not yet configured
api_key = os.getenv("GROQ_API_KEY") or "placeholder_key"
client = Groq(
    api_key=api_key
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

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        response_format={
            "type": "json_object"
        },

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.5
    )

    return json.loads(
        response.choices[0].message.content
    )

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

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        response_format={
            "type":"json_object"
        },

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],

        temperature=0.3
    )

    return json.loads(
        response.choices[0].message.content
    )

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

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        response_format={
            "type": "json_object"
        },

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3
    )

    return json.loads(
        response.choices[0].message.content
    )