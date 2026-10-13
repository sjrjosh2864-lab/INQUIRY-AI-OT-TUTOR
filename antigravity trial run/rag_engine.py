"""
rag_engine.py - Retrieval-Augmented Generation (RAG) & Knowledge Base Engine
Indexes reliable Occupational Therapy textbooks, research papers, and MGRU syllabus materials.
Grounds all AI tutor responses in verified academic literature with verifiable citations.
"""

import os
import json
import re
import math
from typing import List, Dict, Any, Optional

KB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base")


class DocumentChunk:
    def __init__(self, doc_id: str, title: str, source: str, chapter: str, content: str, topics: List[str]):
        self.doc_id = doc_id
        self.title = title
        self.source = source
        self.chapter = chapter
        self.content = content
        self.topics = topics
        self.tokens = self._tokenize(f"{title} {source} {chapter} {' '.join(topics)} {content}")

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return [w.lower() for w in re.findall(r"\b[a-zA-Z0-9_\-]{3,}\b", text)]


class RAGEngine:
    """Manages the indexing, search, and citation grounding for OT academic sources."""

    def __init__(self, kb_path: str = KB_DIR):
        self.kb_path = kb_path
        self.chunks: List[DocumentChunk] = []
        self.uploaded_docs_path = os.path.join(kb_path, "user_uploaded_notes.json")
        self.load_all_sources()

    def load_all_sources(self):
        """Loads and indexes all json files in knowledge_base directory."""
        self.chunks = []
        if not os.path.exists(self.kb_path):
            os.makedirs(self.kb_path, exist_ok=True)

        for filename in os.listdir(self.kb_path):
            if filename.endswith(".json") and not filename.startswith("ot_clinical_cases"):
                full_path = os.path.join(self.kb_path, filename)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            for item in data:
                                chunk = DocumentChunk(
                                    doc_id=item.get("id", filename),
                                    title=item.get("title", item.get("chapter", filename)),
                                    source=item.get("source", "Approved Academic Source"),
                                    chapter=item.get("chapter", "General Reference"),
                                    content=item.get("content", ""),
                                    topics=item.get("topics", [])
                                )
                                self.chunks.append(chunk)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    def add_custom_document(self, title: str, source: str, chapter: str, content: str, topics: Optional[List[str]] = None) -> bool:
        """Allows students or professors to upload custom syllabus notes or lecture materials."""
        if topics is None:
            topics = []
        doc_id = f"custom_{len(self.chunks) + 1}_{int(abs(hash(title)) % 10000)}"
        new_entry = {
            "id": doc_id,
            "title": title,
            "source": source or "Student Uploaded Lecture Notes",
            "chapter": chapter or "Custom Reference",
            "topics": topics,
            "content": content
        }

        # Save to user_uploaded_notes.json
        user_notes = []
        if os.path.exists(self.uploaded_docs_path):
            try:
                with open(self.uploaded_docs_path, "r", encoding="utf-8") as f:
                    user_notes = json.load(f)
            except Exception:
                user_notes = []

        user_notes.append(new_entry)
        with open(self.uploaded_docs_path, "w", encoding="utf-8") as f:
            json.dump(user_notes, f, indent=2, ensure_ascii=False)

        # Append to live index
        chunk = DocumentChunk(
            doc_id=doc_id,
            title=title,
            source=new_entry["source"],
            chapter=new_entry["chapter"],
            content=content,
            topics=topics
        )
        self.chunks.append(chunk)
        return True

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Performs BM25-style relevance retrieval across indexed OT textbooks and notes."""
        if not query or not self.chunks:
            return []

        query_tokens = DocumentChunk._tokenize(query)
        if not query_tokens:
            return []

        # Calculate scores
        scored_results = []
        total_docs = len(self.chunks)

        for chunk in self.chunks:
            score = 0.0
            chunk_tokens_set = set(chunk.tokens)
            doc_len = len(chunk.tokens)

            # Topic and title exact keyword boost
            lower_q = query.lower()
            for topic in chunk.topics:
                if topic.lower() in lower_q:
                    score += 25.0

            if chunk.chapter.lower() in lower_q:
                score += 15.0

            # Term frequency match
            for q_tok in query_tokens:
                if q_tok in chunk_tokens_set:
                    tf = chunk.tokens.count(q_tok)
                    # Simple BM25 weighting approximation
                    idf = math.log((total_docs + 1) / (1 + sum(1 for c in self.chunks if q_tok in c.tokens))) + 1.0
                    score += (tf / (tf + 1.5)) * idf

            if score > 0:
                scored_results.append({
                    "chunk": chunk,
                    "score": score
                })

        scored_results.sort(key=lambda x: x["score"], reverse=True)
        top_chunks = scored_results[:top_k]

        return [
            {
                "doc_id": r["chunk"].doc_id,
                "title": r["chunk"].title,
                "source": r["chunk"].source,
                "chapter": r["chunk"].chapter,
                "topics": r["chunk"].topics,
                "content": r["chunk"].content,
                "relevance_score": round(r["score"], 2)
            }
            for r in top_chunks
        ]

    def build_grounded_context_prompt(self, query: str, top_k: int = 2) -> str:
        """Builds a formatted context block with citations for LLM prompt grounding."""
        results = self.search(query, top_k=top_k)
        if not results:
            return "No specific textbook excerpts retrieved for this query. Rely on standard evidence-based OT literature."

        context_parts = ["=== VERIFIED ACADEMIC KNOWLEDGE BASE (GROUNDING SOURCES) ==="]
        for idx, res in enumerate(results, 1):
            context_parts.append(
                f"\n[Source {idx}]: {res['source']}\n"
                f"Section/Chapter: {res['chapter']}\n"
                f"Key Topics: {', '.join(res['topics'])}\n"
                f"Excerpts:\n{res['content']}\n"
            )
        context_parts.append("=============================================================")
        return "\n".join(context_parts)

    def get_all_sources_summary(self) -> List[Dict[str, Any]]:
        """Returns metadata about all indexed books and papers."""
        sources_map = {}
        for c in self.chunks:
            if c.source not in sources_map:
                sources_map[c.source] = {
                    "source": c.source,
                    "sections_count": 0,
                    "topics": set()
                }
            sources_map[c.source]["sections_count"] += 1
            for t in c.topics:
                sources_map[c.source]["topics"].add(t)

        return [
            {
                "source": k,
                "sections_count": v["sections_count"],
                "topics": list(v["topics"])[:8]
            }
            for k, v in sources_map.items()
        ]
