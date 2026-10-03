import typer
from rich.console import Console
from .llm import create_llm_provider

app = typer.Typer(help="Start a chat session with an LLM.")
console = Console()

@app.command()
def chat(
    provider: str = typer.Option(
        "ollama",
        "--provider",
        "-p",
        help="LLM provider: ollama or openai",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        "-m",
        help="Model name",
    ),
):
    try:
        llm = create_llm_provider(provider, model)
    except ValueError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1) from error

    console.print("\n[bold green]MyChat AI[/bold green]")
    console.print(f"[dim]Provider: {provider} | Model: {model or 'default'}[/dim]")
    console.print("Type 'exit' or 'quit' to exit.\n")

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

    while True:
        user_input = console.input("[bold blue]You:[/bold blue] ")
        if user_input.lower() in ["exit", "quit", "cls", "clear"]:
            console.print("\nGoodbye!")
            break

        messages.append({"role": "user", "content": user_input})
        full_response = ""

        console.print("\n[bold green]AI:[/bold green] ", end="")
        try:
            for token in llm.stream(messages):
                print(token, end="", flush=True)
                full_response += token
        except Exception as error:
            console.print(f"\n[red]Error:[/red] {error}")
            continue

        print()
        messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    app()
