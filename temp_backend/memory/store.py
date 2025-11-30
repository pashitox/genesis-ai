# backend/memory/store.py
import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

STORE_PATH = Path(__file__).parent / "store.json"

class MemoryStore:
    def __init__(self, path: Path = STORE_PATH):
        self.path = path
        self.lock = asyncio.Lock()

    async def _read(self) -> Dict[str, Any]:
        async with self.lock:
            if not self.path.exists():
                default = {"learned": [], "interactions": []}
                self.path.write_text(json.dumps(default, indent=2))
                return default
            text = self.path.read_text()
            return json.loads(text)

    async def _write(self, data: Dict[str, Any]):
        async with self.lock:
            self.path.write_text(json.dumps(data, indent=2))

    async def add_interaction(self, request_id: str, user_message: str, reasoner_resp: str, critic_report: dict, improver_resp: str, rag_context: str = ""):
        data = await self._read()
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "request_id": request_id,
            "user_message": user_message,
            "reasoner": reasoner_resp,
            "critic": critic_report,
            "improver": improver_resp,
            "rag_context": rag_context
        }
        data.setdefault("interactions", []).append(entry)
        await self._write(data)
        return entry

    async def add_learning(self, item: dict):
        data = await self._read()
        data.setdefault("learned", []).append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "item": item
        })
        await self._write(data)

    async def get_state(self):
        return await self._read()
