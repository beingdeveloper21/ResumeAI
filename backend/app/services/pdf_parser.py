import io
import re
from typing import Tuple, Dict, Any
import pypdf

# Try fitz (PyMuPDF) as high-precision fallback
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

class PDFParserService:
    @staticmethod
    def extract_text(file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
        """
        Extracts raw text and metadata from PDF bytes.
        Uses pypdf as primary parser and PyMuPDF as high-fidelity fallback.
        """
        text = ""
        page_count = 0
        metadata: Dict[str, Any] = {}
        
        # Method 1: PyPDF
        try:
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            page_count = len(reader.pages)
            extracted_pages = []
            for idx, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    extracted_pages.append(page_text)
            text = "\n\n".join(extracted_pages)
            if reader.metadata:
                metadata = {
                    "author": str(reader.metadata.author or ""),
                    "creator": str(reader.metadata.creator or ""),
                    "producer": str(reader.metadata.producer or "")
                }
        except Exception as e:
            text = ""

        # Method 2: If PyPDF yielded little or empty text, use PyMuPDF if available
        if (not text or len(text.strip()) < 50) and HAS_PYMUPDF:
            try:
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                page_count = len(doc)
                pages_text = []
                for page in doc:
                    pages_text.append(page.get_text("text"))
                text = "\n\n".join(pages_text)
                metadata = doc.metadata or metadata
            except Exception:
                pass

        # Text cleaning and normalization
        cleaned_text = PDFParserService._clean_text(text)
        words = re.findall(r"\b\w+\b", cleaned_text)
        
        meta = {
            "page_count": max(page_count, 1),
            "word_count": len(words),
            "character_count": len(cleaned_text),
            "pdf_meta": metadata
        }
        
        return cleaned_text, meta

    @staticmethod
    def _clean_text(raw_text: str) -> str:
        if not raw_text:
            return ""
        # Normalize non-breaking spaces and special quotes/dashes
        t = raw_text.replace("\u00a0", " ")
        t = re.sub(r"[\u2010\u2011\u2012\u2013\u2014\u2015]", "-", t)
        t = re.sub(r"[\u2018\u2019]", "'", t)
        t = re.sub(r"[\u201c\u201d]", '"', t)
        t = re.sub(r"[\u2022\u2023\u25E6\u2043\u2219]", "\n- ", t)
        
        # Remove consecutive blank lines
        lines = [re.sub(r"\s+", " ", line).strip() for line in t.splitlines()]
        cleaned = "\n".join([line for line in lines if line])
        return cleaned
