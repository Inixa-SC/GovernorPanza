from typing import List
from ai_connector import AIProvider
from .verificator import Verificator

LLAMA_GUARD = {
        'S1': "Violent Crimes",
        'S2': "Non-Violent Crimes",
        'S3': "Sex-Related Crimes",
        'S4': "Child Sexual Exploitation",
        'S5': "Defamation",
        'S6': "Specialized Advice",
        'S7': "Privacy",
        'S8': "Intellectual Property",
        'S9': "Indisciminate Weapons",
        'S10': "Hate",
        'S11': "Suicide & Self-Harm",
        'S12': "Sexual Content",
        'S13': "Elections",
        }

class LlamaGuard(Verificator):

    def __init__(self, ai_provider: AIProvider):
        self.ai_provider = ai_provider

    def verify(self, conversation: List) -> List:
        analysis = self.ai_provider.chat(conversation.copy())
        is_safe = analysis[-1]['content'] == 'safe'
        conversation[-1]['content']['is_safe'] = conversation[-1]['content']['is_safe'] \
                and is_safe
        issues_found = conversation[-1]['content']['analysis']
        issues_found.append({
            'stage': 'llama_guard',
            'issues': [{
                        'description': LLAMA_GUARD[analysis[-1]['content'].split("\n")[-1]],
                        'line': "---"
                    } if not is_safe else None]
            })
        conversation[-1]['content']['analysis'] = issues_found
        return conversation

