import sys
from unittest.mock import MagicMock

# Avoid loading heavy ML models during API smoke tests
if "sentence_transformers" not in sys.modules:
    mock_st = MagicMock()
    mock_model = MagicMock()
    mock_model.encode.return_value = [[0.1] * 384]
    mock_st.SentenceTransformer.return_value = mock_model
    sys.modules["sentence_transformers"] = mock_st

# Avoid newspaper/lxml import issues in test environments
if "newspaper" not in sys.modules:
    mock_newspaper = MagicMock()
    sys.modules["newspaper"] = mock_newspaper
