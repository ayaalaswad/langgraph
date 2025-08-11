# إنشئ ملف chat.py:
from graph.graph_builder import build_graph

graph = build_graph()

while True:
    question = input("ask here: ")
    if question == "exit":
        break
    
    response = graph.invoke({"messages": [("user", question)]})
    last_message = response["messages"][-1]
    if isinstance(last_message, tuple):
        answer = last_message[1]  # ← الإجابة في العنصر الثاني
    else:
        answer = str(last_message)
    print("الجواب:", answer)
