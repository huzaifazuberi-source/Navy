-- ============================================================
-- Pakistan Navy Recruitment Eligibility Predictor
-- Database Schema  (PostgreSQL / Supabase)
-- ------------------------------------------------------------
-- HOW TO USE:
-- 1. Open your Supabase project.
-- 2. Go to the "SQL Editor".
-- 3. Paste this whole file and click "Run".
-- This creates two tables: users and predictions.
-- ============================================================


-- ------------------------------------------------------------
-- TABLE 1: users
-- Stores the people who can log in (candidates / admin).
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,                 -- unique id for each user (auto number)
    full_name     VARCHAR(100) NOT NULL,              -- user's full name
    email         VARCHAR(120) UNIQUE NOT NULL,       -- email used to log in (must be unique)
    password      VARCHAR(255) NOT NULL,              -- hashed password (never store plain text)
    created_at    TIMESTAMP DEFAULT NOW()             -- when the account was created
);


-- ------------------------------------------------------------
-- TABLE 2: predictions
-- Stores every prediction made, linked to the user who made it.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS predictions (
    id                       SERIAL PRIMARY KEY,       -- unique id for each prediction
    user_id                  INTEGER NOT NULL,         -- which user made this prediction (FOREIGN KEY)

    -- ---- Candidate input data ----
    candidate_id             VARCHAR(20),
    age                      INTEGER  NOT NULL CHECK (age BETWEEN 15 AND 40),
    gender                   VARCHAR(10)  NOT NULL CHECK (gender IN ('Male', 'Female')),
    height_cm                NUMERIC(5,1) NOT NULL CHECK (height_cm BETWEEN 100 AND 230),
    weight_kg                NUMERIC(5,1) NOT NULL CHECK (weight_kg BETWEEN 30 AND 200),
    matric_percentage        NUMERIC(5,2) NOT NULL CHECK (matric_percentage BETWEEN 0 AND 100),
    inter_percentage         NUMERIC(5,2) NOT NULL CHECK (inter_percentage BETWEEN 0 AND 100),
    cgpa                     NUMERIC(4,2) NOT NULL CHECK (cgpa BETWEEN 0 AND 4),
    physical_fitness_score   INTEGER  NOT NULL CHECK (physical_fitness_score BETWEEN 0 AND 100),
    medical_status           VARCHAR(10)  NOT NULL CHECK (medical_status IN ('Fit', 'Unfit')),
    marital_status           VARCHAR(10)  NOT NULL CHECK (marital_status IN ('Single', 'Married')),
    city                     VARCHAR(50)  NOT NULL,
    computer_skills          VARCHAR(20)  NOT NULL CHECK (computer_skills IN ('Beginner', 'Intermediate', 'Advanced')),
    leadership_score         INTEGER  NOT NULL CHECK (leadership_score BETWEEN 0 AND 100),
    communication_score      INTEGER  NOT NULL CHECK (communication_score BETWEEN 0 AND 100),
    branch_preference        VARCHAR(50)  NOT NULL,

    -- ---- Prediction result data ----
    predicted_status         VARCHAR(20)  NOT NULL,    -- "Eligible" or "Not Eligible"
    eligibility_percentage   NUMERIC(5,2) NOT NULL,    -- chance of being eligible (0-100)
    confidence_percentage    NUMERIC(5,2) NOT NULL,    -- model confidence (0-100)
    recommended_branches     TEXT,                     -- suggested branches (comma separated)

    created_at               TIMESTAMP DEFAULT NOW(),  -- when this prediction was saved

    -- ---- Relationship ----
    -- Link each prediction to a user. If a user is deleted,
    -- their predictions are deleted too (ON DELETE CASCADE).
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users (id)
        ON DELETE CASCADE
);


-- ------------------------------------------------------------
-- Helpful index so loading a user's history is fast.
-- ------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON predictions (user_id);
