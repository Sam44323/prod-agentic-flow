from langchain_ollama import ChatOllama
from app.config import settings
from langchain_core.messages import BaseMessage

llm = ChatOllama(
    model=str(settings.MODEL_NAME),
    base_url=settings.OLLAMA_BASE_URL,
)


def generate(messages: list[BaseMessage]) -> str:
    response = llm.invoke(messages, timeout=settings.LLM_TIMEOUT)
    return str(response.content)


def get_llm() -> ChatOllama:
    return llm
