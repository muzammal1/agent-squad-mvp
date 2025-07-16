"""
NeonPanel Dashboard
Dedicated interface for NeonPanel management and monitoring
"""

import streamlit as st
import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.neonpanel_client import neonpanel_client

# Page configuration
st.title("🔧 NeonPanel Dashboard")
st.markdown("Monitor and manage your NeonPanel infrastructure")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    neonpanel_key = st.text_input("NeonPanel API Key", type="password")
    neonpanel_url = st.text_input("NeonPanel Base URL", value="https://api.neonpanel.com")
    
    if st.button("Connect to NeonPanel"):
        if neonpanel_key and neonpanel_url:
            os.environ["NEONPANEL_API_KEY"] = neonpanel_key
            os.environ["NEONPANEL_BASE_URL"] = neonpanel_url
            st.success("Configuration saved!")
        else:
            st.error("Please provide both API key and URL")
    
    st.divider()
    
    # Auto-refresh
    auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
    if auto_refresh:
        st.info("Dashboard will auto-refresh every 30 seconds")

# Check if configured
if not os.getenv("NEONPANEL_API_KEY"):
    st.warning("Please configure your NeonPanel API key in the sidebar to access the dashboard.")
    st.stop()

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🖥️ Servers", "👥 Users", "🔍 Search"])

with tab1:
    st.header("📊 System Overview")
    
    # Refresh button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    with col2:
        last_updated = st.empty()
        last_updated.text(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    # Server statistics
    try:
        with st.spinner("Fetching server statistics..."):
            server_stats = asyncio.run(neonpanel_client.get_server_stats())
        
        if server_stats and 'error' not in server_stats:
            # Display metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Total Servers",
                    value=server_stats.get('total_servers', 'N/A'),
                    delta=server_stats.get('servers_change', None)
                )
            
            with col2:
                st.metric(
                    label="Active Servers",
                    value=server_stats.get('active_servers', 'N/A'),
                    delta=server_stats.get('active_change', None)
                )
            
            with col3:
                st.metric(
                    label="CPU Usage",
                    value=f"{server_stats.get('avg_cpu_usage', 'N/A')}%",
                    delta=f"{server_stats.get('cpu_change', 0)}%"
                )
            
            with col4:
                st.metric(
                    label="Memory Usage",
                    value=f"{server_stats.get('avg_memory_usage', 'N/A')}%",
                    delta=f"{server_stats.get('memory_change', 0)}%"
                )
            
            # Additional charts or data visualization could go here
            st.subheader("📈 Trends")
            st.info("Charts and graphs will be displayed here when real data is available")
            
        else:
            st.error("Unable to fetch server statistics. Please check your API key and connection.")
            if server_stats.get('error'):
                st.error(f"Error: {server_stats['error']}")
    
    except Exception as e:
        st.error(f"Error connecting to NeonPanel: {str(e)}")

with tab2:
    st.header("🖥️ Server Management")
    
    # Server list and actions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Server List")
        # This would typically show a list of servers
        st.info("Server list will be displayed here when connected to NeonPanel API")
    
    with col2:
        st.subheader("Quick Actions")
        
        server_id = st.text_input("Server ID")
        action = st.selectbox("Action", ["start", "stop", "restart", "status"])
        
        if st.button("Execute Action"):
            if server_id and action:
                try:
                    with st.spinner(f"Executing {action} on server {server_id}..."):
                        result = asyncio.run(neonpanel_client.execute_server_action(server_id, action))
                    
                    if result and 'error' not in result:
                        st.success(f"Action '{action}' executed successfully on server {server_id}")
                        st.json(result)
                    else:
                        st.error(f"Failed to execute action: {result.get('error', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"Error executing action: {str(e)}")
            else:
                st.warning("Please provide both server ID and action")

with tab3:
    st.header("👥 User Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("User Lookup")
        user_id = st.text_input("User ID")
        
        if st.button("Get User Data"):
            if user_id:
                try:
                    with st.spinner(f"Fetching data for user {user_id}..."):
                        user_data = asyncio.run(neonpanel_client.get_user_data(user_id))
                    
                    if user_data and 'error' not in user_data:
                        st.success(f"User data retrieved for {user_id}")
                        
                        # Display user information
                        st.subheader("User Information")
                        for key, value in user_data.items():
                            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                    else:
                        st.error("User not found or error retrieving data")
                
                except Exception as e:
                    st.error(f"Error fetching user data: {str(e)}")
            else:
                st.warning("Please provide a user ID")
    
    with col2:
        st.subheader("User Statistics")
        st.info("User statistics will be displayed here")

with tab4:
    st.header("🔍 Resource Search")
    
    search_query = st.text_input("Search Query", placeholder="Enter search terms...")
    
    if st.button("Search Resources") or search_query:
        if search_query:
            try:
                with st.spinner("Searching resources..."):
                    search_results = asyncio.run(neonpanel_client.search_resources(search_query))
                
                if search_results:
                    st.success(f"Found {len(search_results)} results")
                    
                    # Display search results
                    for i, result in enumerate(search_results):
                        with st.expander(f"Result {i+1}: {result.get('name', 'Unknown')}"):
                            st.json(result)
                else:
                    st.info("No results found for your search query")
            
            except Exception as e:
                st.error(f"Error searching resources: {str(e)}")

# Auto-refresh logic
if auto_refresh:
    import time
    time.sleep(30)
    st.rerun()
