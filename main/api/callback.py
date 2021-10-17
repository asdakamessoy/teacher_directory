from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class HttpResponseForbidden(HttpResponse):
    status_code = 403


class ApiCallMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = None
        if hasattr(self, "process_request"):
            response = self.process_request(request)

        if not response:
            response = self.get_response(request)

        if hasattr(self, "process_response"):
            response = self.process_response(request, response)
        return response

    # def process_view(self, request, view_func, args, kwargs):
    #     # trying basic middleware check can be done in many different ways
    #     print(kwargs)
    #     print(request.user)
    #     if not request.user.is_staff:
    #         return HttpResponseForbidden()
