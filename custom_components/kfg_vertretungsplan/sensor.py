from __future__ import annotations
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
    def extra_state_attributes(self):
        return self.coordinator.data
