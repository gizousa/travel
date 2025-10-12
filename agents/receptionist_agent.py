# pylint: disable=invalid-name
import operator
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage, HumanMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END


@tool
def send_notification(employee: str, visitor: str):
    """Sends a notification to an employee about a visitor."""
    return f"Notification sent to {employee}: Your visitor, {visitor}, has arrived."


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


class ReceptionistAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash").bind_tools([send_notification])
        builder = StateGraph(AgentState)
        builder.add_node("llm", self.call_llm)
        builder.set_entry_point("llm")
        builder.add_edge("llm", END)
        self.graph = builder.compile()

    def call_llm(self, state: AgentState):
        messages = state["messages"]
        response = self.llm.invoke(messages)
        return {"messages": [response]}