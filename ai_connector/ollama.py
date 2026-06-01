from ollama import Client
from typing import List
from .interface import AIProvider
import config

class OllamaProvider(AIProvider): 
    def __init__(self, host=config.OLLAMA_URL, model=config.OLLAMA_MODEL):
        self.host = host
        self.model = model
        self.client = Client(
                host = self.host
                )

    def message(self, prompt: str) -> str:
        messages = [
            {
                'role': 'user',
                'content': prompt
            }
        ]
        response = ""
        for part in self.client.chat(self.model, messages=messages, stream=True):
            response = response + part.message.content
        return response

    def chatml_message(self, prompt: str) -> List[any]:
        return [
                {
                    'role': 'user',
                    'content': prompt
                    },
                {
                    'role': 'assistant',
                    'content': self.message(prompt)
                    }
                ]

    def chat(self, history: List[any]) -> List[any]:
        modified_history = []
        for m in history:
            if isinstance(m['content'], str):
                modified_history.append(m.copy())
            else:
                try:
                    new_m = m.copy()
                    new_m['content'] = new_m['content'][0]['text']
                    modified_history.append(new_m)
                except:
                    pass
        response = self.client.chat(self.model, messages=modified_history)
        history.append({
            'role': 'assistant',
            'content': response.message.content
            })
        return history

