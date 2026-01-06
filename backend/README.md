# RAG-Powered Chatbot Backend

Professional recruitment assistant chatbot powered by Qdrant, OpenAI GPT-4o-mini, and LangChain.

## Overview

This backend provides a RAG (Retrieval-Augmented Generation) API for the portfolio chatbot. It:
- Ingests data from multiple sources (resume PDF, portfolio config, GitHub repos, blog articles)
- Stores embeddings in Qdrant Cloud vector database
- Provides a FastAPI chat endpoint for the frontend
- Returns context-aware responses with source attribution

---

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Update Qdrant Cloud Credentials

**IMPORTANT**: The current Qdrant API key appears to have expired (403 Forbidden error).

You need to update your `.env` file with fresh Qdrant Cloud credentials:

1. Go to [Qdrant Cloud](https://cloud.qdrant.io/)
2. Log in to your account
3. Navigate to your cluster
4. Copy the **Cluster URL** (should look like: `https://xxxxx.us-east4-0.gcp.cloud.qdrant.io:6333`)
5. Generate a new **API Key**
6. Update `.env` file (in the **root directory**, not backend):

```bash
QDRANT_URL=your_new_cluster_url_here
QDRANT_API_KEY=your_new_api_key_here
```

**Note**: The `.env` file is in the project root `/Users/james/Library/CloudStorage/Dropbox/GitHub/jamesbmour-portfolio/.env`, not in the backend directory.

### 3. Verify OpenAI API Key

Make sure your OpenAI API key in `.env` is valid:

```bash
OPENAI_API_KEY=sk-proj-...
```

### 4. Run Data Ingestion

Once credentials are updated, run the ingestion pipeline:

```bash
cd backend
source venv/bin/activate
python ingest.py
```

This will:
- Load resume PDF from `../src/data/James-Brendamour-Resume.pdf`
- Parse `gitprofile.config.ts` for skills, experience, education, projects
- Fetch GitHub repositories via GitHub API
- Fetch blog articles from dev.to
- Embed all content using OpenAI text-embedding-3-small
- Create Qdrant collection `portfolio-chat`
- Ingest embeddings into Qdrant

Expected output:
```
============================================================
STARTING DATA INGESTION PIPELINE
============================================================

Creating collection: portfolio-chat
✓ Collection 'portfolio-chat' created

============================================================
LOADING DATA SOURCES
============================================================

Loading data source: resume_pdf
Loading resume PDF from: ../src/data/James-Brendamour-Resume.pdf
Loaded 3 pages from resume PDF
✓ Loaded 3 documents from resume_pdf

...

✓ Total documents loaded: 15
✓ Split into 42 chunks
✓ Ingested 42 chunks into Qdrant

============================================================
INGESTION COMPLETE!
============================================================
```

### 5. Verify Ingestion (Optional)

```bash
python test_ingestion.py --skip-query
```

This validates the Qdrant collection without using OpenAI credits.

---

## Running the Backend Server

### Start the Server

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Test the Server

In a new terminal:

```bash
cd backend
source venv/bin/activate
python test_chat.py
```

This runs several test queries to validate the chatbot responses.

---

## Running the Full Stack

### Terminal 1: Backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Terminal 2: Frontend

```bash
npm run dev
```

Then open `http://localhost:5173` in your browser and click the blue chat button in the **bottom-left corner**.

---

## API Endpoints

### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "RAG chain operational",
  "vector_store": "connected",
  "collection": "portfolio-chat",
  "vector_count": 42
}
```

### POST /api/chat

Chat with the RAG-powered assistant.

**Request:**
```json
{
  "message": "What are James's technical skills?"
}
```

**Response:**
```json
{
  "response": "James has extensive technical skills including...",
  "sources": [
    {
      "content": "Technical Skills: Python, Streamlit, Dash...",
      "metadata": {
        "source": "portfolio_config",
        "type": "skills"
      }
    }
  ],
  "success": true
}
```

---

## Architecture

### Data Flow

```
Resume PDF + Portfolio Config + GitHub + Blog
         ↓
  Text Chunking (1000 chars, 200 overlap)
         ↓
  OpenAI Embeddings (text-embedding-3-small)
         ↓
  Qdrant Cloud Storage
         ↓
  User Question → Similarity Search (k=4)
         ↓
  Context + Question → GPT-4o-mini
         ↓
  Response + Sources
