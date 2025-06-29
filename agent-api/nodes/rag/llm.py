from langchain_openai import ChatOpenAI
from config import BIL_API_KEY, BASE_URL


def get_llm():
    return ChatOpenAI(
        model="phi4:latest",
        api_key=BIL_API_KEY,
        base_url=f"{BASE_URL}/v1/",
        temperature=0.1
    )
