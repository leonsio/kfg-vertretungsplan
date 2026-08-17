from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import KFGCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: KFGCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([KFGSensor(coordinator, entry)])


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
        """Expose only data required by the Lovelace card.

        The coordinator keeps the complete parser result internally. The sensor
        no longer duplicates the derived top-level ``days`` list because Home
        Assistant Recorder limits state attributes to 16 KiB. The card reads
        weeks[].days[] directly.
        """
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
