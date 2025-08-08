from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition, create_react_agent
from graph.llm_node import llm_node, State
from config import LLMConfig
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from config.config import DatabaseConfig
from chroma_search_tool import ChromaSearchTool


def build_graph():
    graph_builder = StateGraph(State)
    llm_conf = LLMConfig()
    llm = ChatOpenAI(temperature=llm_conf.TEMPERATURE, model=llm_conf.MODEL_NAME)
    tools = [ChromaSearchTool()]
    model_with_tools = llm.bind_tools(tools)

    graph_builder.add_node("llm", lambda state: llm_node(state, model_with_tools))
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_edge(START, "llm")
    graph_builder.add_conditional_edges("llm", tools_condition, ["tools", END])
    graph_builder.add_edge("tools", "llm")
    graph = graph_builder.compile()
    return graph
