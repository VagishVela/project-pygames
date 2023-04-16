""" This module implements the EventHandler class """

import pygame.event


class EventHandler:
    """Register and process pygame events and handles"""

    def __init__(self):
        """Initialize the event handler"""
        self.events = {}

    def register(self, key: int):
        """Register a function to an event"""
        if key not in self.events:
            self.events[key] = []

        def _register(func):
            """Register a function to an event"""
            self.events[key].append(func)

        return _register

    def unregister(self, key: int):
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

    def __init__(self, _dict=None):
        if _dict is None:
            _dict = {}
        if CustomEvent.num_left:
            self.type = pygame.event.custom_type()
            CustomEvent.num_left -= 1
            self.event = pygame.event.Event(self.type, _dict)
            self.event.dict.update({"was_waited": False})
        else:
            raise pygame.error("Number of custom type events exceeded pygame limit")

    def post(self, _dict=None) -> None:
        """post the event on the pygame events queue"""
        if _dict is None:
            _dict = {}
        self.event.dict.update(_dict)
        pygame.event.post(self.event)

    def get(self) -> pygame.event.Event | None:
        """get the event state from the pygame events queue"""
        if e := pygame.event.get(self.type):
            event = e[0]
            if event.was_waited and not event.repeat_wait:
                # remove the timer
                pygame.time.set_timer(self.type, 0)
            return event
        return None

    def wait(self, time, _dict=None, repeat=False) -> None:
        """post this event after waiting for `time` ms"""
        if _dict is None:
            _dict = {}
        self.event.dict.update({"was_waited": True, "repeat_wait": repeat} | _dict)
        # set the timer
        pygame.time.set_timer(self.event, time)
