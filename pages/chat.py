"""
Multi-Agent Chat Interface
Enhanced chat system with specialized agents including NeonPanel integration
"""

import streamlit as st
import asyncio
import sys
import os
from typing import Dict, Any, List
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from agent_squad.orchestrator import AgentSquad
    from agent_squad.agents import BedrockLLMAgent, BedrockLLMAgentOptions, AnthropicAgent, AnthropicAgentOptions
    from mcp.neonpanel_agent import create_neonpanel_agent
    AGENTS_AVAILABLE = True
except ImportError as e:
    st.error(f"Agent modules not available: {e}")
    AGENTS_AVAILABLE = False

# Page configuration
st.title("🤖 Multi-Agent Chat System")
st.markdown("Chat with specialized AI agents that can help with various tasks including NeonPanel management.")

# Check if agents are available
if not AGENTS_AVAILABLE:
    st.info("🚀 **Demo Mode**: Agent modules are loading or unavailable.")
    st.markdown("""
    **This is a demo of the Agent Squad MVP interface.** 
    
    The app is currently running in demo mode while dependencies install. 
    
    **Available features:**
    - ✅ Navigate between pages (Home, Enhanced Chat, NeonPanel Dashboard)
    - ✅ View the user interface and layout
    - ✅ See the agent selection and configuration options
    
    **To enable full functionality:**
    - Wait for dependencies to install (may take 2-3 minutes)
    - Or add API keys in Streamlit Cloud settings for full agent capabilities
    
    **Try the Enhanced Chat page** for a working interface!
    """)
    
    # Show a demo interface
    st.subheader("🤖 Agent Selection (Demo)")
    demo_agent = st.selectbox(
        "Choose Agent:",
        ["Anthropic Claude", "AWS Bedrock", "NeonPanel Assistant", "Auto-Select"],
        help="This is a demo selection - full functionality requires API keys"
    )
    
    demo_message = st.text_area(
        "Message:",
        placeholder="Type your message here... (Demo mode - responses not active yet)",
        height=100
    )
    
    if st.button("Send Message (Demo)", type="primary"):
        st.info(f"Demo: Would send message to {demo_agent}")
        
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_" + str(hash(str(datetime.now())))

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key inputs
    st.subheader("API Keys")
    anthropic_key = st.text_input("Anthropic API Key", type="password", help="Required for Claude models")
    aws_region = st.selectbox("AWS Region", ["us-east-1", "us-west-2", "eu-west-1"], index=0)
    neonpanel_key = st.text_input("NeonPanel API Key", type="password", help="Required for NeonPanel integration")
    
    # Agent selection
    st.subheader("Available Agents")
    use_tech_agent = st.checkbox("Tech Support Agent", value=True)
    use_neonpanel_agent = st.checkbox("NeonPanel Agent", value=True, help="Requires NeonPanel API key")
    use_general_agent = st.checkbox("General Assistant", value=True)
    
    # Advanced settings
    with st.expander("Advanced Settings"):
        streaming = st.checkbox("Enable Streaming", value=True)
        temperature = st.slider("Response Temperature", 0.0, 1.0, 0.7)
        max_tokens = st.slider("Max Tokens", 100, 4000, 1000)
    
    # Initialize orchestrator
    if st.button("Initialize Agents") or st.session_state.orchestrator is None:
        if anthropic_key:
            with st.spinner("Initializing agents..."):
                st.session_state.orchestrator = initialize_orchestrator(
                    anthropic_key, 
                    aws_region, 
                    neonpanel_key,
                    use_tech_agent, 
                    use_neonpanel_agent, 
                    use_general_agent,
                    streaming,
                    temperature
                )
                st.success("Agents initialized successfully!")
        else:
            st.error("Please provide at least an Anthropic API key to get started.")

