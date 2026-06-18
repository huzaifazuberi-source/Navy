# Pakistan Navy Recruitment Eligibility Predictor

An academic project that predicts Pakistan Navy recruitment eligibility using
machine learning. Stack: **HTML, CSS, JavaScript, Flask, PostgreSQL (Supabase),
Scikit-Learn**.

## Folder structure
```
navy_predictor/
├── database.sql              # Supabase tables (run once in SQL Editor)
├── requirements.txt          # Python libraries
├── data/navy_dataset.csv     # Dataset
├── notebook/                 # Jupyter notebooks (training + evaluation)
├── model/best_model.pkl      # Trained model (already created)
├── backend/                  # Flask app (config, database, auth, model, app)
└── frontend/
    ├── templates/            # HTML pages
    └── static/               # css, js, assets/images/logo.png
```

## How to run

1. **Install libraries**
   ```
   pip install -r requirements.txt
   ```

2. **Create the database**
   - Open Supabase → SQL Editor → paste `database.sql` → Run.

3. **Add your database details**
   - Open `backend/config.py` and fill in your Supabase host, password, etc.

4. **(Optional) Re-train the model**
   - Open `notebook/model_training.ipynb` and run all cells.
   - Then `notebook/model_evaluation.ipynb` for the scores.
   - This is already done — `model/best_model.pkl` exists.

5. **Start the website**
   ```
   cd backend
   python app.py
   ```
   Open http://127.0.0.1:5000

## Pages
- `/`            Home (public)
- `/about`       About (public)
- `/register`    Create account
- `/login`       Login
- `/dashboard`   Welcome + statistics + prediction history
- `/form`        Candidate input form
- `/prediction`  Detailed eligibility report

## Note
Replace `frontend/static/assets/images/logo.png` with the real Pakistan Navy
logo. This is a guidance tool only and does not replace the official Pakistan
Navy selection process.
"# Navy" 
