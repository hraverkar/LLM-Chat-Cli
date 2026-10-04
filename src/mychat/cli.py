import typer
from rich.console import Console

from memory.sqlite import SQLiteMemory

from .config import Settings
from .llm import create_llm_provider


app = typer.Typer(
    help="CLI based LLM chat application."
)

console = Console()


@app.command()
def chat(
    provider: str | None = typer.Option(
        None,
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
    """
    Start a chat session with the LLM.
    """

    # ----------------------------------------
    # Load application settings
    # ----------------------------------------

    settings = Settings()

    # ----------------------------------------
    # Determine provider and model
    # ----------------------------------------

    selected_provider = (
        provider or settings.llm_provider
    )

    selected_model = model or (
        settings.llm_model
        if selected_provider == "ollama"
        else settings.openai_model
    )

    # ----------------------------------------
    # Create LLM provider
    # ----------------------------------------

    try:
        llm = create_llm_provider(
            provider=selected_provider,
            model=selected_model,
        )

    except ValueError as error:
        console.print(
            f"[red]Error:[/red] {error}"
        )
        raise typer.Exit(code=1) from error

    # ----------------------------------------
    # Initialize SQLite memory
    # ----------------------------------------

    memory = SQLiteMemory()

    # Create a new conversation
    conversation_id = (
        memory.create_conversation()
    )

    # ----------------------------------------
    # Display startup information
    # ----------------------------------------

    console.print(
        f"\n[bold green]"
        f"New conversation started "
        f"with ID: {conversation_id}"
        f"[/bold green]"
    )

    console.print(
        "\n[bold green]MyChat AI[/bold green]"
    )

    console.print(
        f"[dim]"
        f"Provider: {selected_provider} | "
        f"Model: {selected_model}"
        f"[/dim]"
    )

    console.print(
        "Type 'exit' or 'quit' to exit.\n"
    )

    # ----------------------------------------
    # Chat loop
    # ----------------------------------------

    while True:

        user_input = console.input(
            "[bold blue]You:[/bold blue] "
        )

        # ------------------------------------
        # Exit commands
        # ------------------------------------

        if user_input.lower() in {
            "exit",
            "quit",
            "cls",
            "clear"
        }:
            console.print(
                "\n[yellow]Goodbye![/yellow]"
            )
            break

        # Ignore empty messages
        if not user_input.strip():
            continue

        # ------------------------------------
        # Save user message
        # ------------------------------------

        memory.add_message(
            conversation_id=conversation_id,
            role="user",
            content=user_input,
        )

        # ------------------------------------
        # Load conversation history
        # ------------------------------------

        messages = memory.get_conversation(
            conversation_id
        )

        # ------------------------------------
        # Add system prompt
        # ------------------------------------

        messages.insert(
            0,
            {
                "role": "system",
                "content": settings.system_prompt,
            },
        )

        # ------------------------------------
        # Generate response
        # ------------------------------------

        console.print(
            "\n[bold green]AI:[/bold green] ",
            end="",
        )

        full_response = ""

        try:

            for token in llm.stream(messages):

                print(
                    token,
                    end="",
                    flush=True,
                )

                full_response += token

        except Exception as error:

            console.print(
                f"\n[red]Error:[/red] {error}"
            )

            # Important:
            # The user message is already stored.
            # We don't store an incomplete assistant
            # response if the LLM fails.

            continue

        # Move to next line after streaming
        print()

        # ------------------------------------
        # Save assistant response
        # ------------------------------------

        memory.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=full_response,
        )


if __name__ == "__main__":
    app()