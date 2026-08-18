from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import KFGCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: KFGCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        KFGSensor(coordinator, entry),
        KFGKollegiumSensor(coordinator, entry),
    ])


class KFGSensor(CoordinatorEntity[KFGCoordinator], SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Vertretungsplan"
    _attr_icon = "mdi:calendar-account"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_data"

    @property
    def native_value(self):
        return self.coordinator.data.get("generated")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose only data required by the Lovelace card."""
        data = self.coordinator.data
        return {
            "generated": data.get("generated"),
            "today": data.get("today"),
            "current_week": data.get("current_week"),
            "next_week": data.get("next_week"),
            "next_week_available": data.get("next_week_available", False),
            "classes": data.get("classes", []),
            "weeks": data.get("weeks", []),
        }


class KFGKollegiumSensor(CoordinatorEntity[KFGCoordinator], SensorEntity):
    """Expose the school's current teacher abbreviation/name directory."""

    _attr_has_entity_name = True
    _attr_name = "KFG Kollegium"
    _attr_icon = "mdi:account-school"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_kollegium"

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
