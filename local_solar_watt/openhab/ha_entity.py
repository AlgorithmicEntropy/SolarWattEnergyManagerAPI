import re
from dataclasses import dataclass

from local_solar_watt.const import FILTERED_WORDS

NAME_RE = re.compile(
    r'''^                 # start of string
        (.+?)             # 1 device  – anything, *non‑greedy*
        _                 #   underscore that separates device from id
        ([A-Za-z0-9]*\d[A-Za-z0-9]*)  # 2 id – alphanum **but must contain at least one digit**
        _                 #   underscore that separates id from entity
        (.+)              # 3 entity – the rest of the string
        $                 # end of string
    ''',
    re.VERBOSE,
)


@dataclass
class HaEntity:
    device: str
    id: str
    entity: str

    @staticmethod
    def _clean_name(name: str) -> str:
        """
        Clean the name by removing some redundant words
        """
        # strip leading or trailing underscores
        name = name.strip('_')
        # split by underscore
        parts = name.split('_')
        filtered = []
        for i in range(len(parts)):
            if parts[i] not in FILTERED_WORDS:
                filtered.append(parts[i])
        # Re-assemble
        return "_".join(filtered)

    @classmethod
    def from_openhab_name(cls, name: str) -> "HaEntity":
        match = NAME_RE.match(name)
        if match:
            device = cls._clean_name(match.group(1))
            id = match.group(2)
            entity = cls._clean_name(match.group(3))
            return cls(device=device, id=id, entity=entity)
        else:
            raise ValueError(f"Invalid name format: {name}")
