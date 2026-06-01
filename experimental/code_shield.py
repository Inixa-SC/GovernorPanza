import asyncio
from codeshield.cs import CodeShield

async def test_codeshield():
    # 1. Define an insecure code snippet (MD5 is considered weak)
    insecure_code = """
import hashlib
def get_hash(data):
    # MD5 is insecure and should be flagged
    return hashlib.md5(data.encode()).hexdigest()
    """

    # 2. Define a secure code snippet
    secure_code = """
import hashlib
def get_hash(data):
    # SHA256 is generally considered secure
    return hashlib.sha256(data.encode()).hexdigest()
    """

    print("--- Testing Insecure Code ---")
    await run_scan(insecure_code)
    
    print("\n--- Testing Secure Code ---")
    await run_scan(secure_code)

async def run_scan(code_snippet):
    """
    Scans a code snippet using CodeShield and prints the security report.
    """
    # CodeShield.scan_code is an async method
    result = await CodeShield.scan_code(code_snippet)
    
    print(f"Is Insecure: {result.is_insecure}")
    print(f"Recommended Treatment: {result.recommended_treatment}")
    
    if result.issues_found:
        print(f"Issues Found: {len(result.issues_found)}")
        for issue in result.issues_found:
            print(f" - Issue: {issue.description}")
            print(f" - Severity: {issue.severity}")
            print(f" - Rule: {issue.rule}")
    else:
        print("No security issues found.")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(test_codeshield())
