# from fastapi import FastAPI
# from .routes import resume, linkedin, suggestion

# app = FastAPI(title="Resume & LinkedIn Analyzer")

# app.include_router(resume.router, prefix="/upload")
# app.include_router(linkedin.router, prefix="/linkedin")
# app.include_router(suggestion.router, prefix="/suggestion")
from fastapi import FastAPI
from app.routes import routes
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

list_urls=[
    "http://localhost/:8000",
    "http://localhost:5173"
]
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins = list_urls,
    allow_methods = ["*"],
    allow_headers = ["*"]
)