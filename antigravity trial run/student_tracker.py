"""
student_tracker.py - Personalised Student Learning & Weakness Tracker
Learns the student's strengths and weaknesses over time.
Tracks topics studied, recurring clinical mistakes, mastery scores, and generates targeted revision cues.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PROFILE_FILE = os.path.join(DATA_DIR, "student_profile.json")


class StudentTracker:
    """Manages student profile, subject performance, mistake log, and weak-area analytics."""

    def __init__(self, profile_path: str = PROFILE_FILE):
        self.profile_path = profile_path
        self.data: Dict[str, Any] = self._load_profile()

    def _get_default_profile(self) -> Dict[str, Any]:
        return {
            "student_name": "OT Scholar",
            "study_level": "3rd Year BOT (Clinical Phase)",
            "target_university": "The Tamil Nadu Dr. M.G.R. Medical University",
            "joined_date": datetime.now().strftime("%Y-%m-%d"),
            "last_active": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stats": {
                "total_questions_attempted": 0,
                "correct_responses": 0,
                "partial_responses": 0,
                "incorrect_responses": 0,
                "cases_completed": 0,
                "viva_sessions": 0,
                "exams_practiced": 0,
                "study_streak_days": 1
            },
            "subject_mastery": {
                "neurology": {"studied_topics": 0, "mastery_score": 75, "total_attempts": 0},
                "orthopaedics": {"studied_topics": 0, "mastery_score": 70, "total_attempts": 0},
                "paediatrics": {"studied_topics": 0, "mastery_score": 72, "total_attempts": 0},
                "psychiatry": {"studied_topics": 0, "mastery_score": 68, "total_attempts": 0},
                "foundations_models": {"studied_topics": 0, "mastery_score": 80, "total_attempts": 0},
                "community_general": {"studied_topics": 0, "mastery_score": 65, "total_attempts": 0}
            },
            "topic_history": {},
            "recurring_mistakes": [
                {
                    "id": "err_init_1",
                    "subject": "orthopaedics",
                    "topic": "Radial Nerve Palsy Splinting",
                    "mistake": "Selected static resting splint instead of dynamic extensor splint for functional grasp assistance.",
                    "correction": "Dynamic extensor splint is indicated to preserve active grasp while dynamically replacing absent extensor pull.",
                    "occurrences": 1,
                    "date": datetime.now().strftime("%Y-%m-%d")
                }
            ],
            "weak_areas": ["Radial Nerve Palsy Splinting", "Autonomic Dysreflexia Emergency Protocol"],
            "revision_queue": ["Radial Nerve Palsy Splinting", "Mosey's Developmental Groups"],
            "recent_activities": []
        }

    def _load_profile(self) -> Dict[str, Any]:
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        default_data = self._get_default_profile()
        self._save_profile(default_data)
        return default_data

    def _save_profile(self, data: Optional[Dict[str, Any]] = None):
        if data is None:
            data = self.data
        os.makedirs(os.path.dirname(self.profile_path), exist_ok=True)
        try:
            with open(self.profile_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving profile: {e}")

    def update_student_info(self, name: str, level: Optional[str] = None):
        """Updates student display name and academic year."""
        if name:
            self.data["student_name"] = name.strip()
        if level:
            self.data["study_level"] = level.strip()
        self.data["last_active"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_profile()

    def record_attempt(self, subject_id: str, topic_name: str, result: str, notes: str = "", mode: str = "inquiry"):
        """
        Records question outcome: 'correct', 'partial', or 'incorrect'.
        Updates subject mastery, stats, and topic history.
        """
        stats = self.data.setdefault("stats", {})
        stats["total_questions_attempted"] = stats.get("total_questions_attempted", 0) + 1
        self.data["last_active"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if result == "correct":
            stats["correct_responses"] = stats.get("correct_responses", 0) + 1
            delta = 4
        elif result == "partial":
            stats["partial_responses"] = stats.get("partial_responses", 0) + 1
            delta = 1
        else:
            stats["incorrect_responses"] = stats.get("incorrect_responses", 0) + 1
            delta = -5

        # Subject mastery
        subj_map = self.data.setdefault("subject_mastery", {})
        if subject_id not in subj_map:
            subj_map[subject_id] = {"studied_topics": 0, "mastery_score": 60, "total_attempts": 0}
        
        curr = subj_map[subject_id]["mastery_score"]
        new_score = max(10, min(100, curr + delta))
        subj_map[subject_id]["mastery_score"] = new_score
        subj_map[subject_id]["total_attempts"] = subj_map[subject_id].get("total_attempts", 0) + 1

        # Topic history
        topic_key = topic_name.strip()
        th = self.data.setdefault("topic_history", {})
        if topic_key not in th:
            th[topic_key] = {
                "subject": subject_id,
                "attempts": 0,
                "correct": 0,
                "score": 50,
                "last_reviewed": datetime.now().strftime("%Y-%m-%d")
            }
            subj_map[subject_id]["studied_topics"] = subj_map[subject_id].get("studied_topics", 0) + 1

        th[topic_key]["attempts"] += 1
        if result == "correct":
            th[topic_key]["correct"] += 1
            th[topic_key]["score"] = min(100, th[topic_key]["score"] + 15)
        elif result == "partial":
            th[topic_key]["score"] = min(100, th[topic_key]["score"] + 5)
        else:
            th[topic_key]["score"] = max(10, th[topic_key]["score"] - 15)
            self._add_to_weak_areas(topic_key)

        th[topic_key]["last_reviewed"] = datetime.now().strftime("%Y-%m-%d")

        # Log recent activity
        activity_entry = {
            "timestamp": datetime.now().strftime("%H:%M - %d %b"),
            "mode": mode,
            "topic": topic_name,
            "result": result,
            "notes": notes[:80] if notes else ""
        }
        self.data.setdefault("recent_activities", []).insert(0, activity_entry)
        self.data["recent_activities"] = self.data["recent_activities"][:15]

        self._refresh_weak_areas()
        self._save_profile()

    def record_mistake(self, subject: str, topic: str, mistake: str, correction: str):
        """Logs a specific clinical misconception."""
        mistakes = self.data.setdefault("recurring_mistakes", [])
        # Check if already exists
        for m in mistakes:
            if m["topic"].lower() == topic.lower() and mistake[:30].lower() in m["mistake"].lower():
                m["occurrences"] += 1
                m["date"] = datetime.now().strftime("%Y-%m-%d")
                self._save_profile()
                return

        mistakes.insert(0, {
            "id": f"err_{len(mistakes) + 1}",
            "subject": subject,
            "topic": topic,
            "mistake": mistake,
            "correction": correction,
            "occurrences": 1,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        self._add_to_weak_areas(topic)
        self._save_profile()

    def _add_to_weak_areas(self, topic: str):
        weaks = self.data.setdefault("weak_areas", [])
        if topic not in weaks:
            weaks.append(topic)
        rev_queue = self.data.setdefault("revision_queue", [])
        if topic not in rev_queue:
            rev_queue.append(topic)

    def _refresh_weak_areas(self):
        """Identifies topics scoring under 60% as priority weak areas."""
        th = self.data.get("topic_history", {})
        weak_set = set(self.data.get("weak_areas", []))
        for topic, info in th.items():
            if info.get("score", 100) < 60:
                weak_set.add(topic)
            elif info.get("score", 0) >= 80 and topic in weak_set:
                weak_set.remove(topic)
        self.data["weak_areas"] = list(weak_set)

    def record_case_completion(self, case_title: str, score_percent: int):
        """Logs a completed clinical reasoning case."""
        stats = self.data.setdefault("stats", {})
        stats["cases_completed"] = stats.get("cases_completed", 0) + 1
        self.data.setdefault("recent_activities", []).insert(0, {
            "timestamp": datetime.now().strftime("%H:%M - %d %b"),
            "mode": "clinical_reasoning",
            "topic": case_title,
            "result": f"Completed ({score_percent}%)",
            "notes": "OT Reasoning Pathway Mastered"
        })
        self._save_profile()

    def record_viva_session(self, score_out_of_10: int, topic: str):
        """Logs oral viva voce evaluation."""
        stats = self.data.setdefault("stats", {})
        stats["viva_sessions"] = stats.get("viva_sessions", 0) + 1
        self.data.setdefault("recent_activities", []).insert(0, {
            "timestamp": datetime.now().strftime("%H:%M - %d %b"),
            "mode": "viva",
            "topic": topic,
            "result": f"{score_out_of_10}/10",
            "notes": "Rapid Oral Exam"
        })
        self._save_profile()

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Provides a complete data package for the frontend analytics dashboard."""
        stats = self.data.get("stats", {})
        tot = stats.get("total_questions_attempted", 0)
        corr = stats.get("correct_responses", 0)
        acc = round((corr / tot) * 100) if tot > 0 else 0

        # Calculate overall mastery average across subjects
        subjs = self.data.get("subject_mastery", {})
        if subjs:
            avg_mastery = round(sum(s.get("mastery_score", 0) for s in subjs.values()) / len(subjs))
        else:
            avg_mastery = 70

        return {
            "student_name": self.data.get("student_name", "OT Scholar"),
            "study_level": self.data.get("study_level", "3rd Year BOT"),
            "target_university": self.data.get("target_university", "TNMGRU"),
            "accuracy_percent": acc,
            "overall_mastery": avg_mastery,
            "stats": stats,
            "subject_mastery": subjs,
            "weak_areas": self.data.get("weak_areas", [])[:6],
            "revision_queue": self.data.get("revision_queue", [])[:5],
            "recurring_mistakes": self.data.get("recurring_mistakes", [])[:5],
            "recent_activities": self.data.get("recent_activities", [])[:8]
        }
