"""Provider-neutral language-model adapter contracts.

The core engine remains usable without an LLM. A provider adapter can be added
without giving the provider authority to bypass phase validation.
"""

from typing import Protocol


class LanguageModelAdapter(Protocol):
    def generate(self, *, system_instruction: str, user_input: str) -> str:
        """Return generated text. Implementations must surface provider errors."""
        ...
