from typing import Dict
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
    