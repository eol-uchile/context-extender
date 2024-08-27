def calculate_grade(percent, approval_percent=60, max_grade=7, min_grade=1, pass_grade=4):
    # Normalize the percentage to a 0-1 scale
    normalized_percent = percent / 100    
    # Calculate the passing percentage point
    passing_point = approval_percent / 100
    
    if 0 <= normalized_percent <= passing_point:
        # Calculate the grade for percentages below the passing point
        grade = min_grade + (normalized_percent / passing_point) * (pass_grade - min_grade)
    else:
        # Calculate the grade for percentages above the passing point
        grade = pass_grade + ((normalized_percent - passing_point) / (1 - passing_point)) * (max_grade - pass_grade)
    return grade
