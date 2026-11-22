# ResumeAI — Technical & System Design Interview Questions & Answers

## Core Project & Architectural Questions

### 1. Tell me about this project. What problem does it solve and what is the architecture?
**Answer:**
ResumeAI is an automated resume intelligence and job matching platform built to bridge the semantic gap in traditional ATS screening. Over 75% of qualified resumes are filtered out by legacy systems relying on brittle keyword-matching (like BM25). ResumeAI combines a reactive React 18 single-page application with an asynchronous FastAPI gateway, a dual-engine PDF extractor (PyPDF + PyMuPDF), a Sentence-Transformers semantic engine (`all-MiniLM-L6-v2`), and an LLM feedback engine. When a resume and job description are ingested, the platform extracts structured entities, generates 384-dimensional dense embeddings, computes cosine distance, runs an ATS hygiene audit, and synthesizes Google XYZ-formula bullet rewrites and personalized interview questions.

---

### 2. Why choose Sentence-Transformers (all-MiniLM-L6-v2) over standard TF-IDF, BM25, or direct LLM calls?
**Answer:**
- **Versus BM25/TF-IDF:** Traditional lexical methods fail when candidates use synonyms or acronyms (e.g., 'Kubernetes' vs 'K8s', 'ML' vs 'Machine Learning'). Sentence-Transformers maps semantic meaning into a continuous dense vector space where related concepts cluster together.
- **Versus direct LLM calls:** Sending thousands of resumes directly to GPT-4o incurs severe latency (1.5–4s per evaluation), exorbitant API costs, and non-deterministic scoring. `all-MiniLM-L6-v2` runs locally on standard CPU in under 15ms per document, producing deterministic unit vectors whose similarity is computed in $O(d)$ time via dot product.

---

### 3. How do you handle CPU-bound ML inference and PDF parsing in an async FastAPI application without blocking the event loop?
**Answer:**
FastAPI runs on Starlette's single-threaded `asyncio` event loop. Calling CPU-intensive operations (such as PyTorch transformer encoding or PDF parsing) directly inside an `async def` endpoint blocks the main thread, causing all concurrent HTTP I/O requests to freeze. To resolve this, CPU-bound workloads are offloaded to Starlette's threadpool using `starlette.concurrency.run_in_threadpool`, keeping the event loop non-blocking. For large-scale production workloads, these tasks are decoupled to asynchronous Celery/Redis worker queues.

---

### 4. What is Cosine Similarity and why is it preferred over Euclidean Distance?
**Answer:**
Cosine similarity measures the angular orientation between two non-zero vectors:
$$\text{Cosine Similarity}(u, v) = \frac{u \cdot v}{\|u\|_2 \|v\|_2}$$
Euclidean distance measures the geometric distance between points in space ($\sqrt{\sum (u_i - v_i)^2}$). In document analysis, Euclidean distance is biased by document length: a comprehensive 2-page resume with 900 words would have a much larger vector magnitude than a brief 300-word job description, falsely inflating Euclidean distance. Cosine similarity normalizes vector magnitude, evaluating topical alignment independently of length.

---

### 5. How do you handle complex multi-column resumes, unusual fonts, and PDF parsing errors?
**Answer:**
PDF is an instruction set for 2D print rendering, meaning text characters can be stored in arbitrary order. We implemented a dual-engine fallback:
1. `pypdf` provides lightweight, fast stream extraction.
2. If character extraction volume falls below a validation threshold, `PyMuPDF` (`fitz`) triggers automatically. PyMuPDF leverages MuPDF's C-library to sort text blocks by coordinate bounding boxes, reconstructing intended reading order.
3. Extracted text is passed through a regex normalization layer that resolves ligatures (e.g., `fi` $\to$ `fi`), strips non-breaking spaces (`\u00a0`), and unifies bullet glyphs.

---

### 6. How would you scale ResumeAI to handle 100,000 resumes per hour?
**Answer:**
1. **Direct Ingestion:** Resumes are uploaded directly to an object store (e.g., AWS S3) via presigned URLs to avoid API gateway memory bottlenecks.
2. **Message Queuing:** S3 upload triggers an AWS SQS / RabbitMQ queue message.
3. **Autoscaling Workers:** Kubernetes Horizontal Pod Autoscaler (HPA) scales stateless worker pods based on queue length.
4. **Optimized Inference:** Models are exported and quantized to ONNX Runtime format for 4x faster CPU inference.
5. **Caching & Vector DB:** Pre-embedded job descriptions are cached in Redis. Candidate embeddings are stored in a distributed vector database (Qdrant or Milvus) for rapid batch cosine retrieval.
