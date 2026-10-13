"""
syllabus_mgr.py - MGRU Occupational Therapy Syllabus Manager
Organises learning strictly by: Subject -> Unit -> Topic -> Subtopic.
Aligned with The Tamil Nadu Dr. M.G.R. Medical University (TNMGRU) B.O.T Curriculum.
"""

from typing import Dict, List, Optional, Any

MGRU_OT_SYLLABUS: Dict[str, Any] = {
    "subjects": [
        {
            "id": "neurology",
            "name": "Occupational Therapy in Neurology",
            "short_name": "Neurology",
            "description": "Assessment, clinical reasoning, and neuro-rehabilitation for central and peripheral nervous system disorders.",
            "units": [
                {
                    "unit_id": "neuro_u1",
                    "unit_name": "Unit 1: Stroke Rehabilitation (CVA)",
                    "topics": [
                        {
                            "topic_id": "cva_assessment",
                            "title": "Clinical Presentation & OT Evaluation in Stroke",
                            "subtopics": [
                                "MCA, ACA, PCA, Vertebrobasilar vascular syndromes",
                                "Motor assessment: Fugl-Meyer Assessment (FMA), Brunnstrom Stages of Motor Recovery",
                                "Sensory, perceptual and cognitive deficits (Unilateral neglect, Agnosia, Apraxia)",
                                "Upper extremity dysfunction and subluxation evaluation"
                            ],
                            "key_terms": ["Brunnstrom stages", "Fugl-Meyer", "Hemi-inattention", "Pusher syndrome", "Glenohumeral subluxation"]
                        },
                        {
                            "topic_id": "cva_intervention",
                            "title": "Evidence-Based OT Interventions in Stroke",
                            "subtopics": [
                                "Constraint-Induced Movement Therapy (CIMT) protocols & criteria",
                                "Task-Oriented Training and Bilateral Arm Training",
                                "Mirror Therapy and Mental Imagery",
                                "NDT (Bobath approach) vs Motor Relearning Programme (Carr & Shepherd)",
                                "Management of spasticity and shoulder-hand syndrome (CRPS Type 1)"
                            ],
                            "key_terms": ["CIMT", "Mirror therapy", "Task-oriented approach", "Shoulder strapping", "Tone inhibition"]
                        }
                    ]
                },
                {
                    "unit_id": "neuro_u2",
                    "unit_name": "Unit 2: Traumatic Brain Injury (TBI)",
                    "topics": [
                        {
                            "topic_id": "tbi_assessment",
                            "title": "TBI Levels, Prognosis & Cognitive Evaluation",
                            "subtopics": [
                                "Glasgow Coma Scale (GCS) and Rancho Los Amigos Levels of Cognitive Functioning (RLAS I-X)",
                                "Executive dysfunction, memory, attention and agitation management",
                                "Post-concussion syndrome and return-to-work evaluation"
                            ],
                            "key_terms": ["RLAS scale", "GCS", "Amnesia", "Executive function", "Coma stimulation"]
                        },
                        {
                            "topic_id": "tbi_intervention",
                            "title": "OT Management Across RLAS Stages",
                            "subtopics": [
                                "Sensory stimulation protocols for low-level TBI (RLAS I-III)",
                                "Behavioral and environmental modification for agitated states (RLAS IV)",
                                "Cognitive retraining, errorless learning, and compensatory memory aids (RLAS V-VIII)"
                            ],
                            "key_terms": ["Sensory stimulation", "Errorless learning", "Cognitive orthotics", "Social reintegration"]
                        }
                    ]
                },
                {
                    "unit_id": "neuro_u3",
                    "unit_name": "Unit 3: Spinal Cord Injury (SCI)",
                    "topics": [
                        {
                            "topic_id": "sci_management",
                            "title": "Functional Outcomes by Spinal Level & OT Rehabilitation",
                            "subtopics": [
                                "ASIA Impairment Scale (A-E) and neurological level determination",
                                "Functional capabilities from C1-C4, C5, C6 (Tenodesis grasp), C7-C8, T1-T12, Lumbar",
                                "Autonomic Dysreflexia: Emergency protocol and clinical recognition",
                                "Wheelchair seating, pressure relief, transfers, and environmental control units (ECU)"
                            ],
                            "key_terms": ["Tenodesis grip", "Autonomic dysreflexia", "ASIA scale", "Pressure relief", "Wheelchair mobility"]
                        }
                    ]
                },
                {
                    "unit_id": "neuro_u4",
                    "unit_name": "Unit 4: Movement Disorders & Progressive Conditions",
                    "topics": [
                        {
                            "topic_id": "parkinsons_ms_gbs",
                            "title": "Parkinson's Disease, Multiple Sclerosis & Guillain-Barré Syndrome",
                            "subtopics": [
                                "Parkinson's: Hoehn & Yahr staging, auditory/visual cueing for gait and freezing, micrographia",
                                "Multiple Sclerosis: Fatigue management, energy conservation techniques, cooling strategies",
                                "Guillain-Barré Syndrome: Acute phase positioning, PROM, gentle functional reconditioning"
                            ],
                            "key_terms": ["Hoehn and Yahr", "External cueing", "Energy conservation", "Fatigue severity scale", "GBS acute care"]
                        }
                    ]
                }
            ]
        },
        {
            "id": "orthopaedics",
            "name": "Occupational Therapy in Orthopaedics & Hand Rehabilitation",
            "short_name": "Orthopaedics & Hand",
            "description": "Musculoskeletal conditions, hand injuries, peripheral nerve lesions, splinting, and joint protection.",
            "units": [
                {
                    "unit_id": "ortho_u1",
                    "unit_name": "Unit 1: Peripheral Nerve Injuries (PNI)",
                    "topics": [
                        {
                            "topic_id": "radial_nerve",
                            "title": "Radial Nerve Palsy (Wrist Drop)",
                            "subtopics": [
                                "Level of lesion (High: crutch palsy/spiral groove; Low: PIN)",
                                "Motor loss (Wrist, thumb, finger extensors) and sensory loss over first web space",
                                "Splinting: Dynamic extensor splint, static wrist cock-up with tenodesis assist",
                                "Sensory re-education and functional hand training"
                            ],
                            "key_terms": ["Wrist drop", "Dynamic extensor splint", "High vs low lesion", "Extensor digitorum communis"]
                        },
                        {
                            "topic_id": "median_nerve",
                            "title": "Median Nerve Palsy (Ape Hand & Hand of Benediction)",
                            "subtopics": [
                                "High lesion (Benediction sign on making fist) vs Low lesion (Carpal tunnel, Ape thumb deformity)",
                                "Loss of thenar opposition, precision grip, and median sensory distribution",
                                "Splinting: Short opponens / C-bar splint, resting wrist splint",
                                "Sensory re-education protocols (Dellon protocol)"
                            ],
                            "key_terms": ["Ape hand", "Opponens splint", "Carpal tunnel syndrome", "Phalen test", "Tinel sign"]
                        },
                        {
                            "topic_id": "ulnar_nerve",
                            "title": "Ulnar Nerve Palsy (Claw Hand)",
                            "subtopics": [
                                "High lesion (Cubital tunnel) vs Low lesion (Guyon's canal - Ulnar paradox)",
                                "Lumbrical paralysis (4th and 5th digits hyperextension at MCP, flexion at IP)",
                                "Splinting: Knuckle bender / Lumbrical bar splint (prevents MCP hyperextension)",
                                "Froment's sign and intrinsic muscle re-education"
                            ],
                            "key_terms": ["Claw hand", "Ulnar paradox", "Knuckle bender splint", "Froment's sign", "First dorsal interosseous"]
                        },
                        {
                            "topic_id": "brachial_plexus",
                            "title": "Brachial Plexus Injuries (Erb's and Klumpke's)",
                            "subtopics": [
                                "Erb-Duchenne palsy (C5-C6 upper trunk): Policeman's tip hand, aeroplane splint",
                                "Klumpke's palsy (C8-T1 lower trunk): True claw hand, Horner's syndrome",
                                "Total plexus avulsion and reconstructive surgical rehabilitation"
                            ],
                            "key_terms": ["Policeman tip deformity", "Erb's palsy", "Klumpke's palsy", "Aeroplane splint"]
                        }
                    ]
                },
                {
                    "unit_id": "ortho_u2",
                    "unit_name": "Unit 2: Tendon Injuries & Hand Conditions",
                    "topics": [
                        {
                            "topic_id": "flexor_extensor_tendons",
                            "title": "Flexor and Extensor Tendon Rehabilitation Protocols",
                            "subtopics": [
                                "Flexor tendon Zones I-V (Zone II 'No Man's Land')",
                                "Rehabilitation protocols: Kleinert (dynamic traction), Duran (passive motion), Early Active Motion",
                                "Dorsal blocking splint design and mechanical angles",
                                "Extensor tendon Zones I-VIII: Mallet finger (stax splint), Boutonnière, Swan neck"
                            ],
                            "key_terms": ["No man's land", "Kleinert protocol", "Duran protocol", "Dorsal blocking splint", "Boutonniere"]
                        },
                        {
                            "topic_id": "cumulative_trauma",
                            "title": "Repetitive Strain Injuries & Hand Pathologies",
                            "subtopics": [
                                "De Quervain's Tenosynovitis: Finkelstein's test, Long thumb spica splint",
                                "Trigger finger / Tenosynovitis: Ring splinting, tendon gliding exercises",
                                "Dupuytren's Contracture: Palmar fasciectomy rehabilitation, night extension splinting"
                            ],
                            "key_terms": ["De Quervain's", "Thumb spica", "Finkelstein test", "Dupuytren's contracture", "Tendon gliding"]
                        }
                    ]
                },
                {
                    "unit_id": "ortho_u3",
                    "unit_name": "Unit 3: Arthritis, Amputations & Burns",
                    "topics": [
                        {
                            "topic_id": "arthritis_joint_protection",
                            "title": "Rheumatoid Arthritis & Osteoarthritis",
                            "subtopics": [
                                "Deformities: Ulnar drift, Swan neck, Boutonnière, Heberden's & Bouchard's nodes",
                                "Joint Protection Principles (10 golden rules) and Energy Conservation",
                                "Assistive devices: Built-up handles, long-handled reachers, tap turners, jar openers"
                            ],
                            "key_terms": ["Joint protection", "Ulnar drift", "Energy conservation", "Adaptive devices", "Morning stiffness"]
                        },
                        {
                            "topic_id": "burns_rehab",
                            "title": "Burn Rehabilitation & Anti-Deformity Positioning",
                            "subtopics": [
                                "Burn stages: Emergent, Acute, Rehabilitation",
                                "Anti-deformity positioning for neck, axilla (90 deg abduction), elbow, hand (Intrinsic plus position)",
                                "Pressure garments (Jobst garments), scar massage, silicone gel sheets"
                            ],
                            "key_terms": ["Intrinsic plus splint", "Anti-deformity position", "Hypertrophic scar", "Pressure garment"]
                        },
                        {
                            "topic_id": "amputation_prosthetics",
                            "title": "Upper and Lower Limb Amputations",
                            "subtopics": [
                                "Pre-prosthetic training: Residual limb shaping (figure-of-8 bandaging), desensitization",
                                "Prosthetic checkout and training: Body-powered vs Myoelectric prostheses",
                                "Phantom limb pain management (Mirror box therapy)"
                            ],
                            "key_terms": ["Figure-of-8 wrapping", "Phantom limb", "Myoelectric prosthesis", "Terminal device"]
                        }
                    ]
                }
            ]
        },
        {
            "id": "paediatrics",
            "name": "Occupational Therapy in Paediatrics & Developmental Disabilities",
            "short_name": "Paediatrics",
            "description": "Sensory integration, neurodevelopmental therapy, developmental delays, ASD, ADHD, and CP.",
            "units": [
                {
                    "unit_id": "paed_u1",
                    "unit_name": "Unit 1: Cerebral Palsy (CP)",
                    "topics": [
                        {
                            "topic_id": "cp_management",
                            "title": "Classification, Assessment & OT Interventions in CP",
                            "subtopics": [
                                "Topographical (Hemiplegia, Diplegia, Quadriplegia) & Physiological (Spastic, Dyskinetic, Ataxic)",
                                "Gross Motor Function Classification System (GMFCS I-V) & MACS (Manual Ability Classification)",
                                "NDT (Bobath) key points of control: Head, shoulder girdle, pelvic girdle",
                                "Adaptive seating, feeding therapy, hand function training, and orthotic management"
                            ],
                            "key_terms": ["GMFCS", "MACS", "Key points of control", "Spastic diplegia", "Reflex inhibiting posture"]
                        }
                    ]
                },
                {
                    "unit_id": "paed_u2",
                    "unit_name": "Unit 2: Ayres Sensory Integration (ASI) & Sensory Processing",
                    "topics": [
                        {
                            "topic_id": "sensory_integration",
                            "title": "Sensory Systems, Modulation & Dyspraxia",
                            "subtopics": [
                                "Sensory modulation disorders: Hyper-responsiveness, Hypo-responsiveness, Sensory seeking",
                                "Vestibular, Proprioceptive, and Tactile systems in occupational performance",
                                "Sensory Diet formulation (Wilbarger brushing, heavy work activities, calming strategies)",
                                "Praxis and Dyspraxia (Ideation, Motor planning, Execution)"
                            ],
                            "key_terms": ["Ayres Sensory Integration", "Sensory diet", "Proprioception", "Tactile defensiveness", "Dyspraxia"]
                        }
                    ]
                },
                {
                    "unit_id": "paed_u3",
                    "unit_name": "Unit 3: Autism Spectrum Disorder (ASD) & ADHD",
                    "topics": [
                        {
                            "topic_id": "neurodevelopmental_disorders",
                            "title": "ASD, ADHD, and Developmental Coordination Disorder (DCD)",
                            "subtopics": [
                                "ASD: Structured teaching (TEACCH principles), Social Stories, PECS, visual schedules",
                                "ADHD: Sensory-motor strategies for attention, classroom ergonomics, behavioral modification",
                                "Handwriting evaluation and intervention: Pencil grasp development, visual-motor integration (Beery VMI)"
                            ],
                            "key_terms": ["TEACCH", "Social stories", "Sensory breaks", "Dynamic tripod grasp", "Beery VMI"]
                        }
                    ]
                }
            ]
        },
        {
            "id": "psychiatry",
            "name": "Occupational Therapy in Psychiatry & Mental Health",
            "short_name": "Psychiatry",
            "description": "Psychosocial rehabilitation, occupational performance in psychiatric disorders, group dynamics.",
            "units": [
                {
                    "unit_id": "psych_u1",
                    "unit_name": "Unit 1: Psychosocial Rehabilitation & Group Therapy",
                    "topics": [
                        {
                            "topic_id": "group_dynamics",
                            "title": "Mosey's Developmental Groups & Therapeutic Use of Self",
                            "subtopics": [
                                "Mosey's 5 group levels: Parallel, Project, Egocentric-Cooperative, Cooperative, Mature",
                                "Therapeutic Use of Self: Empathy, boundaries, active listening, managing resistance",
                                "Social skills training (SST), assertiveness training, anger and stress management"
                            ],
                            "key_terms": ["Mosey's groups", "Parallel group", "Therapeutic use of self", "Social skills training"]
                        }
                    ]
                },
                {
                    "unit_id": "psych_u2",
                    "unit_name": "Unit 2: Psychiatric Conditions & OT Management",
                    "topics": [
                        {
                            "topic_id": "clinical_psychiatry",
                            "title": "Schizophrenia, Mood Disorders & Anxiety Disorders",
                            "subtopics": [
                                "Schizophrenia: Negative symptoms (avolition, anhedonia), vocational training, daily routine structuring",
                                "Depression & Bipolar: Graded mastery activities, expressive arts, suicide prevention safeguards",
                                "Anxiety & OCD: Progressive muscle relaxation (Jacobson's), systematic desensitization, grounding exercises"
                            ],
                            "key_terms": ["Avolition", "Graded activity", "Allen Cognitive Levels (ACL)", "Jacobson relaxation", "Vocational rehabilitation"]
                        }
                    ]
                }
            ]
        },
        {
            "id": "foundations_models",
            "name": "OT Models, Frames of Reference & Clinical Reasoning",
            "short_name": "Models & Reasoning",
            "description": "Theoretical foundations, models of practice, frames of reference, activity analysis, and reasoning pathway.",
            "units": [
                {
                    "unit_id": "model_u1",
                    "unit_name": "Unit 1: OT Models of Practice",
                    "topics": [
                        {
                            "topic_id": "moho_peo_kawa",
                            "title": "MOHO, PEO, PEOP & Kawa River Model",
                            "subtopics": [
                                "Model of Human Occupation (MOHO): Volition, Habituation, Performance Capacity, Environment",
                                "Person-Environment-Occupation (PEO): Occupational fit, transaction between dimensions",
                                "Kawa (River) Model: Mizu (Life flow), Iwa (Obstacles), Ryuboku (Personal assets), Torimaki (Environment)",
                                "Canadian Model of Occupational Performance and Engagement (CMOP-E & COPM)"
                            ],
                            "key_terms": ["MOHO", "Volition", "Habituation", "PEO model", "Kawa model", "COPM"]
                        }
                    ]
                },
                {
                    "unit_id": "model_u2",
                    "unit_name": "Unit 2: Frames of Reference (FoR) & Approaches",
                    "topics": [
                        {
                            "topic_id": "frames_of_reference",
                            "title": "Biomechanical, Rehabilitative, NDT, Motor Learning & Cognitive FoR",
                            "subtopics": [
                                "Biomechanical: Range of motion, muscle strength, endurance, ergonomics",
                                "Rehabilitative / Compensatory: Adaptive equipment, environmental modification, energy conservation",
                                "Neurodevelopmental (NDT / Bobath): Postural control, normal movement patterns, handling techniques",
                                "Motor Learning / MRP: Task-specific practice, feedback schedules, environmental context"
                            ],
                            "key_terms": ["Biomechanical FoR", "Rehabilitative FoR", "NDT Bobath", "Motor learning", "Compensatory approach"]
                        }
                    ]
                },
                {
                    "unit_id": "model_u3",
                    "unit_name": "Unit 3: Activity Analysis & The OT Reasoning Pathway",
                    "topics": [
                        {
                            "topic_id": "ot_reasoning_spine",
                            "title": "The MGRU OT Clinical Reasoning Pathway",
                            "subtopics": [
                                "The 8-step Clinical Reasoning Sequence: Condition -> Impairment -> Activity Limitation -> Participation/Occupational Performance Problem -> Assessment -> Goals (SMART) -> Intervention -> Clinical Justification",
                                "Activity Analysis: Grading (up/down) vs Adapting (materials, environment)",
                                "Types of Clinical Reasoning: Procedural, Interactive, Conditional, Narrative, Pragmatic, Ethical"
                            ],
                            "key_terms": ["Clinical reasoning pathway", "Activity grading", "Activity adapting", "Procedural reasoning", "Interactive reasoning"]
                        }
                    ]
                }
            ]
        },
        {
            "id": "community_general",
            "name": "General Medicine, Community OT & Ergonomics",
            "short_name": "Community & Ergonomics",
            "description": "Cardiopulmonary rehabilitation, Community-Based Rehabilitation (CBR), Geriatrics, and Work Hardening.",
            "units": [
                {
                    "unit_id": "comm_u1",
                    "unit_name": "Unit 1: Cardiopulmonary & Geriatric OT",
                    "topics": [
                        {
                            "topic_id": "cardiac_geriatric",
                            "title": "Cardiac Rehabilitation, MET Levels & Fall Prevention",
                            "subtopics": [
                                "Cardiac Rehab Phase I-III, MET (Metabolic Equivalent of Task) levels for ADLs, sternal precautions",
                                "Borg Rating of Perceived Exertion (RPE), dyspnea management, pursed-lip breathing",
                                "Geriatric fall risk assessment, home safety checklist, architectural barrier removal"
                            ],
                            "key_terms": ["MET levels", "Sternal precautions", "Borg RPE", "Fall prevention", "Home modification"]
                        }
                    ]
                },
                {
                    "unit_id": "comm_u2",
                    "unit_name": "Unit 2: Community-Based Rehabilitation (CBR) & Ergonomics",
                    "topics": [
                        {
                            "topic_id": "cbr_ergonomics",
                            "title": "CBR Matrix, Work Hardening & Cumulative Trauma Prevention",
                            "subtopics": [
                                "WHO CBR Matrix: Health, Education, Livelihood, Social, Empowerment components",
                                "Work Hardening vs Work Conditioning programs, Job site analysis",
                                "Computer workstation ergonomics: 90-90-90 posture, monitor height, wrist rests"
                            ],
                            "key_terms": ["CBR matrix", "Work hardening", "Job site analysis", "Ergonomic redesign", "Cumulative trauma"]
                        }
                    ]
                }
            ]
        }
    ]
}


