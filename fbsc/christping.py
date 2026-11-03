"""ChristPing: explicit correction requests after an entropy review.

This module records and routes correction decisions. It does not declare that
a result is true merely because it appears coherent.
"""

from dataclasses import dataclass, field
from .models import Phase


@dataclass(frozen=True)
class CorrectionRequest:
    triggered: bool
    reentry_phase: Phase | None
    reason: str
    preserved_conflicts: tuple[str, ...] = field(default_factory=tuple)


class ChristPing:
    def __init__(self, entropy_tolerance: float = 0.7) -> None:
        if not 0.0 <= entropy_tolerance <= 1.0:
            raise ValueError("Entropy tolerance must be between 0 and 1.")
        self.entropy_tolerance = entropy_tolerance

    def evaluate(
        self,
        entropy: float,
        *,
        earliest_failed_phase: Phase = Phase.FRICTION,
        conflicts: list[str] | None = None,
    ) -> CorrectionRequest:
        if not 0.0 <= entropy <= 1.0:
            raise ValueError("Entropy must be between 0 and 1.")
        preserved = tuple(conflicts or ())
        if entropy <= self.entropy_tolerance:
            return CorrectionRequest(False, None, "Entropy remains within tolerance.", preserved)
        if earliest_failed_phase >= Phase.GRACE:
            earliest_failed_phase = Phase.FRICTION
        return CorrectionRequest(
            True,
            earliest_failed_phase,
            "Entropy exceeded tolerance; re-enter at the earliest identified failure.",
            preserved,
        )
