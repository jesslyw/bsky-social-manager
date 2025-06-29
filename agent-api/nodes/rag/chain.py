from langchain.chains import RetrievalQA
from rag.llm import get_llm
from rag.prompts import get_prompt
from rag.vectorstore import get_vectorstore

def get_rag_chain():
    retriever = get_vectorstore().as_retriever()
    llm = get_llm()
    prompt = get_prompt()
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

