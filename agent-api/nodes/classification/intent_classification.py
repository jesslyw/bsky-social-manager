from graph_state_schema import MyGraphState
import requests
from config import BIL_API_KEY, BASE_URL
from langgraph.types import Command, Literal

llm_api_url = f"{BASE_URL}/v1/chat/completions"
api_key = BIL_API_KEY
model = "phi4:latest"

''' 
Intent classification via LLM for Positive and Neutral comments. 
Categories -> (action/bool flag):  
1. Question -> (forward to RAG), 
2. Praise -> (like: true)
3. Feedback -> (feedback: true)
4. Uncategorized -> (uncategorized: true)
'''


def classify_intent(state: MyGraphState) -> MyGraphState:
    print("2) entered intent classification")
    comment = state.comment

    prompt = (
        "You are an intent classifier.\n"
        "My company is called Red Books.\n"
        "Classify the following social media comment which could be in any language, as one of the following intent categories:\n"
        "1. Question — The comment asks a question or requests information.\n"
        "2. Praise — The comment expresses positive feedback or compliments, but doesn't have content worth reposting such as details that would be useful to potential customers.\n"
        "3. Feedback — The comment provides suggestions or criticism.\n"
        "4. Uncategorized — The comment does not fit into the other categories.\n"
        "5. Share — The comment is highly positive, relevant, or newsworthy and worth reposting to amplify.\n"
        "Respond with only one word: Question, Praise, Feedback, Uncategorized, or Share.\n"
        "Do not include any explanation or repeat the input. Just return one label.\n"
    )

    input_text = prompt + "\nComment: " + comment

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": input_text}]
    }

    print(llm_api_url)
    print(api_key)
    try:
        response = requests.post(
            llm_api_url, headers=headers, json=data, timeout=10)
        print("response")
        print(response)
        if response.status_code == 200:
            choices = response.json().get("choices", [])
            if choices:
                output = choices[0].get("message", {}).get(
                    "content", "No output")

                intent = output.strip()

                intent_lower = intent.lower()

                if intent_lower == "question":
                    return Command(
                        update={
                            "intent_result": intent,
                            "question": True
                        },

                        goto="RAG"
                    )
                elif intent_lower == "praise":
                    return Command(
                        update={
                            "intent_result": intent,
                            "like": True},
                        goto="END"
                    )
                elif intent_lower == "feedback":
                    return Command(
                        update={
                            "intent_result": intent,
                            "reply": True,
                            "feedback": True,
                            "hitl_required": True,
                            "hitl_from_sentiment": True
                        },
                        goto="END"
                    )
                elif intent_lower == "uncategorized":
                    return Command(
                        update={
                            "intent_result": intent,
                            "hitl_required": True,
                            "hitl_from_sentiment": True
                        },
                        goto="END"
                    )
                elif intent_lower == "share":
                    return Command(
                        update={
                            "intent_result": intent,
                            "repost": True
                        },
                        goto="END"
                    )

                else:

                    return Command(
                        update={"intent_result": intent,
                                "hitl_required": True},
                        goto="END"
                    )

    except requests.exceptions.Timeout:
        print("Request timed out, LLM currently not reachable.")
        return Command(
            update={"intent_result": "classifier unreachable",
                    "hitl_required": True},
            goto="END"
        )
