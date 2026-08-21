from .admin import admin_bp
from .auth import auth_bp
from .citizen import citizen_bp
from .public import public_bp

__all__ = ['public_bp', 'auth_bp', 'citizen_bp', 'admin_bp']
