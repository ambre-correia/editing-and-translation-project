from typing import List
from .models import Sentence, CorrectionResponse
from .docx_parser import parse_docx
from .chunker import Chunker
from .llm_client import LLMClient
from .annotator import DocxAnnotator

class CoreProcessor:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.chunker = Chunker()
        
    async def process_document(self, file_path: str) -> List[CorrectionResponse]:
        """
        Full document processing pipeline:
        1. Parse DOCX into sentences
        2. Chunk sentences for LLM processing
        3. Call LLM for corrections
        4. Return structured results
        """
        # Step 1: Parse the document
        sentences = parse_docx(file_path)
        
        # Step 2: Chunk sentences
        chunks = self.chunker.chunk_sentences(sentences)
        
        # Step 3: Process each chunk with LLM
        all_corrections = []
        
        for i, chunk in enumerate(chunks):
            # Prepare prompt for this chunk
            prompt = self.chunker.prepare_prompt(chunk)
            
            # Call LLM (this is where the actual API call would happen)
            try:
                # In a real implementation, you'd call:
                # corrections = await self.llm_client.call_llm(prompt)
                
                # For demonstration, we'll simulate a response
                print(f"Processing chunk {i+1} with {len(chunk)} sentences...")
                
                # Mock response - in reality this would be from the LLM
                # This is where you'd add actual correction logic
                corrections = None
                
            except Exception as e:
                raise Exception(f"Failed to process chunk {i+1}: {str(e)}")
        
        return all_corrections
    
    def generate_annotated_document(self, input_file_path: str, output_file_path: str,
                                  sentences: List[Sentence], issues: List[CorrectionIssue]):
        """
        Generate an annotated version of the document with corrections.
        """
        annotator = DocxAnnotator()
        annotator.annotate_document(input_file_path, output_file_path, sentences, issues)