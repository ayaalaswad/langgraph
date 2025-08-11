import chromadb
from chroma import SwaggerFetcher
fetcher = SwaggerFetcher()
all_data = fetcher.fetch_all()

client = chromadb.PersistentClient(path="./my_chroma")
collection = client.get_or_create_collection(name="swagger_apis")
documents = []
ids = []
metadatas = []

for i, api in enumerate(all_data):
    if api['success'] and api['data']:
        swagger_data = api['data']
        api_name = swagger_data.get('info', {}).get('title', f'API_{i}')
        
        for path, methods in swagger_data.get('paths', {}).items():
            for method, details in methods.items():
                if method.lower() in ['get', 'post', 'put', 'delete']:
                    
                    text = f"{method.upper()} {path} - {details.get('summary', 'No description')}"
                    
                    documents.append(text)
                    ids.append(f"{i}_{method}_{path}".replace('/', '_').replace('{', '').replace('}', ''))
                    metadatas.append({
                        "api": api_name,
                        "method": method.upper(),
                        "path": path
                    })

collection.add(documents=documents, ids=ids, metadatas=metadatas)

print(f"✅ تم إضافة {len(documents)} endpoint")
print(f"📊 إجمالي البيانات: {collection.count()}")