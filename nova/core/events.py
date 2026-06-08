from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Any
import time


@dataclass(slots=True)
class Event:
    name: str
    payload: dict[str, Any]
    created_at: float = field(default_factory=time.time)


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[[Event], None]]] = defaultdict(list)
        self.history: list[Event] = []

    def subscribe(self, name: str, handler: Callable[[Event], None]) -> None:
        self._handlers[name].append(handler)

    def publish(self, name: str, **payload: Any) -> Event:
        event = Event(name=name, payload=payload)
        self.history.append(event)
        for handler in list(self._handlers.get(name, [])):
            handler(event)
        return event
