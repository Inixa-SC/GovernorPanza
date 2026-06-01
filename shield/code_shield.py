from codeshield.cs import CodeShield
from typing import List
from .verificator import Verificator
import asyncio

class CodeShieldVerificator(Verificator):
    async def code_shield_scan(self, code_snippet: str):
        return await CodeShield.scan_code(code_snippet)

    def verify(self, conversation: List) -> List:
        last_assistant_message = conversation[-2]['content']
        analysis = asyncio.run(self.code_shield_scan(last_assistant_message))
        conversation[-1]['content']['is_safe'] = conversation[-1]['content']['is_safe'] and not analysis.is_insecure
        issues_found = conversation[-1]['content']['analysis']
        issues_found.append({
            'stage': 'code_shield',
            'issues': [{
                        'cwe_id': issue.cwe_id,
                        'description': issue.description,
                        'line': issue.line
                    } for issue in analysis.issues_found] if analysis.is_insecure else []
            })
        conversation[-1]['content']['analysis'] = issues_found
        return conversation


