# graph/graph_builder.py - بسيط بدون tools

import sys
import os

# إضافة المجلد الرئيسي للمسار
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, START, END
from .llm_node import llm_node, State
from swagger.config import LLMConfig
from langchain_openai import ChatOpenAI

def build_graph():
    """بناء graph بسيط بدون tools"""
    
    print("🏗️ بناء الـ graph...")
    
    graph_builder = StateGraph(State)
    llm_conf = LLMConfig()
    llm = ChatOpenAI(temperature=llm_conf.TEMPERATURE, model=llm_conf.MODEL_NAME)
    
    print("✅ تم إنشاء ChatOpenAI بنجاح!")
    
    # عقدة واحدة فقط - llm ذكي
    graph_builder.add_node("llm", lambda state: llm_node(state, llm))
    
    # توصيل بسيط: START → llm → END
    graph_builder.add_edge(START, "llm")
    graph_builder.add_edge("llm", END)
    
    graph = graph_builder.compile()
    print("✅ تم بناء الـ graph بنجاح!")
    
    return graph

# اختبار
def test_graph():
    try:
        print("🧪 Testing simple graph...")
        graph = build_graph()
        
        # اختبار تشغيل
        test_state = {"messages": [("user", "ابحثلي عن APIs للمصادقة")]}
        result = graph.invoke(test_state)
        
        print("🎉 Graph test successful!")
        print(f"📋 Response preview: {str(result)[:100]}...")
        
        return graph
    except Exception as e:
        print(f"❌ Graph test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_graph()