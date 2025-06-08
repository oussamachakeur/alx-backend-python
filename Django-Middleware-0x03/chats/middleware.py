from datetime import datetime
from django.http import HttpResponseForbidden
import time
from collections import defaultdict

import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Set up logging
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

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
    
    
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip if user is not authenticated
        if request.user.is_authenticated:
            user = request.user
            # Assuming user role is stored in a field `role` on the user model
            # You may need to modify this based on your actual model
            if not hasattr(user, 'role') or user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to access this resource.")
        return self.get_response(request)