""" This module implements the EventHandler class """

from collections import defaultdict

import pygame.event


class EventHandler:
    """Register and process pygame events and handles"""

    def __init__(self):
        self.events = defaultdict(list)

    def register(self, key):
        def _register(func):
            self.events[key].append(func)

        return _register

    def unregister(self, key):
        self.events.get(key).clear()

    def invoke(self, key, event):
        for func in self.events[key]:
            func(event)

    def clear(self):
        self.events.clear()

    def run(self):
        for e in pygame.event.get():
            if (key := e.type) in self.events:
                self.invoke(key, e)
