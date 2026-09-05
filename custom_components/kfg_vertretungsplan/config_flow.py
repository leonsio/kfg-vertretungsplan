from __future__ import annotations

from urllib.parse import urlparse

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    CONF_BASE_URL,
    CONF_CLASS,
    CONF_SCAN_INTERVAL,
    DEFAULT_BASE_URL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

SCAN_INTERVAL_SCHEMA = vol.All(vol.Coerce(int), vol.Range(min=60, max=3600))
CLASS_SCHEMA = vol.All(str, vol.Length(min=1, max=32))


def _configured_class(entry) -> str:
    return str(entry.options.get(CONF_CLASS, entry.data.get(CONF_CLASS, ""))).strip()


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            base_url = user_input[CONF_BASE_URL].strip().rstrip("/")
            class_name = user_input[CONF_CLASS].strip()
            parsed = urlparse(base_url)
            if not class_name:
                errors[CONF_CLASS] = "invalid_class"
            elif parsed.scheme not in ("http", "https") or not parsed.netloc:
                errors[CONF_BASE_URL] = "invalid_url"
            elif any(
                _configured_class(entry).lower() == class_name.lower()
                for entry in self.hass.config_entries.async_entries(DOMAIN)
            ):
                errors[CONF_CLASS] = "class_already_configured"
            else:
                return self.async_create_entry(
                    title=f"KFG Vertretungsplan {class_name}",
                    data={
                        CONF_BASE_URL: base_url,
                        CONF_CLASS: class_name,
                        CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_CLASS): CLASS_SCHEMA,
                    vol.Required(CONF_BASE_URL, default=DEFAULT_BASE_URL): str,
                    vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): SCAN_INTERVAL_SCHEMA,
                }
            ),
            errors=errors,
        )

    async def async_step_import(self, user_input):
        return await self.async_step_user(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return KFGOptionsFlowHandler(config_entry)


class KFGOptionsFlowHandler(config_entries.OptionsFlow):
    """Allow class and polling interval to be changed after installation."""

    def __init__(self, config_entry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            class_name = user_input[CONF_CLASS].strip()
            if not class_name:
                return self.async_show_form(
                    step_id="init",
                    data_schema=self._schema(user_input),
                    errors={CONF_CLASS: "invalid_class"},
                )
            for other in self.hass.config_entries.async_entries(DOMAIN):
                if other.entry_id == self.config_entry.entry_id:
                    continue
                if _configured_class(other).lower() == class_name.lower():
                    return self.async_show_form(
                        step_id="init",
                        data_schema=self._schema(user_input),
                        errors={CONF_CLASS: "class_already_configured"},
                    )
            return self.async_create_entry(
                data={
                    CONF_CLASS: class_name,
                    CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                }
            )

        current_class = self.config_entry.options.get(
            CONF_CLASS,
            self.config_entry.data.get(CONF_CLASS, "alle"),
        )
        current_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        return self.async_show_form(
            step_id="init",
            data_schema=self._schema(
                {CONF_CLASS: current_class, CONF_SCAN_INTERVAL: current_interval}
            ),
        )

    @staticmethod
    def _schema(values):
        return vol.Schema(
            {
                vol.Required(CONF_CLASS, default=values.get(CONF_CLASS, "alle")): CLASS_SCHEMA,
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=values.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                ): SCAN_INTERVAL_SCHEMA,
            }
        )
