from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, DefaultDict
from collections import defaultdict

@dataclass(slots=True)
class Event:
    name: str
    payload: dict = field(default_factory=dict)

class EventBus:
    def __init__(self) -> None:
        self._handlers: DefaultDict[str, list[Callable[[Event], None]]] = defaultdict(list)

    def subscribe(self, name: str, handler: Callable[[Event], None]) -> None:
        self._handlers[name].append(handler)

    def publish(self, name: str, **payload) -> None:
        event = Event(name, payload)
        for handler in list(self._handlers.get(name, [])):
            handler(event)
