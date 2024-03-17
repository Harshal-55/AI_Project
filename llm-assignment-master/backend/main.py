from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any

# Import necessary modules for file handling and text processing
import os
import tempfile
import textract

# Load environment variables from .env file (if any)
load_dotenv()

class Response(BaseModel):
    result: str | None

# Define allowed origins for CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

# Initialize FastAPI app
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Endpoint to handle file upload and user queries
@app.post("/predict", response_model=Response)
async def predict(file: UploadFile = File(...), query: str = "") -> Any:
    try:
        # Check if the file is of supported format
        if file.filename.endswith(('.txt', '.docx', '.pdf')):
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(await file.read())
                tmp_name = tmp.name

            # Process the uploaded file based on its format
            if file.filename.endswith('.txt'):
                text = extract_text_from_txt(tmp_name)
            elif file.filename.endswith('.docx'):
                text = extract_text_from_docx(tmp_name)
            elif file.filename.endswith('.pdf'):
                text = extract_text_from_pdf(tmp_name)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format")

            # Perform text processing based on the user query
            result = process_query(text, query)

            # Delete the temporary file
            os.remove(tmp_name)

            return {"result": result}
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions for text extraction and processing
def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text_from_docx(file_path: str) -> str:
    text = textract.process(file_path)
    return text.decode('utf-8')

def extract_text_from_pdf(file_path: str) -> str:
    text = textract.process(file_path)
    return text.decode('utf-8')

def process_query(text: str, query: str) -> str:
    # Implement your text processing logic here, e.g., search for query in text
    # For simplicity, let's just return the text if query is empty
    if not query:
        return text
    else:
        # Implement your query processing logic here
        # This is a placeholder implementation
        return f"Query: '{query}' not yet supported"
