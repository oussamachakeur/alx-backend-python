from datetime import datetime
from django.http import HttpResponseForbidden
import time
from collections import defaultdict

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)
        return self.get_response(request)




class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to chats is restricted outside 6PM to 9PM.")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_log = defaultdict(list)  # {ip: [timestamps]}

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()
            timestamps = self.ip_log[ip]

            # Remove timestamps older than 60 seconds
            self.ip_log[ip] = [t for t in timestamps if now - t < 60]

            if len(self.ip_log[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded. Only 5 messages per minute allowed.")

            self.ip_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    
    
    
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if request.path.startswith('/chat') and user.is_authenticated:
            if not user.is_superuser and not user.groups.filter(name__in=['moderator']).exists():
                return HttpResponseForbidden("You do not have permission to access this resource.")
        return self.get_response(request)