import streamlit as st
import os
import asyncio
from datetime import datetime
import json
import time

# Import mock agents for demo functionality
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from mock_agents import create_demo_orchestrator, simulate_streaming_response
    DEMO_AVAILABLE = True
except ImportError:
    DEMO_AVAILABLE = False

# Simple chat interface with working demo functionality
st.title("🚀 Enhanced Chat Interface")

st.markdown("""
**Enhanced Multi-Agent Chat System** ✨

This interface provides advanced chat capabilities with multiple agent types,
streaming responses, and conversation management.

🎯 **Working Demo**: This page uses mock agents to demonstrate the full chat experience!
""")

# Check if demo is available
if not DEMO_AVAILABLE:
    st.error("Demo agents not available. Please check the mock_agents.py file.")
    st.stop()

# Initialize session state
if "demo_messages" not in st.session_state:
    st.session_state.demo_messages = []
if "demo_orchestrator" not in st.session_state:
    st.session_state.demo_orchestrator = create_demo_orchestrator()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Chat Configuration")
    
    # Agent selection
    agent_type = st.selectbox(
        "Choose Agent:",
        ["auto", "anthropic", "bedrock", "neonpanel"],
        format_func=lambda x: {
            "auto": "🎯 Auto-Select Best Agent",
            "anthropic": "🤖 Anthropic Claude",
            "bedrock": "⚡ AWS Bedrock",
            "neonpanel": "🔧 NeonPanel Assistant"
        }[x],
        help="Select which agent to use for responses"
    )
    
    # Chat settings
    st.subheader("💬 Chat Settings")
    enable_streaming = st.checkbox("Enable Streaming", value=True)
    show_metadata = st.checkbox("Show Response Metadata", value=False)
    
    # Demo info
    st.subheader("📊 Demo Info")
    st.metric("Messages Sent", len(st.session_state.demo_messages))
    if st.session_state.demo_messages:
        last_agent = st.session_state.demo_messages[-1].get("agent_used", "Unknown")
        st.metric("Last Agent Used", last_agent)
    
    # Clear chat
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.demo_messages = []
        st.rerun()

# Main chat interface
st.subheader("💬 Chat Messages")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.demo_messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])
                if show_metadata and "metadata" in message:
                    with st.expander("🔍 Response Metadata"):
                        st.json(message["metadata"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat
    st.session_state.demo_messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    
    # Display user message immediately
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        if enable_streaming:
            # Simulate streaming response
            response_placeholder = st.empty()
            full_response = ""
            
            # Simulate async response generation
            try:
                # Mock async call
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response, metadata = loop.run_until_complete(
                    st.session_state.demo_orchestrator.process_message(user_input, agent_type)
                )
                loop.close()
                
                # Simulate streaming by displaying response word by word
                words = response.split()
                for i in range(len(words)):
                    partial_response = " ".join(words[:i+1])
                    response_placeholder.write(partial_response)
                    time.sleep(0.05)  # Simulate typing delay
                
                full_response = response
                
            except Exception as e:
                full_response = f"Demo response for: '{user_input}'. This shows how the streaming interface works!"
                metadata = {"demo_mode": True, "error": str(e)}
                
                for word in full_response.split():
                    full_response_partial = full_response[:len(full_response.split())]
                    response_placeholder.write(" ".join(full_response.split()[:len(full_response_partial.split()) + 1]))
                    time.sleep(0.05)
        else:
            # Non-streaming response
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                full_response, metadata = loop.run_until_complete(
                    st.session_state.demo_orchestrator.process_message(user_input, agent_type)
                )
                loop.close()
            except Exception as e:
                full_response = f"Demo response for: '{user_input}'. This shows how the chat interface works!"
                metadata = {"demo_mode": True, "error": str(e)}
            
            st.write(full_response)
        
        # Show metadata if enabled
        if show_metadata:
            with st.expander("🔍 Response Metadata"):
                st.json(metadata)
    
    # Add assistant response to chat history
    st.session_state.demo_messages.append({
        "role": "assistant",
        "content": full_response,
        "agent_used": metadata.get("agent_used", "Demo Agent"),
        "agent_type": agent_type,
        "metadata": metadata,
        "timestamp": datetime.now().isoformat()
    })
    
    # Auto-scroll to bottom (rerun to update the display)
    st.rerun()

# Demo suggestions
if not st.session_state.demo_messages:
    st.subheader("💡 Try These Demo Messages")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔧 Ask about databases", key="demo1"):
            st.session_state.temp_message = "How do I optimize my PostgreSQL database performance?"
            st.rerun()
    
    with col2:
        if st.button("🤖 General AI question", key="demo2"):
            st.session_state.temp_message = "Explain machine learning in simple terms"
            st.rerun()
    
    with col3:
        if st.button("⚡ Enterprise question", key="demo3"):
            st.session_state.temp_message = "What are AWS best practices for scaling applications?"
            st.rerun()

# Handle demo button clicks
if hasattr(st.session_state, 'temp_message'):
    # Simulate user input
    user_input = st.session_state.temp_message
    del st.session_state.temp_message
    
    # Process the message (same logic as above)
    st.session_state.demo_messages.append({
        "role": "user", 
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response, metadata = loop.run_until_complete(
            st.session_state.demo_orchestrator.process_message(user_input, agent_type)
        )
        loop.close()
    except Exception:
        response = f"Demo response for: '{user_input}'"
        metadata = {"demo_mode": True}
    
    st.session_state.demo_messages.append({
        "role": "assistant",
        "content": response,
        "agent_used": metadata.get("agent_used", "Demo Agent"),
        "metadata": metadata,
        "timestamp": datetime.now().isoformat()
    })
    
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>🚀 Agent Squad MVP Demo | Enhanced Chat Interface</small>
</div>
""", unsafe_allow_html=True)
