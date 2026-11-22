from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
    name: Optional[str] = Field(None, description="Candidate's full name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    portfolio: Optional[str] = Field(None, description="Portfolio website URL")
    location: Optional[str] = Field(None, description="Location or City/Country")

class WorkExperienceItem(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    duration: Optional[str] = None
    highlights: List[str] = Field(default_factory=list)

class EducationItem(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None
    gpa_or_details: Optional[str] = None

class ProjectItem(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)

class CategorizedSkills(BaseModel):
    programming_languages: List[str] = Field(default_factory=list)
    frameworks_libraries: List[str] = Field(default_factory=list)
    cloud_devops_databases: List[str] = Field(default_factory=list)
    ai_ml_data: List[str] = Field(default_factory=list)
    tools_platforms: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)

class ExtractedResumeData(BaseModel):
    raw_text: str
    word_count: int
    page_count: int
    contact: ContactInfo
    skills_by_category: CategorizedSkills
    all_skills: List[str] = Field(default_factory=list)
    experience: List[WorkExperienceItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    total_experience_years_est: float = 0.0

class SkillMatchItem(BaseModel):
    name: str
    category: str
    status: str  # "matched" or "missing"
    importance: str  # "must-have" or "preferred"

class ATSCheckItem(BaseModel):
    check_name: str
    passed: bool
    status_label: str  # "Pass", "Warning", "Needs Attention"
    impact: str  # "High", "Medium", "Low"
    details: str

class BulletImprovement(BaseModel):
    original: str
    improved: str
    rationale: str

class InterviewQuestion(BaseModel):
    question: str
    type: str  # "Technical", "System Design", "Behavioral"
    difficulty: str  # "Medium", "Hard", "Fundamental"
    why_asked: str
    key_talking_points: List[str]
    suggested_answer: str

class JobMatchRequest(BaseModel):
    resume_text: Optional[str] = None
    job_description: str
    target_role: Optional[str] = "Software Engineer"

class JobMatchResponse(BaseModel):
    overall_match_score: int
    semantic_similarity_score: int
    keyword_match_score: int
    ats_compatibility_score: int
    experience_level_match: str
    summary_verdict: str
    matched_skills: List[str]
    missing_skills: List[str]
    critical_missing_keywords: List[str]
    skills_breakdown: List[SkillMatchItem]
    ats_checks: List[ATSCheckItem]

class FeedbackResponse(BaseModel):
    ats_score: int
    summary_critique: str
    key_strengths: List[str]
    key_improvements: List[str]
    bullet_improvements: List[BulletImprovement]
    action_verbs_recommended: List[str]
    interview_questions: List[InterviewQuestion]

class FullAnalysisResponse(BaseModel):
    resume: ExtractedResumeData
    match: JobMatchResponse
    feedback: FeedbackResponse

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    openai_available: bool
    version: str
