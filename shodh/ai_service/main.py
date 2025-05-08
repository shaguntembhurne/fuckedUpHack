from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Allow access from Django
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:8000"] for Django only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Hugging Face model (keep lightweight for now)
generator = pipeline("text2text-generation", model="google/flan-t5-large")

# Input format
class PostRequest(BaseModel):
    explanation: str

@app.post("/generate-post/")
def generate_post(data: PostRequest):
    prompt = (
        f"Generate a blog-style post in JSON format (with keys: title, summary, content, category, tags) "
        f"based on this explanation: '{data.explanation}'"
    )
    try:
        result = generator(prompt, max_length=512)[0]["generated_text"]

        # Try parsing output if it looks like JSON
        try:
            parsed = json.loads(result)
        except json.JSONDecodeError:
            # Try using eval() as a fallback
            parsed = eval(result)

        return parsed
    except Exception as e:
        return {"error": str(e)}
