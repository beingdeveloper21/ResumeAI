import io
from typing import Dict, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from app.models.schemas import (
    ExtractedResumeData,
    JobMatchResponse,
    FeedbackResponse
)

class ReportGeneratorService:
    @classmethod
    def generate_pdf_report(
        cls,
        resume: ExtractedResumeData,
        match: JobMatchResponse,
        feedback: FeedbackResponse,
        target_role: str = "Software Engineer"
    ) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        
        styles = getSampleStyleSheet()
        
        # Custom palette
        PRIMARY = colors.HexColor("#1e3a8a")     # Deep Indigo
        SECONDARY = colors.HexColor("#2563eb")   # Royal Blue
        TEXT_DARK = colors.HexColor("#0f172a")   # Slate 900
        TEXT_MUTED = colors.HexColor("#475569")  # Slate 600
        BG_LIGHT = colors.HexColor("#f8fafc")    # Slate 50
        GREEN = colors.HexColor("#16a34a")       # Emerald
        AMBER = colors.HexColor("#d97706")       # Amber
        BORDER = colors.HexColor("#cbd5e1")      # Slate 300

        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=PRIMARY,
            alignment=0
        )
        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=TEXT_MUTED
        )
        section_style = ParagraphStyle(
            "SectionHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=PRIMARY,
            spaceBefore=14,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            "BodyDark",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=TEXT_DARK
        )
        bold_body = ParagraphStyle(
            "BoldBody",
            parent=body_style,
            fontName="Helvetica-Bold"
        )
        bullet_style = ParagraphStyle(
            "ReportBullet",
            parent=body_style,
            leftIndent=15,
            firstLineIndent=-10
        )

        elements = []

        # Header Title
        elements.append(Paragraph("ResumeAI Evaluation & Match Report", title_style))
        elements.append(Paragraph(
            f"<b>Candidate:</b> {resume.contact.name or 'Applicant'} &nbsp;|&nbsp; <b>Target Role:</b> {target_role} &nbsp;|&nbsp; <b>Evaluation Date:</b> Active Session",
            subtitle_style
        ))
        elements.append(Spacer(1, 8))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=4, spaceAfter=12))

        # Executive Scores Table
        score_data = [
            [
                Paragraph("<b>Overall Match</b>", bold_body),
                Paragraph("<b>Semantic Similarity</b>", bold_body),
                Paragraph("<b>Keyword Match</b>", bold_body),
                Paragraph("<b>ATS Compatibility</b>", bold_body),
            ],
            [
                Paragraph(f"<font size=16 color='#1e3a8a'><b>{match.overall_match_score}%</b></font>", bold_body),
                Paragraph(f"<font size=16 color='#2563eb'><b>{match.semantic_similarity_score}%</b></font>", bold_body),
                Paragraph(f"<font size=16 color='#0d9488'><b>{match.keyword_match_score}%</b></font>", bold_body),
                Paragraph(f"<font size=16 color='#ea580c'><b>{match.ats_compatibility_score}/100</b></font>", bold_body),
            ]
        ]
        score_table = Table(score_data, colWidths=[130, 130, 130, 130])
        score_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
            ("BOX", (0, 0), (-1, -1), 1, BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(score_table)
        elements.append(Spacer(1, 10))

        # Executive Summary Verdict
        elements.append(Paragraph("<b>Executive Summary Verdict:</b>", bold_body))
        elements.append(Paragraph(match.summary_verdict, body_style))
        elements.append(Spacer(1, 10))

        # Skills Alignment
        elements.append(Paragraph("1. Technical Skills Matrix", section_style))
        skills_matched_str = ", ".join(match.matched_skills) if match.matched_skills else "None explicitly detected"
        skills_missing_str = ", ".join(match.missing_skills) if match.missing_skills else "No major skill gaps detected"

        skills_data = [
            [Paragraph("<b>Matched Skills</b>", bold_body), Paragraph(f"<font color='#16a34a'>{skills_matched_str}</font>", body_style)],
            [Paragraph("<b>Missing / Gap Skills</b>", bold_body), Paragraph(f"<font color='#dc2626'>{skills_missing_str}</font>", body_style)],
            [Paragraph("<b>Critical Keywords</b>", bold_body), Paragraph(", ".join(match.critical_missing_keywords) or "None", body_style)]
        ]
        skills_table = Table(skills_data, colWidths=[140, 380])
        skills_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), BG_LIGHT),
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        elements.append(skills_table)
        elements.append(Spacer(1, 10))

        # ATS Checklist
        elements.append(Paragraph("2. ATS Parsing & Hygiene Audit", section_style))
        ats_rows = [[Paragraph("<b>Check Item</b>", bold_body), Paragraph("<b>Status</b>", bold_body), Paragraph("<b>Details & Recruiter Impact</b>", bold_body)]]
        for c in match.ats_checks[:5]:
            status_color = "#16a34a" if c.passed else "#dc2626"
            ats_rows.append([
                Paragraph(f"<b>{c.check_name}</b>", body_style),
                Paragraph(f"<font color='{status_color}'><b>{c.status_label}</b></font>", body_style),
                Paragraph(c.details, body_style)
            ])
        ats_table = Table(ats_rows, colWidths=[150, 90, 280])
        ats_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BG_LIGHT),
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(ats_table)
        elements.append(Spacer(1, 10))

        # Bullet Point Rewrites
        if feedback.bullet_improvements:
            elements.append(Paragraph("3. High-Impact Resume Rewrites (XYZ Formula)", section_style))
            for idx, b in enumerate(feedback.bullet_improvements[:3], 1):
                elements.append(Paragraph(f"<b>Revision {idx}:</b>", bold_body))
                elements.append(Paragraph(f"<b>Original:</b> <font color='#64748b'>\"{b.original}\"</font>", body_style))
                elements.append(Paragraph(f"<b>Improved:</b> <font color='#1e3a8a'><b>\"{b.improved}\"</b></font>", body_style))
                elements.append(Paragraph(f"<i>Rationale:</i> {b.rationale}", subtitle_style))
                elements.append(Spacer(1, 5))

        # Interview Preparation
        if feedback.interview_questions:
            elements.append(Spacer(1, 8))
            elements.append(Paragraph("4. Targeted Technical & Architectural Interview Questions", section_style))
            for idx, q in enumerate(feedback.interview_questions[:3], 1):
                elements.append(Paragraph(f"<b>Q{idx} ({q.type} - {q.difficulty}):</b> {q.question}", bold_body))
                elements.append(Paragraph(f"<b>Why Asked:</b> {q.why_asked}", subtitle_style))
                elements.append(Paragraph(f"<b>Model Talking Points:</b> {', '.join(q.key_talking_points)}", body_style))
                elements.append(Paragraph(f"<b>Suggested Answer:</b> {q.suggested_answer}", body_style))
                elements.append(Spacer(1, 6))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
