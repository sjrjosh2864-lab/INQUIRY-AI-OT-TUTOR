"""
app.py - Main Flask Web Application for INQUIRY OT Tutor
Provides web interface and REST APIs for:
- 6 Learning Modes (Inquiry, Tutor, Exam, Viva, Clinical Reasoning, Revision)
- MGRU B.O.T Syllabus Explorer
- Student Weakness & Strength Tracker
- Knowledge Base & RAG Management
- Case Studies & Pathway Stepper
"""

import os
import sys
import json
import socket
import threading
import webbrowser
from flask import Flask, render_template, request, jsonify

# Reconfigure Windows stdout/stderr to UTF-8 to prevent charmap UnicodeEncodeErrors
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Ensure local imports work reliably
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tutor_engine import TutorEngine
from syllabus_mgr import SyllabusManager
from student_tracker import StudentTracker
from rag_engine import RAGEngine

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Instantiate core engines
tutor_engine = TutorEngine()
syllabus_mgr = SyllabusManager()
student_tracker = StudentTracker()
rag_engine = RAGEngine()


@app.route("/")
def index():
    """Renders the main student-friendly application interface."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Processes chat interaction across any of the 6 tutor modes."""
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    mode = data.get("mode", "inquiry")
    context_data = data.get("context_data", {})

    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400

    try:
        result = tutor_engine.process_message(message, mode=mode, context_data=context_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "error": str(e),
            "response": f"An error occurred while processing: {str(e)}",
            "mode": mode,
            "engine": "error_handler",
            "citations": []
        }), 500


@app.route("/api/syllabus", methods=["GET"])
def get_syllabus():
    """Returns the TNMGRU syllabus tree."""
    tree = syllabus_mgr.get_full_tree()
    return jsonify({"subjects": tree})


@app.route("/api/syllabus/search", methods=["GET"])
def search_syllabus():
    """Searches syllabus topics by keyword."""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"results": []})
    results = syllabus_mgr.find_topics_by_keyword(query)
    return jsonify({"results": results})


@app.route("/api/student/dashboard", methods=["GET"])
def get_student_dashboard():
    """Returns student profile, analytics, weak areas, and recurring mistakes."""
    summary = student_tracker.get_dashboard_summary()
    return jsonify(summary)


@app.route("/api/student/profile", methods=["POST"])
def update_student_profile():
    """Updates student profile information."""
    data = request.get_json() or {}
    name = data.get("student_name", "")
    level = data.get("study_level", "")
    student_tracker.update_student_info(name, level)
    return jsonify({"success": True, "summary": student_tracker.get_dashboard_summary()})


@app.route("/api/cases", methods=["GET"])
def get_clinical_cases():
    """Returns all available clinical cases for the Clinical Reasoning Mode."""
    cases_summary = [
        {
            "case_id": c["case_id"],
            "title": c["title"],
            "subject": c["subject"],
            "patient_summary": c["patient_summary"],
            "steps_count": len(c.get("inquiry_sequence", []))
        }
        for c in tutor_engine.clinical_cases
    ]
    return jsonify({"cases": cases_summary})


@app.route("/api/cases/<case_id>", methods=["GET"])
def get_case_detail(case_id):
    """Returns full details and 8-step reasoning pathway for a clinical case."""
    case = tutor_engine.get_clinical_case(case_id)
    if not case:
        return jsonify({"error": "Case not found"}), 404
    return jsonify({"case": case})


@app.route("/api/rag/sources", methods=["GET"])
def get_rag_sources():
    """Returns overview of indexed textbooks and knowledge base documents."""
    summary = tutor_engine.rag.get_all_sources_summary()
    return jsonify({"sources": summary, "total_chunks": len(tutor_engine.rag.chunks)})


@app.route("/api/rag/upload", methods=["POST"])
def upload_notes():
    """Allows uploading custom notes or lecture content into the RAG knowledge store."""
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    source = data.get("source", "Custom Notes").strip()
    content = data.get("content", "").strip()
    chapter = data.get("chapter", "Lecture Notes").strip()
    topics = data.get("topics", [])

    if not title or not content:
        return jsonify({"error": "Title and content are required."}), 400

    success = tutor_engine.rag.add_custom_document(title, source, chapter, content, topics)
    return jsonify({"success": success, "message": f"Successfully indexed '{title}' into knowledge base!"})


@app.route("/api/config", methods=["GET", "POST"])
def handle_config():
    """Retrieves or updates tutor configuration and API keys."""
    if request.method == "POST":
        data = request.get_json() or {}
        tutor_engine.save_config(data)
        return jsonify({"success": True, "config": tutor_engine.config})
    
    # Hide sensitive full API key, show masked version
    conf = dict(tutor_engine.config)
    raw_key = conf.get("api_key", "")
    if raw_key and len(raw_key) > 8:
        conf["api_key_masked"] = raw_key[:4] + "..." + raw_key[-4:]
    else:
        conf["api_key_masked"] = "Not set (using built-in academic engine)"
    return jsonify(conf)


@app.route("/api/test-connection", methods=["POST"])
def test_connection_route():
    """Validates API credentials against Gemini or OpenAI."""
    data = request.get_json() or {}
    provider = data.get("api_provider", "gemini")
    api_key = data.get("api_key", "").strip() or tutor_engine.config.get("api_key", "")
    model = data.get("model") or (tutor_engine.config.get("gemini_model") if provider == "gemini" else tutor_engine.config.get("openai_model"))

    result = tutor_engine.test_connection(provider, api_key, model)
    return jsonify(result)


def find_available_port(start_port: int = 5000, max_attempts: int = 20) -> int:
    """Finds an open TCP port starting from start_port."""
    for p in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', p))
                return p
            except OSError:
                continue
    return start_port


if __name__ == "__main__":
    requested_port = int(os.environ.get("PORT", 5000))
    port = find_available_port(requested_port)
    server_url = f"http://127.0.0.1:{port}"

    print(f"===============================================================")
    print(f"       INQUIRY OT Tutor - AI Mentor for OT Students            ")
    print(f"   TN M.G.R. Medical University (MGRU) Curriculum Aligned      ")
    print(f"===============================================================")
    print(f" Server running at: {server_url}")
    print(f" Press Ctrl+C in this terminal to stop.")
    print(f"===============================================================")

    # Safely open browser in a separate thread after server has initialized
    def open_browser():
        try:
            webbrowser.open(server_url)
        except Exception:
            pass

    threading.Timer(1.2, open_browser).start()
    app.run(host="127.0.0.1", port=port, debug=False)

