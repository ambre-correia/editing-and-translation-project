from pydantic import BaseModel
from typing import List, Optional

class Sentence(BaseModel):
    paragraph_id: int
    sentence_id: int
    text: str

class CorrectionIssue(BaseModel):
    sentence_id: int
    type: str  # GRAMMAR | TYPO | TENSE | PREPOSITION | WORD_CHOICE | UNNATURAL
    issue: str
    fix: str
    suggestions: Optional[List[str]] = None

class CorrectionResponse(BaseModel):
    issues: List[CorrectionIssue]

class DocumentStructure(BaseModel):
    sentences: List[Sentence]