```

### Components

- **config.py**: Environment configuration
- **rag_chain.py**: LangChain RAG pipeline
- **main.py**: FastAPI server
- **ingest.py**: Data ingestion pipeline
- **test_ingestion.py**: Validation script
- **test_chat.py**: API testing script

### Data Sources

1. **Resume PDF** (`../src/data/James-Brendamour-Resume.pdf`)
2. **Portfolio Config** (`gitprofile.config.ts`)
   - Skills (31 technologies)
   - Experience (EY, Freelance, Siemens)
   - Education (OSU, Georgia Tech)
   - External Projects (research papers)
3. **GitHub Repositories** (top 4 updated)
4. **Blog Articles** (dev.to, top 4 recent)

---

## Extensibility

### Adding New Data Sources

The ingestion pipeline uses an extensible loader pattern. To add new data sources:

1. Create a new loader class:

```python
class MarkdownLoader(DataLoader):
    def load(self) -> List[Document]:
        # Your loading logic here
        pass
```

2. Register the loader in `ingest.py`:

```python
pipeline.register_loader(
    "markdown_docs",
    MarkdownLoader("path/to/docs")
)
```

### Example: Adding Markdown Files

```python
from langchain_community.document_loaders import DirectoryLoader

class MarkdownDirectoryLoader(DataLoader):
    def __init__(self, directory: str):
        self.directory = directory

    def load(self) -> List[Document]:
        loader = DirectoryLoader(
            self.directory,
            glob="**/*.md",
            show_progress=True
        )
        docs = loader.load()

        # Add metadata
        for doc in docs:
            doc.metadata["source"] = "documentation"
            doc.metadata["type"] = "markdown"
            doc.metadata["last_updated"] = datetime.now().isoformat()

        return docs
```

---

## Troubleshooting

### 403 Forbidden from Qdrant

- **Cause**: Expired or invalid API key
- **Solution**: Generate new API key from Qdrant Cloud dashboard and update `.env`

### OpenAI Rate Limit

- **Cause**: Too many requests to OpenAI API
- **Solution**: Wait a few minutes or upgrade OpenAI plan

### Import Errors

- **Cause**: Missing dependencies
- **Solution**: `pip install -r requirements.txt`

### Collection Not Found

- **Cause**: Data ingestion not run
- **Solution**: `python ingest.py`

### CORS Errors in Frontend

- **Cause**: Backend not running or CORS configuration issue
- **Solution**: Ensure backend is running on port 8000. Vite proxy should handle CORS.

---

## Environment Variables

Required variables in `../.env`:

```bash
# OpenAI
OPENAI_API_KEY=sk-proj-...

# Qdrant Cloud
QDRANT_API_KEY=your_api_key_here
QDRANT_URL=https://xxxxx.us-east4-0.gcp.cloud.qdrant.io:6333

# Collection
COLLECTION_NAME=portfolio-chat

# Data Sources
GITHUB_USERNAME=jamesbmour
DEV_TO_USERNAME=jamesbmour
PORTFOLIO_CONFIG_PATH=../gitprofile.config.ts

# Frontend
VITE_API_URL=http://localhost:8000
```

---

## Next Steps

1. ✅ **Update Qdrant credentials** in `.env`
2. ✅ **Run data ingestion**: `python ingest.py`
3. ✅ **Start backend server**: `uvicorn main:app --reload`
4. ✅ **Start frontend**: `npm run dev`
5. ✅ **Test chatbot** at `http://localhost:5173`

---

## Production Deployment

For production deployment, consider:

1. **Docker Containerization**:
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Cloud Platform**: Deploy to Railway, Render, Fly.io, or AWS

3. **Environment Variables**: Use platform's secrets management

4. **Monitoring**: Add logging, error tracking (Sentry), and metrics

5. **Rate Limiting**: Implement API rate limiting for production

---

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the implementation plan: `/Users/james/.claude/plans/warm-kindling-cray.md`
- Test endpoints with `test_chat.py`
- Verify Qdrant connection with `test_ingestion.py`
