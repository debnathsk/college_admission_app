from typing import Dict
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    gender: str
    marks: Dict[str, int]
    qualification_exam: str
    desired_course: str