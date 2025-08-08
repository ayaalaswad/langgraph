from typing import TypedDict, Annotated
from langgraph.prebuilt import tools_condition
from config import load_system_prompt
from langchain_openai import ChatOpenAI
from config import LLMConfig

class State(TypedDict):
    messages: Annotated[list, ...]  # placeholder for any validator/decorator logic

def llm_node(state: State, model):
    system_prompt = load_system_prompt()
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": response}
