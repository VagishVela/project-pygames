""" Module to work with game data """

import json
import time
import typing
from dataclasses import dataclass
from json import JSONDecodeError

from game.config import MAX_SLOTS
from game.logger import logger

if typing.TYPE_CHECKING:
    from game.views.map import GameState

logger = logger.getChild("data")


@dataclass
class SlotData:
    """Represents a slot of game data"""

    time: int
    loc: list
    removed: set[tuple]
    health: int
    xp: int

    def to_dict(self) -> dict:
        """convert the slots back to dictionary"""
        return {
            "time": self.time,
            "loc": self.loc,
            "removed": [list(pos) for pos in self.removed],
            "attributes": {"health": self.health, "xp": self.xp},
        }


@dataclass
class Data:
    """Processed data loaded from savefile"""

    # raw data
    _meta: dict
    _slots: list[dict]

    def __post_init__(self) -> None:
        self.max_slots = self._meta.get("max_slots", MAX_SLOTS)
        self.slots = [
            SlotData(
                time=slot["time"],
                removed={tuple(s) for s in slot["removed"]},
                loc=slot["loc"],
                health=slot["attributes"]["health"],
                xp=slot["attributes"]["xp"],
            )
            for slot in self._slots
        ]

    def get_slot(self, slot_index: int) -> SlotData | None:
        """get a slot from the stored slots"""
        return self.slots[slot_index] if slot_index <= self.max_slots else None

    def save_slot(self, slot_data: SlotData) -> None:
        """save a slot internally, constructed by construct_slot"""
        # insert at beginning
        self.slots.insert(0, slot_data)
        # remove the last slot
        if len(self.slots) > self.max_slots:
            self.slots.pop(-1)

    @staticmethod
    def construct_slot(game_state: "GameState") -> SlotData:
        """construct a dict for a slot"""
        level_state = game_state.level_state
        attributes = game_state.attributes
        return SlotData(
            time=int(time.time()),
            loc=level_state.loc,
            removed=level_state.removed,
            health=attributes.health,
            xp=attributes.xp,
        )

    def read(self) -> dict:
        """returns the data as a dict"""
        return {
            "meta": {
                "max_slots": self.max_slots,
            },
            "slots": [slot.to_dict() for slot in self.slots],
        }


class DataIO:
    """Work with the savefile and perform FileIO operations"""

    def __init__(self, file="game/data/game.dat"):
        self._temp = {}
        self.slot_index = None
        self.file = file
        # raw data
        self._data = {}
        self.read()
        # processed data
        self.data = Data(_meta=self._data["meta"], _slots=self._data["slots"])

    @property
    def temp(self):
        """access the stored game data"""
        return self._temp["game_data"]

    def get_temp(self, name):
        """access all values stored in temp"""
        return self._temp[name]

    def save_game_state(self, game_state: "GameState"):
        """save the game state as a Data slot and write that into the file"""
        logger.debug(f"try to save: {game_state.level_state}")
        self.data.save_slot(Data.construct_slot(game_state))
        self._data = self.data.read()
        self.write()

    def load(self, slot_index: int) -> SlotData:
        """load a slot from the Data"""
        self.slot_index = slot_index
        if self._data is None:
            self.read()
        return self.data.get_slot(slot_index)

    def write(self):
        """write the data into the savefile"""
        with open(self.file, "w+", encoding="utf-8") as f:
            json.dump(self._data, f)

    def clean(self):
        """clear the savefile and cleans the data"""
        with open(self.file, "w+", encoding="utf-8") as f:
            f.write("")
        # re-init
        # pylint:disable=unnecessary-dunder-call
        self.__init__()

    def read(self):
        """read the file and save the data internally"""
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                # don't parse if the file is empty
                if contents := f.read():
                    try:
                        self._data = json.loads(contents)
                    except JSONDecodeError as e:
                        logger.warning(f"CORRUPTED DATA, {e}")
                        self._data = {
                            "meta": {
                                "max_slots": MAX_SLOTS,
                            },
                            "slots": [],
                        }
                else:
                    self._data = {
                        "meta": {
                            "max_slots": MAX_SLOTS,
                        },
                        "slots": [],
                    }
        except FileNotFoundError:
            logger.warning("File was not found, creating new savefile")
            with open(self.file, "w+", encoding="utf-8") as f:
                # create an empty file
                f.write("")
            self.read()
        logger.debug("data read successfull")

    def get(self, key):
        """get attributes from a loaded slot"""
        return getattr(self.data.get_slot(self.slot_index), key)

    def save_temp(self, data, name="game_data"):
        """Save something temporarily"""
        self._temp[name] = data


game_data = DataIO()
