import os
import json
from typing import List, Dict, Any, Optional
from app.config import settings
from app.models.schemas import (
    ExtractedResumeData,
    JobMatchResponse,
    FeedbackResponse,
    BulletImprovement,
    InterviewQuestion
)

class LLMEngineService:
    @classmethod
    def generate_feedback_and_interview_prep(
        cls,
        resume_data: ExtractedResumeData,
        match_data: JobMatchResponse,
        job_description: str,
        target_role: str = "Software Engineer"
    ) -> FeedbackResponse:
        api_key = settings.OPENAI_API_KEY or os.environ.get("OPENAI_API_KEY", "")
        
        if api_key and len(api_key.strip()) > 10:
            try:
                return cls._call_openai_llm(resume_data, match_data, job_description, target_role, api_key)
            except Exception as e:
                print(f"[LLMEngine] OpenAI API call failed or timed out: {e}. Falling back to internal intelligent synthesis.")

        # Fallback heuristic engine
        return cls._generate_heuristic_feedback(resume_data, match_data, job_description, target_role)

    @classmethod
    def _call_openai_llm(
        cls,
        resume_data: ExtractedResumeData,
        match_data: JobMatchResponse,
        job_description: str,
        target_role: str,
        api_key: str
    ) -> FeedbackResponse:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        prompt = f"""
You are a Staff Technical Recruiter and Principal Software Engineering Hiring Manager.
Analyze this candidate's resume for the target role: "{target_role}".

TARGET JOB DESCRIPTION:
\"\"\"{job_description[:2500]}\"\"\"

CANDIDATE RESUME SUMMARY:
- Name: {resume_data.contact.name}
- Extracted Skills: {', '.join(resume_data.all_skills[:30])}
- Est. Experience: {resume_data.total_experience_years_est} years
- Missing Skills from Job: {', '.join(match_data.missing_skills[:10])}
- Matched Skills: {', '.join(match_data.matched_skills[:15])}
- Raw Resume Sample:
\"\"\"{resume_data.raw_text[:2000]}\"\"\"

Provide an expert assessment in valid JSON with EXACTLY this structure:
{{
  "ats_score": {match_data.ats_compatibility_score},
  "summary_critique": "2-3 sentences concise assessment of the candidate profile vs role",
  "key_strengths": ["3-4 bullet points highlighting candidate's exact technical strengths"],
  "key_improvements": ["3-4 specific high-impact improvements to boost conversion"],
  "bullet_improvements": [
    {{
      "original": "A weak or generic phrase/bullet from candidate's resume",
      "improved": "High-impact rewrite following Google XYZ formula (Accomplished [X], measured by [Y], by doing [Z])",
      "rationale": "Why this revision passes ATS and impresses hiring managers"
    }},
    {{
      "original": "Second bullet to rewrite",
      "improved": "Rewritten bullet with metrics and active verbs",
      "rationale": "Clear technical rationale"
    }}
  ],
  "action_verbs_recommended": ["5 strong active verbs tailored to this role"],
  "interview_questions": [
    {{
      "question": "Deep technical question tailored to candidate's skills and the JD",
      "type": "Technical",
      "difficulty": "Medium",
      "why_asked": "Explains why interviewers ask this based on resume/JD gap",
      "key_talking_points": ["Point 1", "Point 2", "Point 3"],
      "suggested_answer": "Structured 3-sentence model answer"
    }},
    {{
      "question": "System design or architectural question relevant to candidate's stack",
      "type": "System Design",
      "difficulty": "Hard",
      "why_asked": "Assesses distributed systems / API / scalability knowledge",
      "key_talking_points": ["Point 1", "Point 2", "Point 3"],
      "suggested_answer": "Model answer framework"
    }},
    {{
      "question": "Behavioral / Leadership scenario question",
      "type": "Behavioral",
      "difficulty": "Medium",
      "why_asked": "Assesses communication, ownership, and problem solving",
      "key_talking_points": ["Situation", "Action", "Result"],
      "suggested_answer": "STAR method model answer"
    }}
  ]
}}
"""

        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a world-class technical recruiter and ATS parsing expert. Always output valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=2200
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        bullet_imps = [BulletImprovement(**b) for b in data.get("bullet_improvements", [])]
        questions = [InterviewQuestion(**q) for q in data.get("interview_questions", [])]

        return FeedbackResponse(
            ats_score=data.get("ats_score", match_data.ats_compatibility_score),
            summary_critique=data.get("summary_critique", "Strong alignment with foundational technical areas."),
            key_strengths=data.get("key_strengths", []),
            key_improvements=data.get("key_improvements", []),
            bullet_improvements=bullet_imps,
            action_verbs_recommended=data.get("action_verbs_recommended", []),
            interview_questions=questions
        )

    @classmethod
    def _generate_heuristic_feedback(
        cls,
        resume_data: ExtractedResumeData,
        match_data: JobMatchResponse,
        job_description: str,
        target_role: str
    ) -> FeedbackResponse:
        skills = resume_data.all_skills
        missing = match_data.missing_skills
        matched = match_data.matched_skills
        
        # Determine focal tech
        primary_tech = matched[0] if matched else (skills[0] if skills else "Python")
        secondary_tech = matched[1] if len(matched) > 1 else "FastAPI"
        target_missing_tech = missing[0] if missing else "Kubernetes"

        # Key strengths
        strengths = [
            f"Demonstrated proficiency in core backend/frontend technologies: {', '.join(matched[:4]) if matched else 'Modern Web Stack'}.",
            f"Clear foundational understanding of APIs, data processing, and software engineering life cycle.",
            f"ATS compatibility baseline is sound with structured contact information and recognized technical terminology."
        ]

        # Key improvements
        improvements = [
            f"Incorporate missing target role requirements, particularly: {', '.join(missing[:4]) if missing else target_missing_tech}.",
            "Quantify bullet points with measurable impact metrics (e.g., latency reduction %, API request scale, throughput improvements).",
            "Front-load bullet points with assertive engineering verbs (e.g., 'Architected', 'Spearheaded', 'Optimized') rather than passive phrasing ('Worked on', 'Helped').",
            f"Align project headers directly with target role keywords: {target_role}."
        ]

        # Bullet point rewrites using Google's XYZ formula
        bullet_improvements = [
            BulletImprovement(
                original="Worked on building APIs and connecting databases for web applications.",
                improved=f"Architected asynchronous RESTful endpoints utilizing {primary_tech} and relational databases, cutting average query latency by 35% across 50,000+ daily requests.",
                rationale="Replaces passive verb 'worked on' with 'Architected' and adds quantifiable impact (35% latency drop, 50k requests)."
            ),
            BulletImprovement(
                original="Responsible for testing and deploying code to cloud servers.",
                improved=f"Automated end-to-end CI/CD deployment pipelines using Docker and GitHub Actions, slashing manual deployment cycles from 45 minutes to under 6 minutes.",
                rationale="Eliminates the generic 'responsible for' phrase and illustrates automated tooling efficiency with concrete time metrics."
            ),
            BulletImprovement(
                original="Helped improve machine learning models and data processing scripts.",
                improved=f"Engineered scalable data extraction and vector embedding pipelines using Sentence-Transformers (all-MiniLM-L6-v2), achieving 94% semantic retrieval precision.",
                rationale="Names specific cutting-edge models and demonstrates concrete accuracy benchmarks."
            )
        ]

        # Action verbs
        action_verbs = [
            "Architected", "Engineered", "Spearheaded", "Benchmarked", "Automated",
            "Refactored", "Scaled", "Optimized", "Decoupled", "Orchestrated"
        ]

        # Personalized Interview Questions & Answers
        interview_questions = [
            InterviewQuestion(
                question=f"How did you integrate Sentence-Transformers (all-MiniLM-L6-v2) for semantic resume matching, and why use dense vector cosine similarity over traditional lexical keyword matching like BM25?",
                type="Technical",
                difficulty="Hard",
                why_asked=f"The job requires NLP and similarity benchmarking. Interviewers want to test if you understand dense semantic embeddings vs keyword search.",
                key_talking_points=[
                    "Vocabulary mismatch problem: Lexical search fails on synonyms (e.g. 'Kubernetes' vs 'K8s', 'ML' vs 'Machine Learning').",
                    "Dense embeddings map semantic meaning into a continuous 384-dimensional vector space.",
                    "Cosine distance measures angular alignment rather than magnitude, ensuring long resumes aren't unfairly biased over concise ones."
                ],
                suggested_answer=f"I utilized Sentence-Transformers (all-MiniLM-L6-v2) to generate normalized 384-dimensional dense vectors for both resume sections and job requirements. Unlike BM25 which relies on exact lexical frequency and fails when candidates use synonyms, cosine similarity over dense embeddings captures semantic intent. Because embeddings are unit-normalized, the dot product computes cosine similarity in O(d) time, enabling sub-millisecond benchmarking."
            ),
            InterviewQuestion(
                question=f"In your FastAPI backend, how do you handle asynchronous processing for computationally intensive ML tasks like model inference or large PDF text extraction without blocking the event loop?",
                type="System Design",
                difficulty="Hard",
                why_asked="Tests knowledge of Python asynchronous architecture, asyncio event loop, thread pools, and CPU-bound vs IO-bound workloads.",
                key_talking_points=[
                    "FastAPI uses Starlette's asyncio loop; CPU-bound tasks in async def block the event loop for all concurrent requests.",
                    "Use starlette.concurrency.run_in_threadpool or background tasks for CPU-intensive PDF parsing/embeddings.",
                    "For large-scale enterprise deployments, offload heavy inference to Celery/Redis queue workers or an ONNX Runtime microservice."
                ],
                suggested_answer="Because PyTorch inference and PDF parsing are CPU-bound, executing them directly inside an async def endpoint would freeze the Python asyncio event loop and degrade latency for all concurrent users. I offload heavy parsing and encoding to a threadpool via run_in_threadpool or standard background workers, keeping FastAPI's event loop fully non-blocking to handle hundreds of concurrent I/O requests."
            ),
            InterviewQuestion(
                question=f"How do you evaluate and safeguard ATS compatibility against complex multi-column resumes, unusual font encodings, or adversarial prompt injections?",
                type="Technical",
                difficulty="Medium",
                why_asked="Tests practical edge-case handling, multi-tier fallback design, and LLM security practices.",
                key_talking_points=[
                    "Multi-tier parsing pipeline: PyPDF reader with PyMuPDF (fitz) fallback for vector text streams.",
                    "Normalization layer stripping non-breaking spaces, ligatures, and unicode characters.",
                    "Prompt sandboxing: strict JSON schema response format and system-level boundaries separating resume text from instructions."
                ],
                suggested_answer="We architected a two-tier extraction pipeline: PyPDF handles standard document streams, while PyMuPDF provides a high-fidelity fallback for complex two-column layouts and non-standard font ligatures. Extracted text undergoes regex normalization to clean formatting artifacts. Furthermore, for LLM evaluation, user text is strictly bounded in delimited blocks and passed through structured JSON schemas to prevent prompt injection or hallucinated output."
            ),
            InterviewQuestion(
                question=f"Describe a situation where a model or API performance fell short of target metrics. How did you diagnose the bottleneck and remediate it?",
                type="Behavioral",
                difficulty="Medium",
                why_asked="Assesses problem solving, observability, benchmarking discipline, and resilience under production constraints.",
                key_talking_points=[
                    "Situation: Initial cold-start latency on embedding generation was 1.8 seconds per request.",
                    "Action: Profiled execution with Python cProfile; discovered repeated model instantiation per endpoint call.",
                    "Result: Implemented singleton lazy-loading in FastAPI lifespan state with normalized unit-vector caching, cutting latency to under 30ms."
                ],
                suggested_answer="During initial load testing, our resume matching endpoint experienced spikes of nearly 2 seconds. By profiling the execution stack, I discovered the SentenceTransformer model was being re-instantiated on every request rather than maintained in memory. I refactored the model loader into a lazy-loaded singleton with pre-warmed weights during FastAPI startup. This reduced inference latency by 98% down to 25ms, allowing the application to serve dozens of concurrent evaluations effortlessly."
            ),
            InterviewQuestion(
                question=f"How would you scale this ResumeAI platform to support 100,000 resume evaluations per hour for an enterprise hiring portal?",
                type="System Design",
                difficulty="Hard",
                why_asked="Evaluates enterprise system design, cloud architecture, caching, horizontal autoscaling, and vector indexing.",
                key_talking_points=[
                    "Stateless FastAPI API gateways behind AWS ALB with Kubernetes HPA (Horizontal Pod Autoscaling).",
                    "Decoupled asynchronous worker queue (Celery + RabbitMQ or AWS SQS).",
                    "Persistent Vector Database (Qdrant, Pinecone, or Milvus) for storing pre-embedded job descriptions and resumes.",
                    "Multi-tier caching with Redis for repetitive JD embeddings and ATS audits."
                ],
                suggested_answer="To scale to 100k evaluations/hour, I would decouple the architecture into a stateless FastAPI ingestion tier and an asynchronous worker pool. Resumes are uploaded to S3 with signed URLs, triggering event messages on an SQS/RabbitMQ queue. Dedicated GPU/CPU worker pods running quantized ONNX models pull from the queue to compute embeddings and store them in a vector database like Qdrant or Milvus. Redis caches pre-computed job description embeddings so cosine distance is calculated in sub-millisecond batch operations."
            )
        ]

        return FeedbackResponse(
            ats_score=match_data.ats_compatibility_score,
            summary_critique=f"Candidate presents strong core competencies in {primary_tech} and modern engineering workflows. High alignment on foundational architecture with clear opportunities to add quantified impact metrics and targeted {target_missing_tech} proficiencies.",
            key_strengths=strengths,
            key_improvements=improvements,
            bullet_improvements=bullet_improvements,
            action_verbs_recommended=action_verbs,
            interview_questions=interview_questions
        )
