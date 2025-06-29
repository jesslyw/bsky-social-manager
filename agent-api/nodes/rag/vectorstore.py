from langchain_chroma import Chroma
from nodes.rag.embeddings import get_embeddings


def get_vectorstore():
    return Chroma(

        collection_name="langflow",
        persist_directory="chroma_db",
        embedding_function=get_embeddings(),
    )
