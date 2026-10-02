from openai import OpenAI

class OllamaLLM:
    def __init__(self, model: str= 'llama3.2:latest'): 
        self.model = model

        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )

    def chat(self, messages: list[dict]) :
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream = True
        )

        for chunk in response:
            if not chunk.choices:
                continue
            content = chunk.choices[0].delta.content
            if content:
                yield content
        