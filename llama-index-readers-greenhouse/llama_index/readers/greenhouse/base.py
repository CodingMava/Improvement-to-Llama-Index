import os
import requests
from typing import List, Optional
from llama_index.core.readers.base import BasePydanticReader
from llama_index.core.schema import Document

class GreenhouseReader(BasePydanticReader):
    """Greenhouse ATS reader.
    
    Extracts candidate information and interview feedback from the Greenhouse Harvest API.
    """
    api_key: str
    base_url: str = "https://harvest.greenhouse.io/v1"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Greenhouse API key."""
        api_key = api_key or os.environ.get("GREENHOUSE_API_KEY")
        if not api_key:
            raise ValueError("Greenhouse API key is required. Pass it in or set GREENHOUSE_API_KEY env var.")
        
        super().__init__(api_key=api_key)

    def load_data(self, limit: int = 100) -> List[Document]:
        """Load candidate records from Greenhouse.
        
        Args:
            limit (int): Maximum number of candidates to fetch.
        """
        documents = []
        headers = {
            "Authorization": f"Basic {self._get_auth_token()}",
            "Content-Type": "application/json"
        }

        # Fetch candidates
        response = requests.get(
            f"{self.base_url}/candidates", 
            headers=headers,
            params={"per_page": min(limit, 500)} # Greenhouse max per page is 500
        )
        response.raise_for_status()
        
        candidates = response.json()

        for candidate in candidates:
            # Construct a rich text representation of the candidate
            text_content = f"Candidate Name: {candidate.get('first_name', '')} {candidate.get('last_name', '')}\n"
            text_content += f"Company: {candidate.get('company', 'Unknown')}\n"
            text_content += f"Title: {candidate.get('title', 'Unknown')}\n"
            
            # Extract tags
            tags = [tag.get('name') for tag in candidate.get('tags', [])]
            text_content += f"Tags: {', '.join(tags)}\n"

            # Attach robust metadata for filtering in the Vector Store
            metadata = {
                "candidate_id": candidate.get("id"),
                "application_ids": [app.get("id") for app in candidate.get("applications", [])],
                "source": "greenhouse_ats"
            }

            doc = Document(text=text_content, metadata=metadata)
            documents.append(doc)

            if len(documents) >= limit:
                break

        return documents

    def _get_auth_token(self) -> str:
        """Greenhouse uses Basic Auth with the API key as the username and a blank password."""
        import base64
        token = f"{self.api_key}:"
        return base64.b64encode(token.encode('utf-8')).decode('utf-8')