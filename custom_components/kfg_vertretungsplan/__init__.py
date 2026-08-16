from __future__ import annotations

from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.lovelace.const import LOVELACE_DATA
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, PLATFORMS
from .coordinator import KFGCoordinator

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
CARD_URL = f"/api/{DOMAIN}/static/vertretungsplan-card.js"


async def _register_lovelace_resource(hass: HomeAssistant) -> None:
    """Register or normalize the custom card as a Lovelace module resource."""
    lovelace_data = hass.data.get(LOVELACE_DATA)
    if lovelace_data is None:
        return

    resources = lovelace_data.resources
    if not hasattr(resources, "async_create_item"):
        return

    await resources.async_load()
    matched = False

    for resource in list(resources.async_items()):
        url = resource.get("url", "")
        base_url = url.split("?", 1)[0]
        if base_url != CARD_URL and not base_url.endswith("/vertretungsplan-card.js"):
            continue

        matched = True
        if url != CARD_URL or resource.get("res_type") != "module":
            await resources.async_update_item(
                resource["id"],
                {"url": CARD_URL, "res_type": "module"},
            )

    if not matched:
        await resources.async_create_item(
            {"res_type": "module", "url": CARD_URL}
        )


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the KFG Vertretungsplan integration."""
    static_dir = Path(__file__).parent / "static"
    await hass.http.async_register_static_paths(
        [StaticPathConfig(f"/api/{DOMAIN}/static", str(static_dir), False)]
    )

    add_extra_js_url(hass, CARD_URL)

    if hass.is_running:
        hass.async_create_task(_register_lovelace_resource(hass))
    else:
        async def _on_started(_event):
            await _register_lovelace_resource(hass)

        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _on_started)
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
