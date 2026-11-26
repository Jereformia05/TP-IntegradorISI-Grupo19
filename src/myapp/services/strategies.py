import os
from abc import ABC, abstractmethod

import requests
from google import genai
from openai import OpenAI


class LLMStrategy(ABC):
    @abstractmethod
    def generate_response(self, question: str) -> str:
        pass


class OpenAIStrategy(LLMStrategy):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("Falta configurar OPENAI_API_KEY")

        self.client = OpenAI(api_key=api_key)

    def generate_response(self, question: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sos un asistente académico que responde preguntas "
                        "universitarias de manera clara y didáctica."
                    ),
                },
                {"role": "user", "content": question},
            ],
        )

        return response.choices[0].message.content


class GeminiStrategy(LLMStrategy):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("Falta configurar GEMINI_API_KEY")

        self.client = genai.Client(api_key=api_key)

    def generate_response(self, question: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", contents=question
        )

        return response.text


class LocalModelStrategy(LLMStrategy):
    def __init__(self, model="llama3.2"):
        self.model = model

    def generate_response(self, question: str) -> str:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": self.model, "prompt": question, "stream": False},
            timeout=60,
        )

        response.raise_for_status()

        return response.json()["response"]
