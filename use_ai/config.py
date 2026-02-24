"""OpenAI model configuration.

Manages model name constants and API key loading for the use_ai module.
"""

import os

from dotenv import load_dotenv

DEFAULT_MODEL_NAME = "gpt-4o-mini"

AVAILABLE_MODELS = {
    "gpt-4o-mini": "gpt-4o-mini",
    "gpt-4o": "gpt-4o",
    "gpt-4.5-preview": "gpt-4.5-preview",
    "o3-mini": "o3-mini",
}


def get_openai_api_key() -> str:
    """Load the OpenAI API key from environment variables.

    Returns:
        str: The API key value.

    Raises:
        EnvironmentError: If ``OPENAI_API_KEY_EUGENE`` is not set.
    """
    load_dotenv()
    key = os.getenv("OPENAI_API_KEY_EUGENE")
    if key is None:
        raise EnvironmentError(
            "Missing environment variable: OPENAI_API_KEY_EUGENE"
        )
    return key
