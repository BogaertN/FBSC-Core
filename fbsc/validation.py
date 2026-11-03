"""Structural validation and drift detection."""

from dataclasses import dataclass
from .models import Phase


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    reason: str = ""


class DriftDetector:
    """Rejects phase skips and out-of-order transitions."""

    @staticmethod
    def validate_transition(previous: Phase | None, current: Phase) -> ValidationResult:
        expected = Phase.INITIATION if previous is None else Phase(previous + 1)
        if current != expected:
            return ValidationResult(
                False,
                f"Phase drift: expected {expected.label}, received {current.label}.",
            )
        return ValidationResult(True)

    @staticmethod
    def validate_cycle(phases: list[Phase]) -> ValidationResult:
        expected = list(Phase)
        if phases != expected:
            return ValidationResult(
                False,
                "A complete cycle must traverse all nine phases in order without skips.",
            )
        return ValidationResult(True)
