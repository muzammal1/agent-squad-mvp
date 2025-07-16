import uuid
import os
import chainlit as cl
from agents import create_tech_agent, create_travel_agent, create_health_agent, create_neonpanel_agent
from agent_squad.orchestrator import AgentSquad, AgentSquadConfig
from agent_squad.classifiers import BedrockClassifier, BedrockClassifierOptions, AnthropicClassifier, AnthropicClassifierOptions
from agent_squad.types import ConversationMessage
from agent_squad.agents import AgentResponse

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize the orchestrator with fallback options
def initialize_orchestrator():
    """Initialize orchestrator with available classifier options"""
    classifier = None
    
    # Try Anthropic first (more accessible)
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        classifier = AnthropicClassifier(AnthropicClassifierOptions(
            api_key=anthropic_key,
            model="claude-3-haiku-20240307",
            temperature=0.7
        ))
    else:
        # Fallback to Bedrock if available
        try:
            classifier = BedrockClassifier(BedrockClassifierOptions(
                model_id='anthropic.claude-3-haiku-20240307-v1:0',
                inference_config={
                    'maxTokens': 500,
                    'temperature': 0.7,
                    'topP': 0.9
                }
            ))
        except Exception:
            # Use default classifier if neither available
            pass
    
    return AgentSquad(
        options=AgentSquadConfig(
            LOG_AGENT_CHAT=True,
            LOG_CLASSIFIER_CHAT=True,
            LOG_CLASSIFIER_RAW_OUTPUT=True,
            LOG_CLASSIFIER_OUTPUT=True,
            LOG_EXECUTION_TIMES=True,
            MAX_RETRIES=3,
            USE_DEFAULT_AGENT_IF_NONE_IDENTIFIED=True,
            MAX_MESSAGE_PAIRS_PER_AGENT=10
        ),
        classifier=classifier
    )

orchestrator = initialize_orchestrator()
)

# Add agents to the orchestrator
orchestrator.add_agent(create_tech_agent())
orchestrator.add_agent(create_travel_agent())
orchestrator.add_agent(create_health_agent())

@cl.on_chat_start
async def start():
    cl.user_session.set("user_id", str(uuid.uuid4()))
    cl.user_session.set("session_id", str(uuid.uuid4()))
    cl.user_session.set("chat_history", [])



@cl.on_message
async def main(message: cl.Message):
    user_id = cl.user_session.get("user_id")
    session_id = cl.user_session.get("session_id")

    msg = cl.Message(content="")

    await msg.send()  # Send the message immediately to start streaming
    cl.user_session.set("current_msg", msg)

    response:AgentResponse = await orchestrator.route_request(message.content, user_id, session_id, {})


    # Handle non-streaming responses
    if isinstance(response, AgentResponse) and response.streaming is False:
        # Handle regular response
        if isinstance(response.output, str):
            await msg.stream_token(response.output)
        elif isinstance(response.output, ConversationMessage):
                await msg.stream_token(response.output.content[0].get('text'))
    await msg.update()


if __name__ == "__main__":
    cl.run()