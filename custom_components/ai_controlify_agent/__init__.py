"""AI Control Agent Integration

An integration that gives AI assistants, of your choice, the ability to command you home.

### WARNING ###
Do not expose security related devices (locks, doors, etc.) to the chatbot
"""

from __future__ import annotations

from typing import Literal

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import ulid
from homeassistant.helpers import intent
from homeassistant.core import HomeAssistant
from homeassistant.const import MATCH_ALL

from .const import (
    LOGGER,
    CONF_AGENT
)
from .output_processor import (
    OutputProcessor
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AI Control Agent from a config entry."""
    agent_manager = conversation.agent_manager.get_agent_manager(hass)
    
    agentId = entry.options.get(CONF_AGENT)
    if agentId is None:
        LOGGER.error("No agent configured. Go to the CONFIGURE page for this integration and specify the model to use")
        return False
    
    agent = AiControllerAgent(hass, entry, agent_manager)
    conversation.async_set_agent(hass, entry, agent)
    
    return True

class AiControllerAgent(conversation.models.AbstractConversationAgent):
    """AI Control Agent."""
    
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, agent_manager: conversation.agent_manager.AgentManager) -> None:
        """Initialize the agent."""
        self.hass = hass
        self.entry = entry
        self.agent_manager = agent_manager
    
    
    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        
        return MATCH_ALL
    
    
    async def async_process(self, user_input: conversation.ConversationInput) -> conversation.ConversationResult:
        """Process a sentence."""
        if user_input.conversation_id is None:
            user_input.conversation_id = ulid.ulid()
        
        
        agent = self.agent_manager.async_get_agent(str(self.entry.options.get(CONF_AGENT)))
        
        if agent is None:
            raise ValueError(f"Agent with name {self.entry.options.get(CONF_AGENT)} is non-existent")
        
        result = await agent.async_process(user_input)
        if result.response.response_type == intent.IntentResponseType.ERROR:
            LOGGER.error("AI model returned an error code. Check the logs for the relevant integration")
            return result
        
        result.response.speech["plain"]["speech"] = await self.process_output(result.response.speech["plain"]["speech"])
        
        return result
    
    
    async def process_output(self, output: str) -> str:
        """Process the output from the AI"""
        
        processor = OutputProcessor(self.agent_manager, output)
        
        try:
            processed = await processor.async_parse()
        except ValueError as error:
            LOGGER.warn("AI returned invalid response: %s", error.args)
            return "An error occurred, check logs for more information!"
        
        return processed
