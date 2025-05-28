from config import config
from openai import OpenAI

client = OpenAI(
  base_url=config.MODEL_URL,
  api_key=config.MODEL_API_KEY,
)

def test_model_connection():
    message = "Hello, world!"
    completion = client.chat.completions.create(
    model=config.MODEL_NAME,
    messages=[
        {
        "role": "user",
        "content": message
        }
    ],
    temperature = 0.7
    )
    assert completion.choices[0].message.content is not None, "Model connection failed or returned no content"


def test_get_system_context():
    from .app.model.context import Context
    context = Context()
    system_context = context.system_context_message
    assert isinstance(system_context, dict), "System context should be a dictionary"