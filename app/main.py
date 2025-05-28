import core

import sys, os
import signal, asyncio

from config import config


from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import print as rprint

console = Console()

# так как в некоторых версиях psycopg2 есть предупреждения о DBAPI2, 
# которые могут мешать выводу
# и не мешающие работе программы, мы их игнорируем
import warnings
warnings.filterwarnings('ignore', message='.*DBAPI2.*')

async def async_input(pid):
    user_prompt = Prompt.ask("[bold yellow]Ваш промпт[/bold yellow]")
    if user_prompt.lower() == 'exit':
        console.print(Panel("[bold red]Выход из программы[/bold red]"))
        os.kill(pid, signal.SIGKILL)
    return user_prompt

async def main(pid):
    console.print(Panel(f"[bold cyan]Добро пожаловать в интерфейс модели![/] 💡\nВерсия: {config.VERSION} | Для выхода введите [bold]'exit'[/]"))

    while True:
        prompt = await async_input(pid)
        if prompt.lower() == 'exit':
            break

        with console.status("[green]Загрузка ответа от модели...[/green]"):
            response = await core.Process_prompt(prompt).pipeline()

        console.print(Panel(Text("Модель:\n" + response, style="green"), title="[bold]Ответ модели[/]"))
        console.print("[italic]Введите новый промпт или 'exit' для выхода.[/italic]\n")

if __name__ == "__main__":
    pid = os.getpid()
    try:
        asyncio.run(main(pid))
    except KeyboardInterrupt:
        console.print("\n[bold red]Программа остановлена вручную.[/red bold]")
    

    



    