# ============================================================
# model_utils.py
# Loads the trained model and turns candidate input into a
# full report: status, percentages, branches, strengths,
# weaknesses, and suggestions.
# ------------------------------------------------------------
# The model file (best_model.pkl) is a Scikit-Learn Pipeline
# that already handles encoding + scaling, so we just give it
# a normal table of values and it does the rest.
# ============================================================

import joblib
import pandas as pd

import config


# The exact feature columns the model was trained on (order matters).
FEATURE_COLUMNS = [
    "age", "gender", "height_cm", "weight_kg",
    "matric_percentage", "inter_percentage", "cgpa",
    "physical_fitness_score", "medical_status", "marital_status",
    "city", "computer_skills", "leadership_score",
    "communication_score", "branch_preference",
]

# Load the trained model ONCE when this file is first imported.
model = joblib.load(config.MODEL_PATH)


def prepare_input(data):
    """Turn the input dictionary into a one-row DataFrame
    with the columns in the order the model expects."""
    row = {col: data[col] for col in FEATURE_COLUMNS}
    return pd.DataFrame([row])


def predict(data):
    """Run the model and build the full report.
    'data' is a dictionary of the candidate's input values.
    Returns a dictionary with all report fields.
    """
    input_df = prepare_input(data)

    # Predicted class: "Eligible" or "Not Eligible"
    predicted_status = model.predict(input_df)[0]

    # Probabilities for each class.
    probabilities = model.predict_proba(input_df)[0]
    classes = list(model.classes_)

    # Eligibility % = probability of the "Eligible" class.
    if "Eligible" in classes:
        eligible_index = classes.index("Eligible")
        eligibility_percentage = round(probabilities[eligible_index] * 100, 2)
    else:
        eligibility_percentage = 0.0

    # Confidence % = the highest probability among the classes.
    confidence_percentage = round(max(probabilities) * 100, 2)

    # Build the explanation parts using simple rules.
    strengths = find_strengths(data)
    weaknesses = find_weaknesses(data)
    suggestions = make_suggestions(weaknesses)
    recommended_branches = recommend_branches(data, predicted_status)

    return {
        "predicted_status": predicted_status,
        "eligibility_percentage": eligibility_percentage,
        "confidence_percentage": confidence_percentage,
        "recommended_branches": recommended_branches,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
    }


# ------------------------------------------------------------
# SIMPLE RULE-BASED HELPERS (easy to read and explain)
# ------------------------------------------------------------
def find_strengths(d):
    """List the things the candidate is doing well."""
    strengths = []
    if d["physical_fitness_score"] >= 70:
        strengths.append("Strong physical fitness score.")
    if d["leadership_score"] >= 70:
        strengths.append("Good leadership ability.")
    if d["communication_score"] >= 70:
        strengths.append("Strong communication skills.")
    if d["inter_percentage"] >= 70 or d["matric_percentage"] >= 70:
        strengths.append("Good academic record.")
    if d["medical_status"] == "Fit":
        strengths.append("Medically fit.")
    if d["computer_skills"] == "Advanced":
        strengths.append("Advanced computer skills.")
    if not strengths:
        strengths.append("Meets the basic entry information.")
    return strengths


def find_weaknesses(d):
    """List the weak areas that may lower eligibility."""
    weaknesses = []
    if d["physical_fitness_score"] < 50:
        weaknesses.append("Low physical fitness score.")
    if d["leadership_score"] < 50:
        weaknesses.append("Leadership score needs improvement.")
    if d["communication_score"] < 50:
        weaknesses.append("Communication skills need improvement.")
    if d["inter_percentage"] < 50 and d["matric_percentage"] < 50:
        weaknesses.append("Academic percentages are low.")
    if d["medical_status"] == "Unfit":
        weaknesses.append("Medical status is Unfit.")
    if d["computer_skills"] == "Beginner":
        weaknesses.append("Basic computer skills only.")
    return weaknesses


def make_suggestions(weaknesses):
    """Turn each weakness into friendly advice."""
    advice = []
    for w in weaknesses:
        if "fitness" in w:
            advice.append("Follow a regular fitness and running routine.")
        elif "Leadership" in w:
            advice.append("Take part in team activities to build leadership.")
        elif "Communication" in w:
            advice.append("Practice spoken and written communication daily.")
        elif "Academic" in w:
            advice.append("Improve academic results before applying.")
        elif "Unfit" in w:
            advice.append("Consult a doctor and work on medical fitness.")
        elif "computer" in w:
            advice.append("Take a basic computer/IT course.")
    if not advice:
        advice.append("Keep maintaining your strong profile.")
    return advice


def recommend_branches(d, predicted_status):
    """Recommend Navy branches using simple rules.
    Always keeps the candidate's own preference if it fits well.
    """
    branches = []

    # IT & Cyber: good computer skills.
    if d["computer_skills"] in ("Intermediate", "Advanced"):
        branches.append("IT & Cyber")

    # Combat / Naval Aviation: high fitness.
    if d["physical_fitness_score"] >= 65:
        branches.append("Combat")
        branches.append("Naval Aviation")

    # Marine Engineering: good academics.
    if d["inter_percentage"] >= 60 or d["cgpa"] >= 2.5:
        branches.append("Marine Engineering")

    # Logistics: good communication / leadership.
    if d["communication_score"] >= 60 or d["leadership_score"] >= 60:
        branches.append("Logistics")

    # Medical Corps: medically fit + decent academics.
    if d["medical_status"] == "Fit" and d["inter_percentage"] >= 60:
        branches.append("Medical Corps")

    # Always consider the candidate's stated preference.
    if d["branch_preference"] not in branches:
        branches.append(d["branch_preference"])

    # Remove duplicates while keeping order.
    seen = []
    for b in branches:
        if b not in seen:
            seen.append(b)

    # If not eligible, still show suggestions but keep the list short.
    return seen[:4]
