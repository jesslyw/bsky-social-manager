from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain.chains import RetrievalQA
from nodes.rag.llm import get_llm
from nodes.rag.vectorstore import get_vectorstore
from nodes.rag.prompts import get_prompt



class GraphState(TypedDict):
    comment: str
    answer: str


# def create_rag_flow():
#     retriever = get_vectorstore().as_retriever()
#     llm_chain = RetrievalQA.from_chain_type(
#             llm=get_llm(),
#             retriever=retriever,
#             chain_type="stuff",
#             chain_type_kwargs={"prompt": get_prompt()},
#             return_source_documents=True
#         )

#     def rag_node(state):
#         query = state["question"]
#         result = llm_chain.invoke({"query": query})
#         return {"question": query, "answer": result["result"]}

    # graph = StateGraph(GraphState)
    # graph.add_node("RAG", rag_node)
    # graph.set_entry_point("RAG")
    # graph.set_finish_point("RAG")
    # return graph.compile()
