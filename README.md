# AI Controlify Agent

This is a custom component for Home Assistant.

## Features

This custom component allows an LLM (Large Language Model) to manage devices in your home.

It is built on top of the voice agent system in Home Assistant, so you can use any LLM service (e.g., Ollama, OpenAI), and even different LLMs for each agent.

## Installation

1. Set up your LLM integration with at least one voice agent.
2. Install by registering it as a [custom repository in HACS](https://www.hacs.xyz/docs/faq/custom_repositories/) (type: integration) or by copying the `ai_controlify_agent` folder into `<config>/custom_components`.
3. Restart Home Assistant.
4. Go to **Settings** --> **Devices & Services**.
5. In the bottom right corner, select the **Add Integration** button.
6. Search for and click on "AI Controlify Agent."
7. Set a name for the agent.
8. Click on **AI Controlify Agent** and select **Configure** for your created agent.
9. Set the **AI Conversation Agent** to your LLM voice agent.
10. Restart Home Assistant (yep, again—sorry for the inconvenience; Home Assistant doesn’t support choosing voice agents during the initial configuration).
11. Go to **Settings** --> **Voice Assistants**.
12. Click to edit the Assistant (named "Home Assistant" by default).
13. Select the name of your AI Controlify Agent from the **Conversation Agent** tab.
14. Click on **Expose** and add all the entities you want to give the LLM access to (Note: Do not expose security-related devices, as we cannot guarantee the AI’s responses).
15. Set the prompt of your LLM agent to the one in `prompt.txt`.

## Suggestions

I recommend to enable `Prefer handling commands locally` on the **AI Controlify Agent**, to reduce the wait time (and cost) for simple commands. This setting attempts to use the fast local text matching assistant, before calling this integration and using an LLM.

## Contributions

Contributions are welcome! Feel free to open issues or submit PRs.
