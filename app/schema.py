from pydantic import BaseModel
from typing import List, Dict

class ResumeUpload(BaseModel):
    filename: str

class LinkedInData(BaseModel):
    name: str
    about: str
    skills: List[str]
    experience: List[Dict]
    education: List[Dict]

class SuggestionRequest(BaseModel):
    linkedin: LinkedInData
    resume_text: str
