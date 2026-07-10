from langchain_chroma import Chroma

from app.retrieval.embeddings import embeddings

# creating the vector-db core-object using the embeddings
vector_store = Chroma(
    collection_name="agentic_rag",
    embedding_function=embeddings,
    persist_directory="./data/chroma",  # storing the data in the local-directory (disk)
)
