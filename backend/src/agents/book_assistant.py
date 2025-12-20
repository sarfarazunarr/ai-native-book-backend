from typing import Dict, Any, List
from ..config import settings, MODEL
from ..tools.search_tool import search_tool
from agents import function_tool
import logging
import uuid
import json

logger = logging.getLogger(__name__)

try:
    from agents import Agent, Runner, function_tool
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    logger.error("openai-agents library not available.")

class BookAssistant:
    """BookAssistant using decorated function tools for automatic schema handling."""

    def __init__(self):
        if not AGENTS_AVAILABLE:
            raise ImportError("openai-agents library is required.")

        self.search_tool = search_tool
        
        # 1. Define the tool using the decorator
        @function_tool
        def search_knowledge_base(query: str) -> str:
            """
            Search the knowledge base for content relevant to the robotics book.
            
            Args:
                query: The specific search term or question to look up in the book.
            """
            results = self.search_tool.search_knowledge_base(
                query,
                limit=settings.vector_search_limit
            )

            formatted = [
                {
                    "url": r.get("url", ""),
                    "title": r.get("title", ""),
                    "content": r.get("content", "")[:500],
                    "score": r.get("relevance_score", 0.0)
                }
                for r in results
            ]
            return json.dumps(formatted)

        # 2. Initialize the Agent with the decorated tool
        self.agent = Agent(
            name="Book Assistant",
            instructions=(
                "You are an assistant for the Physical AI & Humanoid Robotics book. "
                "Use the search_knowledge_base tool to find facts. "
                "Answer based ONLY on provided search results and cite the Source Title and URL."
            ),
            tools=[search_knowledge_base],
            model=MODEL
        )

    async def process_query(self, query: str, session_id: str = None) -> Dict[str, Any]:
        """Process query using the Agent Runner."""
        try:
            # Runner handles the tool loop automatically
            result = await Runner.run(self.agent, query)
            
            response_text = result.final_output

            # Secondary search for citation metadata in the return dictionary
            search_results = self.search_tool.search_knowledge_base(
                query,
                limit=settings.vector_search_limit
            )
            
            return {
                "response": response_text,
                "sources": self._extract_sources(search_results),
                "session_id": session_id or self._create_new_session_id()
            }

        except Exception as e:
            logger.error(f"Agent execution failed: {str(e)}")
            return {
                "response": "I encountered an error accessing the book database.",
                "sources": [],
                "session_id": session_id or self._create_new_session_id()
            }

    def _extract_sources(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        return [
            {"url": r.get("url", ""), "title": r.get("title", "")} 
            for r in search_results
        ]

    def _create_new_session_id(self) -> str:
        return f"sess-{uuid.uuid4()}"

    def cleanup(self):
        pass