# 🧠 Linkedlence – AI-Powered LinkedIn & Resume Analyzer
# Screen Shots
<p align="center">
  <img width="45%" src="https://github.com/user-attachments/assets/fe19a658-fd56-4d57-8567-b2b83df4069a" />
  <img width="45%" src="https://github.com/user-attachments/assets/63ece164-d28f-4381-8c45-b00eba8ce2eb" />
</p>

<p align="center">
  <img width="50%" src="https://github.com/user-attachments/assets/2f268455-8460-456f-9bae-f701efdf0de5" />
</p>

**Linkedlence** is an 
intelligent AI-driven tool that analyzes LinkedIn profiles and PDF resumes to provide ATS scores, strengths, weaknesses, formatting issues, missing keywords, and actionable suggestions using NLP and Google's Gemini model.

---

## 🎬 Demo Video

[![Watch the video](https://github.com/user-attachments/assets/a63d1231-22c2-4424-8de4-64076282873f)](https://www.youtube.com/watch?v=cXS6Po2JqH0)

---
## 🎯 Features

- 🔗 Analyze **LinkedIn profiles** directly using a username
- 📄 Upload **PDF resumes** and extract data with SpaCy
- 🧠 Generate **Gemini-powered analysis** (summary, ATS score, sections)
- 🕵️ Data scraping with **Selenium** + **BeautifulSoup**
- 📦 Queue processing with **Celery** + **Redis**
- 🎥 **Tailwind-based UI** with responsive design
- 🔧 Debug with `/logs` route and activity logging
- 🔐 Clean separation of **frontend** and **backend**

---

## 🛠️ Tech Stack

| Layer         | Tools / Libraries                                 |
| ------------- | ------------------------------------------------- |
| 🖥️ Frontend   | React, Redux Toolkit, Tailwind CSS                |
| ⚙️ Backend    | FastAPI, Pydantic, SpaCy, Celery, Redis           |
| 🤖 AI/NLP     | Gemini (Google Generative AI), SpaCy              |
| 🕸️ Scraping   | Selenium (undetected_chromedriver), BeautifulSoup |
| 📄 Resume     | PDF file processing, NLP-based section extraction |
| 📦 Task Queue | Celery, Redis                                     |
| 📝 Logging    | Custom log file viewer via `/logs` endpoint       |

---

## 📁 Project Structure

```bash
linkedlence/
│
├── app/                                # FastAPI backend
│   ├── features/
│   │   └── linkedin_scraper.py         # LinkedIn scraping logic (Selenium + BS4)
│   ├── routes/
│   │   └── routes.py                   # API routes: /upload-resume, /analyze-linkedin
│   ├── tasks.py                        # Celery task queue management
│   ├── gimini/
│   │   └── gimini_api.py               # Gemini API integration and task handlers
│   ├── logs/
│   │   └── logs.py                     # Scraping and backend logs
│   ├── utils/                          # Utility modules
│   │   ├── pdf_operation.py           # Resume text extraction and SpaCy processing
│   │   └── gimin_prompt.py            # Prompt template generation for Gemini
│   └── main.py                         # FastAPI entrypoint
│
├── frontend/                           # React frontend
│   ├── src/
│   │   ├── components/                 # Reusable UI components
│   │   ├── services/                   # Axios or API service calls
│   │   ├── redux/                      # Redux slices and async thunks
│   │   ├── assets/                     # SVGs, icons, images
│   │   ├── AnalyzedResponse.jsx       # Analysis results UI
│   │   ├── HomeScreen.jsx             # Upload and input UI
│   │   └── App.jsx                    # Main React component
│   ├── store.jsx                      # Redux store config
│   └── tailwind.config.js             # TailwindCSS configuration
│
├── .env                                # Environment variables (API keys, etc.)
├── README.md                           # Project documentation (this file)
├── Requirments.txt                     # Python dependencies
```

---

## ⚙️ Installation & Setup

### 📦 Prerequisites

- Python 3.10+
- Node.js 18+
- Redis server
- Chrome installed (for Selenium)
- Gemini API key (via Google AI Studio)
- Vs Code Editor

---

### 🚀 Backend Setup (FastAPI + Celery)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Start FastAPI:**

```bash
uvicorn app.main:app --reload
```

**Start Celery Worker:**

```bash
celery -A celery_app worker --loglevel=info
```

**Start Redis (if not running):**

```bash
redis-server
```

---

### 🌐 Frontend Setup (React + Tailwind)

```bash
cd frontend
npm install
npm run dev  # or npm start
```

---

## 🔗 API Routes

| Endpoint            | Method | Description                                |
| ------------------- | ------ | ------------------------------------------ |
| `/upload-resume`    | POST   | Uploads PDF resume and returns AI analysis |
| `/analyze-linkedin` | POST   | Accepts LinkedIn username and analyzes it  |
| `/logs`             | GET    | Fetches internal scraping/debug logs       |

---

## 🧪 Sample Output

```json
{
  "ats_score": 72,
  "summary": "Entry-level Bootcamp Instructor...",
  "suggestions": ["Add a Certifications section", ...],
  "strengths": ["Quantifiable fitness outcomes", ...],
  "weak_sections": ["Projects section missing", ...],
  "missing_keywords": ["Nutrition Coaching", "Retention"],
  "formatting_issues": ["Inconsistent section titles"],
  "section_scores": {
    "education": 80,
    "experience": 90,
    "skills": 60,
    "projects": 20,
    "certifications": 65,
    "formatting": 30
  }
}
```

---


## 🔐 Environment Variables

Create a `.env` file in the `backend/` folder with:

```env
OPENAI_API_KEY=your_gemini_key
REDIS_URL=redis://localhost:6379
```

---

## 🧠 AI Prompt Logic

The Gemini prompt is structured to:

- Return only valid JSON
- Score resume on ATS metrics
- Suggest improvements and highlight strengths/weaknesses
- Enforce section parsing consistency

Prompt Template: `app/gemini_utils.py`

---

## 🧹 To Do / Improvements

- [ ] Add authentication / user history
- [ ] Upload .docx support
- [ ] See reports Web Page
- [ ] Graphical chart improvements (Bar chart, Radar chart, etc.)

---

## ⚠️ Disclaimer & Legal Notice

> **Important**:
> This project is intended **only for educational and non-commercial research purposes**.

- ❌ Do not use this tool to scrape LinkedIn at scale or bypass LinkedIn’s terms.
- ✅ This tool does not store any user credentials or personal data.
- ⚖️ Respect ethical guidelines while testing scraping logic.
- 🧪 All data shown in demos is anonymized or synthetic.

---

## 👤 Author

**Manish Yadav**

- 💼 [LinkedIn](https://www.linkedin.com/in/manishgk9)
- 🐦 [Twitter/X](https://x.com/manishgk9)
- 💻 [GitHub](https://github.com/manishgk9)

> For collaboration, issues, or improvements, feel free to open a PR or contact me!

---

## 🧠 Contribution Ideas

- Add resume export as PDF
- Use charts (bar, radar) to display scores
- Add user authentication & dashboards
- Use vector DB for similarity search on resumes

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for more details.

---

> Made with ❤️ using FastAPI, React, and Generative AI.

## 💬 Contact

Built with ❤️ by [Manish Yadav](https://github.com/manishgk9)

---
