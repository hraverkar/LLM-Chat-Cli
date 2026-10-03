import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    def __init__(self):
        self.app_name = os.getenv("APP_NAME", "MyChat")
        self.system_prompt = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")
        self.llm_provider = os.getenv("LLM_PROVIDER", "ollama")
        self.llm_model = os.getenv("LLM_MODEL", "llama3.2:latest")
        self.ollama_api_key = os.getenv("OLLAMA_API_KEY", "ollama")
        self.llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434/v1")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")