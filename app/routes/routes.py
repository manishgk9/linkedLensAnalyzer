import os
import tempfile
from fastapi import APIRouter, HTTPException, UploadFile, File
import json
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
from app.tasks import pdfScanOperation,get_linkedin_data,get_gemini
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "logs", "linkedin_scraper.log")
router = APIRouter()

class UserRequest(BaseModel):
    username: str


# @router.post("/upload-resume")
# async def upload_pdf(file: UploadFile = File(...)):
#     if not file.filename.endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Invalid file format. Only PDFs are allowed.")

#     try:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#             tmp.write(await file.read())
#             tmp_path = tmp.name
#         pdf_data=pdfScanOperation(tmp_path)
#         gimini_response=get_gemini(json_data=pdf_data)
        
#         return {'response':gimini_response}
#     finally:
#         os.remove(tmp_path)


@router.post("/analyze-linkedin")
async def analyze_linkedin(data:UserRequest):
    if not data.username or data.username.lower() == "string":
        raise HTTPException(status_code=400, detail="Username is required")
    linkedin_data=get_linkedin_data(username=data.username)
    gemini_response=get_gemini(json_data=linkedin_data)
    return {"response":gemini_response}


@router.get("/logs", response_class=PlainTextResponse)
async def get_linkedin_logs():
    try:
        with open(LOG_FILE_PATH, "r") as log_file:
            return log_file.read()
    except FileNotFoundError:
        return "Log file not found."

@router.post('/test-server')
async def test_server(data:UserRequest):
    return {"response": "{\n\"ats_score\": 50,\n\"summary\": \"The candidate demonstrates strong experience and exceptional, quantifiable achievements in fitness instruction and client management, including significant improvements in client health outcomes and business growth. However, the resume's structure, as reflected in the provided data, is highly disorganized. Key information such as skills and accomplishments are misplaced or mixed within other sections, which would severely hinder an Applicant Tracking System's ability to correctly parse and interpret the candidate's qualifications.\",\n\"suggestions\": [\n\"Standardize section headings (e.g., 'Summary', 'Experience', 'Education', 'Skills', 'Certifications') for ATS compatibility.\",\n\"Create a dedicated 'Skills' section with bulleted hard skills (e.g., Cardio Training, HIIT, Client Assessments) and soft skills (e.g., Client Management, Sales, Communication).\",\n\"Integrate the impressive 'Accomplishments' bullet points into the relevant job descriptions under the 'Experience' section, demonstrating impact within specific roles.\",\n\"Establish a distinct 'Certifications' section to list qualifications like 'CrossFit Level 1 Instructor' and 'Coach’s Prep Certified'.\",\n\"Clearly delineate and separate different employment roles within the 'Experience' section, ensuring each role has its own set of responsibilities and achievements.\",\n\"Ensure location data is correctly formatted and free of parsing errors (e.g., 'San Antonio Driving', 'Los Angeles\\\" Event' should be corrected).\",\n\"Review the resume for any redundant information and ensure all points are concise and professional.\",\n\"Consider removing 'Hobbies' unless directly relevant to the target job or company culture.\"\n],\n\"strengths\": [\n\"Exceptional use of quantifiable achievements and metrics (e.g., 110% participation increase, 18% utilization, 29% sales increase, 140+ clients managed, documented client health improvements).\",\n\"Strong command of relevant industry skills and knowledge (e.g., HIIT, Cardio Training, Client Assessments, Program Development).\",\n\"Demonstrated capabilities in leadership, client acquisition, and client management.\",\n\"Proficiency in multiple languages (English and Spanish).\",\n\"Experience in sales and marketing within the fitness industry.\"\n],\n\"weak_sections\": [\n\"Formatting and layout (sections are mixed and disorganized).\",\n\"Skills section (contains job duties rather than a clear list of skills).\",\n\"Certifications section (missing, though certifications are mentioned elsewhere).\",\n\"Projects section (empty).\"\n],\n\"missing_keywords\": [\n\"Client Retention\",\n\"Program Evaluation\",\n\"Fitness Technology\",\n\"Nutrition Coaching\",\n\"Wellness Programs\",\n\"Group Fitness Management\"\n],\n\"formatting_issues\": [\n\"Skills, Hobbies, Languages, and Accomplishments are grouped under the 'Education' section.\",\n\"Experience details are scattered and found within the 'Skills' data.\",\n\"The 'PROFILE' is placed within the 'Experience' section as a heading.\",\n\"Unclear separation between different job roles, particularly later in the employment history.\",\n\"Location data appears to have parsing errors or extraneous information.\"\n],\n\"section_scores\": {\n\"education\": 6,\n\"experience\": 7,\n\"skills\": 4,\n\"projects\": 0,\n\"certifications\": 0,\n\"formatting\": 2\n}\n}"}


@router.post("/upload-resume")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file format. Only PDFs are allowed.")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        pdf_data=pdfScanOperation(tmp_path)
        gimini_response=get_gemini(json_data=pdf_data)
        
        return {'response':gimini_response}
    finally:
        os.remove(tmp_path)