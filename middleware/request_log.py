# middleware/request_log.py
# from: https://wilspi.com/post/tech/django-middleware-to-log-requests/
# adapted by mb to add a PATH_FILTER settings variable
"""
Middleware to log `*/api/*` requests and responses.
"""
import socket
import time
import json
import logging
from django.conf import settings

request_logger = logging.getLogger(__name__)
REQUEST_LOGGER_FILTER = settings.REQUEST_LOGGER


class RequestLogMiddleware:
    """Request Logging Middleware."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.filter = settings.REQUEST_LOGGER_FILTER

    def __call__(self, request):
        start_time = time.time()
        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
        }

        # Only logging "*/api/*" patterns
        if settings.REQUEST_LOGGER_PATH_FILTER in str(request.get_full_path()):
            req_body = json.loads(request.body.decode("utf-8")) if request.body else {}
            log_data["request_body"] = req_body

        # request passes on to controller
        response = self.get_response(request)

        # add runtime to our log_data
        if response and response["content-type"] == "application/json":
            response_body = json.loads(response.content.decode("utf-8"))
            log_data["response_body"] = response_body
        log_data["run_time"] = time.time() - start_time

        request_logger.info(msg=log_data)

        return response

    # Log unhandled exceptions as well
    def process_exception(self, request, exception):
        try:
            raise exception
        except Exception as e:
            request_logger.exception("Unhandled Exception: " + str(e))
        return exception
