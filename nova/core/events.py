from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Any
from datetime import datetime, timezone

@dataclass(slots=True)
class Event:
    name: str
    payload: dict[str, Any]
    ts: str

class EventBus:
    def __init__(self):
        self._subs: dict[str, list[Callable[[Event], None]]] = defaultdict(list)

    def subscribe(self, name: str, handler: Callable[[Event], None]) -> None:
        self._subs[name].append(handler)

    def publish(self, name: str, **payload: Any) -> Event:
        event = Event(name, payload, datetime.now(timezone.utc).isoformat())
        for handler in list(self._subs.get(name, [])):
            handler(event)
        return event
