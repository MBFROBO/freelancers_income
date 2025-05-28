import model, database, config
import pandas as pd
import sqlglot
import warnings

class Process_prompt:
    """
    Класс для обработки пользовательского промпта.
    """
    def __init__(self, prompt):
        self.prompt = str(prompt).strip()
        self.model = model.Model()
        self.retry_count = 0
        self.max_retries = 1

    async def _process_query_result(self, table: pd.DataFrame):
        """
        Метод для обработки результата запроса к БД.
        В случае ошибки возвращает 0 - перезапрашиваем у модели новый SQL запрос один раз.
        """        
        try:
            result_json = table.to_json(orient='records', force_ascii=False)
            return result_json
        except Exception as e:
            print(f"Ошибка при обработке результата запроса: {e}")
            print("Пробуем перезапросить SQL запрос у модели...")
            return 0

    async def _process_prompt_result(self, sql_query: str):
        """
        Метод для обработки SQL запроса.
        В случае ошибки возвращает 0 - перезапрашиваем у модели новый SQL запрос один раз.
        """
        try:
            sqlglot.parse_one(sql_query)
            return sql_query
        except Exception as e:
            print("Ошибка синтаксиса SQL запроса: {e}")
            print("Перезапрос SQL запроса у модели...")
            return 0
    
    @database.Database.db_connect
    async def _execute_sql_query(self, sql_query: str, conn = None) -> pd.DataFrame:
        with warnings.catch_warnings():
            table = pd.read_sql_query(sql_query, conn)
            return table
    
    async def _send_to_model(self, question: str):
        """
        Метод для отправки запроса к модели и получения SQL запроса.
        """
        sql_query = await self.model.input_prompt(question)
        if sql_query is None:
            print("Не удалось получить SQL запрос от модели.")
            return 0
        return sql_query
    
    async def _send_hidden_prompt(self, result_json: str, sql_query: str = None):
        """
        Метод для отправки промежуточного запроса к модели для объяснения полученных данных.
        """
        response = await self.model.hidden_prompt(result_json, self.prompt, sql_query)
        if response is None:
            print("Не удалось получить ответ от модели.")
            return 0
        return response
    
    async def pipeline(self):
        """
        Последовательность методов для обработки промпта.
            1. Отправка промпта в модель для получения SQL запроса.  
            1.1 Проверка полученного SQL запроса на синтаксические ошибки.  
            2. Выполнение SQL запроса к БД.  
            2.1 Преобразование таблицы pandas в JSON формат.  
            3. Отправка результата JSON скрытым промптом в нейронную сеть.  
            4. Вывод результата пользователю.  
        """
        sql_query = await self._send_to_model(self.prompt)
        if sql_query == 0:
            return "Ошибка при получении SQL запроса от модели. Попробуйте переформулировать вопрос."

        sql_query = await self._process_prompt_result(sql_query)
        if sql_query == 0:
            if self.retry_count < self.max_retries:
                self.retry_count += 1
                return await self.pipeline()
            else:
                return "Ошибка синтаксиса SQL запроса. Попробуйте переформулировать вопрос."

        table = await self._execute_sql_query(sql_query)
        if table.empty:
            return "Запрос не вернул данных. Попробуйте переформулировать вопрос."
        
        result_json = await self._process_query_result(table)
        if result_json == 0:
            if self.retry_count < self.max_retries:
                self.retry_count += 1
                return await self.pipeline()
            else:
                return "Ошибка при обработке результата запроса. Попробуйте переформулировать вопрос."

        response = await self._send_hidden_prompt(result_json, sql_query)
        if response == 0:
            return "Ошибка при отправке промежуточного запроса к модели. Попробуйте переформулировать вопрос."
        
        return response

    def get_prompt(self):
        return self.prompt