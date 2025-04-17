import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from local_solar_watt.openhab import HaEntity


@dataclass(slots=True)
class StateDescription:
    pattern: Optional[str]
    readOnly: bool
    options: List[Dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class Item:
    """
    Exactly one entry returned by /rest/items
    (Only the properties we actually need are modelled.)
    """
    name: str
    label: str
    state: str
    type: str
    editable: bool
    link: str
    tags: List[str]
    groupNames: List[str]
    stateDescription: Optional[StateDescription]
    # HomeAssistant style attributes
    ha_entity: HaEntity

    _TS_PREFIX = re.compile(r"^\d+\|")
    _UNIT = re.compile(r"\s[^\d\.]+$")

    @property
    def cleaned_state(self) -> Any:
        """
        Return the numeric value (float) if possible,
        otherwise the raw string. Handles timestamps and units.
        """
        raw = self.state
        if raw in ("NULL", "UNDEF", ""):
            return None

        raw = self._TS_PREFIX.sub("", raw)  # drop “epoch|”
        raw = self._UNIT.sub("", raw)  # drop trailing unit

        try:
            return float(raw)
        except ValueError:
            return raw

    # factory -------------------------------------------------
    @classmethod
    def from_json(cls, d: Dict[str, Any]) -> "Item":
        sd = d.get("stateDescription")
        if sd:
            # convert state description to StateDescription object
            sd = StateDescription(
                pattern=sd.get("pattern"),
                readOnly=sd.get("readOnly", False),
                options=sd.get("options", []),
            )
        ha_entity = HaEntity.from_openhab_name(d["name"])
        return cls(
            name=d["name"],
            label=d.get("label", ""),
            state=d.get("state", ""),
            type=d.get("type", ""),
            editable=d.get("editable", False),
            link=d.get("link", ""),
            tags=d.get("tags", []),
            groupNames=d.get("groupNames", []),
            stateDescription=sd,
            ha_entity=ha_entity,
        )
