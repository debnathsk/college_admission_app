import re
import json
from datetime import datetime
import sqlite3
from typing import Dict, List
from .database import create_connection
from .exceptions import ValidationError, DatabaseError

SIMILAR_COURSES = {
    "Computer Science Engineering": [
        "Mechanical Engineering",
        "Electrical Engineering",
        "Civil Engineering",
        "Electronics and Communication Engineering"

    ],
    "Mechanical Engineering": [
        "Electrical Engineering",
        "Civil Engineering",
        "Electronics and Communication Engineering"
    ],
    "Electrical Engineering": [
        "Civil Engineering",
        "Electronics and Communication Engineering"
    ],
    "Civil Engineering": [
        "Electronics and Communication Engineering"
    ],
    "MBBS": [
        "BDS (Dentistry)",
        "BAMS (Ayurveda)",
        "BHMS (Homeopathy)",
        "BPT (Physiotherapy)"
    ],
    "B.Com (Bachelor of Commerce)": [
        "BBA (Bachelor of Business Administration)",
        "BBM (Bachelor of Business Management)",
        "CA (Chartered Accountancy)"
    ]
}

def validate_input(data: Dict) -> None:
    """
    Validate input data using regular expressions and ensure 6 subjects are provided.
    Raises ValueError if validation fails.
    """
    # Validate name
    if not re.match(r"^[A-Za-z\s]+$", data['name']):
        raise ValidationError("Name should only contain letters and spaces.")

    # Validate age
    if not 17 <= data['age'] <= 25:
        raise ValidationError("Age should be between 17 and 25.")

    # Validate gender
    if data['gender'] not in ["Male", "Female", "Other"]:
        raise ValidationError("Gender should be one of 'Male', 'Female', or 'Other'.")

    # Validate marks (ensure exactly 6 subjects)
    if len(data['marks']) != 6:
        raise ValidationError("Exactly 6 subjects must be provided.")

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
            "cutoff": 35,
            "required_exam": "12"
        },
        "BBA (Bachelor of Business Administration)": {
            "required_subjects": ["Accountancy", "Business Studies", "Economics"],
            "cutoff": 35,
            "required_exam": "12"
        },
        "BBM (Bachelor of Business Management)": {
            "required_subjects": ["Accountancy", "Business Studies", "Economics"],
            "cutoff": 35,
            "required_exam": "12"
        },
        "CA (Chartered Accountancy)": {
            "required_subjects": ["Accountancy", "Business Studies", "Economics"],
            "cutoff": 35,
            "required_exam": "12"
        },
        "BA in History": {
            "required_subjects": ["History", "Political Science", "Geography"],
            "cutoff": 35,
            "required_exam": "12"
        },
        "BA in Psychology": {
            "required_subjects": ["Psychology", "Sociology,", "English"],
            "cutoff": 35,
            "required_exam": "12"
        },
        "BA in Sociology": {
            "required_subjects": ["Sociology", "Political Science", "History"],
            "cutoff": 35,
            "required_exam": "12"
        },
        "BA in Political Science": {
            "required_subjects": ["Political Science", "History", "Geography"],
            "cutoff": 35,
            "required_exam": "12"
        },
        "BA in English": {
            "required_subjects": ["English", "History", "Political Science"],
            "cutoff": 35,
            "required_exam": "12"
        },
        
    }

    # Check if the desired course exists in the criteria
    if desired_course not in eligibility_criteria:
        raise ValidationError(f"Desired course '{desired_course}' is not recognized.")

    criteria = eligibility_criteria[desired_course]

    # Check if the student has the required subjects
    for subject in criteria['required_subjects']:
        if subject not in marks:
            raise ValidationError(f"Missing required subject: {subject}")

    # Check if the student has qualified the required exam
    if qualification_exam != criteria['required_exam']:
        raise ValidationError(f"Required exam '{criteria['required_exam']}' not qualified.")

    # Calculate average marks for required subjects
    total_marks = sum(marks[subject] for subject in criteria['required_subjects'])
    average_marks = total_marks / len(criteria['required_subjects'])

    # Check if the student meets the cutoff marks
    if average_marks < criteria['cutoff']:
        # Student is not eligible for the desired course
        # Check eligibility for similar courses
        similar_courses = SIMILAR_COURSES.get(desired_course, [])
        eligible_courses = []

        for course in similar_courses:
            if course in eligibility_criteria:
                course_criteria = eligibility_criteria[course]

                # Check if the student meets the criteria for the similar course
                meets_subjects = all(subject in marks for subject in course_criteria['required_subjects'])
                meets_exam = qualification_exam == course_criteria['required_exam']
                meets_cutoff = (sum(marks[subject] for subject in course_criteria['required_subjects']) / len(course_criteria['required_subjects'])) >= course_criteria['cutoff']

                if meets_subjects and meets_exam and meets_cutoff:
                    eligible_courses.append(course)

        if eligible_courses:
            return {
                "eligible": False,
                "message": f"You are not eligible for {desired_course}, but you are eligible for the following similar courses: {', '.join(eligible_courses)}."
            }
        else:
            return {
                "eligible": False,
                "message": f"You are not eligible for {desired_course} or any similar courses."
            }

    # If all checks pass, the student is eligible
    return {
        "eligible": True,
        "message": f"Congratulations! You are eligible for {desired_course}."
    }

def store_student_data(data: Dict, eligibility_status: Dict) -> None:
    """
    Store student data in the database.
    If a student applies twice, the first record is deleted and the new record is inserted.
    """
    conn = create_connection()
    if conn is None:
        raise DatabaseError("Failed to connect to the database.")

    try:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        student_id = f"STU{hash(data['name'] + timestamp)}"

        # Check if the student already exists in the database
        cursor.execute("SELECT id FROM students WHERE name = ?", (data['name'],))
        existing_student = cursor.fetchone()

        # If the student exists, delete the old record
        if existing_student:
            cursor.execute("DELETE FROM students WHERE name = ?", (data['name'],))
            print(f"Deleted old record for student: {data['name']}")

        # Insert the new record
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
        print(f"Inserted new record for student: {data['name']}")
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error: {str(e)}")
    finally:
        conn.close()


def get_admitted_students() -> List[Dict]:
    """
    Retrieve the list of admitted students from the database.
    Returns a list of dictionaries containing student details.
    """
    conn = create_connection()
    if conn is None:
        raise DatabaseError("Failed to connect to the database.")

    try:
        cursor = conn.cursor()
        # Query to fetch all admitted students (where eligibility_status is True)
        cursor.execute("""
            SELECT student_id, name, age, gender, marks, qualification_exam, desired_course, timestamp
            FROM students
            WHERE json_extract(eligibility_status, '$.eligible') = 1
        """)
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        admitted_students = []
        for row in rows:
            student = {
                "student_id": row[0],
                "name": row[1],
                "age": row[2],
                "gender": row[3],
                "marks": json.loads(row[4]),  # Convert JSON string back to dictionary
                "qualification_exam": row[5],
                "desired_course": row[6],
                "timestamp": row[7]
            }
            admitted_students.append(student)

        return admitted_students
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error: {str(e)}")
    finally:
        conn.close()