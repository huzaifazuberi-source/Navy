def save_prediction(user_id, data, result):
    """Save one prediction row.
    'data'   = the candidate input (a dictionary)
    'result' = the prediction output (a dictionary)
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Raw parameter values array
    raw_values = [
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
    ]
    
    # Clean values: Converts any numpy types (np.int64, np.float64) to native Python types (int, float)
    clean_values = tuple(
        v.item() if hasattr(v, "item") and not isinstance(v, (str, bytes)) else v 
        for v in raw_values
    )

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
        clean_values,
    )
    
    conn.commit()
    cur.close()
    conn.close()
