# use_ai

General-purpose OpenAI model utilities.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file with your API key:

```
OPENAI_API_KEY_EUGENE=sk-...
```

## Usage

```python
from use_ai import test_model_connection, prompt_to_model

# Test connection
result = test_model_connection()
print(result)

# Send a prompt
answer = prompt_to_model("Hello, world!")
print(answer)
```

## Available Functions

| Function | Description |
|---|---|
| `get_available_models()` | Fetch available model IDs from the OpenAI API |
| `test_model_connection(model_name)` | Test connectivity to a model |
| `prompt_to_model(prompt, ...)` | Send a prompt and get the response text |
