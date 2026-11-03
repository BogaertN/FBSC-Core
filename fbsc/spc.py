"""Symbolic Phase Capacitor: thresholded accumulation of validated signals."""

from dataclasses import dataclass, field


@dataclass
class SymbolicPhaseCapacitor:
    minimum_charge: float = 1.0
    minimum_coherence: float = 0.7
    charge: float = 0.0
    weighted_coherence: float = 0.0
    _weight: float = 0.0
    signals: list[str] = field(default_factory=list)

    def add(self, signal: str, charge: float, coherence: float) -> None:
        if not signal.strip():
            raise ValueError("Signal cannot be empty.")
        if charge < 0:
            raise ValueError("Charge cannot be negative.")
        if not 0.0 <= coherence <= 1.0:
            raise ValueError("Coherence must be between 0 and 1.")
        self.charge += charge
        self.weighted_coherence += charge * coherence
        self._weight += charge
        self.signals.append(signal)

    @property
    def coherence(self) -> float:
        return self.weighted_coherence / self._weight if self._weight else 0.0

    @property
    def ready(self) -> bool:
        return self.charge >= self.minimum_charge and self.coherence >= self.minimum_coherence

    def discharge(self) -> list[str] | None:
        if not self.ready:
            return None
        released = list(self.signals)
        self.charge = 0.0
        self.weighted_coherence = 0.0
        self._weight = 0.0
        self.signals.clear()
        return released
