import time
from flask import request

def register_middlewares(app):
    """
    Attach any middlewares (before_request, after_request, etc.) to the app.
    """

    @app.before_request
    def start_timer():
        # Example: start a timer for each request
        request._start_time = time.time()

    @app.after_request
    def log_request(response):
        # Example: log request method, path, status, and duration
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
            app.logger.info(
                f"{request.method} {request.path} "
                f"Status: {response.status_code} "
                f"Duration: {duration:.4f}s"
            )
        return response
