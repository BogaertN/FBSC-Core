import tempfile
import unittest
from pathlib import Path

from fbsc import FBSCEngine, Phase, SymbolicPhaseCapacitor
from fbsc.memory import SymbolicMemory
from fbsc.validation import DriftDetector


class DriftTests(unittest.TestCase):
    def test_complete_order_is_valid(self):
        self.assertTrue(DriftDetector.validate_cycle(list(Phase)).valid)

    def test_skip_is_rejected(self):
        result = DriftDetector.validate_transition(Phase.FRICTION, Phase.NAMING)
        self.assertFalse(result.valid)
        self.assertIn("expected Entropy", result.reason)


class EngineTests(unittest.TestCase):
    def test_nine_phase_cycle_completes(self):
        result = FBSCEngine().run_cycle("test input")
        self.assertTrue(result.completed)
        self.assertEqual(len(result.records), 9)
        self.assertEqual(result.records[-1].phase, Phase.RECURSION)

    def test_handler_failure_becomes_ghost_loop(self):
        def fail(_text, _state):
            raise RuntimeError("deliberate test failure")

        result = FBSCEngine().run_cycle("test input", {Phase.ENTROPY: fail})
        self.assertFalse(result.completed)
        self.assertEqual(result.ghost_loop.failed_phase, Phase.ENTROPY)
        self.assertEqual(len(result.records), 4)


class CapacitorTests(unittest.TestCase):
    def test_requires_charge_and_coherence(self):
        capacitor = SymbolicPhaseCapacitor(minimum_charge=2, minimum_coherence=0.8)
        capacitor.add("weak", 1, 0.5)
        self.assertFalse(capacitor.ready)
        capacitor.add("strong", 1, 1.0)
        self.assertFalse(capacitor.ready)
        capacitor.add("stronger", 1, 1.0)
        self.assertTrue(capacitor.ready)
        self.assertEqual(len(capacitor.discharge()), 3)
        self.assertEqual(capacitor.charge, 0)


class MemoryTests(unittest.TestCase):
    def test_identity_and_ghost_loop_persist(self):
        with tempfile.TemporaryDirectory() as folder:
            memory = SymbolicMemory(Path(folder) / "memory.db")
            memory.set_identity("name", "FBSC")
            engine = FBSCEngine(memory)
            result = engine.run_cycle("input", {
                Phase.POLARITY: lambda _text, _state: ""
            })
            self.assertFalse(result.completed)
            restored = FBSCEngine(memory)
            self.assertEqual(restored.state.identity["name"], "FBSC")
            self.assertEqual(len(restored.state.ghost_loops), 1)


if __name__ == "__main__":
    unittest.main()
