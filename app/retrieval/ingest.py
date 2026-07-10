from pathlib import Path
from app.config import settings
from app.logger import logger

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.retrieval.vectordb import vector_store

# getting the data from the /data/documents directory (for now it is empty anyways)
DATA_DIR = Path(settings.DOCUMENT_PATH)


def load_documents() -> list[Document]:
    documents = []

    for file in DATA_DIR.glob("*.txt"):
        text = file.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file.name,
                },
            )
        )

    return documents


def ingest() -> None:
    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        # this means that if a paragraph is greater than than 700 tokens, we will split it into smaller chunks
        chunk_size=1000,
        chunk_overlap=200,
    )

    # splitting the documents into chunks
    chunks = splitter.split_documents(documents)

    # adding the chunks to the vector-db
    vector_store.add_documents(chunks)

    logger.info(f"Added {len(documents)} documents to the vector-db.")


if __name__ == "__main__":
    ingest()
