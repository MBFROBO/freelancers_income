import core

import sys, os
import signal, asyncio

from config import config
import warnings

# так как в некоторых версиях psycopg2 есть предупреждения о DBAPI2, 
# которые могут мешать выводу
# и не мешающие работе программы, мы их игнорируем
warnings.filterwarnings('ignore', message='.*DBAPI2.*')

async def async_input(pid):
    prompt = input("Ваш промпт: ")
    if prompt == 'exit':
        os.kill(pid, signal.SIGKILL)
    return prompt
        

async def main(pid):
    while True:
        prompt = await async_input(pid)
        if prompt == 'exit':
            print("Выход из программы...")
            break
        print("Загрузка ответа от модели...")
        response = await core.Process_prompt(prompt).pipeline()
        print(f"Ответ от модели: {response}")
        print("Введите новый промпт или 'exit' для выхода.")

if __name__ == "__main__":
    print(f"app version: {config.VERSION} | Для выхода введите exit ")
    pid = os.getpid()

    asyncio.run(main(pid))
    

    



    