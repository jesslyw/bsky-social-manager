from langgraph.graph import StateGraph, END
from nodes.classification.sentiment_classification import classify_sentiment
from nodes.classification.intent_classification import classify_intent
from graph_state_schema import MyGraphState
from nodes.rag.flow import create_rag_flow
from flask import Flask, Response, json, request, jsonify

app = Flask(__name__)
rag_node = create_rag_flow()
graph = StateGraph(state_schema=MyGraphState)

graph.add_node("classify_sentiment", classify_sentiment)
graph.add_node("classify_intent", classify_intent)
graph.add_node("RAG", rag_node)

graph.set_entry_point("classify_sentiment")


classifier = graph.compile()


@app.route('/analyze-comment', methods=['POST'])
def analyze_comment():
    data = request.get_json()
    comment = data.get("input_data", "").strip()
    print(comment)
    if not comment:
        return jsonify({"error": "No comment provided"}), 400

    output = classifier.invoke({"comment": comment})
    output_state = MyGraphState.model_validate(output)

    return Response(
        json.dumps({
            "data": {
                "graph_output": output_state.model_dump()
            }
        }, ensure_ascii=False, indent=2),
        content_type="application/json"
    )


if __name__ == "__main__":
    app.run(debug=True)
