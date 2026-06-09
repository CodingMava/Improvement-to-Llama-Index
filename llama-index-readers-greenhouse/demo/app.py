import os
import json
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Document
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import Settings

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Fetch the key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("CRITICAL ERROR: GEMINI_API_KEY not found in .env file.")

# Configure LlamaIndex Core Settings
Settings.llm = GoogleGenAI(model="gemini-2.5-flash", api_key=api_key)
Settings.embed_model = GoogleGenAIEmbedding(model="models/text-embedding-004", api_key=api_key)

MOCK_JSON_PATH = os.path.join(os.path.dirname(__file__), 'demo_candidates.json')

class MockGreenhouseReader:
    """Simulates the real GreenhouseReader for local testing."""
    def __init__(self, json_path: str):
        self.json_path = json_path

    def load_data(self):
        with open(self.json_path, 'r') as f:
            candidates = json.load(f)
        
        documents = []
        for candidate in candidates:
            text_content = f"Candidate Name: {candidate.get('first_name', '')} {candidate.get('last_name', '')}\n"
            text_content += f"Company: {candidate.get('company', 'Unknown')}\n"
            text_content += f"Title: {candidate.get('title', 'Unknown')}\n"
            
            tags = [tag.get('name') for tag in candidate.get('tags', [])]
            text_content += f"Tags: {', '.join(tags)}\n"

            metadata = {
                "candidate_id": candidate.get("id"),
                "source": "greenhouse_ats_mock"
            }
            documents.append(Document(text=text_content, metadata=metadata))
        return documents

# UI ROUTE - Serves the main dashboard
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# API ROUTE - Returns raw candidates for UI listing
@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    try:
        with open(MOCK_JSON_PATH, 'r') as f:
            candidates = json.load(f)
        return jsonify(candidates), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# API ROUTE - Executes RAG pipeline query
@app.route('/api/analyze_candidates', methods=['GET'])
def analyze_candidates():
    try:
        reader = MockGreenhouseReader(MOCK_JSON_PATH)
        docs = reader.load_data()
        index = VectorStoreIndex.from_documents(docs)
        
        query_engine = index.as_query_engine()
        query = request.args.get('query', 'Who are the candidates and what are their strengths?')
        response = query_engine.query(query)
        
        return jsonify({
            "status": "success",
            "query": query,
            "response": str(response)
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)