from __future__ import annotations

import json
import re
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_CLASS, DOMAIN
from .coordinator import KFGCoordinator


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def _entry_matches_class(entry: dict[str, Any], class_name: str) -> bool:
    raw = str(entry.get("klasse", ""))
    classes = [item.strip().lower() for item in raw.replace("(", "").replace(")", "").split(",") if item.strip()]
    return class_name.strip().lower() in classes


def _filtered_data(data: dict[str, Any], class_name: str) -> dict[str, Any]:
    weeks: list[dict[str, Any]] = []
    for week in data.get("weeks", []):
        week_copy = {key: value for key, value in week.items() if key != "days"}
        days = []
        for day in week.get("days", []):
            day_copy = dict(day)
            day_copy["entries"] = [entry for entry in day.get("entries", []) if _entry_matches_class(entry, class_name)]
            days.append(day_copy)
        week_copy["days"] = days
        weeks.append(week_copy)

    return {
        "generated": data.get("generated"),
        "today": data.get("today"),
        "current_week": data.get("current_week"),
        "next_week": data.get("next_week"),
        "next_week_available": data.get("next_week_available", False),
        "class": class_name,
        "classes": [class_name],
        "weeks": weeks,
    }


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: KFGCoordinator = hass.data[DOMAIN][entry.entry_id]
    class_name = entry.options.get(CONF_CLASS, entry.data.get(CONF_CLASS, ""))
    entities = [
        KFGClassSensor(coordinator, entry, class_name),
        KFGClassJsonSensor(coordinator, entry, class_name),
    ]

    # The Kollegium sensor is global. Only the designated owner entry creates it.
    if hass.data[DOMAIN].get("kollegium_owner") == entry.entry_id:
        entities.append(KFGKollegiumSensor(coordinator))

    async_add_entities(entities)


class KFGClassSensor(CoordinatorEntity[KFGCoordinator], SensorEntity):
    _attr_has_entity_name = False
    _attr_icon = "mdi:calendar-account"

    def __init__(self, coordinator, entry, class_name: str):
        super().__init__(coordinator)
        self.class_name = class_name
        suffix = _slug(class_name)
        self._attr_unique_id = f"{entry.entry_id}_data"
        self._attr_name = f"Vertretungsplan {class_name}"
        self._attr_suggested_object_id = f"vertretungsplan_{suffix}"

    @property
    def native_value(self):
        return self.coordinator.data.get("generated")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return _filtered_data(self.coordinator.data, self.class_name)


class KFGClassJsonSensor(CoordinatorEntity[KFGCoordinator], SensorEntity):
    """Expose the class-specific plan as compact JSON in an attribute.

    Home Assistant sensor states are limited in length, therefore the JSON
    payload is stored in the `json` attribute while the state is the generation
    timestamp.
    """

    _attr_has_entity_name = False
    _attr_icon = "mdi:code-json"

    def __init__(self, coordinator, entry, class_name: str):
        super().__init__(coordinator)
        self.class_name = class_name
        suffix = _slug(class_name)
        self._attr_unique_id = f"{entry.entry_id}_json"
        self._attr_name = f"Vertretungsplan {class_name} JSON"
        self._attr_suggested_object_id = f"vertretungsplan_{suffix}_json"

    @property
    def native_value(self):
        return self.coordinator.data.get("generated")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        filtered = _filtered_data(self.coordinator.data, self.class_name)
        return {
            "class": self.class_name,
            "json": json.dumps(filtered, ensure_ascii=False, separators=(",", ":")),
        }


class KFGKollegiumSensor(CoordinatorEntity[KFGCoordinator], SensorEntity):
    """Expose the school's current teacher abbreviation/name directory once."""

    _attr_has_entity_name = False
    _attr_name = "KFG Kollegium"
    _attr_icon = "mdi:account-school"
    _attr_unique_id = "kfg_vertretungsplan_kollegium"
    _attr_suggested_object_id = "kfg_kollegium"

    @property
    def native_value(self) -> int:
        return len(self.coordinator.data.get("colleagues", {}))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = self.coordinator.data
        return {
            "lehrer": data.get("colleagues", {}),
            "aktualisiert": data.get("colleagues_updated"),
            "quelle": "https://www.kaiserin-friedrich.de/schule/kollegium/",
        }
