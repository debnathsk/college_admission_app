# app/services.py

import re
import json
from datetime import datetime
import sqlite3
from typing import Dict
from .database import create_connection
from .exceptions import ValidationError, DatabaseError

def validate_input(data: Dict) -> None:
    """Validate input data using regular expressions."""
    if not re.match(r"^[A-Za-z\s]+$", data['name']):
        raise ValidationError("Name should only contain letters and spaces.")
    if not 17 <= data['age'] <= 25:
        raise ValidationError("Age should be between 17 and 25.")
    if data['gender'] not in ["Male", "Female", "Other"]:
        raise ValidationError("Gender should be one of 'Male', 'Female', or 'Other'.")
    for subject, mark in data['marks'].items():
        if not 0 <= mark <= 100:
            raise ValidationError(f"Marks for {subject} should be between 0 and 100.")

def check_eligibility(data: Dict) -> Dict:
    """Check if the student is eligible for the desired course."""
    desired_course = data['desired_course']
    marks = data['marks']
    qualification_exam = data['qualification_exam']

    # Define course eligibility criteria
    eligibility_criteria = {
        "Computer Science Engineering": {
            "required_subjects": ["Physics", "Chemistry", "Mathematics"],
            "cutoff": 75,
            "required_exam": "JEE"
        },
        "Mechanical Engineering": {
            "required_subjects": ["Physics", "Chemistry", "Mathematics"],
            "cutoff": 70,
            "required_exam": "JEE"
        },
        "Electrical Engineering": {
            "required_subjects": ["Physics", "Chemistry", "Mathematics"],
            "cutoff": 70,
            "required_exam": "JEE"
        },
        "Civil Engineering": {
            "required_subjects": ["Physics", "Chemistry", "Mathematics"],
            "cutoff": 65,
            "required_exam": "JEE"
        },
        "Electronics and Communication Engineering": {
            "required_subjects": ["Physics", "Chemistry", "Mathematics"],
            "cutoff": 70,
            "required_exam": "JEE"
        },
        "MBBS": {
            "required_subjects": ["Physics", "Chemistry", "Biology"],
            "cutoff": 85,
            "required_exam": "NEET"
        },
        "BDS (Dentistry)": {
            "required_subjects": ["Physics", "Chemistry", "Biology"],
            "cutoff": 80,
            "required_exam": "NEET"
        },
        "BAMS (Ayurveda)": {
            "required_subjects": ["Physics", "Chemistry", "Biology"],
            "cutoff": 75,
            "required_exam": "NEET"
        },
        "BHMS (Homeopathy)": {
            "required_subjects": ["Physics", "Chemistry", "Biology"],
            "cutoff": 75,
            "required_exam": "NEET"
        },
        "BPT (Physiotherapy)": {
            "required_subjects": ["Physics", "Chemistry", "Biology"],
            "cutoff": 70,
            "required_exam": "NEET"
        },
        "B.Com (Bachelor of Commerce)": {
            "required_subjects": ["Accountancy", "Business Studies", "Economics"],
            "required_exam": "12"
        },
        "BBA (Bachelor of Business Administration)": {
            "required_subjects": ["Accountancy", "Business Studies", "Economics"],
            "required_exam": "12"
        },
        "BBM (Bachelor of Business Management)": {
            "required_subjects": ["Accountancy", "Business Studies", "Economics"],
            "required_exam": "12"
        },
        "CA (Chartered Accountancy)": {
            "required_subjects": ["Accountancy", "Business Studies", "Economics"],
            "required_exam": "12"
        },
        "BA in History": {
            "required_subjects": ["History", "Political Science", "Geography"],
            "required_exam": "12"
        },
        "BA in Psychology": {
            "required_subjects": ["Psychology", "Sociology,", "English"],
            "required_exam": "12"
        },
        "BA in Sociology": {
            "required_subjects": ["Sociology", "Political Science", "History"],
            "required_exam": "12"
        },
        "BA in Political Science": {
            "required_subjects": ["Political Science", "History", "Geography"],
            "required_exam": "12"
        },
        "BA in English": {
            "required_subjects": ["English", "History", "Political Science"],
            "required_exam": "12"
        },
        
    }

    if desired_course not in eligibility_criteria:
        raise ValidationError(f"Desired course '{desired_course}' is not recognized.")

    criteria = eligibility_criteria[desired_course]

    for subject in criteria['required_subjects']:
        if subject not in marks:
            raise ValidationError(f"Missing required subject: {subject}")

    if qualification_exam != criteria['required_exam']:
        raise ValidationError(f"Required exam '{criteria['required_exam']}' not qualified.")

    total_marks = sum(marks[subject] for subject in criteria['required_subjects'])
    average_marks = total_marks / len(criteria['required_subjects'])

    if average_marks < criteria['cutoff']:
        raise ValidationError(f"Average marks ({average_marks:.2f}%) do not meet the cutoff ({criteria['cutoff']}%).")

    return {
        "eligible": True,
        "message": f"Congratulations! You are eligible for {desired_course}."
    }

def store_student_data(data: Dict, eligibility_status: Dict) -> None:
    """Store student data in the database."""
    conn = create_connection()
    if conn is None:
        raise DatabaseError("Failed to connect to the database.")

    try:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        student_id = f"STU{hash(data['name'] + timestamp)}"

        # Insert data into the database
        cursor.execute("""
            INSERT INTO students (student_id, name, age, gender, marks, qualification_exam, desired_course, eligibility_status, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            data['name'],
            data['age'],
            data['gender'],
            json.dumps(data['marks']),
            data['qualification_exam'],
            data['desired_course'],
            json.dumps(eligibility_status),
            timestamp
        ))
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error: {str(e)}")
    finally:
        conn.close()