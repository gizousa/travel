# pylint: disable=invalid-name
import operator
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END

KNOWLEDGE_BASE = {
    "如何申请报销？": "要申请报销，请填写报销表，并将其与所有相关收据一起提交给您的经理。",
    "公司的差旅政策是什么？": "公司的差旅政策规定，所有差旅都必须提前两周预订，并且必须在预算范围内。",
    "如何预订会议室？": "要预订会议室，请使用AI接待功能并指定与会人数和会议时长。",
}


@tool
def query_knowledge_base(query: str):
    """Queries the knowledge base for information."""
    return KNOWLEDGE_BASE.get(query, "Sorry, I don't have an answer for that.")


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


class KnowledgeBaseAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash").bind_tools([query_knowledge_base])
        builder = StateGraph(AgentState)
        builder.add_node("llm", self.call_llm)
        builder.set_entry_point("llm")
        builder.add_edge("llm", END)
        self.graph = builder.compile()

    def call_llm(self, state: AgentState):
        messages = state["messages"]
        response = self.llm.invoke(messages)
        return {"messages": [response]}