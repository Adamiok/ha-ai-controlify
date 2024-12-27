"""Process output from the AI."""

from homeassistant.core import Context
from homeassistant.components import conversation
from homeassistant.util import json
from homeassistant.helpers import intent

class OutputProcessor:
    """Process output from the AI."""
    
    def __init__(self, agent_manager: conversation.agent_manager.AgentManager, output: str) -> None:
        """Initialize the processor."""
        self.agent_manager = agent_manager
        self.output = output
    
    async def async_parse(self) -> str:
        """Parse the output. Returns the value to print to the user."""
        defaultAgent = self.agent_manager.async_get_agent(conversation.HOME_ASSISTANT_AGENT)
        
        if defaultAgent is None:
            raise ValueError(f"Default home assistant agent ({conversation.HOME_ASSISTANT_AGENT}) is non-existent. This indicates an issue with your installation")
        
        # {
        #     "response": "<response>",
        #     "actions": [
        #         "<commandWord> <params...>",
        #         "<commandWord> <params...>"
        #     ]
        # }
        aiResponseJson = json.json_loads_object(self.output)
        
        textToSpeak = aiResponseJson.get("response")
        if not isinstance(textToSpeak, str):
            raise ValueError(f"Expected string for response value, got {type(textToSpeak)}")
        
        commands = aiResponseJson.get("actions")
        if not isinstance(commands, list):
            raise ValueError(f"Expected a list for actions, got {type(commands)}")
        
        for command in commands:
            if not isinstance(command, str):
                raise ValueError(f"Expected a string for command, got {type(command)}")
            
            commandStr = str(command)
            conversationInput = conversation.ConversationInput(commandStr, Context(), None, None, "en")
            result = await defaultAgent.async_process(conversationInput)
            
            if result.response.response_type == intent.IntentResponseType.ERROR and (result.response.error_code == intent.IntentResponseErrorCode.NO_INTENT_MATCH or result.response.error_code == intent.IntentResponseErrorCode.NO_VALID_TARGETS):
                raise ValueError(f"Command executor could not execute command: {commandStr}")
        
        return str(textToSpeak)
        
