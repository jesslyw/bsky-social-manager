from langchain_ollama import OllamaEmbeddings
from config import BIL_API_KEY, BASE_URL

def get_embeddings():
    return OllamaEmbeddings(
        model="jina/jina-embeddings-v2-base-de",
        base_url=BASE_URL,
        client_kwargs={
            "headers": {
                "Authorization": f"Bearer {BIL_API_KEY}"
            }
        }
    )
