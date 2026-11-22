import pytest
import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.services.pdf_parser import PDFParserService
from app.services.nlp_extractor import NLPExtractorService
from app.services.similarity_engine import SimilarityEngineService
from app.services.llm_engine import LLMEngineService
from app.services.report_generator import ReportGeneratorService

def test_pdf_parser_and_nlp_extraction():
    sample_pdf_path = backend_dir / "sample_resumes" / "sample_software_engineer.pdf"
    assert sample_pdf_path.exists(), "Sample PDF must exist"
    
    with open(sample_pdf_path, "rb") as f:
        pdf_bytes = f.read()

    text, meta = PDFParserService.extract_text(pdf_bytes)
    assert len(text) > 200, "Text should be extracted"
    assert meta["page_count"] >= 1
    assert "Alex Morgan" in text

    resume_data = NLPExtractorService.extract_all(text, page_count=meta["page_count"])
    assert resume_data.contact.name == "Alex Morgan"
    assert resume_data.contact.email == "alex.morgan.tech@gmail.com"
    assert "Python" in resume_data.all_skills
    assert "FastAPI" in resume_data.all_skills
    assert "React" in resume_data.all_skills
    assert len(resume_data.all_skills) >= 5

def test_similarity_engine():
    sample_text = """
    Alex Morgan - Software Engineer
    Skills: Python, FastAPI, React, Docker, Kubernetes, PostgreSQL, Sentence-Transformers, OpenAI API.
    Experience: Built high-throughput REST APIs and microservices.
    """
    resume_data = NLPExtractorService.extract_all(sample_text)
    
    job_desc = """
    Looking for a Full Stack Engineer with Python, FastAPI, React, and Docker experience.
    Must understand microservices, relational databases, and cloud deployment.
    """
    
    match = SimilarityEngineService.match_resume_to_job(resume_data, job_desc, "Full Stack Engineer")
    assert 0 <= match.overall_match_score <= 100
    assert 0 <= match.semantic_similarity_score <= 100
    assert len(match.matched_skills) > 0
    assert "FastAPI" in match.matched_skills or "Python" in match.matched_skills
    assert len(match.ats_checks) >= 4

def test_llm_engine_and_report_generation():
    sample_text = "Alex Morgan. Software Engineer. Skills: Python, FastAPI, React, PyTorch."
    resume_data = NLPExtractorService.extract_all(sample_text)
    job_desc = "Software Engineer with Python and FastAPI."
    match = SimilarityEngineService.match_resume_to_job(resume_data, job_desc)
    
    feedback = LLMEngineService.generate_feedback_and_interview_prep(
        resume_data, match, job_desc, "Software Engineer"
    )
    assert len(feedback.key_strengths) > 0
    assert len(feedback.bullet_improvements) > 0
    assert len(feedback.interview_questions) >= 3

    pdf_bytes = ReportGeneratorService.generate_pdf_report(resume_data, match, feedback)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")
