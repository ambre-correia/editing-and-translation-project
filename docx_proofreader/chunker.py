from typing import List
from .models import Sentence, CorrectionResponse

class Chunker:
    def __init__(self, max_words_per_chunk: int = 2000):
        self.max_words_per_chunk = max_words_per_chunk
    
    def chunk_sentences(self, sentences: List[Sentence]) -> List[List[Sentence]]:
        """
        Group sentences into chunks that don't exceed the maximum word count.
        Maintains sentence IDs across chunks and preserves ordering.
        """
        chunks = []
        current_chunk = []
        current_word_count = 0
        
        for sentence in sentences:
            # Estimate word count in the sentence
            word_count = len(sentence.text.split())
            
            # If adding this sentence would exceed the limit, start a new chunk
            if current_word_count + word_count > self.max_words_per_chunk and current_chunk:
                chunks.append(current_chunk)
                current_chunk = [sentence]
                current_word_count = word_count
            else:
                current_chunk.append(sentence)
                current_word_count += word_count
        
        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks
    
    def prepare_prompt(self, sentences: List[Sentence]) -> str:
        """
        Prepare a prompt for the LLM with sentence IDs and text.
        """
        prompt_parts = []
        
        # Add instructions
        prompt_parts.append("Please proofread these sentences. For each sentence, identify:")
        prompt_parts.append("- Grammar errors")
        prompt_parts.append("- Typos") 
        prompt_parts.append("- Incorrect word usage")
        prompt_parts.append("- Unnatural phrasing (only if clearly non-native or confusing)")
        prompt_parts.append("")
        prompt_parts.append("Return ONLY valid JSON in this exact format:")
        prompt_parts.append("{")
        prompt_parts.append('  "issues": [')
        prompt_parts.append('    {')
        prompt_parts.append('      "sentence_id": 12,')
        prompt_parts.append('      "type": "GRAMMAR | TYPO | TENSE | PREPOSITION | WORD_CHOICE | UNNATURAL",')
        prompt_parts.append('      "issue": "short description of problem",')
        prompt_parts.append('      "fix": "minimal correction OR corrected token/phrase",')
        prompt_parts.append('      "suggestions": ["optional", "only", "for unnatural phrasing"]')
        prompt_parts.append('    }')
        prompt_parts.append('  ]')
        prompt_parts.append("}")
        prompt_parts.append("")
        prompt_parts.append("IMPORTANT: ONLY return the JSON. No explanations, no additional text.")
        prompt_parts.append("")
        prompt_parts.append("Sentences:")
        prompt_parts.append("")
        
        # Add sentences with IDs
        for sentence in sentences:
            prompt_parts.append(f"{sentence.sentence_id}. {sentence.text}")
            
        return "\n".join(prompt_parts)