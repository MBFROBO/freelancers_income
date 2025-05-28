from pathlib import Path
import json

class Context():
    """
    Класс хранения контекста общения с пользователем и системных контекстов.
    """
    
    def __init__(self):
        self.data = {}
        self.system_context_message = self.system_context()
        self.system_prompt = {
            "role":"system",
            "content": f"""Ты - Аналитик данных и отлично знаешь PostgreSQL. Твоя задача - создать для пользователя оптмиальный SQL зпрос для СУБД PostgreSQL.
                    Таблица, с которой ты работаешь, содержит следующе данные:
                    {self.system_context_message}
                    Не придумывай данные, используй только приведённую структуру. Существующие имена таблиц и переменных.
                    На выход дай ТОЛЬКО SQL - запрос к таблице. Запрос выводи текстом без кавычек и без форматирования.
            """
        }

    def set(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)

    def clear(self):
        self.data.clear()

    def system_context(self):
        """
        Метод для получения ситемного контекста
        """
        with open(Path(__file__).parent.absolute() / Path("rag/context.json"), 'r') as f:
            context = json.load(f)
        return context
    
    def system_post_prompt_context(self, prompt=None, sql_query=None):
        """
        Метод для получения пост-промпт контекста.
        """
        post_promt_context = None
        sql_context = f"""Ты создал SQL запрос {sql_query} к базе данных по запросу '{prompt}' и получил результат."""

        with open(Path(__file__).parent.absolute() / Path("rag/post_prompt_context.json"), 'r') as f:
            post_promt_context = json.load(f)
        post_promt_context['content'] = sql_context + '\n' + post_promt_context['content']
        return post_promt_context