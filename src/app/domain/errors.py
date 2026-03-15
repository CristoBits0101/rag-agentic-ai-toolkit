class DomainError(Exception):
    """Base exception for domain-level errors."""


class PolicyViolation(DomainError):
    """Raised when a domain policy blocks an operation."""
