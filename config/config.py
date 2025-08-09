

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

class ChromaConfig:
    """إعدادات ChromaDB الأساسية فقط"""
    
    # الإعدادات الضرورية الوحيدة
    DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./my_chroma")
    COLLECTION_NAME: str = os.getenv("CHROMA_COLLECTION_NAME", "swagger_apis")
    
    # إعداد واحد إضافي مفيد (اختياري)
    MAX_RESULTS: int = int(os.getenv("CHROMA_MAX_RESULTS", "5"))
    
    @classmethod
    def get_config_dict(cls) -> dict:
        """إرجاع الإعدادات الأساسية فقط"""
        return {
            'db_path': cls.DB_PATH,
            'collection_name': cls.COLLECTION_NAME,
            'max_results': cls.MAX_RESULTS
        }
    
__all__ = ["DatabaseConfig", "LLMConfig", "ChromaConfig", "load_system_prompt"]