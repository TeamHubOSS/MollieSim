from threading import BoundedSemaphore
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from uuid import uuid4

s = BoundedSemaphore(value=1)

MEMSTOR = defaultdict(dict)


@dataclass
class ResourceType:
    group_key: str
    id_prefix: str


class ResourceTypes(Enum):
    PAYMENT = ResourceType(group_key="P", id_prefix="tr_")


class Storage:
    def __init__(self, resource_type):
        self.resource_type = resource_type.value

    def get(self, _id):
        return MEMSTOR[self.resource_type.group_key][_id]

    def list(self):
        return list(MEMSTOR[self.resource_type.group_key].values())

    def set(self, item):
        with s:
            if not item.id:
                item.id = self.find_id()
            MEMSTOR[self.resource_type.group_key][item.id] = item

    def clear(self):
        MEMSTOR[self.resource_type.group_key].clear()

    def find_id(self):
        while True:
            candidate = f"{self.resource_type.id_prefix}{str(uuid4()).split('-')[0]}"
            if candidate not in MEMSTOR[self.resource_type.group_key]:
                return candidate

    @staticmethod
    def clear_all():
        MEMSTOR.clear()


class PaymentStorage(Storage):
    def __init__(self):
        super().__init__(ResourceTypes.PAYMENT)
