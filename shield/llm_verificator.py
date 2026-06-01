import re
from typing import List

from codeshield.insecure_code_detector.issues import json
from ai_connector import AIProvider
from .verificator import Verificator

PROMPT = """You are an advanced Security Logic Analyzer powered by Qwen3-Coder. Your goal is to detect **exploitable security vulnerabilities** while ignoring bad practices or non-exploitable warnings.

### OUTPUT FORMAT
You must output a single, valid JSON object with no markdown formatting. The JSON must follow this EXACT schema:
{
  "_analysis": "Step-by-step reasoning here. 1. Identify sources/sinks. 2. Is the input tainted? 3. Is it exploitable?",
  "unsafe": boolean, 
  "explain": {
      "type": "String (e.g., SQL Injection, RCE) or null",
      "line": integer or null,
      "description": "Brief description of the exploit"
  } 
  // If unsafe is false, 'explain' should be null.
}

### ANALYSIS RULES
1. **Differentiate Warnings vs. Errors:**
   - **Warning:** Hardcoded secrets in tests, missing comments, using `print()`, poor variable names. -> **unsafe: false**
   - **Error:** SQL Injection, RCE, XSS, Path Traversal. -> **unsafe: true**
   
2. **Deprecated & Broken Algorithms (STRICT):**
   - **Flag as UNSAFE:** Any use of deprecated cryptographic algorithms (MD5, SHA1, DES, RC4) or libraries (e.g., Python `telnetlib`, old `xml.etree` without defusedxml).
   - **Reasoning:** Even if the code implementation is correct, the underlying algorithm is mathematically broken. This is an Error, not a Warning.

3. **Context Matters:**
   - If a dangerous function (like `eval`) is used on a hardcoded string or safe integer, it is **unsafe: false**.
   - If user input is sanitized (e.g., using parameterized queries), it is **unsafe: false**.
   - Eval each function as if it were to be called from anywhere and/or with any parameters. 

### EXAMPLES (Few-Shot Learning)

**Input:**
```python
import os
# Dev script to test connectivity
def ping_local():
    ip = "127.0.0.1"
    os.system("ping " + ip)
Output: { "_analysis": "The code uses os.system which is dangerous, BUT the input 'ip' is hardcoded to '127.0.0.1'. There is no user input entering the command. Not exploitable.", "unsafe": false, "explain": null }

Input:

JavaScript

// User profile update
const query = `UPDATE users SET name = '${req.body.name}' WHERE id = ${req.user.id}`;
db.run(query);
Output: { "_analysis": "The code constructs a SQL query using a template literal. 'req.body.name' comes directly from the user and is inserted into the query string without sanitization. This is a classic SQL Injection.", "unsafe": true, "explain": { "type": "SQL Injection", "line": 3, "description": "User input 'req.body.name' is interpolated directly into a SQL query string, allowing attackers to manipulate the database." } }

YOUR TURN
Analyze the following code: {{USER_CODE}}"""


class LLMVerificator(Verificator):

    def __init__(self, ai_provider: AIProvider):
        self.ai_provider = ai_provider

    def llm_parser_json(self, llm_response):
        try:
            return json.loads(llm_response)
        except:
            pass
        match = re.search(r'\{.*\}', llm_response, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except:
                pass
        return {'unsafe': False, "explain": None}
                

    def verify(self, conversation: List) -> List:
        last_assistant_message = conversation[-2]['content']
        response = self.llm_parser_json(self.ai_provider.message(PROMPT.replace("{{USER_CODE}}",str(last_assistant_message))))
        if 'unsafe' not in response \
            or (response['unsafe'] \
                and 'explain' not in response):
            return conversation


        conversation[-1]['content']['is_safe'] = conversation[-1]['content']['is_safe'] and not response['unsafe']
        issues_found = conversation[-1]['content']['analysis']
        issues_found.append({
            'stage': 'llm_analysis',
            'issues': [{
                        'description': response["explain"]["description"],
                        'line': response["explain"]["line"]
                    }] if response["explain"] is not None else []
            })
        conversation[-1]['content']['analysis'] = issues_found
        return conversation


