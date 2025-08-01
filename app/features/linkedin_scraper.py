import time
import json
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from typing import Literal
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
class LinkedInUserScraper:
    def __init__(self,username=None, password=None, save_cookies=False, cookie_file=None,  headless=False):
        options = uc.ChromeOptions()
        self.cookie_file = cookie_file
        self.username = username
        self.password = password
        self.save_cookies = save_cookies
        self.headless = headless
        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-translate")
        options.add_argument("--disable-features=VizDisplayCompositor")

        self.driver = uc.Chrome(options=options)

        if self.cookie_file or os.path.exists('linkedin_cookies.json'):
            self._load_cookies(self.cookie_file)
            time.sleep(3)
            if "login" in self.driver.current_url.lower():
                self._login()
        else:
            self._login()

    def add_pin(self, pin=None):
        if not pin:
            raise ValueError("2FA code pin is required")
        try:
            code_pin = self.driver.find_element(By.XPATH, '//*[@id="input__email_verification_pin"]')
            code_pin.send_keys(pin)
            code_pin.submit()
            time.sleep(2)
            self.__dump_cookies(self.cookie_file)
        except Exception as e:
            print(f"Error adding 2FA code: {e}")
           
    def get_driver(self):
        return self.driver
    
    def get_page_source(self):
        return self.driver.page_source
    
    def get_profile_info(self, username=None,timeout=5):
        profile_data={}
        if not username:
            print("Please provide a LinkedIn username")
            return {}

        url = f'https://www.linkedin.com/in/{username}'
        if url.lower().rstrip('/') in self.driver.current_url.rstrip('/'):
            #No page load required
            source_page=self.driver.page_source
            return self._helper_get_user_info(source_page)
        try:
            
            self.driver.get(url)
            WebDriverWait(self.driver, timeout,poll_frequency=.7).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1")) )
            
            source_page=self.driver.page_source
            return self._helper_get_user_info(source_page)

        except Exception as e:
            print('Data is not found')
            return profile_data


    def get_user_experience(self, username=None,number_of_experience=5,timeout=6):
        if not username:
            print('Username is required.')
            return []

        page_source = self._helper_get_source_page(username, 'experience',timeout=timeout)
        if page_source:
            return self._helper_get_user_experience(page_source,number_of_experience)
        else:
            print('[-] Failed to retrieve experience.')
            return []
    def get_user_skills(self, username=None,number_of_skills=10,timeout=6):
        if not username:
            print('Username is required.')
            return []

        page_source = self._helper_get_source_page(username, 'skills',timeout=timeout)
        if page_source:
            return self._helper_get_user_skills(page_source, number_of_skills)
        else:
            print('[-] Failed to retrieve skills.')
            return []
    
    def get_user_education(self, username=None,timeout=6):
        if not username:
            print('Username is required.')
            return []

        page_source = self._helper_get_source_page(username, 'education',timeout=timeout)
        if page_source:
            return self._helper_get_user_educations(page_source)
        else:
            print('[-] Failed to retrieve education.')
            return []
    
    def get_user_certifications(self, username=None,timeout=6):
        if not username:
            print('Username is required.')
            return []

        page_source = self._helper_get_source_page(username, 'certifications',timeout=timeout)
        if page_source:
            return self._helper_get_user_certifications(page_source)
        else:
            print('[-] Failed to retrieve certifications.')
            return []

    def get_user_projects(self, username=None, num_of_projects=4,timeout=6):
        if not username:
            print('username of target is must required..')
            return []

        # Use the helper to get the project section source
        page_source = self._helper_get_source_page(username=username, label='projects',timeout=timeout)

        if page_source:
            return self._helper_get_project_info(page_source, num_of_projects)
        else:
            print(f"Could not retrieve project section for {username}")
            return []

        

    def help(self):
        help_text = '''
         LinkedUserScraper Complete Help
        ════════════════════════════════════

        🔹 login(username: str, password: str)
        → Logs into LinkedIn using your credentials.
        ✔ Example:
            scraper=LinkedinUserScraper('manish@example.com', 'yourpassword',save_cookie=True,cookie_path='')

        🔹 add_pin(pin: str)
        → Adds 2FA code if required after login.
        ✔ Example:
            scraper.add_pin('123456')

        🔹 get_driver()
        → Returns current Selenium driver instance.
        ✔ Example:
            driver = scraper.get_driver()

        🔹 get_page_source()
        → Returns HTML content of the current page.
        ✔ Example:
            html = scraper.get_page_source()

        🔹 get_profile_info(username: str)
        → Scrapes name, headline, about, location.
        ✔ Example:
            data = scraper.get_profile_info('manishgk9')
        ✔ Output:
            {'name': 'Manish Yadav', 'headline': 'Python Developer', 'about': 'Building web scrapers', 'location': 'India'}

        🔹 get_user_projects(username: str, num_of_projects: int = 3)
        → Scrapes user projects section.
        ✔ Example:
            projects = scraper.get_user_projects('manishgk9', 2)
        ✔ Output:
            [{'title': 'AI Resume Builder', 'description': 'Built using NLP'}, ...]

        🔹 get_user_experiences(username: str, num_of_experiences: int = 2)
        → Gets work experience details.
        ✔ Example:
            experiences = scraper.get_user_experiences('manishgk9', 2)
        ✔ Output:
            [{'position': 'Software Engineer', 'company': 'Google', 'duration': '2 years'}, ...]

        🔹 get_user_education(username: str, num_of_education: int = 2)
        → Gets education info of the user.
        ✔ Example:
            education = scraper.get_user_education('manishgk9', 2)
        ✔ Output:
            [{'school': 'IIT Delhi', 'degree': 'B.Tech CSE'}, ...]

        🔹 get_user_skills(username: str)
        → Gets list of user's skills.
        ✔ Example:
            skills = scraper.get_user_skills('manishgk9')
        ✔ Output:
            ['Python', 'Web Scraping', 'Django', 'Automation']

        🔹 get_user_certifications(username: str)
        → Gets list of user's certifications.
        ✔ Example:
            certs = scraper.get_user_certifications('manishgk9')
        ✔ Output:
            [{'name': 'AWS Certified Developer', 'issuer': 'Amazon', 'date': '2024'}, ...]

        🔹 quit()
        → Closes the browser and quits driver.
        ✔ Example:
            scraper.quit()

        ════════════════════════════════════
         Tip: This is in experimental mode and it is only for educational perpous...
        '''
        print(help_text)

    def quit(self):
        if self.save_cookies:
            self._dump_cookies(self.cookie_file)
        self.driver.quit()
    
    def _helper_clean_multiline_text(self,text):
        if not text:
            return ""
        return ' '.join(text.split())

    def _helper_get_user_info(self,html_page=None):
        soup = BeautifulSoup(html_page, "lxml")

        data = {}

        try:
            name = soup.find("h1")
            data["name"] = name.get_text(strip=True) if name else None

            headline = soup.find("div", {"class": "text-body-medium"})
            data["headline"] = headline.get_text(strip=True) if headline else None

            location = soup.find("span", {"class": "text-body-small inline t-black--light break-words"})
            data["location"] = location.get_text(strip=True) if location else None

            about = soup.find("div", {"class": "display-flex ph5 pv3"})
            if about:
                about_raw = about.get_text(strip=True)
                data["about"] = self._helper_clean_multiline_text(about_raw)
            else:
                data["about"] = None
            profile_picture_tag = soup.find('button', {'aria-label': 'open profile picture'})
            profile_pic=profile_picture_tag.find('img').get('src') if profile_picture_tag else None
            data["profile_pic"] = profile_pic
        except Exception as e:
            print(f'something when wtong {e}')
            return data
        return data

    def _helper_get_project_info(self,page_source,num_of_projects=4):
        soup=BeautifulSoup(page_source,'lxml')
        projects = []
        main_div = soup.find('div', class_="pvs-list__container")
        if main_div:
            all_project_ul = main_div.find('ul')
            if all_project_ul:
                all_project_detail_container = all_project_ul.find_all('li')
                for one_project_detail_container in all_project_detail_container:
                    spans = one_project_detail_container.find_all('span', {'aria-hidden': 'true'})
                    text_blocks = [span.get_text(strip=True).replace("Â", "") for span in spans if span.get_text(strip=True)]

                    # Skip if too short or irrelevant
                    if len(text_blocks) < 3:
                        continue

                    # Build dictionary
                    project = {
                        'title': '',
                        'date': '',
                        'description': '',
                        'skills': '',
                        'github': ''
                    }

                    for text in text_blocks:
                        if not project['title']:
                            project['title'] = text
                        elif re.search(r'\b\d{4}\b', text):  # has a year, likely date
                            project['date'] = text
                        elif 'Skills:' in text or '·' in text:
                            project['skills'] = re.sub(r'^Skills:\s*', '', text)
                        
                        elif 'GitHub' in text or 'github.com' in text:
                            project['github'] = text
                        else:
                            project['description'] += " " + text

                    # Clean up spacing
                    for key in project:
                        project[key] = re.sub(r'\s+', ' ', project[key]).strip()

                    # Only append valid ones
                    if project['title'] and project['description']:
                        projects.append(project)
        return projects[:num_of_projects]

    def _helper_get_user_certifications(self,page_html=None,number_of_certificates=5):
        soup=BeautifulSoup(page_html,'lxml')
        certificate_details=soup.find_all('li',{'class':"pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
        if not certificate_details:
            return ["There are no posting of certifications by user.."]
        certifications_data=[]
        for details in certificate_details:
            spans=details.find_all('span',{'aria-hidden':"true"})
            temp_data=[span.get_text().strip() for span in spans]
            certifications_data.append(temp_data)
        return certifications_data[:number_of_certificates]
    
    def _helper_get_user_experience(self,page_html=None,number_of_experience=5):
        soup=BeautifulSoup(page_html,'lxml')
        experience_items=soup.find_all('li',{'class':"pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
        if not experience_items:
            return ["Experience Section has no data.."]
        experience_data=[]
        for items in experience_items:
            spans=items.find_all('span',{'aria-hidden':"true"})
            temp_data=[span.get_text().strip() for span in spans]
            experience_data.append(temp_data)
        return experience_data[:number_of_experience]

    def _helper_get_user_skills(self,page_html=None,number_of_skills=5):
        soup=BeautifulSoup(page_html,'lxml')
        skills_items=soup.find('main',{'aria-label':'Skills'})
        if not skills_items:
            return ["No skills data available"]
        skills=skills_items.find_all('li',class_='pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        skills_data=[]
        for skill in skills:
            skill=skill.find('span',{'aria-hidden':'true'}).get_text().strip()
            skills_data.append(skill)
        return skills_data[:number_of_skills]

    def _helper_get_user_educations(self,page_html=None):
        soup=BeautifulSoup(page_html,'lxml')
        education_details=soup.find_all('li',{'class':"pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})
        if not education_details:
            return ["Education data is not there.."]
        education_data=[]
        for details in education_details:
            spans=details.find_all('span',{'aria-hidden':"true"})
            temp_data=[span.get_text().strip() for span in spans]
            education_data.append(temp_data)
        return education_data
    
    def _helper_get_source_page(self,
        username: str = None,
        label: Literal['skills', 'projects', 'experience', 'certifications', 'education'] = None,timeout=6):
        if not username or not label:
            print('Username and label are required.')
            return None

        label_map = {
            'skills': 'Skills',
            'projects': 'Projects',
            'experience': 'Experience',
            'education': 'Education',
            'certifications': 'Licenses & certifications'
        }

        if label not in label_map:
            print("The provided label is not from the given list.")
            return None

        url = f'https://www.linkedin.com/in/{username}/details/{label}'
        heading_text = label_map[label]

        if url.lower().rstrip('/') in self.driver.current_url.lower().rstrip('/'):
            # Page is already loaded
            return self.driver.page_source

        try:
            self.driver.get(url)
            WebDriverWait(self.driver, timeout,poll_frequency=0.6).until(
                EC.presence_of_element_located((By.XPATH, f'//h1[normalize-space()="{heading_text}"]'))
            )
            page_source = self.driver.page_source
            # self.driver.back()
            return page_source
        except Exception as e:
            print(f"Error loading page: {e}")
            return None

    def _login(self):
        if not self.username or not self.password:
            raise ValueError("Username and password are required for login")

        self.driver.get("https://www.linkedin.com/login")
        time.sleep(2)

        email = self.driver.find_element(By.ID, 'username')
        email.send_keys(self.username)

        passwd = self.driver.find_element(By.ID, 'password')
        passwd.send_keys(self.password)
        passwd.submit()

        time.sleep(3)
        try:
            code_pin = self.driver.find_element(By.XPATH, '//*[@id="input__email_verification_pin"]')
            if code_pin:
                print("2FA code required. Use `add_pin(pin)` to continue.")
        except Exception:
            if self.save_cookies:
                self._dump_cookies(self.cookie_file)

    def _dump_cookies(self, filename=None):
        if self.save_cookies:
            filename = filename or self.cookie_file or "linkedin_cookies.json"
            cookies = self.driver.get_cookies()
            with open(filename, "w") as f:
                json.dump(cookies, f)
            print(f"Cookies saved to {filename}")

    def _load_cookies(self, filename=None):
        filename = filename or self.cookie_file or "linkedin_cookies.json"
        try:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    cookies = json.load(f)
                self.driver.get("https://www.linkedin.com/")
                time.sleep(2)
                for cookie in cookies:
                    if 'expiry' in cookie and not isinstance(cookie['expiry'], (int, float)):
                        del cookie['expiry']
                    self.driver.add_cookie(cookie)
                self.driver.refresh()
                time.sleep(1)
                print(f"Cookies loaded from {filename}")
            else:
                print(f"Cookie file not found at: {filename}")
        except Exception as e:
            print(f"Could not load cookies: {e}")