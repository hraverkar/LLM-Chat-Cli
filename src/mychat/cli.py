import typer
from rich.console import Console
from rich.markdown import Markdown
from .llm import OllamaLLM

app = typer.Typer(
    invoke_without_command=True,
    no_args_is_help=False,
)
console = Console()

@app.callback()
def main():
    """
    A simple command-line chat application using the Ollama LLM.
    
    """
    chat()

def chat():
    """
    Start a chat session with the Ollama LLM.
    """
    llm = OllamaLLM()

    console.print("[bold green]Welcome to the Ollama Chat! Type 'exit' to quit.[/bold green]")
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    console.print("[bold blue]You:[/bold blue] Hello! How can I assist you today?")
    console.print("[bold yellow]Ollama:[/bold yellow] Hello! I'm here to help. What would you like to talk about? \n")

    while True:
        user_input = console.input("[bold blue]You:[/bold blue] ")
        if user_input.lower() in ["exit", "quit", "bye", "cls", "clear"]:
            console.print("[bold red]Exiting chat...[/bold red]")
            break
        
        messages.append({"role": "user", "content": user_input})
        console.print("[bold yellow]🤔 Thinking...:[/bold yellow] ", end="\r")
        full_response = ""
        
        try:
            response_stream = llm.stream(messages)
            console.print(" " * 30, end="\r")  # Clear the "Thinking..." line

            console.print("[bold yellow]Ollama:[/bold yellow] ", end="")

            for chunk in response_stream:
                full_response += chunk
                console.print(chunk, end="", markup=True)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            continue
        console.print() 
        
        messages.append({"role": "assistant", "content": full_response})  # New line after the response
if __name__ == "__main__":
    app()
