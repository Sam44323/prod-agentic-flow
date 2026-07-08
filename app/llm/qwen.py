from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage

from app.config import MODEL_NAME, OLLAMA_BASE_URL

llm = ChatOllama(
    model=str(MODEL_NAME),
    base_url=OLLAMA_BASE_URL,
)


def generate(messages: list[BaseMessage]) -> str:
    response = llm.invoke(messages)
    return str(response.content)


def get_llm() -> ChatOllama:
    return llm
