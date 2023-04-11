""" This module implements the EventHandler class """

from collections import defaultdict

import pygame.event


class EventHandler:
    """Register and process pygame events and handles"""

    def __init__(self):
        """Initialize the event handler"""
        self.events = defaultdict(list)

    def register(self, key):
        """Register a function to an event"""

        def _register(func):
            """Register a function to an event"""
            self.events[key].append(func)

        return _register

    def unregister(self, key):
        """Unregister a function from an event"""
        self.events.get(key).clear()

    def invoke(self, key, event):
        """Invoke all functions registered to an event"""
        for func in self.events[key]:
            func(event)

    def clear(self):
        """Clear all events"""
        self.events.clear()

    def run(self):
        """Run the event handler"""
        for e in pygame.event.get():
            if (key := e.type) in self.events:
                self.invoke(key, e)


class CustomEvent:
    """Creates a custom event"""

    # total number of custom events limited by pygame
    num_left = 32668

    def __init__(self):
        if CustomEvent.num_left:
            self.type = pygame.event.custom_type()
            CustomEvent.num_left -= 1
            self.event = pygame.event.Event(self.type)
        else:
            raise pygame.error("Number of custom type events exceeded pygame limit")

    def post(self) -> None:
        """post the event on the pygame events queue"""
        pygame.event.post(self.event)

    def get(self) -> bool:
        """get the event state from the pygame events queue"""
        return bool(pygame.event.get(self.type))
