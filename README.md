# Greenhouse ATS Connector for LlamaIndex

A production-ready LlamaIndex data connector that enables AI applications to securely ingest candidate profiles, resumes, interview scorecards, and hiring feedback directly from Greenhouse ATS.

## Why This Project?

Modern companies store valuable hiring information inside Applicant Tracking Systems (ATS) such as Greenhouse. However, this data is difficult to access through AI-powered workflows.

This project bridges that gap by transforming Greenhouse candidate data into LlamaIndex Documents, making it instantly searchable by LLM-powered applications.

With this connector, teams can build:

* AI Recruiting Assistants
* Candidate Search Agents
* Talent Intelligence Platforms
* Hiring Analytics Systems
* Internal HR Knowledge Bases

---

## Problem

Recruiting teams often need answers to questions such as:

* Which candidates passed technical interviews this month?
* Show all Python developers with FastAPI experience.
* Which candidates received strong backend engineering feedback?
* Find candidates with cloud experience and interview scores above 8/10.

Today, answering these questions requires manually searching through hundreds or thousands of candidate records.

---

## Solution

This connector automatically:

1. Connects to Greenhouse Harvest API
2. Retrieves candidate information
3. Extracts interview feedback and scorecards
4. Converts records into LlamaIndex Documents
5. Makes data searchable through vector search and LLMs

The result is an AI-ready recruiting knowledge base.

---

## Architecture

```text
                +----------------------+
                |   Greenhouse ATS     |
                |   Harvest API        |
                +----------+-----------+
                           |
                           |
                           v
                +----------------------+
                |  Greenhouse Reader   |
                |  Data Connector      |
                +----------+-----------+
                           |
                           |
                           v
                +----------------------+
                |  LlamaIndex Docs     |
                +----------+-----------+
                           |
                           |
                           v
                +----------------------+
                |  Vector Database     |
                +----------+-----------+
                           |
                           |
                           v
                +----------------------+
                | Gemini / GPT / Claude|
                +----------------------+
```

---

## Features

✅ Greenhouse Harvest API Integration

✅ Candidate Profile Extraction

✅ Interview Feedback Parsing

✅ Resume Metadata Support

✅ LlamaIndex Document Conversion

✅ Vector Search Ready

✅ Gemini Compatible

✅ Open Source

✅ Modular Architecture

✅ Extensible for Future ATS Platforms

---

## Example Workflow

### Step 1

Load candidates from Greenhouse

```python
from greenhouse_reader.greenhouse import GreenhouseReader

reader = GreenhouseReader(
    api_key="YOUR_API_KEY"
)

documents = reader.load_data()
```

### Step 2

Create an index

```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)
```

### Step 3

Ask questions

```python
query_engine = index.as_query_engine()

response = query_engine.query(
    "Find candidates with Python and FastAPI experience"
)

print(response)
```

---

## Example AI Queries

* Show candidates with FastAPI experience.
* Find backend engineers who passed technical interviews.
* Which applicants received the highest interview scores?
* List candidates with AWS and Kubernetes skills.
* Find candidates recommended for final rounds.

---

## Project Structure

```text
llama-index-readers-greenhouse/

├── greenhouse_reader/
│   ├── __init__.py
│   └── greenhouse/
│       ├── __init__.py
│       └── base.py
│
├── demo/
│   └── app.py
│
├── tests/
│   └── test_greenhouse.py
│
├── README.md
├── CONTRIBUTING.md
├── pyproject.toml
└── .gitignore
```

---

## Technical Highlights

### Standard LlamaIndex Reader Interface

Built using the same reader architecture used throughout the LlamaIndex ecosystem.

### Metadata-Aware Documents

Each candidate record preserves structured metadata such as:

* Candidate ID
* Source System
* Application Status
* Interview Scores

This enables filtering before retrieval.

### RAG-Ready Design

The connector is designed specifically for Retrieval-Augmented Generation (RAG) systems.

Documents are converted into embeddings and stored in vector databases for efficient retrieval.

---

## Demo Application

A lightweight Flask demo demonstrates:

* Data ingestion
* Vector indexing
* Gemini integration
* Natural language candidate search

Example:

> Find Python developers who passed technical interviews and have AWS experience.

The system retrieves relevant candidates and generates a contextual answer using Gemini.

---

## Future Roadmap

* Resume PDF Parsing
* Greenhouse Webhook Support
* Incremental Syncing
* Candidate Embeddings Cache
* Pinecone Integration
* Qdrant Integration
* Chroma Integration
* Multi-ATS Support (Lever, Ashby, Workday)

---

## Why This Matters

Most AI recruiting systems still rely on custom scripts and fragmented integrations.

This project provides a reusable, open-source connector that helps organizations integrate Greenhouse data directly into modern AI workflows.

By contributing infrastructure instead of another chatbot demo, the goal is to strengthen the LlamaIndex ecosystem and make enterprise recruiting data more accessible to AI applications.

---

## Contributing

Contributions, reviews, and suggestions are welcome.

Potential areas for improvement:

* Additional Greenhouse endpoints
* Enhanced metadata extraction
* ATS interoperability
* Performance optimization



Built as an open-source contribution to expand the LlamaIndex ecosystem and demonstrate practical AI infrastructure engineering.
