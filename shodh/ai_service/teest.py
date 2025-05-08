from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from datetime import datetime

app = FastAPI()

# Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

summarizer = pipeline("text2text-generation", model="google/flan-t5-small")

@app.post("/generate-post/")
async def generate_post(request: Request):
    try:
        # Get the explanation from the request
        data = await request.json()
        explanation = data.get("explanation", "")
        
        # If explanation is not provided, return an error
        if not explanation:
            return {"error": "Missing 'explanation' in request"}

        # Generate the post content based on the explanation
        result = summarizer(explanation, max_length=300, do_sample=False)[0]["generated_text"]

        # Automatically generate a title (can be a simple truncated version of the explanation)
        title = explanation[:50] + "..." if len(explanation) > 50 else explanation

        # Construct the Post model response based on the generated text
        post_data = {
            "author": "sample_author_id",  # You can replace this with actual author data later
            "title": title,  # Title generated from the explanation
            "category": "news",  # Default category
            "summary": result[:100],  # First 100 characters as summary
            "content": result,  # Full content as generated post
            "image_url": None,  # Image URL can be left empty or you can provide one
            "tags": "AI, Event",  # Default tags or you can set it as needed
            "views": 0,  # Default views
            "is_published": True,  # Default to published
            "published_at": datetime.now().isoformat(),  # Current timestamp
            "updated_at": datetime.now().isoformat(),  # Current timestamp
            "target_branches": [],  # Empty for now; update as needed
            "target_years": [],  # Empty for now; update as needed
        }

        # Return the generated post as a response
        return {"generated_post": post_data}
    except Exception as e:
        return {"error": str(e)}
