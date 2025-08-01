from celery import shared_task
from app.utils.pdf_operation import PdfOperation
from app.features.linkedin_scraper import LinkedInUserScraper
from dotenv import load_dotenv
import os
from typing import Optional
import logging
from app.gimini.gimin_api import get_gimini_response
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, "linkedin_scraper.log")

load_dotenv()
Email=os.getenv('EMAIL')
Password=os.getenv('PASSWORD')
scraper=LinkedInUserScraper(username=Email,password=Password,save_cookies=True)

# Prevent duplicate handlers
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'  # Append mode to avoid overwriting
    )
logger = logging.getLogger(__name__)

@shared_task
def pdfScanOperation(pdf:str):
    pdf_data=PdfOperation(pdf).pdfscan
    # get_gemini()
    return pdf_data

@shared_task
def get_linkedin_data(username: str):
    result = {}

    try:
        result['profile'] = scraper.get_profile_info(username=username)
        logger.info('Found user info: %s', result['profile'])
    except Exception as e:
        logger.warning('Profile fetch failed: %s', str(e))
        result['profile'] = None

    try:
        result['education'] = scraper.get_user_education(username=username)
        logger.info('Found education: %s', result['education'])
    except Exception as e:
        logger.warning('Education fetch failed: %s', str(e))
        result['education'] = None

    try:
        result['experience'] = scraper.get_user_experience(username=username)
        logger.info('Found experience: %s', result['experience'])
    except Exception as e:
        logger.warning('Experience fetch failed: %s', str(e))
        result['experience'] = None

    try:
        result['projects'] = scraper.get_user_projects(username=username)
        logger.info('Found projects: %s', result['projects'])
    except Exception as e:
        logger.warning('Projects fetch failed: %s', str(e))
        result['projects'] = None

    try:
        result['skills'] = scraper.get_user_skills(username=username)
        logger.info('Found skills: %s', result['skills'])
    except Exception as e:
        logger.warning('Skills fetch failed: %s', str(e))
        result['skills'] = None

    try:
        result['certifications'] = scraper.get_user_certifications(username=username)
        logger.info('Found certifications: %s', result['certifications'])
    except Exception as e:
        logger.warning('Certifications fetch failed: %s', str(e))
        result['certifications'] = None

    return result
    
@shared_task
def get_gemini(json_data: Optional[dict] = None):
    if json_data is None:
        return {"error": "No data provided"}
    response=get_gimini_response(json_data)
    return response