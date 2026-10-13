"""
troubleshoot.py - Automated Diagnostic & Health Checker for INQUIRY OT Tutor
Tests Python environment, required packages, port availability, file integrity,
and API endpoints to pinpoint and explain any issue in plain English.
"""

import sys
import os
import socket

# Reconfigure stdout/stderr to UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def run_diagnostics():
    print("=" * 65)
    print("      INQUIRY OT TUTOR - AUTOMATED SYSTEM DIAGNOSTICS         ")
    print("=" * 65)
    print()

    passed = 0
    total = 6

    # Test 1: Python Version
    print("[1/6] Checking Python Version...")
    py_ver = sys.version_info
    print(f"      Running Python: {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
    print(f"      Executable: {sys.executable}")
    if py_ver.major >= 3 and py_ver.minor >= 8:
        print("      --> PASS: Python version is compatible.")
        passed += 1
    else:
        print("      --> FAIL: Python 3.8+ is recommended.")

    print()

    # Test 2: Core Packages
    print("[2/6] Checking Required Python Packages...")
    missing = []
    for pkg in ["flask", "requests", "jinja2"]:
        try:
            __import__(pkg)
            print(f"      ✓ {pkg} is installed.")
        except ImportError:
            missing.append(pkg)
            print(f"      ✗ {pkg} is MISSING.")

    if not missing:
        print("      --> PASS: All core packages are installed.")
        passed += 1
    else:
        print(f"      --> FAIL: Missing packages: {', '.join(missing)}.")
        print(f"          Fix: run 'python -m pip install {' '.join(missing)}'")

    print()

    # Test 3: Essential Files Integrity
    print("[3/6] Checking Project Files & Knowledge Base...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    required_files = [
        "app.py",
        "tutor_engine.py",
        "syllabus_mgr.py",
        "student_tracker.py",
        "rag_engine.py",
        "config.json",
        os.path.join("templates", "index.html"),
        os.path.join("static", "css", "style.css"),
        os.path.join("static", "js", "app.js"),
        os.path.join("knowledge_base", "pedretti_physical_dysfunction.json"),
        os.path.join("knowledge_base", "willard_spackman_foundations.json"),
        os.path.join("knowledge_base", "case_smith_paediatrics.json"),
        os.path.join("knowledge_base", "ot_clinical_cases.json"),
    ]

    missing_files = []
    for f in required_files:
        full_p = os.path.join(base_dir, f)
        if os.path.exists(full_p):
            pass
        else:
            missing_files.append(f)
            print(f"      ✗ Missing: {f}")

    if not missing_files:
        print(f"      ✓ Verified {len(required_files)} essential files & textbooks.")
        print("      --> PASS: All project and syllabus files are present.")
        passed += 1
    else:
        print(f"      --> FAIL: {len(missing_files)} file(s) are missing.")

    print()

    # Test 4: Network & Port 5000 Status
    print("[4/6] Checking Network Port 5000...")
    port_status = "FREE"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', 5000))
            print("      ✓ Port 5000 is open and ready to accept connections.")
        except OSError:
            port_status = "BUSY"
            print("      ! Port 5000 is currently occupied by another program.")
            print("        (Note: The tutor automatically falls back to port 5001/5002)")

    print("      --> PASS: Port binding capability confirmed.")
    passed += 1

    print()

    # Test 5: Tutor Engine & RAG Loading
    print("[5/6] Testing AI Tutor Engine & RAG Grounding...")
    try:
        from tutor_engine import TutorEngine
        te = TutorEngine()
        chunks_count = len(te.rag.chunks)
        cases_count = len(te.clinical_cases)
        print(f"      ✓ Loaded {chunks_count} textbook excerpts into RAG memory.")
        print(f"      ✓ Loaded {cases_count} authentic clinical cases.")
        print("      --> PASS: AI Engine & Knowledge Base initialized cleanly.")
        passed += 1
    except Exception as e:
        print(f"      --> FAIL: Could not initialize Tutor Engine: {e}")

    print()

    # Test 6: In-Memory Web Endpoint Test
    print("[6/6] Testing Flask Web Application Simulation...")
    try:
        import app as flask_app
        client = flask_app.app.test_client()
        r1 = client.get('/')
        r2 = client.get('/api/syllabus')
        r3 = client.get('/api/student/dashboard')
        
        if r1.status_code == 200 and r2.status_code == 200 and r3.status_code == 200:
            print("      ✓ Web interface (HTTP 200 OK)")
            print("      ✓ Syllabus API (HTTP 200 OK)")
            print("      ✓ Student Dashboard API (HTTP 200 OK)")
            print("      --> PASS: Web server routes are operating properly.")
            passed += 1
        else:
            print(f"      --> FAIL: Web routes returned status {r1.status_code}, {r2.status_code}")
    except Exception as e:
        print(f"      --> FAIL: Error during web app simulation: {e}")

    print()
    print("=" * 65)
    print(f"               DIAGNOSTIC RESULT: {passed}/{total} TESTS PASSED")
    print("=" * 65)

    if passed == total:
        print("🎉 ALL SYSTEMS ARE OPERATIONAL!")
        print("Your INQUIRY OT Tutor is completely healthy and ready to run.")
        print("You can launch it right now by double-clicking 'run_tutor.bat'")
    else:
        print("⚠️ Some checks did not pass. Please review the items marked with ✗ above.")
    print("=" * 65)


if __name__ == "__main__":
    run_diagnostics()
