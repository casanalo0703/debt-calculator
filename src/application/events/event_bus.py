# src/application/events/event_bus.py
from typing import Callable, Type, Any, Dict, List
from .domain_events import DomainEvent

# Define the type for an event handler callback
EventHandler = Callable[[DomainEvent], None]

class EventBus:
    """
    A simple Publisher-Subscriber pattern implementation for decoupling components.
    Subscribers listen to domain events and react accordingly.
    """
    def __init__(self):
        # Structure: {EventType: [handler1, handler2, ...]}
        self._subscribers: Dict[Type[DomainEvent], List[EventHandler]] = {}

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Registers a handler function for a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        print(f"EventBus subscribed handler to {event_type.__name__}")

    def publish(self, event: DomainEvent) -> None:
        """Publishes an event, triggering all registered handlers."""
        event_type = type(event)
        if event_type in self._subscribers:
            print(f"\n--- Publishing Event: {event_type.__name__} ---")
            for handler in self._subscribers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    # Critical: Failing handlers should not stop event propagation.
                    print(f"WARNING: Handler failed for {event_type.__name__}: {e}")
        else:
            print(f"\n--- Publishing Event: {event_type.__name__} (No subscribers) ---")

    def unsubscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Removes a specific handler subscription."""
        if event_type in self._subscribers and handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)

# Global instance (or injected via Container)
event_bus = EventBus()