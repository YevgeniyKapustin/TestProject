from django.core.cache import cache
from django.http import HttpResponseForbidden

from config import settings


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        key = f'rate_limit:{ip}'
        requests = cache.get(key, 0)

        if requests >= settings.RATE_LIMIT:
            return HttpResponseForbidden('Too many requests')

        cache.set(key, requests + 1, timeout=60)
        return self.get_response(request)
