"""
NeonPanel Agent - Specialized agent for NeonPanel operations
"""

import asyncio
from typing import Dict, Any, List
from agent_squad.agents import BedrockLLMAgent, BedrockLLMAgentOptions
from mcp.neonpanel_client import neonpanel_client

class NeonPanelAgent:
    """Agent specialized for NeonPanel operations and data retrieval"""
    
    def __init__(self, name: str = "NeonPanel Agent"):
        self.name = name
        self.description = """
        Specializes in NeonPanel server management, user data retrieval, 
        server statistics, and resource operations. Can help with:
        - Server status and monitoring
        - User account management
        - Resource allocation and usage
        - System administration tasks
        """
        
        # Initialize the underlying LLM agent
        self.llm_agent = BedrockLLMAgent(BedrockLLMAgentOptions(
            name=self.name,
            description=self.description,
            streaming=True,
            model_id="anthropic.claude-3-sonnet-20240229-v1:0"
        ))
    
    async def process_request(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Process user request with NeonPanel-specific functionality"""
        
        # Analyze the request to determine what NeonPanel data is needed
        neonpanel_data = await self._gather_neonpanel_data(user_input, context)
        
        # Enhance the prompt with NeonPanel data
        enhanced_prompt = self._enhance_prompt_with_data(user_input, neonpanel_data)
        
        # Process through the LLM agent
        response = await self.llm_agent.process_request(enhanced_prompt, context)
        
        return response
    
    async def _gather_neonpanel_data(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Gather relevant NeonPanel data based on user input"""
        data = {}
        
        # Convert to lowercase for easier matching
        input_lower = user_input.lower()
        
        try:
            # If asking about servers or stats
            if any(keyword in input_lower for keyword in ['server', 'stats', 'status', 'performance']):
                data['server_stats'] = await neonpanel_client.get_server_stats()
            
            # If asking about users
            if any(keyword in input_lower for keyword in ['user', 'account', 'profile']):
                # Get user ID from context if available
                user_id = context.get('user_id') if context else None
                if user_id:
                    data['user_data'] = await neonpanel_client.get_user_data(user_id)
            
            # If asking about search or specific resources
            if any(keyword in input_lower for keyword in ['search', 'find', 'list', 'show']):
                # Extract search terms (simple implementation)
                search_terms = self._extract_search_terms(user_input)
                if search_terms:
                    data['search_results'] = await neonpanel_client.search_resources(search_terms)
        
        except Exception as e:
            print(f"Error gathering NeonPanel data: {e}")
            data['error'] = str(e)
        
        return data
    
    def _extract_search_terms(self, user_input: str) -> str:
        """Extract search terms from user input (simple implementation)"""
        # Remove common words and extract meaningful terms
        stop_words = {'what', 'is', 'are', 'the', 'show', 'me', 'list', 'find', 'search', 'for'}
        words = user_input.lower().split()
        search_terms = [word for word in words if word not in stop_words and len(word) > 2]
        return ' '.join(search_terms[:3])  # Limit to first 3 meaningful terms
    
    def _enhance_prompt_with_data(self, user_input: str, neonpanel_data: Dict[str, Any]) -> str:
        """Enhance the user prompt with NeonPanel data"""
        enhanced_prompt = f"User Question: {user_input}\n\n"
        
        if neonpanel_data:
            enhanced_prompt += "Available NeonPanel Data:\n"
            
            if 'server_stats' in neonpanel_data:
                enhanced_prompt += f"Server Statistics: {neonpanel_data['server_stats']}\n"
            
            if 'user_data' in neonpanel_data:
                enhanced_prompt += f"User Data: {neonpanel_data['user_data']}\n"
            
            if 'search_results' in neonpanel_data:
                enhanced_prompt += f"Search Results: {neonpanel_data['search_results']}\n"
            
            if 'error' in neonpanel_data:
                enhanced_prompt += f"Note: There was an issue accessing some data: {neonpanel_data['error']}\n"
            
            enhanced_prompt += "\nPlease answer the user's question using the available NeonPanel data above. If no relevant data is available, provide a helpful response based on your knowledge of NeonPanel operations.\n"
        
        return enhanced_prompt

# Factory function for easy integration
def create_neonpanel_agent() -> NeonPanelAgent:
    """Create and return a NeonPanel agent instance"""
    return NeonPanelAgent()