class SyllabusManager:
    """Helper class to query, browse, and validate syllabus topics."""

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self.data = data or MGRU_OT_SYLLABUS

    def get_all_subjects(self) -> List[Dict[str, Any]]:
        """Returns list of all subjects with basic info."""
        return [
            {
                "id": s["id"],
                "name": s["name"],
                "short_name": s["short_name"],
                "description": s["description"],
                "units_count": len(s.get("units", []))
            }
            for s in self.data["subjects"]
        ]

    def get_subject(self, subject_id: str) -> Optional[Dict[str, Any]]:
        """Finds subject by ID."""
        for s in self.data["subjects"]:
            if s["id"] == subject_id:
                return s
        return None

    def get_topic(self, topic_id: str) -> Optional[Dict[str, Any]]:
        """Finds topic by ID across all subjects and units."""
        for s in self.data["subjects"]:
            for u in s.get("units", []):
                for t in u.get("topics", []):
                    if t["topic_id"] == topic_id:
                        return {
                            **t,
                            "subject_id": s["id"],
                            "subject_name": s["name"],
                            "unit_id": u["unit_id"],
                            "unit_name": u["unit_name"]
                        }
        return None

    def find_topics_by_keyword(self, query: str) -> List[Dict[str, Any]]:
        """Searches topics, subtopics, and key terms by keyword."""
        q = query.lower().strip()
        results = []
        for s in self.data["subjects"]:
            for u in s.get("units", []):
                for t in u.get("topics", []):
                    match_score = 0
                    if q in t["title"].lower():
                        match_score += 10
                    for sub in t.get("subtopics", []):
                        if q in sub.lower():
                            match_score += 5
                    for term in t.get("key_terms", []):
                        if q in term.lower():
                            match_score += 8
                    
                    if match_score > 0:
                        results.append({
                            "subject_id": s["id"],
                            "subject_name": s["name"],
                            "unit_id": u["unit_id"],
                            "unit_name": u["unit_name"],
                            "topic_id": t["topic_id"],
                            "title": t["title"],
                            "subtopics": t.get("subtopics", []),
                            "key_terms": t.get("key_terms", []),
                            "score": match_score
                        })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def get_full_tree(self) -> List[Dict[str, Any]]:
        """Returns the full hierarchical syllabus tree for frontend sidebar rendering."""
        return self.data["subjects"]
