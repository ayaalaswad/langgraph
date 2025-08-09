# graph/llm_node.py - ذكي مع البحث التلقائي

import sys
import os

# إضافة المجلد الرئيسي للمسار
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import TypedDict, Annotated
from config.config import load_system_prompt

class State(TypedDict):
    messages: Annotated[list, ...]

def llm_node(state: State, model):
    """عقدة LLM ذكية مع بحث تلقائي"""
    try:
        # الحصول على آخر رسالة
        last_message = state["messages"][-1] if state["messages"] else ""
        user_input = ""
        
        if isinstance(last_message, tuple):
            user_input = last_message[1]
        elif hasattr(last_message, 'content'):
            user_input = last_message.content
        else:
            user_input = str(last_message)
        
        # فحص إذا كان يحتاج بحث
        search_keywords = [
            'api', 'apis', 'endpoint', 'endpoints', 
            'authentication', 'auth', 'login', 'signin',
            'visa', 'travel', 'user', 'management',
            'ابحث', 'بحث', 'ابحثلي', 'اظهر', 'اعرض',
            'find', 'search', 'show', 'get', 'post', 'delete', 'put'
        ]
        
        needs_search = any(keyword.lower() in user_input.lower() for keyword in search_keywords)
        
        if needs_search:
            print(f"🔍 البحث مطلوب للسؤال: {user_input}")
            
            # استيراد دالة البحث
            try:
                from tools.chroma_search_tool import search_apis
                search_result = search_apis(user_input)
                
                # prompt محسن مع نتائج البحث
                enhanced_prompt = f"""
المستخدم سأل: {user_input}

نتائج البحث في قاعدة البيانات:
{search_result}

قم بالإجابة على سؤال المستخدم باستخدام المعلومات من نتائج البحث أعلاه.
اجعل الإجابة مفيدة ومنظمة.
"""
                
                # استدعاء LLM مع البيانات
                messages = [("system", load_system_prompt()), ("user", enhanced_prompt)]
                response = model.invoke(messages)
                
            except Exception as e:
                print(f"❌ خطأ في البحث: {e}")
                # إجابة عادية لو فشل البحث
                messages = [("system", load_system_prompt())] + state["messages"]
                response = model.invoke(messages)
        else:
            print(f"💬 إجابة عادية للسؤال: {user_input}")
            
            # إجابة عادية بدون بحث
            messages = [("system", load_system_prompt())] + state["messages"]
            response = model.invoke(messages)
        
        # إرجاع الإجابة
        if hasattr(response, 'content'):
            return {"messages": [("assistant", response.content)]}
        else:
            return {"messages": [("assistant", str(response))]}
        
    except Exception as e:
        print(f"❌ Error in llm_node: {e}")
        return {"messages": [("assistant", f"عذراً، حدث خطأ: {str(e)}")]}

# اختبار
if __name__ == "__main__":
    print("🧪 Testing smart llm_node...")
    try:
        prompt = load_system_prompt()
        print(f"✅ System prompt loaded: {len(prompt)} characters")
        
        from tools.chroma_search_tool import search_apis
        result = search_apis("test")
        print(f"✅ Search function works: {len(result)} characters")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")