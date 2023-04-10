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
