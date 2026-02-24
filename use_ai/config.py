"""OpenAI model configuration.

Manages model name constants and API key loading for the use_ai module.
"""

import os

from dotenv import load_dotenv

DEFAULT_MODEL_NAME = "gpt-5.2"

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
