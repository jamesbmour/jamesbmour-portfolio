"""
Configuration module for the RAG chatbot backend.
Loads environment variables and provides configuration settings.
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for backend settings"""

    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Qdrant Configuration
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "portfolio-chat")

    # Model Configuration
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))

    # Data Sources
    GITHUB_USERNAME: str = os.getenv("GITHUB_USERNAME", "jamesbmour")
    DEV_TO_USERNAME: str = os.getenv("DEV_TO_USERNAME", "jamesbmour")
    PORTFOLIO_CONFIG_PATH: str = os.getenv("PORTFOLIO_CONFIG_PATH", "../gitprofile.config.ts")

    # CORS Configuration
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,https://jamesbmour.com,https://www.jamesbmour.com"
    ).split(",")

    # RAG Configuration
    RETRIEVER_K: int = int(os.getenv("RETRIEVER_K", "4"))
    SCORE_THRESHOLD: float = float(os.getenv("SCORE_THRESHOLD", "0.7"))

    # Text Splitting Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present"""
        required_vars = [
            ("OPENAI_API_KEY", cls.OPENAI_API_KEY),
            ("QDRANT_API_KEY", cls.QDRANT_API_KEY),
            ("QDRANT_URL", cls.QDRANT_URL),
        ]

        missing = [var_name for var_name, var_value in required_vars if not var_value]

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please check your .env file and ensure all required variables are set."
            )

        return True


# Create a singleton instance
config = Config()
