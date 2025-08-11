from dotenv import load_dotenv
import os
import requests
import json


class SwaggerFetcher:
    def __init__(self):
        load_dotenv()
        self.urls = self.get_urls_from_env()
    
    def get_urls_from_env(self):
        urls_string = os.getenv('SWAGGER_URLS', '')
        return [url.strip() for url in urls_string.split(',') if url.strip()]
    
    def fetch_all(self):
        results = []
        for url in self.urls:
            result = self.fetch_single(url)
            results.append(result)
        return results