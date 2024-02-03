from threading import local
from uuid import uuid4
_thread_locals = local()


def get_current_request():
    """Returns the request object in thread local storage."""
    return getattr(_thread_locals, "request", None)


def get_current_user():
    """Returns the current user, if exist, otherwise returns None."""
    request = get_current_request()
    if request:
        return getattr(request, "user", None)

def get_txid():
    """Returns the current transaction id, if exist, otherwise returns None."""
    return getattr(_thread_locals, "txid", None)

def get_current_user_id():
    """Returns authenticated user's id for this thread, if not present returns 0."""
    user = get_current_user()
    if user and user.id:
        return user.id
    return 0


class PopulateLocalsThreadMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("custom middleware before next middleware/view")
        # Populate the request object in thread local storage to be accessible anywhere
        _thread_locals.request = request
        _thread_locals.txid = str(uuid4())
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Clean up the thread local storage
        _thread_locals.request = None
        _thread_locals.tx_id = None
        print("custom middleware after response is returned")
        return response
