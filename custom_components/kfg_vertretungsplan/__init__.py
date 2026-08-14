from __future__ import annotations

from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, PLATFORMS
from .coordinator import KFGCoordinator

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
CARD_URL = f"/api/{DOMAIN}/static/vertretungsplan-card.js"
CARD_RESOURCE_URL = f"{CARD_URL}?v=1.0.5"


async def _register_lovelace_resource(hass: HomeAssistant) -> None:
    """Register the custom card as a Lovelace module resource."""
    resources = hass.data["lovelace"]["resources"]
    await resources.async_load()

    for resource in resources.async_items():
        if resource["url"].split("?", 1)[0] == CARD_URL:
            return

    await resources.async_create_item(
        {
            "res_type": "module",
            "url": CARD_RESOURCE_URL,
        }
    )


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the KFG Vertretungsplan integration."""
    static_dir = Path(__file__).parent / "static"
    await hass.http.async_register_static_paths(
        [StaticPathConfig(f"/api/{DOMAIN}/static", str(static_dir), False)]
    )
    await _register_lovelace_resource(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = KFGCoordinator(
        hass,
        base_url=entry.data["base_url"],
        scan_interval=entry.options.get("scan_interval", entry.data["scan_interval"]),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return ok
