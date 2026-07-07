from dotenv import load_dotenv
import os

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
