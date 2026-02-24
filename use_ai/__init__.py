"""use_ai – General-purpose OpenAI model utilities."""

from use_ai.config import (
    DEFAULT_MODEL_NAME,
    AVAILABLE_MODELS,
    get_openai_api_key,
)
from use_ai.basis import (
    get_available_models,
    test_model_connection,
    prompt_to_model,
)

__all__ = [
    "DEFAULT_MODEL_NAME",
    "AVAILABLE_MODELS",
    "get_openai_api_key",
    "get_available_models",
    "test_model_connection",
    "prompt_to_model",
]
