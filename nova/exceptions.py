class NovaError(Exception):
    """Base NOVA exception."""

class SafetyError(NovaError):
    """Raised when a requested operation violates the local safety policy."""

class ModelUnavailableError(NovaError):
    """Raised when a local model backend is not available."""

class PluginError(NovaError):
    """Raised for plugin discovery or execution errors."""
