"""
RAG Chain module for the chatbot backend.
Configures LangChain with Qdrant vector store and OpenAI for retrieval-augmented generation.
"""
from typing import Dict, Any, List
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from qdrant_client import QdrantClient
from config import config


class RAGChain:
    """
    Retrieval-Augmented Generation chain for portfolio chatbot.
    Handles vector store retrieval and LLM-based question answering.
    """

    def __init__(self):
        """Initialize RAG chain components"""
        # Validate configuration
        config.validate()

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY,
        )

        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY,
        )

        # Initialize vector store
        self.vector_store = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=config.COLLECTION_NAME,
            embedding=self.embeddings,
        )

        # Initialize retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": config.RETRIEVER_K,
                "score_threshold": config.SCORE_THRESHOLD,
            },
        )

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE,
            openai_api_key=config.OPENAI_API_KEY,
        )

        # Create prompt template
        self.prompt_template = self._create_prompt_template()

        # Build RAG chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template},
        )

    def _create_prompt_template(self) -> PromptTemplate:
        """
        Create the prompt template for the RAG chain.

        Returns:
            PromptTemplate: Configured prompt template for recruitment assistant
        """
        template = """You are a professional recruitment assistant for James Brendamour's portfolio website.

Your role is to help recruiters and hiring managers learn about James's qualifications:
- Technical skills and expertise
- Professional experience and projects
- Education and certifications
- Blog articles and thought leadership

Guidelines:
- Be professional, concise, and helpful
- Use the context provided to answer accurately
- If the answer isn't in the context, acknowledge that honestly
- Highlight relevant skills and achievements
- Provide specific examples when available
- Keep responses focused and to-the-point
- Don't make up information not present in the context

Context from James's portfolio:
{context}

Question: {question}

Professional Answer:"""

        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

    async def query(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG chain with a question.

        Args:
            question: User's question

        Returns:
            Dictionary with response and source documents
        """
        try:
            # Run the QA chain
            result = await self.qa_chain.ainvoke({"query": question})

            # Extract response and sources
            response_text = result.get("result", "")
            source_docs = result.get("source_documents", [])

            # Format sources for response
            sources = self._format_sources(source_docs)

            return {
                "response": response_text,
                "sources": sources,
                "success": True,
            }

        except Exception as e:
            return {
                "response": f"I apologize, but I encountered an error: {str(e)}",
                "sources": [],
                "success": False,
                "error": str(e),
            }

    def _format_sources(self, source_docs: List[Any]) -> List[Dict[str, Any]]:
        """
        Format source documents for API response.

        Args:
            source_docs: List of source documents from retrieval

        Returns:
            List of formatted source dictionaries
        """
        sources = []
        for doc in source_docs:
            source_info = {
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata,
            }
            sources.append(source_info)

        return sources

    def health_check(self) -> Dict[str, Any]:
        """
        Check health of RAG chain components.

        Returns:
            Dictionary with health status
        """
        try:
            # Check Qdrant connection
            collections = self.qdrant_client.get_collections()
            collection_exists = any(
                col.name == config.COLLECTION_NAME
                for col in collections.collections
            )

            if not collection_exists:
                return {
                    "status": "unhealthy",
                    "message": f"Collection '{config.COLLECTION_NAME}' not found in Qdrant",
                    "vector_store": "disconnected",
                }

            # Get collection info
            collection_info = self.qdrant_client.get_collection(config.COLLECTION_NAME)

            return {
                "status": "healthy",
                "message": "RAG chain operational",
                "vector_store": "connected",
                "collection": config.COLLECTION_NAME,
                "vector_count": collection_info.vectors_count,
            }

        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Health check failed: {str(e)}",
                "vector_store": "error",
                "error": str(e),
            }


# Create a singleton instance
rag_chain = RAGChain()
