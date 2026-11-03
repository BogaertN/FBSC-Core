# FBSC Core Architecture

## Runtime boundary

FBSC-Core is a deterministic orchestration and state-management layer. Language-model calls are optional phase handlers or provider adapters. The model does not control the phase counter, validation rules, memory writes, or GhostLoop retention.

## Nine phases

1. Initiation: establish the input and its scope.
2. Polarity: identify contrasts, alternatives, and opposing propositions.
3. Desire: state the target question or coherence objective.
4. Friction: challenge assumptions and seek counterevidence.
5. Entropy: expose uncertainty, divergence, and unresolved conflict.
6. Grace: attempt correction by reconciling the strongest available evidence. This phase is not a license to erase inconvenient evidence or force agreement.
7. Naming: state the best-supported interpretation and label uncertainty.
8. Power: express the result in a useful form.
9. Recursion: review whether the result answers the original input and identify what should recur.

## Drift and suspension

The transition validator requires the exact next phase. A handler failure or invalid result suspends the cycle and records a GhostLoop. The initial implementation does not automatically retry or claim that a contradiction has been resolved.

## GhostLoops

A GhostLoop preserves the original input, failed phase, reason, completed phase sequence, unresolved material, and reintegration condition. SQLite persistence is optional and local.

## Symbolic Phase Capacitor

The SPC accumulates caller-supplied signals with nonnegative charge and coherence in the range 0..1. It releases only when both configured thresholds pass. These values are engineering parameters, not measured physical frequencies.

## Identity

Identity is an explicit key/value record stored independently of model weights. The first version persists identity and GhostLoops in SQLite. Phase history is currently in-memory only.

## Evidence discipline

The architecture can enforce sequence and preserve failures. It cannot, by itself, prove factual correctness, eliminate hallucinations, or guarantee zero contradictions. Those outcomes require benchmark datasets, independent evaluators, and repeatable comparisons.