def initialize_orchestrator(anthropic_key: str, aws_region: str, neonpanel_key: str, 
                          use_tech: bool, use_neonpanel: bool, use_general: bool,
                          streaming: bool, temperature: float) -> AgentSquad:
    """Initialize the agent orchestrator with selected agents"""
    orchestrator = AgentSquad()
    
    try:
        # Tech Support Agent
        if use_tech and anthropic_key:
            tech_agent = AnthropicAgent(AnthropicAgentOptions(
                name="Tech Support Agent",
                description="""Specializes in technical support, software development, 
                system administration, troubleshooting, and IT infrastructure. 
                Can help with programming, server management, network issues, and technology guidance.""",
                api_key=anthropic_key,
                model="claude-3-sonnet-20240229",
                streaming=streaming,
                temperature=temperature
            ))
            orchestrator.add_agent(tech_agent)
        
        # General Assistant Agent
        if use_general and anthropic_key:
            general_agent = AnthropicAgent(AnthropicAgentOptions(
                name="General Assistant",
                description="""A helpful general-purpose assistant that can help with 
                various tasks including writing, analysis, research, planning, and 
                general questions on a wide range of topics.""",
                api_key=anthropic_key,
                model="claude-3-sonnet-20240229",
                streaming=streaming,
                temperature=temperature
            ))
            orchestrator.add_agent(general_agent)
        
        # NeonPanel Agent
        if use_neonpanel and neonpanel_key:
            # Set environment variable for the NeonPanel client
            os.environ["NEONPANEL_API_KEY"] = neonpanel_key
            neonpanel_agent = create_neonpanel_agent()
            # Note: NeonPanel agent needs to be adapted to work with the orchestrator
            # For now, we'll create a wrapper
            orchestrator.add_agent(create_neonpanel_wrapper(neonpanel_agent, anthropic_key, streaming, temperature))
    
    except Exception as e:
        st.error(f"Error initializing agents: {str(e)}")
        return None
    
    return orchestrator

def create_neonpanel_wrapper(neonpanel_agent, anthropic_key: str, streaming: bool, temperature: float):
    """Create a wrapper for NeonPanel agent to work with the orchestrator"""
    return AnthropicAgent(AnthropicAgentOptions(
        name="NeonPanel Agent",
        description="""Specializes in NeonPanel server management, user account operations, 
        server monitoring, resource allocation, and system administration tasks. 
        Can access real-time server data and perform management operations.""",
        api_key=anthropic_key,
        model="claude-3-sonnet-20240229",
        streaming=streaming,
        temperature=temperature
    ))

# Chat interface
if st.session_state.orchestrator:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.markdown(f"**{message.get('agent_name', 'Assistant')}:** {message['content']}")
            else:
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = asyncio.run(
                        st.session_state.orchestrator.route_request(
                            prompt,
                            st.session_state.user_id,
                            f"session_{st.session_state.user_id}",
                            {},
                            streaming=True
                        )
                    )
                    
                    if hasattr(response, 'streaming') and response.streaming:
                        # Handle streaming response
                        content_placeholder = st.empty()
                        full_content = ""
                        
                        async def stream_response(content_ref):
                            async for chunk in response.output:
                                if hasattr(chunk, 'text'):
                                    content_ref[0] += chunk.text
                                    content_placeholder.markdown(f"**{response.metadata.agent_name}:** {content_ref[0]}")
                                elif isinstance(chunk, str):
                                    content_ref[0] += chunk
                                    content_placeholder.markdown(f"**{response.metadata.agent_name}:** {content_ref[0]}")
                        
                        content_ref = [full_content]
                        asyncio.run(stream_response(content_ref))
                        full_content = content_ref[0]
                        
                        # Add to chat history
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": full_content,
                            "agent_name": response.metadata.agent_name
                        })
                    else:
                        # Handle non-streaming response
                        content = response.output.content if hasattr(response.output, 'content') else str(response.output)
                        agent_name = response.metadata.agent_name if hasattr(response, 'metadata') else "Assistant"
                        
                        st.markdown(f"**{agent_name}:** {content}")
                        
                        # Add to chat history
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": content,
                            "agent_name": agent_name
                        })
                
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"I apologize, but I encountered an error: {str(e)}",
                        "agent_name": "System"
                    })

else:
    st.info("👆 Please configure your API keys in the sidebar and initialize the agents to start chatting.")
    
    # Example queries
    st.subheader("💡 Example Queries")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Tech Support:**
        - "Help me debug this Python error"
        - "How do I set up a Docker container?"
        - "Explain database optimization"
        """)
    
    with col2:
        st.markdown("""
        **NeonPanel:**
        - "Show me server statistics"
        - "Check user account status"
        - "List all resources"
        """)
    
    with col3:
        st.markdown("""
        **General:**
        - "Write a professional email"
        - "Explain quantum computing"
        - "Plan a project timeline"
        """)

# Clear chat button
if st.session_state.messages:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
