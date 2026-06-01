from typing import List
from .verificator import *
from .code_shield import *
from .llm_verificator import *
from .llama_guard import *

class Governor():
    def __init__(self, verificators: List[Verificator]):
        self.verificators = verificators
    
    def check_safe_chatml(self, conversation: List[any]):
        modified_conversation = conversation.copy()
        if len(conversation) == 0 \
            or not 'role' in conversation[-1] \
            or not conversation[-1]['role'] == 'assistant' \
            or not 'content' in conversation[-1]:
                return modified_conversation
        modified_conversation.append({
            'role': 'verificator',
            'content': {
                'is_safe': True,
                'analysis': []
                }
            })
        for verificator in self.verificators:
            modified_conversation = verificator.verify(modified_conversation)
        return modified_conversation

