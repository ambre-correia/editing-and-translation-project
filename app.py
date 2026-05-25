#!/usr/bin/env python3

import os
import sys
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import json

# Add the docx_proofreader module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from docx_proofreader.models import Sentence, CorrectionResponse
from docx_proofreader.docx_parser import parse_docx
from docx_proofreader.chunker import Chunker
from docx_proofreader.core_processor import CoreProcessor
from docx_proofreader.llm_client import LLMClient

app = FastAPI(title="DOCX Proofreader API")

@app.get("/")
async def root():
    return {"message": "DOCX Proofreader API is running"}

@app.post("/proofread")
async def proofread_document(file: UploadFile = File(...)):
    """
    Process a DOCX file for proofreading.
    """
    try:
        # Check if the uploaded file is a .docx
        if not file.filename.endswith('.docx'):
            raise HTTPException(status_code=400, detail="Only .docx files are allowed")
        
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Parse the DOCX file
        sentences = parse_docx(temp_file_path)
        
        # Clean up temporary file
        os.remove(temp_file_path)
        
        # Chunk the sentences for LLM processing
        chunker = Chunker()
        chunks = chunker.chunk_sentences(sentences)
        
        # For demonstration, we'll return the sentences without actual LLM processing
        # In a real implementation, this would call an LLM API
        
        return {
            "sentences": [sentence.dict() for sentence in sentences],
            "chunks_count": len(chunks),
            "total_sentences": len(sentences)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)