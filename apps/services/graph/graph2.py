import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from config import LLMConfig, load_system_prompt
from utils.search_tool import AVAILABLE_TOOLS

def build_react_graph():    
    print("🏗️ building ReAct Agent...")
    
    llm_config = LLMConfig()
    llm = ChatOpenAI(
        temperature=llm_config.TEMPERATURE, 
        model=llm_config.MODEL_NAME
    )
    
    print("✅  ChatOpenAI!")
    
    system_prompt = load_system_prompt()
    
    agent = create_react_agent(
        model=llm,
        tools=AVAILABLE_TOOLS,
        prompt=system_prompt  
    )
    
    print(f"✅ تم بناء ReAct Agent مع {len(AVAILABLE_TOOLS)} أدوات!")
    print(f"🛠️ الأدوات المتاحة: {[tool.name for tool in AVAILABLE_TOOLS]}")
    
    return agent