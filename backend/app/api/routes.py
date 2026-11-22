import os
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Response
from fastapi.responses import JSONResponse
from app.config import settings
from app.models.schemas import (
    ExtractedResumeData,
    JobMatchRequest,
    JobMatchResponse,
    FeedbackResponse,
    FullAnalysisResponse,
    HealthResponse
)
from app.services.pdf_parser import PDFParserService
from app.services.nlp_extractor import NLPExtractorService
from app.services.similarity_engine import SimilarityEngineService, get_sentence_transformer_model
from app.services.llm_engine import LLMEngineService
from app.services.report_generator import ReportGeneratorService

router = APIRouter()

SAMPLE_PRESETS = [
    {
        "role": "Full Stack Engineer (React & FastAPI)",
        "company": "NextGen Cloud Labs",
        "description": """We are looking for a Senior Full Stack Software Engineer to build scalable microservices and responsive user interfaces. 
Requirements:
- 3+ years experience with Python, FastAPI or Django, and asynchronous backend architectures.
- Strong proficiency in modern React, JavaScript/TypeScript, Tailwind CSS, and RESTful APIs.
- Experience with Docker, Kubernetes, CI/CD pipelines (GitHub Actions), and AWS/GCP cloud platforms.
- Solid understanding of SQL (PostgreSQL), Redis caching, and database schema design.
- Familiarity with AI/ML integration, vector embeddings, or OpenAI API is a strong plus.
- Excellent problem-solving skills, system design experience, and ability to lead code reviews."""
    },
    {
        "role": "Machine Learning / AI Engineer",
        "company": "DeepCognition AI",
        "description": """Seeking a Machine Learning Engineer to design, fine-tune, and deploy transformer-based NLP models and LLM agent pipelines.
Requirements:
- Strong background in Python, PyTorch, Hugging Face Transformers, and Sentence-Transformers.
- Hands-on experience with Retrieval-Augmented Generation (RAG), vector databases (ChromaDB, Pinecone, Qdrant), and LLM orchestration (OpenAI API, LangChain).
- Proven ability deploying models to production using FastAPI, Docker, and ONNX Runtime.
- Solid mathematical foundation in linear algebra, cosine similarity, loss functions, and NLP evaluation metrics.
- Experience with large-scale data preprocessing, Pandas, NumPy, and Scikit-Learn."""
    },
    {
        "role": "DevOps & Cloud Infrastructure Engineer",
        "company": "HyperScale Systems",
        "description": """Join our Platform Engineering team managing cloud-native infrastructure and deployment automation.
Requirements:
- 3+ years of production experience with AWS (ECS, EKS, Lambda, S3, IAM) or GCP.
- Deep expertise with Docker containerization, Kubernetes orchestration, and Terraform Infrastructure as Code.
- Proficient in Linux systems administration, Bash scripting, and Python automation.
- Experience building resilient CI/CD pipelines with GitHub Actions or GitLab CI.
- Working knowledge of monitoring and observability stacks (Prometheus, Grafana, OpenTelemetry)."""
    }
]

@router.get("/health", response_model=HealthResponse)
async def health_check():
    model = get_sentence_transformer_model()
    has_openai = bool(settings.OPENAI_API_KEY and len(settings.OPENAI_API_KEY.strip()) > 10)
    return HealthResponse(
        status="healthy",
        model_loaded=(model is not None),
        openai_available=has_openai,
        version=settings.PROJECT_VERSION
    )

@router.get("/presets")
async def get_presets():
    return {"presets": SAMPLE_PRESETS}

