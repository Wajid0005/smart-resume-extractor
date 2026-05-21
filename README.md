<div align="center">
  <img src="https://img.icons8.com/nolan/128/github.png" alt="Smart GitHub Resume Extractor Logo">
  <h1>Smart GitHub Resume Extractor 🚀</h1>
  <p><b>An AI-powered GitHub intelligence platform that analyzes developer profiles, repositories, and job compatibility using FastAPI, GitHub API, and Groq LLMs.</b></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Groq-000000?style=for-the-badge&logo=openai&logoColor=white" alt="Groq AI" />
    <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
    <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
    <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
  </p>
</div>

---

## 📌 Project Vision

The goal of this project is to build a recruiter-style AI platform capable of:
- 🔍 **Analyzing** GitHub profiles
- ✍️ **Generating** realistic developer summaries
- 📊 **Evaluating** repository quality
- 🎯 **Matching** developers against job descriptions
- 💡 **Identifying** strengths and missing skills
- 📈 **Helping** users improve their portfolios and resumes

Unlike generic AI portfolio analyzers, this platform focuses on:
- **Realistic evaluation** (No fake senior-level praise)
- **Structured outputs**
- **Recruiter-focused insights**
- **Anti-overhype prompting**

> *Because modern AI tools love calling every calculator app an "enterprise-grade scalable architecture"—which recruiters absolutely hate.*

---

## 🏗️ Current Architecture

```mermaid
graph TD
    A[Frontend HTML/CSS/JS] --> B(FastAPI Backend)
    B --> C{GitHub API Integration}
    C --> D[Repository Data Cleaning]
    D --> E((Groq LLM Analysis))
    E --> F[Structured JSON Response]
    F --> A
```

---

## ⚙️ Tech Stack

| Domain | Technologies |
|---|---|
| **Backend** | Python, FastAPI, Uvicorn |
| **AI Layer** | Groq API, Llama 3.3 70B Versatile |
| **Frontend** | HTML, CSS, Vanilla JavaScript |
| **Integrations** | GitHub REST API |

---

## 📂 Current Project Structure

```text
smart-github-resume-extractor/
│
├── app/
│   ├── main.py
│   ├── services/
│   │     ├── github_service.py
│   │     ├── analyzer_service.py
│   │     └── ai_service.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
├── .env
├── .gitignore
└── requirements.txt
```

---

## ✅ Features Completed

### 1. GitHub Profile Fetching
* Fetches GitHub user profiles and public repositories.
* Extracts core `README.md` data.
* **Core Functions:** `get_github_profile()`, `get_user_repositories()`, `get_readme()`

### 2. Repository Data Cleaning
* Utilizes `extract_repo_data()` to parse the raw GitHub payload.
* Extracts: Repository name, description, language, stars, and forks to use as clean AI context injection.

### 3. AI-Powered Profile Summary
* Utilizes `generate_summary()` to create realistic insights.
* **AI Generates:** Professional summary, Key skills, Company matches, Realistic resume bullet points.
* **Improvements:** Anti-overhype prompt engineering and structured JSON outputs.

### 4. Repository Deep Analysis
* Utilizes `analyze_readme()` to dive deep into project complexity.
* **Analyzes:** Repo metadata, README contents, project complexity, probable skill level.
* **Returns:** Project summary, features, tech stack, difficulty level, and resume bullets.

### 5. Job Description Matching Engine
* Utilizes `match_job_description()` to cross-reference a profile with a job description.
* **Returns:** Realistic match percentage, strengths, missing skills, and top matching repositories.

```json
{
  "match_percentage": 74,
  "strengths": [
    "FastAPI backend development",
    "Python-based ML projects"
  ],
  "missing_skills": [
    "Docker",
    "CI/CD"
  ]
}
```

### 6. Dynamic Frontend Integration
* Beautifully styled dark-theme UI with responsive design.
* Smooth API `fetch` calls dynamically rendering the DOM.
* Handles profile rendering, deep-dive repository panels, and donut-chart job-match analytics.

---

## 🛣️ API Routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | API status route |
| `GET` | `/profile-summary` | Returns AI-generated developer analysis & repository list |
| `GET` | `/analyze-repo` | Returns detailed repository intelligence |
| `POST` | `/match-job` | Returns job compatibility analysis from a Pydantic payload |

---

## 🐞 Major Bugs Fixed
- [x] `.env` loading problems and Groq API key errors
- [x] Invalid JSON parsing & Broken AI responses
- [x] CORS issues and Frontend fetch failures
- [x] Local file system security errors
- [x] JavaScript silent crashes
- [x] Malformed AI output handling

---

## 🧠 Key Engineering Learnings

- **Backend:** FastAPI routing, API response handling, service-based architecture.
- **AI Engineering:** Strict Prompt engineering, structured JSON outputs, realistic AI evaluation, and LLM context injection.
- **Frontend:** Async fetch APIs, dynamic rendering, DOM manipulation, responsive CSS variables.
- **Architecture:** Modular services, clean data pipelines, and API-first application design.

> **Developer Note:** *Frontend bugs can consume more life energy than the actual AI system. A timeless law of software engineering.*

---

## 🚧 Current Status & Progress

```text
🔥 Overall Project Completion: ~65%
```
The main backend intelligence system is largely complete. Current focus is shifting towards refining the frontend experience, advanced analytics, and cloud deployment.

| Section | Status |
|---|---|
| **Backend Core** | ✅ Strong |
| **GitHub Integration** | ✅ Complete |
| **AI Integration** | ✅ Complete |
| **Job Match Engine** | ✅ Complete |
| **Frontend Logic** | ✅ Complete |
| **UI/UX Polish** | 🟡 In Progress |
| **Deployment** | ❌ Pending |
| **Authentication** | ❌ Pending |
| **Database** | ❌ Pending |

---

## 🎯 Planned Features

### Frontend & UI
- Modern SaaS UI with recruiter dashboards.
- Charts, analytics, and dynamic loading animations.

### AI Features
- Repository ranking and skill scoring.
- Contribution graph analysis.
- AI mock interview questions and Resume PDF generation.

### Production
- Docker deployment (Render/Vercel).
- Caching & PostgreSQL database integration.
- User Authentication.

---

<div align="center">
  <p>Built with ☕ and AI | <b>Realism over Hype</b></p>
</div>
