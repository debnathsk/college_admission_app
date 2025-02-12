# app/main.py

import logging
from fastapi import FastAPI, HTTPException
import uvicorn
from typing import List, Dict
from .services import validate_input, check_eligibility, store_student_data, get_admitted_students
from .schemas import StudentRequest, EligibilityResponse
from .exceptions import ValidationError, DatabaseError
from .utils import setup_logging

# Configure logging
setup_logging()

app = FastAPI()

@app.post("/check_eligibility", response_model=EligibilityResponse)
async def check_eligibility_endpoint(student_data: StudentRequest):
    try:
        # Log the input
        logging.info(f"Received request: {student_data.dict()}")

        validate_input(student_data.dict())
        eligibility_status = check_eligibility(student_data.dict())
        store_student_data(student_data.dict(), eligibility_status)

        # Log the output
        logging.info(f"Eligibility status: {eligibility_status}")

        return eligibility_status
    except ValidationError as e:
        logging.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        logging.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/admitted_students", response_model=List[Dict])
async def get_admitted_students_endpoint():
    try:
        admitted_students = get_admitted_students()
        return admitted_students
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)