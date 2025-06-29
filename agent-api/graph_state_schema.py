from pydantic import BaseModel, Field
import operator
from typing import Annotated
# state schema for a social media comment


class MyGraphState(BaseModel):
    comment: str
    sentiment_result: str | None = None
    intent_result: str | None = None
    like: bool = False
    reply: bool = False
    repost: bool = False
    reply_text: str | None = None
    flag: bool = False
    feedback: bool = False
    question: bool = False
    answer: str | None = None
    hitl_required: bool = False
    hitl_from_rag_failure: bool = False
    hitl_from_sentiment: bool = False
    hitl_from_intent: bool = False
    hitl_reviewed: bool = False
