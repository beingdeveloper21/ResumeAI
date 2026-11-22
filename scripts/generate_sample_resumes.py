import os
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def create_resume_pdf(output_path: str, candidate_data: dict):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    name_style = ParagraphStyle(
        "CandName",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a")
    )
    contact_style = ParagraphStyle(
        "CandContact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#475569")
    )
    section_title = ParagraphStyle(
        "CandSection",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        "CandBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1e293b")
    )
    bold_style = ParagraphStyle(
        "CandBold",
        parent=body_style,
        fontName="Helvetica-Bold"
    )
    bullet_style = ParagraphStyle(
        "CandBullet",
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10
    )

    story = []

    # Name and Title
    story.append(Paragraph(candidate_data["name"], name_style))
    story.append(Paragraph(f"<b>{candidate_data['title']}</b>", bold_style))
    story.append(Paragraph(candidate_data["contact_line"], contact_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceBefore=2, spaceAfter=8))

    # Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_title))
    story.append(Paragraph(candidate_data["summary"], body_style))
    story.append(Spacer(1, 4))

    # Technical Skills
    story.append(Paragraph("TECHNICAL SKILLS", section_title))
    for category, skill_str in candidate_data["skills"].items():
        story.append(Paragraph(f"<b>{category}:</b> {skill_str}", body_style))
    story.append(Spacer(1, 4))

    # Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_title))
    for exp in candidate_data["experience"]:
        exp_header = [
            [Paragraph(f"<b>{exp['role']}</b> | {exp['company']}", bold_style),
             Paragraph(f"<font color='#64748b'>{exp['duration']}</font>", ParagraphStyle("RightDate", parent=body_style, alignment=2))]
        ]
        t = Table(exp_header, colWidths=[380, 140])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(t)
        for b in exp["bullets"]:
            story.append(Paragraph(f"• {b}", bullet_style))
        story.append(Spacer(1, 5))

    # Projects
    story.append(Paragraph("KEY PROJECTS", section_title))
    for proj in candidate_data["projects"]:
        story.append(Paragraph(f"<b>{proj['name']}</b> | <i>{proj['tech']}</i>", bold_style))
        for b in proj["bullets"]:
            story.append(Paragraph(f"• {b}", bullet_style))
        story.append(Spacer(1, 4))

    # Education
    story.append(Paragraph("EDUCATION", section_title))
    for edu in candidate_data["education"]:
        story.append(Paragraph(f"<b>{edu['degree']}</b> - {edu['school']} ({edu['year']})", body_style))

    doc.build(story)
    print(f"Generated resume PDF: {output_path}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    sample_dir = base_dir / "backend" / "sample_resumes"
    public_dir = base_dir / "frontend" / "public"
    sample_dir.mkdir(parents=True, exist_ok=True)
    public_dir.mkdir(parents=True, exist_ok=True)

    swe_data = {
        "name": "Alex Morgan",
        "title": "Full Stack & Machine Learning Software Engineer",
        "contact_line": "alex.morgan.tech@gmail.com | +1 (555) 234-5678 | San Francisco, CA | linkedin.com/in/alexmorgan-dev | github.com/alexmorgan-dev",
        "summary": "Full Stack Engineer with 3+ years of experience designing scalable microservices with FastAPI and React. Specialized in NLP extraction, dense vector similarity benchmarking, and distributed cloud deployments.",
        "skills": {
            "Languages": "Python, TypeScript, JavaScript, SQL, C++, HTML5, CSS3, Bash",
            "Frameworks": "FastAPI, React, Node.js, Express, PyTorch, Scikit-Learn, Tailwind CSS, Redux",
            "Cloud & DevOps": "AWS, Docker, Kubernetes, GitHub Actions, PostgreSQL, Redis, MongoDB",
            "AI / NLP": "Sentence-Transformers (all-MiniLM-L6-v2), OpenAI API, Hugging Face, Vector Databases, Cosine Distance"
        },
        "experience": [
            {
                "role": "Software Engineer II",
                "company": "Cognitive Solutions Inc.",
                "duration": "2023 - Present",
                "bullets": [
                    "Architected high-throughput RESTful microservices with FastAPI and PostgreSQL handling 40,000+ daily requests with sub-50ms latency.",
                    "Implemented semantic search pipelines using Sentence-Transformers (all-MiniLM-L6-v2) and cosine similarity, elevating document match precision by 32%.",
                    "Engineered reactive single-page user dashboards in React and Tailwind CSS, increasing candidate submission conversion by 28%.",
                    "Automated multi-stage Docker container builds and CI/CD pipelines in GitHub Actions, slashing deploy times by 65%."
                ]
            },
            {
                "role": "Software Development Engineer",
                "company": "Apex Cloud Systems",
                "duration": "2021 - 2023",
                "bullets": [
                    "Developed asynchronous API endpoints and database schemas in Python and MySQL supporting 100k active users.",
                    "Integrated Redis caching layer reducing database read load by 45% during peak traffic bursts.",
                    "Collaborated with cross-functional teams in 2-week Agile sprints and maintained 90%+ unit test coverage using PyTest."
                ]
            }
        ],
        "projects": [
            {
                "name": "ResumeAI - Automated Evaluation & Job Matcher",
                "tech": "FastAPI, OpenAI API, Sentence-Transformers, React, PyPDF",
                "bullets": [
                    "Built an automated resume evaluation platform that extracts structured skills, experience, and education from candidate PDF resumes using NLP pipelines.",
                    "Implemented semantic similarity scoring using Sentence-Transformers (all-MiniLM-L6-v2) and cosine distance to benchmark resumes against job descriptions.",
                    "Engineered an LLM-driven feedback engine delivering targeted suggestions for resume enhancement and personalized technical interview questions."
                ]
            }
        ],
        "education": [
            {
                "degree": "Bachelor of Science in Computer Science",
                "school": "University of California, Berkeley",
                "year": "2017 - 2021"
            }
        ]
    }

    create_resume_pdf(str(sample_dir / "sample_software_engineer.pdf"), swe_data)
    create_resume_pdf(str(public_dir / "sample-resume.pdf"), swe_data)
