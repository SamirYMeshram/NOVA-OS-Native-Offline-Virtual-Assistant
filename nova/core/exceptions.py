class NovaError(Exception):
    """Base exception for NOVA."""

class SafetyError(NovaError):
    """Raised when an action violates a safety policy."""

class ConfigurationError(NovaError):
    """Raised when configuration is invalid."""

class ProviderUnavailable(NovaError):
    """Raised when a model provider is unavailable."""
