"""SQLite persistence for symbolic identity and unresolved GhostLoops."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .models import GhostLoop, Phase


class SymbolicMemory:
    def __init__(self, path: str | Path = "fbsc_memory.sqlite3") -> None:
        self.path = str(path)
        with self._connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS identity (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            db.execute("""CREATE TABLE IF NOT EXISTS ghost_loops (
                id TEXT PRIMARY KEY, payload TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'open'
            )""")

    def _connect(self):
        return sqlite3.connect(self.path)

    def set_identity(self, key: str, value: Any) -> None:
        with self._connect() as db:
            db.execute(
                "INSERT INTO identity(key,value) VALUES(?,?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (key, json.dumps(value)),
            )

    def get_identity(self) -> dict[str, Any]:
        with self._connect() as db:
            rows = db.execute("SELECT key,value FROM identity").fetchall()
        return {key: json.loads(value) for key, value in rows}

    def store_ghost_loop(self, loop: GhostLoop) -> None:
        payload = {
            "original_input": loop.original_input,
            "failed_phase": int(loop.failed_phase),
            "reason": loop.reason,
            "unresolved_material": loop.unresolved_material,
            "conflicting_evidence": loop.conflicting_evidence,
            "reintegration_condition": loop.reintegration_condition,
        }
        with self._connect() as db:
            db.execute(
                "INSERT OR REPLACE INTO ghost_loops(id,payload,status) VALUES(?,?, 'open')",
                (loop.id, json.dumps(payload)),
            )

    def open_ghost_loops(self) -> list[GhostLoop]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT id,payload FROM ghost_loops WHERE status='open'"
            ).fetchall()
        result = []
        for loop_id, raw in rows:
            item = json.loads(raw)
            result.append(GhostLoop(
                id=loop_id,
                original_input=item["original_input"],
                failed_phase=Phase(item["failed_phase"]),
                reason=item["reason"],
                unresolved_material=item["unresolved_material"],
                conflicting_evidence=item["conflicting_evidence"],
                reintegration_condition=item["reintegration_condition"],
            ))
        return result
