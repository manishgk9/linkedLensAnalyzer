from pypdf import PdfReader
import re
import spacy
import phonenumbers

nlp = spacy.load("en_core_web_sm")

SECTION_HEADERS = {
    "education": ["education", "academic"],
    "experience": ["experience", "work experience", "employment"],
    "projects": ["projects"],
    "certifications": ["certifications", "licenses", "achievements"],
    "skills": ["skills", "technical skills"],
    "extracurricular": ["extracurricular", "activities", "interests"],
    "languages": ["languages"]
}
class PdfOperation:
    def __init__(self, pdf):
        # self.pdf = pdf
        self.reader = PdfReader(pdf)
        all_text=self._get_pdf_data()
        self.pdfscan=self._parse_resume(all_text)

    def _get_pdf_data(self):
        try:
            all_text = ""
            for page in self.reader.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"

            return all_text
        except Exception as e:
            return 'Error is found'

    def _get_links(self):
        links_data = []
        for page in self.reader.pages:
            if "/Annots" in page:
                for annot in page["/Annots"]:
                    annot_obj = annot.get_object()
                    if "/A" in annot_obj and "/URI" in annot_obj["/A"]:
                        link = annot_obj["/A"]["/URI"]
                        if 'https' in link:
                            links_data.append(link)
        return links_data
                    
    def _clean_lines(self,lines):
        return [line.strip() for line in lines if line.strip()]

    def _extract_name(self,text):
        first_line = text.split("\n")[0]
        doc = nlp(first_line)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return first_line

    def _extract_email(self,text):
        return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

    def _extract_phone(self,text):
        return [phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                for match in phonenumbers.PhoneNumberMatcher(text, "IN")]

    def _extract_location(self,text):
        doc = nlp(text)
        return list(set([ent.text for ent in doc.ents if ent.label_ == "GPE"]))

    def _identify_sections(self,lines):
        sections = {}
        current_section = None

        for idx, line in enumerate(lines):
            for key, keywords in SECTION_HEADERS.items():
                if any(kw in line.lower() for kw in keywords):
                    current_section = key
                    sections[current_section] = []
                    break
            if current_section:
                sections[current_section].append(line)

        return sections

    def _parse_skills_block(self,skills_block):
        text = " ".join(skills_block)
        skills = re.split(r",|\n|•|\||;", text)
        return list({skill.strip() for skill in skills if skill.strip() and len(skill.strip()) > 1})

    def _parse_resume(self,text):
        lines = self._clean_lines(text.splitlines())

        resume = {
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "location": self._extract_location(text),
            "education": [],
            "experience": [],
            "projects": [],
            "certifications": [],
            "extracurricular": [],
            "languages": [],
            "skills": [],
            "links":self._get_links()
        }

        sections = self._identify_sections(lines)

        for key in resume:
            if key in sections:
                if key == "skills":
                    resume[key] = self._parse_skills_block(sections[key])
                else:
                    resume[key] = sections[key]

        return resume

