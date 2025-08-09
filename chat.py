# إنشئ ملف chat.py:
from graph.graph_builder import build_graph

graph = build_graph()

while True:
    question = input("كم api endpoint عنا: ")
    if question == "exit":
        break
    
    response = graph.invoke({"messages": [("user", question)]})
    print("الجواب:", response["messages"][-1].content)