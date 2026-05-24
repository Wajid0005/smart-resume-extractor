from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.services.analyzer_service import extract_repo_data
from app.services.github_service import get_readme, get_user_repositories, get_github_profile, clean_profile_data
from app.services.ai_service import analyze_readme, generate_summary
from app.services.ai_service import (
    match_job_description
)
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

class JobMatchRequest(BaseModel):
    username: str
    job_description: str

@app.get("/")
def home():

    return {
        "message": "Smart Github Resume Extractor API"
    }

@app.get("/analyze-repo")
def analyze_repo(username: str, repo_name: str):
    readme = get_readme(username,repo_name)

    analysis = analyze_readme(readme)

    return {
        "username":username,
        "repo": repo_name,
        "analysis": analysis
    }

@app.get("/profile-summary")
def profile_summary(username: str):

    profile = get_github_profile(username)
    cleaned_profile = clean_profile_data(profile)

    repos = get_user_repositories(username)
    cleaned_data = extract_repo_data(repos)

    summary = generate_summary(cleaned_data)

    repo_list =[]

    for index, repo in enumerate(cleaned_data, start=1):

        repo_list.append({
            "id": index,
            "repo_name": repo["name"],
            "description": repo.get("description", ""),
            "language": repo.get("language", ""),
            "stars": repo.get("stars", 0)
        })

    return {
        "username": username,
        "profile": cleaned_profile,
        "profile_analysis": summary,
        "repositories": repo_list
    }

@app.post("/match-job")
def match_job(request: JobMatchRequest):

    result = match_job_description(
        request.username,
        request.job_description
    )

    return result

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")