from pathlib import Path
import json

def system_context():
    """
    Метод для получения ситемного контекста
    """
    with open(Path(__file__).parent.absolute() / Path("rag/context.json"), 'r') as f:
        context = json.loads(f)
    return context

system_context()