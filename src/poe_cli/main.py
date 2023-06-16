import argparse
import sys

import poe
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table


def parse_args() -> argparse.ArgumentParser:
    """
    Parse command line arguments for the script.

    :returns: An argparse.ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        description="Command line interface for Poe.")
    parser.add_argument("-t", "--token", type=str, help="POE token",
                        required=True)
    parser.add_argument("-l", "--list", help="List bots", action="store_true")
    parser.add_argument("-b", "--bot", type=str,
                        default="chinchilla", help="Bot ID")
    parser.add_argument("-B", "--break", help="Force chat break",
                        dest="no_break", action="store_true")
    parser.add_argument("-m", "--message", type=str, help="Message to send")
    parser.add_argument("-c", "--chat", help="Chat mode", action="store_true")
    return parser


def load_token(token: str, console: Console) -> poe.Client:
    """
    Load the POE (Poe) token and create a Poe client.

    :param token: The POE token as a string.
    :param console: A rich Console object for displaying progress.
    :returns: A connected poe.Client instance.
    """
    with console.status("[bold red]POE[/bold red][green] is loading..."):
        client = poe.Client(token)
        console.print("[bold red]POE[/bold red][green] is ready!")
    return client


def list_bots(client: poe.Client) -> Table:
    """
    Get a list of available bots and format them as a rich Table.

    :param client: A connected poe.Client instance.
    :returns: A rich Table containing the bot ID and bot name.
    """
    bots = client.bot_names
    table = Table(title="Bots")
    table.add_column("Bot ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Bot Name", justify="center", style="magenta",
                     no_wrap=True)
    for bot in bots:
        table.add_row(bot, bots[bot])
    return table


def live_panel(console: Console, client: poe.Client, bot: str,
               message: str, with_chat_break: bool = True) -> None:
    """
    Display the live panel with the chat conversation.

    :param console: A rich Console object for displaying the live panel.
    :param client: A connected poe.Client instance.
    :param bot: The bot ID to send the message to.
    :param message: The message to send to the bot.
    """
    # Create a Panel to show the message in
    panel = Panel("")

    # Create a Live context manager with the Panel to update text
    with Live(panel, console=console) as live:
        response = ""
        for chunk in client.send_message(bot, message,
                                         with_chat_break=with_chat_break):
            response += chunk["text_new"]
            panel = Panel(Markdown(response))
            live.update(panel)


def main():
    # Parse arguments
    parser = parse_args()
    args = parser.parse_args()

    # Assign arguments
    TOKEN = args.token
    MESSAGE = args.message
    BOT = args.bot
    LIST_BOTS = args.list
    CHAT = args.chat
    BREAK = args.no_break

    # If there is no argument, print help
    if (not LIST_BOTS and not MESSAGE) and not CHAT:
        parser.print_help()
        sys.exit(2)

    # Create console, for cool stuff
    console = Console()
    # Create POE client
    client = load_token(TOKEN, console)

    # List bots
    if LIST_BOTS:
        console.print(list_bots(client))
        sys.exit(0)

    if CHAT:
        client.send_chat_break(BOT)
        while True:
            # Ask for another message
            MESSAGE = input("> ")
            # If the message is empty, exit
            if not MESSAGE:
                exit(0)
            # Display the live panel with the chat conversation
            live_panel(console, client, BOT, MESSAGE, False)
    else:
        live_panel(console, client, BOT, MESSAGE, not BREAK)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Console().print("\n[bold red]POE[/bold red][green] shut down.")
        sys.exit(1)
