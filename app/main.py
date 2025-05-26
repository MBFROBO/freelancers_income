import core
import database
import model

import sys, os
import queue, yaml
import signal, asyncio

from yaml import load

confs = {}
with open(f"{sys.path[0]}/config/config.yaml", 'r') as f:
    confs = load(f, yaml.Loader)


async def async_input(pid):
    
    prompt = input("Ваш промпт: ")
    if prompt == 'exit':
        os.kill(pid, signal.SIGKILL)
    return prompt
        

async def main(pid, q):
    while True:
        prompt = await async_input(pid)
 

if __name__ == "__main__":
    print(f"app version: {confs['version']} | Для выхода введите exit ")
    q = queue.Queue()
    pid = os.getpid()

    asyncio.run(main(pid, q))
    

    



    