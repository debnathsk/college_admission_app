from typing import Dict, List
from pydantic import BaseModel

class StudentRequest(BaseModel):
    name: str
    age: int
    gender: str
    marks: Dict[str, int]
    qualification_exam: str
    desired_course: str

class EligibilityResponse(BaseModel):
    eligible: bool
    message: str

class AdmittedStudentResponse(BaseModel):
    student_id: str
    name: str
    age: int
    gender: str
    marks: Dict[str, int]
    qualification_exam: str
    desired_course: str
    timestamp: str