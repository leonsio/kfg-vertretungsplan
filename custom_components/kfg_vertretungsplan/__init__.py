from __future__ import annotations

from pathlib import Path
import re

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.lovelace.const import LOVELACE_DATA
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, entity_registry as er

from .const import CONF_CLASS, CONF_SCAN_INTERVAL, DOMAIN, PLATFORMS
from .coordinator import KFGCoordinator

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
CARD_URL = f"/api/{DOMAIN}/static/vertretungsplan-card.js"


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


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
        await resources.async_create_item({"res_type": "module", "url": CARD_URL})


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the KFG Vertretungsplan integration."""
    static_dir = Path(__file__).parent / "static"
    await hass.http.async_register_static_paths(
        [StaticPathConfig(f"/api/{DOMAIN}/static", str(static_dir), False)]
    )
    add_extra_js_url(hass, CARD_URL)
    hass.data.setdefault(DOMAIN, {})
    if hass.is_running:
        hass.async_create_task(_register_lovelace_resource(hass))
    else:
        async def _on_started(_event):
            await _register_lovelace_resource(hass)
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _on_started)
    return True


def _migrate_kollegium_entity(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Keep the old sensor.kfg_kollegium entity when upgrading from 1.0.x."""
    registry = er.async_get(hass)
    old_unique_id = f"{entry.entry_id}_kollegium"
    old_entity_id = registry.async_get_entity_id("sensor", DOMAIN, old_unique_id)
    global_entity_id = registry.async_get_entity_id("sensor", DOMAIN, "kfg_vertretungsplan_kollegium")
    if old_entity_id and not global_entity_id:
        registry.async_update_entity(
            old_entity_id,
            new_unique_id="kfg_vertretungsplan_kollegium",
        )


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Rename class entities if needed and reload changed options."""
    class_name = str(entry.options.get(CONF_CLASS, entry.data.get(CONF_CLASS, "alle"))).strip() or "alle"
    suffix = _slug(class_name) or "alle"

    registry = er.async_get(hass)
    desired_ids = {
        f"{entry.entry_id}_data": f"sensor.vertretungsplan_{suffix}",
        f"{entry.entry_id}_json": f"sensor.vertretungsplan_{suffix}_json",
    }
    for unique_id, desired_entity_id in desired_ids.items():
        entity_id = registry.async_get_entity_id("sensor", DOMAIN, unique_id)
        if entity_id and entity_id != desired_entity_id and registry.async_get(desired_entity_id) is None:
            registry.async_update_entity(entity_id, new_entity_id=desired_entity_id)

    hass.config_entries.async_update_entry(
        entry,
        title=f"KFG Vertretungsplan {class_name}",
        unique_id=class_name.lower(),
    )
    await hass.config_entries.async_reload(entry.entry_id)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    domain_data = hass.data.setdefault(DOMAIN, {})
    if "kollegium_owner" not in domain_data:
        domain_data["kollegium_owner"] = entry.entry_id
        _migrate_kollegium_entity(hass, entry)

    coordinator = KFGCoordinator(
        hass,
        base_url=entry.data["base_url"],
        scan_interval=entry.options.get(
            CONF_SCAN_INTERVAL,
            entry.data.get(CONF_SCAN_INTERVAL),
        ),
    )
    await coordinator.async_config_entry_first_refresh()
    domain_data[entry.entry_id] = coordinator
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        domain_data = hass.data[DOMAIN]
        domain_data.pop(entry.entry_id, None)
        if domain_data.get("kollegium_owner") == entry.entry_id:
            domain_data.pop("kollegium_owner", None)
            remaining = [
                item.entry_id
                for item in hass.config_entries.async_entries(DOMAIN)
                if item.entry_id != entry.entry_id and item.entry_id in domain_data
            ]
            if remaining:
                domain_data["kollegium_owner"] = remaining[0]
                if hass.is_running:
                    hass.async_create_task(hass.config_entries.async_reload(remaining[0]))
    return ok
