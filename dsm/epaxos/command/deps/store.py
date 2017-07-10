from typing import List

from dsm.epaxos.command.state import AbstractCommand
from dsm.epaxos.instance.state import InstanceState, Slot


class AbstractDepsStore:
    def __init__(self):
        pass

    def update(self, slot: Slot, old_inst: InstanceState, new_inst: InstanceState):
        raise NotImplementedError()

    def query(self, slot: Slot, command: AbstractCommand) -> List[Slot]:
        raise NotImplementedError()


