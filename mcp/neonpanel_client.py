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
    
    def __init__(self, demo_mode=False):
        self.base_url = os.getenv("NEONPANEL_BASE_URL", "https://api.neonpanel.com")
        self.api_key = os.getenv("NEONPANEL_API_KEY")
        self.mcp_server_url = os.getenv("NEONPANEL_MCP_SERVER_URL", "http://localhost:3000")
        self.demo_mode = demo_mode or not self.api_key
        
        if not self.api_key and not demo_mode:
            import warnings
            warnings.warn("NEONPANEL_API_KEY not found - running in demo mode")
            self.demo_mode = True
    
    async def get_user_data(self, user_id: str) -> Dict[str, Any]:
        """Fetch user data from NeonPanel"""
        if self.demo_mode:
            return {
                "user_id": user_id,
                "username": f"demo_user_{user_id[:8]}",
                "email": f"demo_{user_id[:8]}@example.com",
                "created_at": "2024-01-15T10:30:00Z",
                "last_login": "2024-07-16T09:15:00Z",
                "status": "active",
                "demo_mode": True
            }
        
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
        if self.demo_mode:
            import random
            return {
                "total_servers": random.randint(15, 25),
                "active_servers": random.randint(12, 20),
                "cpu_usage": round(random.uniform(20, 80), 1),
                "memory_usage": round(random.uniform(30, 70), 1),
                "disk_usage": round(random.uniform(40, 85), 1),
                "network_in": round(random.uniform(100, 500), 2),
                "network_out": round(random.uniform(50, 300), 2),
                "uptime": "15 days, 8 hours, 23 minutes",
                "demo_mode": True
            }
        
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
        if self.demo_mode:
            import random
            return [
                {
                    "id": f"res_{i}",
                    "name": f"Demo Resource {i}",
                    "type": random.choice(["server", "database", "service"]),
                    "status": random.choice(["active", "inactive", "pending"]),
                    "created_at": "2024-07-15T10:00:00Z",
                    "demo_mode": True
                }
                for i in range(1, random.randint(3, 8))
                if query.lower() in f"demo resource {i}".lower()
            ]
        
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

# Global client instance with demo mode enabled
try:
    neonpanel_client = NeonPanelMCPClient(demo_mode=True)
except Exception:
    # Fallback for any initialization issues
    neonpanel_client = NeonPanelMCPClient(demo_mode=True)
