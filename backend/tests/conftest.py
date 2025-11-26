import sys
import os
from unittest.mock import MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create mocks for google.adk.models.lite_llm and google.adk.agents
mock_adk_models_lite_llm = MagicMock()
mock_adk_models_lite_llm.LiteLlm = MagicMock()
sys.modules["google.adk.models.lite_llm"] = mock_adk_models_lite_llm

mock_adk_models = MagicMock() # Keep google.adk.models as a package if other imports rely on it
sys.modules["google.adk.models"] = mock_adk_models

mock_adk_agents = MagicMock()
mock_adk_agents.Agent = MagicMock()
sys.modules["google.adk.agents"] = mock_adk_agents

mock_litellm = MagicMock()
sys.modules["litellm"] = mock_litellm
