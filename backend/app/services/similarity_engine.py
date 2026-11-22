import re
import math
import numpy as np
from typing import Dict, Any, List, Tuple
from app.models.schemas import (
    ExtractedResumeData,
    JobMatchResponse,
    SkillMatchItem,
    ATSCheckItem
)
from app.services.nlp_extractor import SKILL_TAXONOMY, NLPExtractorService

# Lazy model holder
import threading
_ST_MODEL = None
_MODEL_LOADED = False
_MODEL_LOCK = threading.Lock()

def get_sentence_transformer_model():
    global _ST_MODEL, _MODEL_LOADED
    with _MODEL_LOCK:
        if _ST_MODEL is None and not _MODEL_LOADED:
            try:
                from sentence_transformers import SentenceTransformer
                # Load all-MiniLM-L6-v2
                _ST_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
                _MODEL_LOADED = True
            except Exception as e:
                print(f"[SimilarityEngine] Warning: Could not load SentenceTransformer: {e}. Falling back to TF-IDF cosine similarity.")
                _ST_MODEL = None
                _MODEL_LOADED = True
    return _ST_MODEL

def is_model_loaded() -> bool:
    return _ST_MODEL is not None

class SimilarityEngineService:
    @classmethod
    def match_resume_to_job(cls, resume_data: ExtractedResumeData, job_description: str, target_role: str = "") -> JobMatchResponse:
        resume_text = resume_data.raw_text
        
        # 1. Semantic Similarity via Sentence-Transformers all-MiniLM-L6-v2
        semantic_score = cls.compute_semantic_similarity(resume_text, job_description)
        
        # 2. Extract Job Requirements & Skills
        _, job_skills = NLPExtractorService.extract_skills(job_description)
        
        # In addition, extract keywords from Job Description
        job_keywords = cls.extract_job_keywords(job_description)
        
        # 3. Match Analysis
        resume_skills_lower = {s.lower() for s in resume_data.all_skills}
        resume_text_lower = resume_text.lower()
        
        matched_skills: List[str] = []
        missing_skills: List[str] = []
        breakdown_items: List[SkillMatchItem] = []
        
        for js in job_skills:
            js_clean = js.strip()
            # Check either in extracted skills or in full resume text
            if js_clean.lower() in resume_skills_lower or re.search(r"\b" + re.escape(js_clean.lower()) + r"\b", resume_text_lower):
                matched_skills.append(js_clean)
                breakdown_items.append(SkillMatchItem(
                    name=js_clean,
                    category=cls._guess_category(js_clean),
                    status="matched",
                    importance="must-have"
                ))
            else:
                missing_skills.append(js_clean)
                breakdown_items.append(SkillMatchItem(
                    name=js_clean,
                    category=cls._guess_category(js_clean),
                    status="missing",
                    importance="must-have"
                ))

        # Add candidate's extra matching technical skills
        for rs in resume_data.all_skills:
            if rs not in matched_skills and re.search(r"\b" + re.escape(rs.lower()) + r"\b", job_description.lower()):
                matched_skills.append(rs)
                breakdown_items.append(SkillMatchItem(
                    name=rs,
                    category=cls._guess_category(rs),
                    status="matched",
                    importance="preferred"
                ))

        # Critical missing keywords from JD
        critical_missing = []
        for kw in job_keywords:
            if kw.lower() not in resume_text_lower and kw not in missing_skills:
                critical_missing.append(kw)

        # 4. Keyword Match Score (0 - 100)
        total_required = max(len(job_skills), 1)
        direct_matches = len([s for s in job_skills if s in matched_skills])
        keyword_score = int(round((direct_matches / total_required) * 100))
        keyword_score = min(max(keyword_score, 20 if matched_skills else 5), 100)

        # 5. ATS Compatibility Checklist
        ats_score, ats_checks = cls.run_ats_checklist(resume_data)

        # 6. Overall Weighted Score: 45% Semantic + 35% Skills/Keywords + 20% ATS
        overall_score = int(round(
            (semantic_score * 0.45) + (keyword_score * 0.35) + (ats_score * 0.20)
        ))
        overall_score = min(max(overall_score, 10), 98)

        # Experience level match
        exp_verdict = cls._evaluate_experience_level(resume_data.total_experience_years_est, job_description)

        # Summary verdict
        if overall_score >= 80:
            summary = "Excellent match! Candidate exhibits high technical alignment, semantic overlap with role objectives, and strong ATS hygiene."
        elif overall_score >= 60:
            summary = "Moderate-to-strong match. Core foundations are present, but candidate should incorporate target keywords and measurable achievements."
        else:
            summary = "Low match. Noticeable gaps in required domain tools and terminology. Significant resume keyword tailoring recommended."

        return JobMatchResponse(
            overall_match_score=overall_score,
            semantic_similarity_score=semantic_score,
            keyword_match_score=keyword_score,
            ats_compatibility_score=ats_score,
            experience_level_match=exp_verdict,
            summary_verdict=summary,
            matched_skills=matched_skills[:20],
            missing_skills=missing_skills[:15],
            critical_missing_keywords=critical_missing[:12],
            skills_breakdown=breakdown_items[:30],
            ats_checks=ats_checks
        )

    @classmethod
    def compute_semantic_similarity(cls, text_a: str, text_b: str) -> int:
        """
        Computes cosine similarity between embeddings of text_a and text_b
        using all-MiniLM-L6-v2. Falls back to scikit-learn TF-IDF if needed.
        """
        model = get_sentence_transformer_model()
        if model is not None:
            try:
                # Truncate to reasonable context window (~1000 tokens)
                chunk_a = text_a[:3500]
                chunk_b = text_b[:3500]
                embeddings = model.encode([chunk_a, chunk_b], normalize_embeddings=True)
                # Dot product of normalized vectors equals cosine similarity
                cos_sim = float(np.dot(embeddings[0], embeddings[1]))
                # Scale from [-1, 1] / typically [0.2, 0.9] to a readable percentage [0, 100]
                # A cosine similarity of 0.35 is moderate, 0.7+ is very high in MiniLM
                normalized = (cos_sim + 0.1) / 1.0  # calibration
                score = int(round(min(max(normalized * 100, 15), 98)))
                return score
            except Exception as e:
                print(f"[SimilarityEngine] SentenceTransformer encode error: {e}")

        # Fallback: TF-IDF Cosine Similarity
        return cls._tfidf_similarity(text_a, text_b)

    @classmethod
    def _tfidf_similarity(cls, text_a: str, text_b: str) -> int:
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=500)
            tfidf_mat = vec.fit_transform([text_a, text_b])
            sim = float(cosine_similarity(tfidf_mat[0:1], tfidf_mat[1:2])[0][0])
            score = int(round(min(max((sim * 1.3) * 100, 20), 96)))
            return score
        except Exception:
            # Simple Jaccard word set fallback
            words_a = set(re.findall(r"\b\w{3,}\b", text_a.lower()))
            words_b = set(re.findall(r"\b\w{3,}\b", text_b.lower()))
            if not words_b:
                return 50
            jaccard = len(words_a & words_b) / len(words_a | words_b)
            return int(round(min(max(jaccard * 200, 25), 95)))

    @classmethod
    def extract_job_keywords(cls, job_description: str) -> List[str]:
        common_words = {
            "experience", "years", "candidate", "responsibilities", "requirements", "team",
            "working", "ability", "skills", "knowledge", "strong", "preferred", "degree",
            "including", "must", "have", "role", "work", "join", "help", "build", "company",
            "opportunity", "environment", "position", "looking", "qualifications"
        }
        tokens = re.findall(r"\b[A-Za-z][A-Za-z0-9+#.-]{2,}\b", job_description)
        freq: Dict[str, int] = {}
        for t in tokens:
            tl = t.lower()
            if tl not in common_words and len(tl) > 3:
                freq[t] = freq.get(t, 0) + 1
        
        sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [k for k, v in sorted_tokens[:15]]

    @classmethod
    def run_ats_checklist(cls, resume_data: ExtractedResumeData) -> Tuple[int, List[ATSCheckItem]]:
        checks: List[ATSCheckItem] = []
        score = 100

        # Check 1: Contact Information Complete
        has_email = bool(resume_data.contact.email)
        has_phone = bool(resume_data.contact.phone)
        has_links = bool(resume_data.contact.linkedin or resume_data.contact.github)
        
        if has_email and has_phone:
            checks.append(ATSCheckItem(
                check_name="Contact Information",
                passed=True,
                status_label="Pass",
                impact="High",
                details=f"Email ({resume_data.contact.email or 'Found'}) and Phone detected."
            ))
        else:
            score -= 15
            checks.append(ATSCheckItem(
                check_name="Contact Information",
                passed=False,
                status_label="Needs Attention",
                impact="High",
                details="Missing either direct email or telephone number. Recruiter ATS systems require both."
            ))

        # Check 2: Word Count & Length
        wc = resume_data.word_count
        if 350 <= wc <= 1200:
            checks.append(ATSCheckItem(
                check_name="Resume Length & Word Count",
                passed=True,
                status_label="Pass",
                impact="Medium",
                details=f"Optimal length ({wc} words, ~{resume_data.page_count} page(s))."
            ))
        elif wc < 350:
            score -= 10
            checks.append(ATSCheckItem(
                check_name="Resume Length & Word Count",
                passed=False,
                status_label="Warning",
                impact="Medium",
                details=f"Resume is brief ({wc} words). Consider elaborating on project impacts and methodologies."
            ))
        else:
            score -= 5
            checks.append(ATSCheckItem(
                check_name="Resume Length & Word Count",
                passed=True,
                status_label="Warning",
                impact="Low",
                details=f"Resume is lengthy ({wc} words). Aim for concise bullet points under 2 pages."
            ))

        # Check 3: Structured Skills Section
        skills_count = len(resume_data.all_skills)
        if skills_count >= 8:
            checks.append(ATSCheckItem(
                check_name="Skills Extraction & Density",
                passed=True,
                status_label="Pass",
                impact="High",
                details=f"Extracted {skills_count} recognized industry skills across programming, tools, and platforms."
            ))
        else:
            score -= 15
            checks.append(ATSCheckItem(
                check_name="Skills Extraction & Density",
                passed=False,
                status_label="Needs Attention",
                impact="High",
                details=f"Only {skills_count} technical skills detected. Explicitly list standard tools and libraries in a dedicated Skills section."
            ))

        # Check 4: Measurable Impact & Metrics
        metric_matches = re.findall(r"\b(?:\d+%(?:[\s-]*\w+)?|\$\d+[\d,.]*(?:[kKmMbB])?|\b\d+x\b|\b\d+(?:\.\d+)?\s*(?:ms|seconds|minutes|hours|users|req/s|rps))\b", resume_data.raw_text)
        if len(metric_matches) >= 3:
            checks.append(ATSCheckItem(
                check_name="Quantified Achievements & Metrics",
                passed=True,
                status_label="Pass",
                impact="High",
                details=f"Great job! Found {len(metric_matches)} quantified achievement indicators (e.g., '{metric_matches[0]}')."
            ))
        else:
            score -= 12
            checks.append(ATSCheckItem(
                check_name="Quantified Achievements & Metrics",
                passed=False,
                status_label="Needs Attention",
                impact="High",
                details="Few quantified metrics found. Use numbers, %, latency reductions, or scale (e.g. 'Reduced latency by 35%')."
            ))

        # Check 5: Action Verbs Usage
        action_verbs = ["built", "architected", "engineered", "designed", "deployed", "implemented", "optimized", "spearheaded", "accelerated", "scaled", "automated"]
        found_verbs = [v for v in action_verbs if re.search(r"\b" + v + r"\b", resume_data.raw_text.lower())]
        if len(found_verbs) >= 4:
            checks.append(ATSCheckItem(
                check_name="Strong Action Verbs",
                passed=True,
                status_label="Pass",
                impact="Medium",
                details=f"Detected high-impact verbs: {', '.join(found_verbs[:4])}."
            ))
        else:
            score -= 8
            checks.append(ATSCheckItem(
                check_name="Strong Action Verbs",
                passed=False,
                status_label="Warning",
                impact="Medium",
                details="Incorporate strong active verbs (Engineered, Architected, Automated, Deployed) at the start of bullet points."
            ))

        # Check 6: Education & Degree Section
        if resume_data.education:
            checks.append(ATSCheckItem(
                check_name="Education Section Clarity",
                passed=True,
                status_label="Pass",
                impact="Medium",
                details=f"Found: {resume_data.education[0].degree or 'Degree'} from {resume_data.education[0].institution or 'University'}."
            ))
        else:
            score -= 8
            checks.append(ATSCheckItem(
                check_name="Education Section Clarity",
                passed=False,
                status_label="Warning",
                impact="Medium",
                details="Education degree or institution not clearly recognized by parser."
            ))

        ats_score = max(min(score, 100), 25)
        return ats_score, checks

    @staticmethod
    def _evaluate_experience_level(years: float, jd_text: str) -> str:
        jd_l = jd_text.lower()
        if "senior" in jd_l or "lead" in jd_l or "principal" in jd_l:
            req_years = 5
        elif "mid" in jd_l or "3+" in jd_l:
            req_years = 3
        else:
            req_years = 1

        if years >= req_years:
            return f"Matched ({years:.1f} yrs est. vs ~{req_years}+ yrs required)"
        else:
            return f"Slight Gap ({years:.1f} yrs est. vs ~{req_years}+ yrs target)"

    @staticmethod
    def _guess_category(skill_name: str) -> str:
        s = skill_name.lower()
        for cat, list_s in SKILL_TAXONOMY.items():
            if s in list_s:
                if cat == "programming_languages":
                    return "Language"
                elif cat == "frameworks_libraries":
                    return "Framework/Lib"
                elif cat == "cloud_devops_databases":
                    return "Cloud/DB/DevOps"
                elif cat == "ai_ml_data":
                    return "AI/ML/Data"
                elif cat == "tools_platforms":
                    return "Tool/Platform"
                else:
                    return "Concept"
        return "Technical Skill"
