import streamlit as st
import asyncio
import uuid
from datetime import datetime
try:
    from agent_squad.orchestrator import AgentSquad
    from agent_squad.agents import AnthropicAgent, BedrockLLMAgent, BedrockLLMAgentOptions
    AGENTS_AVAILABLE = True
except ImportError as e:
    st.error(f"Agent modules not available: {e}")
    AGENTS_AVAILABLE = False

try:
    from streamlit_chat import message
    STREAMLIT_CHAT_AVAILABLE = True
except ImportError:
    st.warning("streamlit_chat not available - using basic chat interface")
    STREAMLIT_CHAT_AVAILABLE = False
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("🤖 Enhanced Multi-Agent Chat")
st.markdown("Interact with specialized AI agents through our enhanced chat interface")

# Check if agents are available
if not AGENTS_AVAILABLE:
    st.error("Agent modules are not properly installed. Please check your installation.")
    st.code("pip install -r requirements.txt")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None
if "chat_session_id" not in st.session_state:
    st.session_state.chat_session_id = str(uuid.uuid4())

# Sidebar configuration
with st.sidebar:
    st.header("🔧 Chat Configuration")
    
    # Agent selection
    available_agents = {
        "Anthropic Claude": "anthropic",
        "AWS Bedrock Claude": "bedrock",
        "NeonPanel Assistant": "neonpanel",
        "Auto-Select Best Agent": "auto"
    }
    
    selected_agent = st.selectbox(
        "Choose Agent:",
        options=list(available_agents.keys()),
        index=3  # Default to auto-select
    )
    
    # Chat settings
    st.subheader("💬 Chat Settings")
    enable_streaming = st.checkbox("Enable Streaming", value=True)
    save_history = st.checkbox("Save Chat History", value=True)
    max_context_messages = st.slider("Context Messages", 1, 20, 10)
    
    # API Configuration Status
    st.subheader("🔑 API Status")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    aws_configured = bool(os.getenv("AWS_ACCESS_KEY_ID"))
    neonpanel_key = os.getenv("NEONPANEL_API_KEY")
    
    st.write("🔹 Anthropic:", "✅" if anthropic_key else "❌")
    st.write("🔹 AWS Bedrock:", "✅" if aws_configured else "❌")
    st.write("🔹 NeonPanel:", "✅" if neonpanel_key else "❌")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chat_session_id = str(uuid.uuid4())
        st.rerun()

# Initialize orchestrator
@st.cache_resource
def get_orchestrator():
    orchestrator = AgentSquad()
    
    # Add Anthropic agent if API key available
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            anthropic_agent = AnthropicAgent({
                "name": "Claude Assistant",
                "description": "Helpful AI assistant powered by Anthropic's Claude",
                "streaming": True
            })
            orchestrator.add_agent(anthropic_agent)
        except Exception as e:
            st.sidebar.error(f"Failed to initialize Anthropic agent: {e}")
    
    # Add Bedrock agent if AWS configured
    if os.getenv("AWS_ACCESS_KEY_ID"):
        try:
            bedrock_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
                name="Bedrock Claude",
                description="AWS Bedrock Claude for enterprise tasks",
                streaming=True,
                model_id="anthropic.claude-3-sonnet-20240229-v1:0"
            ))
            orchestrator.add_agent(bedrock_agent)
        except Exception as e:
            st.sidebar.error(f"Failed to initialize Bedrock agent: {e}")
    
    return orchestrator

# Get orchestrator instance
if st.session_state.orchestrator is None:
    try:
        st.session_state.orchestrator = get_orchestrator()
        st.success("✅ Agent orchestrator initialized successfully!")
    except Exception as e:
        st.error(f"❌ Failed to initialize agents: {e}")
        st.info("💡 Please configure your API keys in the .env file")

# Display chat history
st.subheader("💬 Chat History")

# Create chat container
chat_container = st.container()

with chat_container:
    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                message(msg["content"], is_user=True, key=f"user_{i}")
            else:
                agent_name = msg.get("agent_name", "Assistant")
                message(
                    f"**{agent_name}:** {msg['content']}", 
                    is_user=False, 
                    key=f"assistant_{i}"
                )
    else:
        st.info("👋 Start a conversation by typing a message below!")

# Chat input
st.subheader("✍️ Your Message")

# Create input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Type your message here...",
        height=100,
        placeholder="Ask me anything! I can help with various tasks.",
        key="user_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        submit_button = st.form_submit_button("🚀 Send Message", use_container_width=True)
    with col2:
        example_btn = st.form_submit_button("💡 Try Example", use_container_width=True)
    with col3:
        voice_btn = st.form_submit_button("🎤 Voice Input", use_container_width=True, disabled=True)

# Handle example button
if example_btn:
    examples = [
        "What are the latest trends in AI?",
        "Help me plan a trip to Japan",
        "Explain quantum computing in simple terms",
        "Write a creative story about space exploration",
        "What are best practices for software development?"
    ]
    import random
    user_input = random.choice(examples)
    submit_button = True  # Trigger processing

