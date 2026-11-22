# ResumeAI — REST API Documentation

Base URL: `http://localhost:8000/api` (or cloud production URL)

Interactive OpenAPI / Swagger UI: `http://localhost:8000/docs`

---

## 1. Endpoints Overview

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/health` | System health, model preload status, OpenAI availability | None |
| `GET` | `/presets` | Preset job descriptions (Full Stack, ML/AI, DevOps) | None |
| `POST` | `/analyze-resume` | Upload PDF or text, extracts structured candidate data | None |
| `POST` | `/match-job` | Computes semantic similarity and keyword scores against JD | None |
| `POST` | `/full-analysis` | **Primary:** End-to-end extraction, matching, ATS audit, & AI interview prep | None |
| `POST` | `/export-report` | Downloads formatted PDF report of evaluation | None |
| `GET` | `/master-guide-pdf` | Downloads comprehensive architecture & interview PDF | None |

---

## 2. Primary Endpoint: `POST /api/full-analysis`

### Request (Multipart Form Data):
- `file`: (Optional) PDF or TXT resume file.
- `resume_text`: (Optional) Raw resume text if file is not provided.
- `job_description`: (Required) String containing job requirements.
- `target_role`: (Optional) String, e.g. "Full Stack Software Engineer".

### Response (`200 OK`):
```json
{
  "resume": {
    "raw_text": "...",
    "word_count": 480,
    "page_count": 1,
    "contact": {
      "name": "Alex Morgan",
      "email": "alex.morgan.tech@gmail.com",
      "phone": "+1 (555) 234-5678",
      "linkedin": "linkedin.com/in/alexmorgan-dev",
      "github": "github.com/alexmorgan-dev"
    },
    "skills_by_category": {
      "programming_languages": ["Python", "TypeScript", "SQL"],
      "frameworks_libraries": ["FastAPI", "React", "Node.js"],
      "cloud_devops_databases": ["Docker", "Kubernetes", "AWS", "PostgreSQL"],
      "ai_ml_data": ["Sentence-Transformers", "OpenAI API", "PyTorch"]
    },
    "all_skills": ["FastAPI", "Python", "React", "Docker", "Sentence-Transformers"],
    "total_experience_years_est": 3.0
  },
  "match": {
    "overall_match_score": 88,
    "semantic_similarity_score": 91,
    "keyword_match_score": 85,
    "ats_compatibility_score": 92,
    "experience_level_match": "Matched (3.0 yrs est. vs ~3+ yrs required)",
    "summary_verdict": "Excellent match! Candidate exhibits high technical alignment...",
    "matched_skills": ["Python", "FastAPI", "React", "Docker"],
    "missing_skills": ["Terraform"],
    "critical_missing_keywords": ["Terraform", "Microservices"],
    "ats_checks": [
      {
        "check_name": "Contact Information",
        "passed": true,
        "status_label": "Pass",
        "impact": "High",
        "details": "Email and Phone detected."
      }
    ]
  },
  "feedback": {
    "ats_score": 92,
    "summary_critique": "Candidate presents strong core competencies...",
    "key_strengths": ["Demonstrated proficiency in core backend/frontend technologies"],
    "key_improvements": ["Incorporate missing target role requirements"],
    "bullet_improvements": [
      {
        "original": "Worked on building APIs and connecting databases.",
        "improved": "Architected asynchronous RESTful endpoints utilizing FastAPI and PostgreSQL, cutting query latency by 35%.",
        "rationale": "Replaces passive verb with 'Architected' and adds quantifiable impact."
      }
    ],
    "action_verbs_recommended": ["Architected", "Engineered", "Benchmarked"],
    "interview_questions": [
      {
        "question": "How did you integrate Sentence-Transformers for semantic resume matching?",
        "type": "Technical",
        "difficulty": "Hard",
        "why_asked": "Tests understanding of dense embeddings vs lexical search.",
        "key_talking_points": ["Vocabulary mismatch problem", "384-dim dense vectors", "Cosine distance in O(d)"],
        "suggested_answer": "..."
      }
    ]
  }
}
```
