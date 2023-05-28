import argparse
import json
import sys

import poe
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table


def parse_args() -> argparse.Namespace:
    """TODO: Docstring for parse_args.
    :returns: TODO

    """
    parser = argparse.ArgumentParser(
        description="Command line interface for Poe.")
    parser.add_argument("-t", "--token", type=str, help="POE token",
                        required=True)
    parser.add_argument("-l", "--list", help="List bots", action="store_true")
    parser.add_argument("-b", "--bot", type=str,
                        default="chinchilla", help="Bot ID")
    parser.add_argument("-m", "--message", type=str, help="Message to send")
    return parser


def load_token(token: str, console: Console) -> poe.Client:
    with console.status("[bold red]POE[/bold red][green] is loading..."):
        client = poe.Client(token)
        console.print("[bold red]POE[/bold red][green] is ready!")
    return client


def list_bots(client: poe.Client) -> Table:
    """TODO: Docstring for list_bots.

    :client: TODO
    :returns: TODO

    """
    bots = json.dumps(client.bot_names)
    bots = json.loads(bots)
    table = Table(title="Bots")
    table.add_column("Bot ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Bot Name", justify="center",
                     style="magenta", no_wrap=True)
    for bot in bots:
        table.add_row(bot, bots[bot])
    return table


def main():
    # Parse arguments
    parser = parse_args()
    args = parser.parse_args()

    # Assign arguments
    TOKEN = args.token
    MESSAGE = args.message
    BOT = args.bot
    LIST_BOTS = args.list

    # if there is no argument, print help
    if not LIST_BOTS and not MESSAGE:
        parser.print_help()
        sys.exit(1)

    # Create console, for cool stuff
    console = Console()
    # Create POE client
    client = load_token(TOKEN, console)

    # List bots
    if LIST_BOTS:
        console.print(list_bots(client))
        sys.exit(0)

    # Create a Panel to show the message in
    panel = Panel("")

    # Create a Live context manager with the Panel to update text
    with Live(panel, console=console) as live:
        response = ""
        for chunk in client.send_message(BOT, MESSAGE,
                                         with_chat_break=True):
            response += chunk["text_new"]
            panel = Panel(Markdown(response))
            live.update(panel)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Console().print("\n[bold red]POE[/bold red][green] shut down.")
        sys.exit(1)
