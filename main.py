from difflib import SequenceMatcher

from fastapi import FastAPI
from ai.ai_workflow import analyze_complaint
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
submitted_complaints = []


def normalize(value):
    return " ".join(str(value or "").lower().split())


def find_duplicate(complaint):
    product_name = normalize(complaint.get("productName"))
    batch_number = normalize(complaint.get("batchNumber"))
    description = normalize(complaint.get("description"))

    for previous in submitted_complaints:
        same_product = product_name == normalize(previous.get("productName"))
        same_batch = batch_number == normalize(previous.get("batchNumber"))
        description_similarity = SequenceMatcher(
            None, description, normalize(previous.get("description"))
        ).ratio()

        if same_product and same_batch and description_similarity >= 0.65:
            return "Possible duplicate complaint found for this product and batch."

    return None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "AIVOA Complaint Management System is running"}


@app.post("/complaints")
def create_complaint(complaint: dict):
    result = analyze_complaint(complaint)
    duplicate_warning = None

    if complaint.get("check_duplicate", False):
        duplicate_warning = find_duplicate(complaint)
        submitted_complaints.append(complaint.copy())

    return {
        "message": "Complaint recieved sucessfully",
        "ai_result": result,
        "duplicate_warning": duplicate_warning,
    }
    
