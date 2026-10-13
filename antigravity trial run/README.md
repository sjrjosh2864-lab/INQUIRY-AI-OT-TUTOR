# 🌿 INQUIRY OT Tutor
### *A Personalised AI Tutor & Clinical Mentor for Occupational Therapy Students*
**Aligned with The Tamil Nadu Dr. M.G.R. Medical University (TNMGRU) B.O.T Curriculum & Global OT Standards**

---

## 🌟 Overview

**INQUIRY OT Tutor** is an interactive, inquiry-based AI learning platform designed specifically for Occupational Therapy (OT) students. Rather than spoon-feeding direct answers immediately, it functions as a clinical mentor—asking guiding questions, identifying gaps in understanding, offering progressive hints, and helping students cultivate genuine clinical reasoning.

The tutor strictly enforces the standard **OT Clinical Reasoning Pathway**:
```
CONDITION ➔ IMPAIRMENT ➔ ACTIVITY LIMITATION ➔ PARTICIPATION PROBLEM ➔ ASSESSMENT ➔ GOALS (SMART) ➔ INTERVENTION ➔ CLINICAL JUSTIFICATION ➔ PROGNOSIS
```

---

## 🚀 Quick Start (No Coding Experience Needed!)

### For Windows Users (1-Click Launch):
1. Navigate to this folder (`antigravity trial run`).
2. **Double-click** the file named:
   ```
   run_tutor.bat
   ```
3. Your default web browser will automatically open:
   ```
   http://127.0.0.1:5000
   ```
4. Start learning! That's all.

---

### Manual Launch (Command Line):
If you prefer running via terminal:
```bash
python app.py
```
Then open `http://127.0.0.1:5000` in Google Chrome, Microsoft Edge, or any browser.

---

## 🎯 The 6 Learning Modes

You can switch between any of these 6 modes at any time using the navigation tabs at the top:

| Mode | Purpose | How It Works |
| :--- | :--- | :--- |
| 🧠 **Inquiry Mode** | Socratic Guided Reasoning | Teaches through questions and progressive hints. Never gives away the answer upfront; encourages self-discovery. |
| 📚 **Tutor Mode** | Clear Academic Teaching | Provides direct, structured explanations with anatomy, standardized tests, and clinical pearls. |
| 📝 **Exam Mode** | TNMGRU University Prep | Prepares answers formatted according to marks: **2/3 Marks** (Short), **5 Marks** (Brief), **10/15 Marks** (Essays). Also evaluates and grades your own written answers. |
| 🎓 **Viva Mode** | Rapid Oral Examination | Simulates an external oral examiner asking rapid clinical questions. Awards an oral viva score out of 10 with examiner feedback. |
| 🩺 **Clinical Reasoning Mode** | Interactive Case Simulator | Walks you step-by-step through real-world patient cases (Stroke, Radial Nerve, CP, etc.) along the 8-stage OT reasoning pathway. |
| 🔄 **Revision Mode** | Diagnostic Weakness Remediation | Pinpoints your low-scoring topics and recurring clinical misconceptions, generating targeted recall quizzes. |

---

## 📖 Occupational Therapy Subjects Covered

The tutor comes pre-configured with the **TNMGRU B.O.T Syllabus** organized by **Subject ➔ Unit ➔ Topic ➔ Subtopic**:

1. **OT in Neurology**: Stroke (MCA/ACA/PCA), TBI (RLAS Levels I-X), Spinal Cord Injury (ASIA scale, Tenodesis grasp, Autonomic Dysreflexia), Parkinson's, Multiple Sclerosis, Guillain-Barré Syndrome.
2. **OT in Orthopaedics & Hand**: Radial/Median/Ulnar nerve injuries, Brachial Plexus palsies (Erb's & Klumpke's), Tendon repair protocols (Kleinert, Duran), De Quervain's, Rheumatoid Arthritis, Burns (Intrinsic Plus splint), Amputations.
3. **OT in Paediatrics**: Cerebral Palsy (GMFCS & MACS), Ayres Sensory Integration (Modulation, Sensory Diet, Wilbarger protocol), Autism Spectrum Disorder (TEACCH, Social Stories), ADHD, Handwriting ergonomics.
4. **OT in Psychiatry & Mental Health**: Schizophrenia, Mood disorders, Anxiety, Mosey's 5 Developmental Groups, Therapeutic Use of Self, Psychosocial Rehabilitation.
5. **OT Models & Frames of Reference**: MOHO (Volition, Habituation), PEO, PEOP, Kawa (River) Model, Biomechanical FoR, Rehabilitative FoR, NDT (Bobath), Motor Learning (Carr & Shepherd).
6. **Community OT & General Medicine**: Cardiac rehabilitation (MET levels, Sternal precautions), Geriatric fall prevention, WHO CBR Matrix, Industrial ergonomics & Work Hardening.

