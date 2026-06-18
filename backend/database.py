# ============================================================
# database.py
# Simple functions to talk to the PostgreSQL (Supabase) database.
# We use psycopg2, which is a beginner-friendly PostgreSQL library.
# ------------------------------------------------------------
# Install once:  pip install psycopg2-binary
# ============================================================

import psycopg2
import psycopg2.extras  # lets us get rows as dictionaries (easy to read)

import config


def get_connection():
    """Open and return a new connection to the database."""
    connection = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
    )
    return connection


# ------------------------------------------------------------
# USER FUNCTIONS
# ------------------------------------------------------------
def create_user(full_name, email, hashed_password):
    """Insert a new user. Returns the new user's id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO users (full_name, email, password)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (full_name, email, hashed_password),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id


def get_user_by_email(email):
    """Find one user by email. Returns a dictionary or None."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


# ------------------------------------------------------------
# PREDICTION FUNCTIONS
# ------------------------------------------------------------
def save_prediction(user_id, data, result):
    """Save one prediction row.
    'data'   = the candidate input (a dictionary)
    'result' = the prediction output (a dictionary)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO predictions (
            user_id, candidate_id, age, gender, height_cm, weight_kg,
            matric_percentage, inter_percentage, cgpa, physical_fitness_score,
            medical_status, marital_status, city, computer_skills,
            leadership_score, communication_score, branch_preference,
            predicted_status, eligibility_percentage, confidence_percentage,
            recommended_branches
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            user_id,
            data.get("candidate_id"),
            data["age"],
            data["gender"],
            data["height_cm"],
            data["weight_kg"],
            data["matric_percentage"],
            data["inter_percentage"],
            data["cgpa"],
            data["physical_fitness_score"],
            data["medical_status"],
            data["marital_status"],
            data["city"],
            data["computer_skills"],
            data["leadership_score"],
            data["communication_score"],
            data["branch_preference"],
            result["predicted_status"],
            result["eligibility_percentage"],
            result["confidence_percentage"],
            ", ".join(result["recommended_branches"]),
        ),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_user_predictions(user_id):
    """Return all predictions made by one user (newest first)."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        """
        SELECT * FROM predictions
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
