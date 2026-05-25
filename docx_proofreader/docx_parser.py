import re
from typing import List
from docx import Document
from .models import Sentence

def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences while preserving sentence boundaries.
    """
    # Split on sentence endings but keep the delimiters
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s+', text)
    
    # Filter out empty strings
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences

def parse_docx(file_path: str) -> List[Sentence]:
    """
    Parse a DOCX file and extract sentences with their paragraph IDs.
    """
    doc = Document(file_path)
    
    sentences = []
    sentence_id = 0
    
    for paragraph_id, paragraph in enumerate(doc.paragraphs):
        if not paragraph.text.strip():
            continue
            
        # Split paragraph into sentences
        paragraph_sentences = split_into_sentences(paragraph.text)
        
        for sentence_text in paragraph_sentences:
            sentence_id += 1
            sentences.append(Sentence(
                paragraph_id=paragraph_id,
                sentence_id=sentence_id,
                text=sentence_text
            ))
    
    return sentences