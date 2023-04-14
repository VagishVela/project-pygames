""" Module to work with game data """

import json
import time
from json import JSONDecodeError

from game.config import MAX_SLOTS
from game.logger import logger

logger = logger.getChild("data")


class Data:
    """Processed data loaded from savefile"""

    meta = {}
    slots = []

    def __init__(self, _data):
        self.meta: dict = _data.get("_meta") or {"max_slots": MAX_SLOTS}
        self.max_slots: int = self.meta["max_slots"]
        self.slots: list[dict] = _data.get("slots") or []

    def get_slot(self, slot) -> dict:
        """get a slot from the stored slots"""
        if slot <= self.max_slots:
            return self.slots[slot]
        return {}

    def save_slot(self, slot_data) -> None:
        """save a slot"""
        self.slots.insert(0, slot_data)
        if len(self.slots) > self.max_slots:
            self.slots.pop(-1)

    @staticmethod
    def construct_slot(loc, defeated) -> dict:
        """construct a dict for a slot"""
        return {
            "time": int(time.time()),
            "loc": [int(loc[0]), int(loc[1])],
            "defeated": defeated,
        }

    def read(self) -> dict:
        """returns the data as a dict"""
        return {
            "_meta": {
                "max_slots": self.max_slots,
            },
            "slots": self.slots,
        }


class DataIO:
    """Work with the savefile and perform FileIO operations"""

    def __init__(self, file="game/data/game.dat"):
        self.slot = None
        self.file = file
        self._data = None  # raw
        self.data = Data(
            {
                "_meta": {"max_slots": MAX_SLOTS},
                "slots": [],
            }
        )  # processed
        # initiate the Data if something is already stored or create the savefile if not present
        self.read()

    def save(self, loc, defeated):
        """save the game data as a Data slot and write into the file"""
        logger.debug(f"try to save: {loc}, {defeated}")
        # self._data["player_pos"] =
        _temp = Data.construct_slot(loc, defeated)
        self.data.save_slot(_temp)
        self._data = self.data.read()
        self.write()

    def load(self, slot: int):
        """load a slot from the Data"""
        self.slot = slot
        if self._data is None:
            self.read()
        return self.data.get_slot(slot)

    def write(self):
        """write the data into the savefile"""
        with open(self.file, "w+", encoding="utf-8") as f:
            json.dump(self._data, f)

    def read(self):
        """read the file and save the data internally"""
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                try:
                    self._data = json.load(f)
                except JSONDecodeError as e:
                    logger.warning(f"CORRUPTED DATA, {e}")
                    self._data = {}
                self.data = Data(self._data)
        except FileNotFoundError:
            with open(self.file, "w+", encoding="utf-8") as f:
                # create an empty file
                f.write("")
            self.read()

    def get(self, key):
        """get attributes from a loaded slot"""
        return self.data.get_slot(self.slot)[key]


game_data = DataIO()
