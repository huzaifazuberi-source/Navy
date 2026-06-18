# ============================================================
# config.py
# All settings in one simple place.
# ------------------------------------------------------------
# Beginner note:
# We read values from "environment variables" if they exist,
# otherwise we use the default values written here.
# Replace the Supabase values below with your own.
# ============================================================

import os

# ---- Flask secret key (used to keep login sessions safe) ----
# In a real project keep this secret. For the academic project,
# any long random text works.
SECRET_KEY = os.environ.get("SECRET_KEY", "sb_secret_RQ6VPHrLFoBUudZzBLs0Kg_yfjpDCXB")


# ---- Supabase PostgreSQL connection details ----
# Find these in Supabase:  Project Settings -> Database -> Connection info
DB_HOST     = os.environ.get("DB_HOST", "aws-1-ap-south-1.pooler.supabase.com")  # your host
DB_PORT     = os.environ.get("DB_PORT", "5432")                        # usually 5432
DB_NAME     = os.environ.get("DB_NAME", "postgres")                    # usually 'postgres'
DB_USER     = os.environ.get("DB_USER", "postgres.vhkcuydaynhecbvadlkf")                    # your db user
DB_PASSWORD = os.environ.get("DB_PASSWORD", "wasifabbasrizvi")  # your db password


# ---- Path to the trained machine learning model ----
# This points to the file saved by the training notebook.
MODEL_PATH = os.environ.get(
    "MODEL_PATH",
    os.path.join(os.path.dirname(__file__), "..", "model", "best_model.pkl")
)
