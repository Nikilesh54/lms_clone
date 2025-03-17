from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
import time
import re

class CacheMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.cache_timeout = 60 * 15  # 15 minutes

    def process_request(self, request):
        if request.method != 'GET':
            return None
        
        cache_key = f"cache__{request.path}_{request.GET.urlencode()}"
        response = cache.get(cache_key)
        
        if response:
            return response
        
        return None

    def process_response(self, request, response):
        if request.method != 'GET':
            return response
        
        if response.status_code == 200 and not re.search(r'^/admin/', request.path):
            cache_key = f"cache__{request.path}_{request.GET.urlencode()}"
            cache.set(cache_key, response, self.cache_timeout)
        
        return response
