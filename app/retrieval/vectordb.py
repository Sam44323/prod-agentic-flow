from langchain_chroma import Chroma
from app.config import settings

from app.retrieval.embeddings import embeddings

# creating the vector-db core-object using the embeddings
vector_store = Chroma(
    collection_name="agentic_rag",
    embedding_function=embeddings,
    persist_directory=settings.CHROMA_PATH,  # storing the data in the local-directory (disk)
)
