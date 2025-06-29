from langgraph.graph import StateGraph, END
from langchain.chains import RetrievalQA
from nodes.rag.llm import get_llm
from nodes.rag.vectorstore import get_vectorstore
from nodes.rag.prompts import get_prompt
from langgraph.types import Command


def create_rag_flow():
    retriever = get_vectorstore().as_retriever()

    llm_chain = RetrievalQA.from_chain_type(
        llm=get_llm(),
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": get_prompt()},
        return_source_documents=True
    )

    def rag_node(state):
        # Only run RAG if question is True
        if not state.question:
            return state
        print("[RAG] entered RAG")
        query = state.comment
        result = llm_chain.invoke({"query": query})
        answer = result.get("result", "").strip()

        rag_failed = (
            not answer or
            "no relevant information found" in answer.lower()
        )

        if rag_failed:
            print("[RAG] failed")
            return Command(
                update={
                    "hitl_required": True,
                    "hitl_from_rag_failure": True,
                },
                goto="END"
            )
        print("[RAG] completed")
        return Command(
            update={
                "reply": True,
                "reply_text": answer,
                "hitl_required": True,
            },
            goto="END"
        )

    return rag_node
