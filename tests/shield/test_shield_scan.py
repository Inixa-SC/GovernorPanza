import asyncio
from shield import CodeShieldVerificator
import pytest

@pytest.fixture(scope='session')  # one server to rule'em all
def governor():
    governor = CodeShieldVerificator()
    return governor

def test_code_insecure(governor):
    code_test = """
import hashlib
def get_hash(data):
    # MD5 is insecure and should be flagged
    return hashlib.md5(data.encode()).hexdigest()
    """
    analysis = asyncio.run(governor.code_shield_scan(code_test))
    assert analysis.is_insecure

def test_code_secure(governor):
    code_test = """
    # Nothing insecure here
    print('hello world!')
    """
    analysis = asyncio.run(governor.code_shield_scan(code_test))
    assert not analysis.is_insecure

def test_code_with_more_text(governor):
    code_test = """
    Hello! here is a hello world basic code:
        ```python
    # Nothing insecure here
    print('hello world!')
        ```
    """
    analysis = asyncio.run(governor.code_shield_scan(code_test))
    assert not analysis.is_insecure

def test_code_insecure_c(governor):
    code_test = """
    int num1, num2, num;
    scanf("%s", &num1);
    scanf("%s", &num2);
    sum = num1 + num2;
    printf("%d", sum);
    """
    analysis = asyncio.run(governor.code_shield_scan(code_test))
    assert analysis.is_insecure