---

## 📊 Personalised Learning & Weakness Tracker

The tutor remembers your performance across study sessions:
- **Topics Studied Count**: Keeps a tally of topics reviewed.
- **Overall Mastery (%)**: Computes mastery scores across each of the 6 subjects.
- **Logged Misconceptions**: Detects recurring errors (e.g., choosing a static splint when a dynamic splint was indicated) and saves them with a "Golden Correction Pearl".
- **Priority Revision Queue**: Automatically places low-scoring topics into your revision queue.
- **Persistent Data**: Stored safely in `data/student_profile.json`.

---

## 📚 Knowledge Base & Future-Ready RAG System

All answers are grounded in standard OT academic literature:
- *Pedretti's Occupational Therapy: Practice Skills for Physical Dysfunction*
- *Willard & Spackman's Occupational Therapy*
- *Occupational Therapy for Children and Adolescents* (Case-Smith & O'Brien)
- *The Tamil Nadu Dr. M.G.R. Medical University (TNMGRU) B.O.T Curriculum Guidelines*

### Uploading Your Own College Notes / Syllabus Materials:
1. Click the **📖 Library** button in the top navigation bar.
2. Fill in the note title, source (e.g. *College Lecture*), and paste your text or exam notes.
3. Click **"Index Note into Knowledge Base"**.
4. The tutor will immediately begin citing and using your uploaded material in future responses!

---

## ⚙️ AI Engine: Offline vs. Live AI

**INQUIRY OT Tutor works 100% offline out-of-the-box!**
- **Offline Mode (Default)**: Uses the built-in, verified Academic OT Knowledge Engine. No internet or API key is required.
- **Live AI Mode (Optional)**: If you would like to connect Google Gemini or OpenAI:
  1. Click **⚙️ Settings** in the top navigation bar.
  2. Select **Google Gemini API** (Google offers a free API key at [Google AI Studio](https://aistudio.google.com/)).
  3. Paste your API key into the box and click **Save Settings**.
  4. The status badge will switch to **✨ Live AI Connected**.

---

## 🛠️ Project Structure (Easy Maintenance)

```
antigravity trial run/
├── app.py                   # Main Flask server and web routes
├── tutor_engine.py          # AI agent reasoning logic for the 6 modes
├── rag_engine.py            # Knowledge base search and document indexer
├── syllabus_mgr.py          # TNMGRU B.O.T syllabus structure
├── student_tracker.py       # Personalised student learning & mistake tracker
├── config.json              # App settings, API key, student name
├── run_tutor.bat            # 1-Click launcher for Windows
├── requirements.txt         # Minimal Python dependencies
├── knowledge_base/          # Pre-grounded textbooks & clinical cases
│   ├── pedretti_physical_dysfunction.json
│   ├── willard_spackman_foundations.json
│   ├── case_smith_paediatrics.json
│   ├── mgru_bot_curriculum_guidelines.json
│   ├── ot_splints_and_assessments.json
│   └── ot_clinical_cases.json
├── static/
│   ├── css/style.css        # Clean medical-academic styling
│   └── js/app.js            # Interactive UI controller
├── templates/
│   └── index.html           # Main student interface
└── data/
    └── student_profile.json # Student study history and weak areas
```

---

## 💡 How to Customize & Add More Content (For Beginners)

- **To add new clinical cases**: Open `knowledge_base/ot_clinical_cases.json` in Notepad, copy one of the case templates, and edit the patient details!
- **To add new syllabus units**: Open `syllabus_mgr.py` and add your unit or topic into the `MGRU_OT_SYLLABUS` dictionary.
- **To reset your student profile**: Delete `data/student_profile.json`—the app will automatically create a fresh profile the next time it starts.
