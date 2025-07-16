"""
MCP Integration Package
Provides Model Context Protocol integration for NeonPanel
"""

from .neonpanel_client import neonpanel_client
from .neonpanel_agent import NeonPanelAgent, create_neonpanel_agent

__all__ = ['neonpanel_client', 'NeonPanelAgent', 'create_neonpanel_agent']
