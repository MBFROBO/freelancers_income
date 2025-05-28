from .context import Context
from openai import OpenAI
from config import config

class Model(Context):
    def __init__(self):
        self.name = config.MODEL_NAME
        self.client = self._connect()
        super().__init__()

    def __repr__(self):
        return f"Model(name={self.name}, client={self.client})"
 
    def _connect(self):
        """
        Метод для подключения к API модели.
        """
        try:
            client = OpenAI(
                base_url=config.MODEL_URL,
                api_key=config.MODEL_API_KEY,
            )
        except Exception as e:
            print(f"Ошибка подключения к модели: {e}")
            return None
        return client
    
    async def input_prompt(self, question):
        """
        Метод для отправки запроса к модели и получения SQL запроса.
        """
        try:

            completion = self.client.chat.completions.create(
            model= config.MODEL_NAME,
            messages=[
                self.system_prompt,
                {
                "role": "user",
                "content": question
                }
            ],
            temperature = 0.7
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            return None

    async def hidden_prompt(self, result_json, prompt = None, sql_query = None):
        """
        Метод для отправки промежуточного запроса к модели для обяснения полученных данных.
        """
        try:
            
            completion = self.client.chat.completions.create(
            model= config.MODEL_NAME,
            messages=[
                self.system_post_prompt_context(prompt, sql_query),
                {
                "role": "user",
                "content": f"""Ответь на вопрос ниже по представленным данным\n{prompt} \n{result_json}"""
                }
            ],
            temperature = 0.5
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Ошибка при обработке промежуточного запроса: {e}")
            return None