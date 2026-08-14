from __future__ import annotations
from urllib.parse import urlparse
import voluptuous as vol
from homeassistant import config_entries
from .const import CONF_BASE_URL, CONF_SCAN_INTERVAL, DEFAULT_BASE_URL, DEFAULT_SCAN_INTERVAL, DOMAIN

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        errors = {}
        if user_input is not None:
            base_url = user_input[CONF_BASE_URL].strip().rstrip("/")
            parsed = urlparse(base_url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                errors[CONF_BASE_URL] = "invalid_url"
            else:
                return self.async_create_entry(title="KFG Vertretungsplan", data={CONF_BASE_URL: base_url, CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL]})
        return self.async_show_form(step_id="user", data_schema=vol.Schema({vol.Required(CONF_BASE_URL, default=DEFAULT_BASE_URL): str, vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600))}), errors=errors)

    async def async_step_import(self, user_input):
        return await self.async_step_user(user_input)
