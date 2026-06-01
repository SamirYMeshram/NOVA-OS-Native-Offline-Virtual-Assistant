class NovaError(Exception):
    """Base class for NOVA errors."""

class UnsafeActionError(NovaError):
    """Raised when a command violates safety policy."""

class ModelUnavailableError(NovaError):
    """Raised when a local model backend is unavailable."""

class PluginError(NovaError):
    """Raised when plugin loading or execution fails."""
