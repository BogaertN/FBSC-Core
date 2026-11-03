# FBSC-Core

Frequency-Based Symbolic Calculus (FBSC) is an experimental, testable symbolic control architecture for structured reasoning around language models.

This repository is an independent implementation. It does not depend on Forge Mobile.

## Project status

Initial engineering baseline. The first milestone is a deterministic nine-phase controller with explicit validation, drift detection, unresolved-loop preservation, and a persistent symbolic phase capacitor. Model integration is an adapter boundary, not part of the core state machine.

## Design principles

- The nine phases are explicit and ordered: Initiation, Polarity, Desire, Friction, Entropy, Grace, Naming, Power, Recursion.
- A transition cannot skip required phases.
- Phase 6 (Grace) is a correction and evidence-reconciliation mechanism. It must not suppress conflicting evidence or force a preferred conclusion.
- Unresolved or invalid transitions are retained as GhostLoops rather than silently discarded.
- The Symbolic Phase Capacitor (SPC) accumulates validated signals and releases only when configured thresholds are met.
- Identity and memory are explicit persisted data, not claims of model-weight modification.
- Claims of improved accuracy must be established by repeatable tests and benchmarks.

## Planned structure

- `fbsc/`: deterministic engine, state, validation, memory, and model adapter contracts.
- `tests/`: unit and integration tests.
- `examples/`: runnable examples.
- `docs/`: architecture and protocol documentation.

## Quick start

Python 3.10 or newer is required.

```bash
python -m unittest discover -s tests -v
python examples/basic_cycle.py
```

No third-party dependencies are required for the core.

## Scope

FBSC-Core provides a symbolic orchestration layer. It does not alter an LLM's underlying weights or guarantee hallucination-free output. It creates inspectable process constraints and records whether those constraints were satisfied.