@router.post("/analyze-resume", response_model=ExtractedResumeData)
async def analyze_resume(
    file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None)
):
    """
    Parses an uploaded PDF file or raw resume text into structured candidate profile.
    """
    if file:
        if not file.filename.lower().endswith(".pdf") and not file.filename.lower().endswith(".txt"):
            raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported.")
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"File exceeds max size of {settings.MAX_UPLOAD_SIZE_MB}MB.")
        
        if file.filename.lower().endswith(".pdf"):
            text, meta = PDFParserService.extract_text(content)
            page_count = meta.get("page_count", 1)
        else:
            text = content.decode("utf-8", errors="ignore")
            page_count = 1
    elif resume_text and resume_text.strip():
        text = resume_text.strip()
        page_count = 1
    else:
        raise HTTPException(status_code=400, detail="Either a resume file or resume text must be provided.")

    if not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract readable text from the provided resume.")

    extracted = NLPExtractorService.extract_all(text, page_count=page_count)
    return extracted

@router.post("/match-job", response_model=JobMatchResponse)
async def match_job(
    job_description: str = Form(...),
    target_role: Optional[str] = Form("Software Engineer"),
    file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None)
):
    """
    Benchmarks a resume against a job description using Sentence-Transformers and cosine similarity.
    """
    if file:
        content = await file.read()
        text, meta = PDFParserService.extract_text(content)
        resume_data = NLPExtractorService.extract_all(text, page_count=meta.get("page_count", 1))
    elif resume_text and resume_text.strip():
        resume_data = NLPExtractorService.extract_all(resume_text.strip())
    else:
        raise HTTPException(status_code=400, detail="Resume file or text required.")

    match_result = SimilarityEngineService.match_resume_to_job(resume_data, job_description, target_role)
    return match_result

@router.post("/full-analysis", response_model=FullAnalysisResponse)
async def full_analysis(
    job_description: str = Form(...),
    target_role: Optional[str] = Form("Software Engineer"),
    file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None)
):
    """
    Comprehensive single-call analysis:
    Extracts structured entities, computes semantic & lexical match scores, runs ATS audit,
    and generates AI-powered bullet rewrites and interview questions.
    """
    if file:
        content = await file.read()
        text, meta = PDFParserService.extract_text(content)
        resume_data = NLPExtractorService.extract_all(text, page_count=meta.get("page_count", 1))
    elif resume_text and resume_text.strip():
        resume_data = NLPExtractorService.extract_all(resume_text.strip())
    else:
        raise HTTPException(status_code=400, detail="Please upload a PDF resume or paste resume text.")

    match_result = SimilarityEngineService.match_resume_to_job(resume_data, job_description, target_role)
    feedback_result = LLMEngineService.generate_feedback_and_interview_prep(
        resume_data, match_result, job_description, target_role
    )

    return FullAnalysisResponse(
        resume=resume_data,
        match=match_result,
        feedback=feedback_result
    )

@router.post("/export-report")
async def export_report(payload: FullAnalysisResponse, target_role: str = "Software Engineer"):
    """
    Generates and downloads a publication-grade PDF report of the evaluation.
    """
    try:
        pdf_bytes = ReportGeneratorService.generate_pdf_report(
            payload.resume,
            payload.match,
            payload.feedback,
            target_role=target_role
        )
        candidate_slug = (payload.resume.contact.name or "Candidate").replace(" ", "_")
        filename = f"ResumeAI_Report_{candidate_slug}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report PDF: {str(e)}")

@router.get("/master-guide-pdf")
async def get_master_guide_pdf():
    """
    Downloads the comprehensive Master Architecture & Interview Preparation PDF.
    """
    from pathlib import Path
    from fastapi.responses import FileResponse
    doc_path = Path(__file__).resolve().parent.parent.parent.parent / "docs" / "ResumeAI_Complete_Architecture_and_Interview_Mastery.pdf"
    if not doc_path.exists():
        # Generate on the fly if needed
        from scripts.generate_interview_pdf import build_pdf
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        build_pdf(str(doc_path))
    
    return FileResponse(
        str(doc_path),
        media_type="application/pdf",
        filename="ResumeAI_Complete_Architecture_and_Interview_Mastery.pdf"
    )

