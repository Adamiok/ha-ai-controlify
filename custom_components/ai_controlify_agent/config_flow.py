"""Config flow for AI Control Agent integration."""

from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    ConversationAgentSelector,
    ConversationAgentSelectorConfig
)

from .const import (
    LOGGER,
    DOMAIN,
    CONF_AGENT,
    DEFAULT_NAME
)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """AI Controller config flow handler."""
    
    VERSION=1
    
    async def async_step_user(self, user_input: None = None) -> FlowResult:
        """Handle the initial step."""
        LOGGER.debug("Adding new integration")
        
        return self.async_show_form(
            step_id="final",
            data_schema= await self.async_config_user_data_schema()
        )
    
    
    async def async_step_final(self, user_input: dict[str, Any]) -> FlowResult:
        """Handle the final step."""
        LOGGER.debug("ConfigFlow::async_step_final %s", user_input)
        
        return self.async_create_entry(
            title=user_input.get(CONF_NAME, DEFAULT_NAME),
            data=user_input,
        )
    
    async def async_config_user_data_schema(self) -> vol.Schema:
        """Return schema for configuration."""
        return vol.Schema({
            vol.Required(CONF_NAME, default=DEFAULT_NAME): str, # type: ignore
        })
    
    
    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlow(config_entry)


class OptionsFlow(config_entries.OptionsFlow):
    """AI Constroller options flow handler."""
    
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry
    
    
    async def async_step_init(self, user_input: None = None) -> FlowResult:
        """Handle the initial step."""
        return self.async_show_form(
            step_id="final",
            data_schema= await self.async_options_init_data_schema()
        )
    
    
    async def async_step_final(self, user_input: dict[str, Any]) -> FlowResult:
        """Handle the final step."""
        LOGGER.debug("OptionsFlow::async_step_final %s", user_input)
        
        options = dict(self.config_entry.options)
        options.update(user_input)
        return self.async_create_entry(
            data=options,
        )
    
    
    async def async_options_init_data_schema(self) -> vol.Schema:
        """Return schema for configuration"""
        return vol.Schema({
            vol.Required(
                CONF_AGENT,
                description={"suggested_value": self.config_entry.options.get(CONF_AGENT, "")}
            ): ConversationAgentSelector(ConversationAgentSelectorConfig())
        })
