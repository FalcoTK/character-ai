# pycai3/__init__.py

# Importing specific classes for easier access
from .method.chat import Chat
from .method.auth import Authentication
from .method.utils import Request

from .error import CAIError, ServerError, AuthError, NotFoundError, JSONError

# Optional: Uncomment if needed
# from .method.voice import Voice
