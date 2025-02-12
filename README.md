# College Admission Eligibility Application

This is a Python-based application that checks the eligibility of students for college admission based on their demographic details, 12th-grade marks, and qualification exam results. The application uses **FastAPI** to create an API endpoint, **SQLite** for database storage, and **Pydantic** for input validation.

## Features

- **Input Validation**: Validates student details such as name, age, gender, 12th-grade marks (6 subjects), qualification exam results, and desired course.
- **Eligibility Check**: Checks if the student is eligible for the desired course based on predefined criteria.
- **Duplicate Handling**: If a student applies twice, the first record is deleted, and a new record is inserted.
- **Recommendations**: If the student is not eligible for the desired course, the application recommends similar courses they are eligible for.
- **Database Storage**: Stores student data in a SQLite database.
- **Logging**: Logs input and output details with timestamps.

## Technologies Used

- **Python**: Core programming language.
- **FastAPI**: Framework for building the API.
- **SQLite**: Database for storing student records.
- **Pydantic**: Data validation and settings management.
- **Logging**: For logging input and output details.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package manager)

## Setup:
### Create a Virtual Environment:
python -m venv venv

### Activate the Virtual Environment:
For Windows MAchine-: venv\Scripts\activate

### Install Dependencies:
pip install -r requirements.txt

### Initialize the Database:
python app/database.py

## Running the Application:

### Start the FastAPI server:
uvicorn app.main:app --reload

### The API will be available at:
http://127.0.0.1:8000

Use tools like Postman, cURL, or the Swagger UI (available at http://127.0.0.1:8000/docs) to interact with the API.

## API Endpoints

### POST /check_eligibility
Description: Checks if a student is eligible for their desired course. If the student is not eligible, it recommends similar courses they are eligible for.
#### Request Body-:

{
    "name": "Kartik Aryan",
    "age": 20,
    "gender": "Male",
    "marks": {
        "Physics": 85,
        "Chemistry": 80,
        "Mathematics": 90,
        "Biology": 75,
        "English": 85,
        "Computer Science": 95
    },
    "qualification_exam": "JEE",
    "desired_course": "Computer Science Engineering"
}

#### Response:
If eligible-:
{
    "eligible": true,
    "message": "Congratulations! You are eligible for Computer Science Engineering."
}

If not eligible but similar courses are available-:
{
    "eligible": false,
    "message": "You are not eligible for Computer Science Engineering, but you are eligible for the following similar courses: Information Technology, Software Engineering."
}

If not eligible for any courses-:
{
    "eligible": false,
    "message": "You are not eligible for Computer Science Engineering or any similar courses."
}

#### Error Responses:
400 Bad Request: If input validation fails (e.g., invalid name, age, or marks).

500 Internal Server Error: If there is a database error.


### GET /admitted_students
Retrieves a list of all admitted students (students who are eligible for their desired course).

#### Response:
{
    "eligible": true,
    "message": "Congratulations! You are eligible for Computer Science Engineering."
}

#### Error Response:
500 Internal Server Error: If there is a database error.

### GET /docs
Provides interactive API documentation using Swagger UI. You can test the API endpoints directly from the browser.
URL: http://127.0.0.1:8000/docs

