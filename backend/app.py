# ============================================================
# app.py
# The main Flask application.
# Handles: pages, registration, login, logout, sessions,
#          prediction, saving, and prediction history.
# ------------------------------------------------------------
# Run with:  python app.py
# Then open: http://127.0.0.1:5000
# ============================================================

from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash, jsonify
)
import os
import json

import config
import auth
import database
import model_utils


# ---- Create the Flask app ----
# We point Flask to the frontend folder for templates and static files.
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)
app.secret_key = config.SECRET_KEY


# ------------------------------------------------------------
# SMALL HELPER: check if a user is logged in
# ------------------------------------------------------------
def is_logged_in():
    return "user_id" in session


# ------------------------------------------------------------
# HOME PAGE  (public landing page)
# ------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html", logged_in=is_logged_in())


# ------------------------------------------------------------
# ABOUT PAGE  (public)
# ------------------------------------------------------------
@app.route("/about")
def about():
    return render_template("about.html", logged_in=is_logged_in())


# ------------------------------------------------------------
# REGISTRATION
# ------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")

        success, message = auth.register_user(full_name, email, password)
        flash(message)
        if success:
            return redirect(url_for("login"))

    return render_template("register.html")


# ------------------------------------------------------------
# LOGIN  (starts the session)
# ------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        success, message, user = auth.login_user(email, password)
        if success:
            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]
            return redirect(url_for("dashboard"))
        else:
            flash(message)

    return render_template("login.html")


# ------------------------------------------------------------
# LOGOUT  (ends the session)
# ------------------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


# ------------------------------------------------------------
# DASHBOARD  (welcome + statistics + history)
# ------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))

    records = database.get_user_predictions(session["user_id"])

    # Simple statistics calculated from the user's records.
    total = len(records)
    eligible = sum(1 for r in records if r["predicted_status"] == "Eligible")
    not_eligible = total - eligible
    if total > 0:
        avg_elig = round(
            sum(float(r["eligibility_percentage"]) for r in records) / total, 1
        )
    else:
        avg_elig = 0

    stats = {
        "total": total,
        "eligible": eligible,
        "not_eligible": not_eligible,
        "avg_eligibility": avg_elig,
    }

    return render_template(
        "dashboard.html",
        user_name=session.get("user_name"),
        stats=stats,
        records=records,
    )


# ------------------------------------------------------------
# CANDIDATE FORM PAGE
# ------------------------------------------------------------
@app.route("/form")
def candidate_form():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("candidate_form.html", user_name=session.get("user_name"))


# ------------------------------------------------------------
# PREDICTION RESULT PAGE  (the page that shows the report)
# The JavaScript on this page reads the saved result and shows it.
# ------------------------------------------------------------
@app.route("/prediction")
def prediction():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("prediction.html", user_name=session.get("user_name"))


# ------------------------------------------------------------
# PREDICT  (receives form data, runs model, saves result)
# Returns the report as JSON for the frontend to display.
# ------------------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    if not is_logged_in():
        return jsonify({"error": "Please log in first."}), 401

    form = request.get_json()

    try:
        data = {
            "candidate_id": form.get("candidate_id", ""),
            "age": int(form["age"]),
            "gender": form["gender"],
            "height_cm": float(form["height_cm"]),
            "weight_kg": float(form["weight_kg"]),
            "matric_percentage": float(form["matric_percentage"]),
            "inter_percentage": float(form["inter_percentage"]),
            "cgpa": float(form["cgpa"]),
            "physical_fitness_score": int(form["physical_fitness_score"]),
            "medical_status": form["medical_status"],
            "marital_status": form["marital_status"],
            "city": form["city"],
            "computer_skills": form["computer_skills"],
            "leadership_score": int(form["leadership_score"]),
            "communication_score": int(form["communication_score"]),
            "branch_preference": form["branch_preference"],
        }
    except (KeyError, ValueError):
        return jsonify({"error": "Please fill all fields correctly."}), 400

    result = model_utils.predict(data)

    database.save_prediction(session["user_id"], data, result)

    return jsonify(result)


# ------------------------------------------------------------
# ALGORITHM COMPARISON PAGE
# Reads the saved metrics (model_results.json) and shows them.
# ------------------------------------------------------------
@app.route("/comparison")
def comparison():
    if not is_logged_in():
        return redirect(url_for("login"))

    # Build the path to the results file saved by the training notebook.
    results_path = os.path.join(
        os.path.dirname(__file__), "..", "model", "model_results.json"
    )

    # Try to read it. If it is missing, show an empty page with a note.
    try:
        with open(results_path) as f:
            data = json.load(f)
    except FileNotFoundError:
        data = None

    return render_template(
        "comparison.html",
        data=data,
        user_name=session.get("user_name"),
    )


# ------------------------------------------------------------
# START THE APP
# ------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
