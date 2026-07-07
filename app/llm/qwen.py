from langchain_ollama import ChatOllama
from app.config import MODEL_NAME, OLLAMA_BASE_URL

# creating an LLM-Wrapper to avoid duplicating code
llm = ChatOllama(model_name=MODEL_NAME, base_url=OLLAMA_BASE_URL)

# getting the LLM instance for the interaction
def get_llm():
    return llm
