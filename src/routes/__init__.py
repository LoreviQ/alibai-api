"""Init file for routes package."""

# Import all route files to ensure their routes are registered with the Blueprint
from . import x_twitter
from .main import register_routes
