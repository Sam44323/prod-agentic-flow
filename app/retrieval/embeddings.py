from langchain_ollama import OllamaEmbeddings

# creating the embeddings core-object
# it overall gives the embeddings for the user-input
# which means for example, if the user-input is "hello"
# the embeddings will be the embeddings be in terms of vector-space
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)
