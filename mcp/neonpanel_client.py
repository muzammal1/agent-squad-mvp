"""
NeonPanel MCP (Model Context Protocol) Client
Handles communication with NeonPanel API through MCP server
"""

import os
import json
import asyncio
import httpx
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class NeonPanelMCPClient:
    """Client for communicating with NeonPanel via MCP server"""
    
    def __init__(self):
        self.base_url = os.getenv("NEONPANEL_BASE_URL", "https://api.neonpanel.com")
        self.api_key = os.getenv("NEONPANEL_API_KEY")
        self.mcp_server_url = os.getenv("NEONPANEL_MCP_SERVER_URL", "http://localhost:3000")
        
        if not self.api_key:
            raise ValueError("NEONPANEL_API_KEY environment variable is required")
    
    async def get_user_data(self, user_id: str) -> Dict[str, Any]:
        """Fetch user data from NeonPanel"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                response = await client.get(
                    f"{self.base_url}/users/{user_id}",
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error fetching user data: {e}")
            return {}
    
    async def get_server_stats(self) -> Dict[str, Any]:
        """Get server statistics from NeonPanel"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                response = await client.get(
                    f"{self.base_url}/servers/stats",
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error fetching server stats: {e}")
            return {}
    
    async def execute_server_action(self, server_id: str, action: str) -> Dict[str, Any]:
        """Execute an action on a server"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                payload = {"action": action}
                response = await client.post(
                    f"{self.base_url}/servers/{server_id}/actions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error executing server action: {e}")
            return {"error": str(e)}
    
    async def search_resources(self, query: str) -> List[Dict[str, Any]]:
        """Search for resources in NeonPanel"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                params = {"q": query}
                response = await client.get(
                    f"{self.base_url}/search",
                    headers=headers,
                    params=params
                )
                response.raise_for_status()
                return response.json().get("results", [])
        except Exception as e:
            print(f"Error searching resources: {e}")
            return []

# Global client instance
neonpanel_client = NeonPanelMCPClient()
