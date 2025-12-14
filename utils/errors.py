"""Custom error classes for SwarmMaster."""


class SwarmError(Exception):
    """Base exception for SwarmMaster errors."""
    pass


class ConfigurationError(SwarmError):
    """Raised when configuration is invalid."""
    pass


class APIError(SwarmError):
    """Raised when API calls fail."""
    pass


class ValidationError(SwarmError):
    """Raised when input validation fails."""
    pass

