

import os
from dotenv import load_dotenv
load_dotenv()

class LLMConfig:
    
    TEMPERATURE: float = 0    
    MODEL_NAME: str = "gpt-4o"
    
def load_system_prompt() -> str:
    import os
    prompt_path = os.path.join(os.path.dirname(__file__), 'search_agent_prompt.md')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()
    
__all__ = ["DatabaseConfig", "LLMConfig", "load_system_prompt"]
