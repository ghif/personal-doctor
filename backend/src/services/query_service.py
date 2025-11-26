from src.models.models import UserQuery
from src.agents.query_agent import QueryAgent

# Initialize the agent
agent = QueryAgent()

async def process_query(user_query: UserQuery):
    """
    Process the user query using the QueryAgent.
    """
    async for chunk in agent.process_query(user_query.query_text, user_query.image_data):
        yield chunk

