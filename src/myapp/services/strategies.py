import os
from abc import ABC, abstractmethod

import requests
from google import genai
from google.genai import types
from openai import OpenAI

SYSTEM_PROMPT = (
    "Sos un asistente académico que responde preguntas "
    "universitarias de manera clara y didáctica."
)


class LLMStrategy(ABC):
    @abstractmethod
    def generate_response(self, question: str) -> str:
        pass


class MockLLMStrategy(LLMStrategy):
    def generate_response(self, question: str) -> str:
        return f"Respuesta automática de prueba para: {question}"


class OpenAIStrategy(LLMStrategy):
    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Falta configurar OPENAI_API_KEY")

        self.model = model
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, question: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
        )
        return (response.choices[0].message.content or "").strip()


class GeminiStrategy(LLMStrategy):
    def __init__(self, model: str = "gemini-2.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Falta configurar GEMINI_API_KEY")

        self.model = model
        self.client = genai.Client(api_key=api_key)

    def generate_response(self, question: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=question,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        return (response.text or "").strip()


class LocalModelStrategy(LLMStrategy):
    def __init__(self, model: str = "llama3.2", base_url: str | None = None):
        self.model = model
        self.base_url = (base_url or os.getenv("OLLAMA_URL") or "http://localhost:11434").rstrip("/")

    def generate_response(self, question: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "system": SYSTEM_PROMPT,
                "prompt": question,
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()
        return (response.json().get("response") or "").strip()