from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

load_dotenv()


class Settings(BaseSettings):
    # models
    MODEL_NAME = os.getenv("MODEL_NAME")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")

    # timeouts
    WEATHER_TIMEOUT: int = 10
    RETRIEVAL_TIMEOUT: int = 5
    LLM_TIMEOUT: int = 120
    GRAPH_TIMEOUT: int = 180

    # storage
    CHROMA_PATH: str = "./data/chroma"
    DOCUMENT_PATH: str = "./data/documents"


settings = Settings()
