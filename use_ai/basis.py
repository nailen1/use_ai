"""Basic OpenAI API interaction functions."""

from openai import OpenAI, BadRequestError

from use_ai.config import (
    DEFAULT_MODEL_NAME,
    get_openai_api_key,
)


def _get_client() -> OpenAI:
    """Create an OpenAI client using the project API key."""
    return OpenAI(api_key=get_openai_api_key())


def _chat_completion(client: OpenAI, **kwargs) -> object:
    """Call chat completions with automatic parameter fallback.

    Handles two known incompatibilities across model generations:
      1. max_tokens → max_completion_tokens (newer models)
      2. temperature not supported (reasoning models like o3-mini)

    Retries once per unsupported parameter, stripping or replacing it.
    """
    try:
        return client.chat.completions.create(**kwargs)
    except BadRequestError as e:
        body = e.body or {}
        param = body.get("param", "") if isinstance(body, dict) else ""

        if param == "max_tokens" and "max_tokens" in kwargs:
            kwargs["max_completion_tokens"] = kwargs.pop("max_tokens")
            return _chat_completion(client, **kwargs)

        if param == "temperature" and "temperature" in kwargs:
            del kwargs["temperature"]
            return _chat_completion(client, **kwargs)

        raise


def get_available_models() -> list[str]:
    """Fetch the list of available model IDs from the OpenAI API.

    Returns:
        list[str]: Sorted list of model ID strings.
    """
    client = _get_client()
    return sorted([m.id for m in client.models.list()])


def test_model_connection(model_name: str = DEFAULT_MODEL_NAME) -> dict:
    """Test connectivity to an OpenAI model with a simple ping-like prompt.

    Args:
        model_name: The model to test. Defaults to ``DEFAULT_MODEL_NAME``.

    Returns:
        dict: Contains ``success`` (bool), ``model`` (str),
              and ``message`` (str) with the model's response or error detail.
    """
    client = _get_client()
    try:
        response = _chat_completion(
            client,
            model=model_name,
            messages=[{"role": "user", "content": "Say 'hello' in one word."}],
            max_tokens=10,
        )
        return {
            "success": True,
            "model": model_name,
            "message": response.choices[0].message.content,
        }
    except Exception as e:
        return {
            "success": False,
            "model": model_name,
            "message": str(e),
        }


def prompt_to_model(
    prompt: str,
    model_name: str = DEFAULT_MODEL_NAME,
    system_message: str | None = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> str:
    """Send a prompt to an OpenAI model and return the response text.

    Args:
        prompt: The user message to send.
        model_name: The model to use. Defaults to ``DEFAULT_MODEL_NAME``.
        system_message: Optional system-level instruction.
        max_tokens: Maximum tokens in the response.
        temperature: Sampling temperature (0.0 – 2.0).

    Returns:
        str: The model's response text.
    """
    client = _get_client()

    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    response = _chat_completion(
        client,
        model=model_name,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content
