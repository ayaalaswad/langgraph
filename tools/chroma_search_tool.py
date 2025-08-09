# tools/chroma_search_tool.py - دالة بحث بسيطة فقط

import chromadb

# ============================================
# إعدادات بسيطة
# ============================================

DB_PATH = './my_chroma'
COLLECTION_NAME = 'swagger_apis'
MAX_RESULTS = 5

# متغيرات الاتصال
_client = None
_collection = None

def _setup_connection():
    """إعداد الاتصال"""
    global _client, _collection
    
    try:
        print(f"🔗 Connecting to: {DB_PATH}")
        _client = chromadb.PersistentClient(path=DB_PATH)
        _collection = _client.get_collection(name=COLLECTION_NAME)
        print(f"✅ Connected! Data count: {_collection.count()}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

# إعداد الاتصال عند تحميل الملف
_setup_connection()

# ============================================
# دالة البحث الوحيدة
# ============================================

def search_apis(query):
    """البحث في ChromaDB - دالة بسيطة"""
    global _collection
    
    if not _collection:
        if not _setup_connection():
            return "❌ Cannot connect to ChromaDB"
    
    try:
        results = _collection.query(
            query_texts=[query],
            n_results=MAX_RESULTS
        )
        
        if not results['documents'][0]:
            return f"🔍 No results found for: '{query}'"
        
        # تنسيق بسيط
        output = [f"🔍 Found {len(results['documents'][0])} API endpoints:\n"]
        
        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
            api_name = metadata.get('api', 'Unknown')
            method = metadata.get('method', 'Unknown')
            path = metadata.get('path', 'Unknown')
            
            output.append(f"{i+1}. 📡 {api_name}")
            output.append(f"   🔹 {method} {path}")
            output.append(f"   📝 {doc}\n")
        
        return "\n".join(output)
        
    except Exception as e:
        return f"❌ Search error: {str(e)}"

# اختبار
if __name__ == "__main__":
    print("🧪 Testing search function...")
    result = search_apis("authentication")
    print(result)