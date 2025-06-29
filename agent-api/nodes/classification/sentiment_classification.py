from transformers import pipeline
from graph_state_schema import MyGraphState
from langgraph.types import Command, Literal

pipe = pipeline("text-classification",
                model="tabularisai/multilingual-sentiment-analysis")


def classify_sentiment(state: MyGraphState) -> Command[Literal["classify_intent"]]:
    sentiment_dict = pipe(state.comment)[0]
    sentiment_dict_label = sentiment_dict["label"]

    allowed = {"Neutral", "Positive", "Very Positive"}

    if sentiment_dict_label in allowed:
        return Command(
            update={"sentiment_result": sentiment_dict_label},
            goto="classify_intent"
        )

    else:
        return Command(
            update={"sentiment_result": sentiment_dict_label,
                    "hitl_required": True, "hitl_from_sentiment": True},
            goto="END"
        )
