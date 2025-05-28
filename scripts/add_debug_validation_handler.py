"""
install_validation_handler is a development-time hook for route validation auditing.
In production or minimal environments, it safely does nothing.
"""

def install_validation_handler(app):
    """
    No-op fallback for environments without audit tools.

    Args:
        app: FastAPI application instance (unused in this stub)
    """
    # Route auditing is disabled in this environment.
    # No validation hook is installed.
    return
