# tools/search_tool.py
from langchain.tools import tool
from utils.chroma_search_tool import search_apis
from typing import Annotated

@tool

def search_swagger_apis(query: Annotated[str, "The Chromadb search to provide information about apis from their swagger api."],
):
    """
    Search in the Swagger APIs database.
    
    Use this tool when the user asks about:
    - Specific API endpoints
    - How to implement certain functions
    - Authentication information
    - Details about HTTP methods
    - Any technical information about APIs
    
    Args:
        query: The text to search for
    
    Returns:
        Search results from the database
    """

    try:
        result = search_apis(query)
        return result
    except Exception as e:
        return f"❌ خطأ في البحث: {str(e)}"


AVAILABLE_TOOLS = [search_swagger_apis]