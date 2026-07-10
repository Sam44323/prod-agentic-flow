from langchain_core.documents import Document
from app.config import settings

from app.retrieval.vectordb import vector_store


# core-retriever function
def retrieve(query: str, k: int = 4) -> list[Document]:
    return vector_store.similarity_search(
        query=query,
        k=k,
        timeout=settings.RETRIEVAL_TIMEOUT,
    )
