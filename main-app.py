import streamlit as st

st.set_page_config(
    page_title="Agent Squad MVP",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/awslabs/agent-squad',
        'Report a bug': "https://github.com/awslabs/agent-squad/issues",
        'About': "Agent Squad MVP - Multi-Agent AI Assistant"
    }
)

# Load custom CSS for mobile responsiveness
st.markdown("""
<style>
/* Mobile-first responsive design */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Chat message styling */
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    border-left: 4px solid #ddd;
    background-color: #f8f9fa;
}

.agent-response {
    border-left-color: #2196F3;
}

.user-message {
    border-left-color: #FF9800;
    background-color: #fff3e0;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .main .block-container {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    
    .stSelectbox > div > div {
        font-size: 14px;
    }
    
    .stButton > button {
        width: 100%;
        margin-top: 0.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Navigation
pg = st.navigation(
    [
        st.Page("pages/home.py", title="Home", icon="🏠"),
        st.Page("pages/chat.py", title="Basic Chat", icon="💬"),
        st.Page("pages/simple_chat.py", title="Enhanced Chat", icon="🚀"),
        # st.Page("pages/enhanced_chat.py", title="Advanced Chat", icon="⚡"),
        # st.Page("movie-production/movie-production-demo.py", title="AI Movie Production", icon="🎬"),
        # st.Page("travel-planner/travel-planner-demo.py", title="AI Travel Planner", icon="✈️"),
        st.Page("pages/neonpanel.py", title="NeonPanel Dashboard", icon="🔧"),
    ])
pg.run()