# Process user input
if submit_button and user_input.strip():
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    
    # Show thinking spinner
    with st.spinner("🤔 Agent is thinking..."):
        try:
            if st.session_state.orchestrator:
                # Prepare context from recent messages
                context = {
                    "session_id": st.session_state.chat_session_id,
                    "recent_messages": st.session_state.messages[-max_context_messages:],
                    "agent_preference": available_agents.get(selected_agent, "auto")
                }
                
                # Route request to appropriate agent
                response = asyncio.run(
                    st.session_state.orchestrator.route_request(
                        user_input,
                        user_id="streamlit_user",
                        session_id=st.session_state.chat_session_id,
                        additional_params=context
                    )
                )
                
                # Handle response
                if hasattr(response, 'streaming') and response.streaming and enable_streaming:
                    # Streaming response
                    with st.empty():
                        response_placeholder = st.empty()
                        
                        async def process_stream():
                            full_response = ""
                            async for chunk in response.output:
                                if hasattr(chunk, 'text'):
                                    full_response += chunk.text
                                elif isinstance(chunk, str):
                                    full_response += chunk
                                
                                # Update display
                                response_placeholder.markdown(
                                    f"**🤖 {response.metadata.agent_name}:** {full_response}"
                                )
                            return full_response
                        
                        full_response = asyncio.run(process_stream())
                        
                        # Add to chat history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": full_response,
                            "agent_name": response.metadata.agent_name,
                            "timestamp": datetime.now().isoformat()
                        })
                else:
                    # Non-streaming response
                    agent_name = getattr(response.metadata, 'agent_name', 'Assistant')
                    content = response.output if hasattr(response, 'output') else str(response)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": content,
                        "agent_name": agent_name,
                        "timestamp": datetime.now().isoformat()
                    })
                
                # Auto-save chat history if enabled
                if save_history:
                    try:
                        os.makedirs("data/chat_history", exist_ok=True)
                        history_file = f"data/chat_history/{st.session_state.chat_session_id}.json"
                        with open(history_file, 'w') as f:
                            json.dump(st.session_state.messages, f, indent=2)
                    except Exception as e:
                        st.sidebar.warning(f"Failed to save chat history: {e}")
                
            else:
                st.error("❌ No agents available. Please configure your API keys.")
                
        except Exception as e:
            st.error(f"❌ Error processing message: {e}")
            st.info("💡 This might be due to missing API keys or network issues.")
    
    # Rerun to update the chat display
    st.rerun()

# Chat statistics
if st.session_state.messages:
    with st.expander("📊 Chat Statistics"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Messages", len(st.session_state.messages))
        
        with col2:
            user_messages = [msg for msg in st.session_state.messages if msg["role"] == "user"]
            st.metric("User Messages", len(user_messages))
        
        with col3:
            assistant_messages = [msg for msg in st.session_state.messages if msg["role"] == "assistant"]
            st.metric("Assistant Messages", len(assistant_messages))
        
        with col4:
            if assistant_messages:
                agents_used = set(msg.get("agent_name", "Unknown") for msg in assistant_messages)
                st.metric("Agents Used", len(agents_used))

# Export chat functionality
if st.session_state.messages:
    with st.expander("💾 Export Chat"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Export as JSON"):
                chat_export = {
                    "session_id": st.session_state.chat_session_id,
                    "export_time": datetime.now().isoformat(),
                    "messages": st.session_state.messages
                }
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(chat_export, indent=2),
                    file_name=f"chat_export_{st.session_state.chat_session_id[:8]}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📝 Export as Text"):
                text_export = f"Chat Session: {st.session_state.chat_session_id}\n"
                text_export += f"Exported: {datetime.now().isoformat()}\n"
                text_export += "=" * 50 + "\n\n"
                
                for msg in st.session_state.messages:
                    timestamp = msg.get("timestamp", "")
                    if msg["role"] == "user":
                        text_export += f"👤 User [{timestamp}]:\n{msg['content']}\n\n"
                    else:
                        agent = msg.get("agent_name", "Assistant")
                        text_export += f"🤖 {agent} [{timestamp}]:\n{msg['content']}\n\n"
                
                st.download_button(
                    label="Download Text",
                    data=text_export,
                    file_name=f"chat_export_{st.session_state.chat_session_id[:8]}.txt",
                    mime="text/plain"
                )

# Help section
with st.expander("❓ Help & Tips"):
    st.markdown("""
    ### 🚀 **How to Use Enhanced Chat:**
    
    1. **Configure API Keys**: Add your API keys to the `.env` file
    2. **Select Agent**: Choose which agent to use or let the system auto-select
    3. **Type Message**: Enter your question or request
    4. **Get Response**: The agent will provide a helpful response
    
    ### 💡 **Features:**
    - ✅ **Multi-Agent Support**: Switch between different AI models
    - ✅ **Streaming Responses**: Real-time response generation
    - ✅ **Chat History**: Persistent conversation memory
    - ✅ **Export Options**: Save your conversations
    - ✅ **Context Awareness**: Agents remember conversation history
    
    ### 🔧 **Troubleshooting:**
    - **No agents available**: Configure API keys in `.env` file
    - **Slow responses**: Check your internet connection
    - **Errors**: Try refreshing the page or clearing chat history
    """)

# Footer
st.markdown("---")
st.markdown(
    "🤖 **Enhanced Multi-Agent Chat** | Built with Agent Squad & Streamlit | "
    f"Session ID: `{st.session_state.chat_session_id[:8]}...`"
)
