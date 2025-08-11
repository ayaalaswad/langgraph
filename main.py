from apps.services.graph.graph2 import build_react_graph   

graph = build_react_graph()

while True:
    question = input("ask here: ")
    if question == "exit":
        break
   
    
    print("answer: ", end="", flush=True)
    complete_answer = ""
    
    for chunk in graph.stream({"messages": [("user", question)]}, stream_mode="values"):
        if not isinstance(chunk, dict):
            continue

        for node_name, node_data in chunk.items():
            # تأكد أن node_data عبارة عن dict وفيه messages
            msgs = []
            if isinstance(node_data, dict):
                msgs = node_data.get("messages", [])
            elif isinstance(node_data, list):
                msgs = node_data  # إذا طلع list، اعتبره مباشرةً messages

            if not msgs:
                continue

            last_message = msgs[-1]

            # استخرج محتوى الـ AI فقط
            ai_content = None
            if isinstance(last_message, tuple):
                # متوقع شكل: (role, content)
                role = last_message[0] if len(last_message) > 0 else None
                content = last_message[1] if len(last_message) > 1 else ""
                if role in ("ai", "assistant"):
                    ai_content = content
            else:
                # كائن Message من لانغتشين/لانغراف
                if getattr(last_message, "type", "") == "ai":
                    ai_content = getattr(last_message, "content", "") or ""

            # اطبع فقط الجزء الجديد من جواب الـ AI
            if ai_content:
                new_part = ai_content[len(complete_answer):]
                if new_part:
                    print(new_part, end="", flush=True)
                    complete_answer += new_part

print()
