# main.py
import asyncio
import urllib.parse
from fastapi import FastAPI
from scrappers.indeed import scrape_indeed
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Set up CORS to allow requests from the Next.js frontend
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}


#indeed listings
@app.get("/indeed_jobs")
async def get_jobs(job_name: str, location: str):
    # URL encode job name and location to handle spaces and special characters
    encoded_job_name = urllib.parse.quote_plus(job_name)
    encoded_location = urllib.parse.quote_plus(location)

    # Construct the URL dynamically
    job_url = f"https://www.indeed.com/jobs?q={encoded_job_name}&l={encoded_location}&radius=50&fromage=1"

    # Call the scrape_indeed function and get job listings
    jobs = await scrape_indeed(job_url)
    return {"jobs": jobs}  # Return jobs as JSON

#xvfb-run -a uvicorn main:app --reload
