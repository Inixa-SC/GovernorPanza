from shield import Governor, CodeShieldVerificator
import pytest


@pytest.fixture(scope='session')  # one server to rule'em all
def governor():
    governor = Governor([CodeShieldVerificator()])
    return governor


def test_chatml_void(governor):
    chatml_test = []
    analysed_chatml = governor.check_safe_chatml(chatml_test)
    assert analysed_chatml == chatml_test

def test_chatml_without_final_role_assistant(governor):
    chatml_test = [
            {
                'role': 'user',
                'content': 'Hello chatbot'
            }
        ]
    analysed_chatml = governor.check_safe_chatml(chatml_test)
    assert analysed_chatml == chatml_test

def test_chatml_malformed_last_message(governor):
    chatml_test = [
            {
                'role': 'user',
                'content': 'Hello chatbot'
            },
            {
                'role': 'assistant'
            }
        ]
    analysed_chatml = governor.check_safe_chatml(chatml_test)
    assert analysed_chatml == chatml_test

def test_chatml_safe_response(governor):
    chatml_test = [
            {
                'role': 'user',
                'content': 'Hello chatbot'
            },
            {
                'role': 'assistant',
                'content': ''
            }
        ]
    analysed_chatml = governor.check_safe_chatml(chatml_test)
    assert analysed_chatml[:-1] == chatml_test
    assert analysed_chatml[-1]['role'] == 'verificator'
    assert 'content' in analysed_chatml[-1] and 'is_safe' in analysed_chatml[-1]['content']
    assert analysed_chatml[-1]['content']['is_safe']
    assert 'analysis' in analysed_chatml[-1]['content']
    assert len(analysed_chatml[-1]['content']['analysis']) == 1
    assert 'stage' in analysed_chatml[-1]['content']['analysis'][0]
    assert analysed_chatml[-1]['content']['analysis'][0]['stage'] == "code_shield"
    assert 'issues' in analysed_chatml[-1]['content']['analysis'][0]
    assert analysed_chatml[-1]['content']['analysis'][0]['issues'] == []

def test_chatml_safe_in_c(governor):
    chatml_test = [
            {
                'role': 'user',
                'content': 'Create a basic hello + user in C asking for name of user'
            },
            {
                'role': 'assistant',
                'content': '''
                int num1, num2, num;
                scanf("%s", &num1);
                scanf("%s", &num2);
                sum = num1 + num2;
                printf("%d", sum);
                '''
            }
        ]
    analysed_chatml = governor.check_safe_chatml(chatml_test)
    assert analysed_chatml[:-1] == chatml_test
    assert analysed_chatml[-1]['role'] == 'verificator'
    assert 'content' in analysed_chatml[-1] and 'is_safe' in analysed_chatml[-1]['content']
    assert not analysed_chatml[-1]['content']['is_safe']
    assert 'analysis' in analysed_chatml[-1]['content']
    assert len(analysed_chatml[-1]['content']['analysis']) == 1
    assert 'stage' in analysed_chatml[-1]['content']['analysis'][0]
    assert analysed_chatml[-1]['content']['analysis'][0]['stage'] == "code_shield"
    assert 'issues' in analysed_chatml[-1]['content']['analysis'][0]
    assert analysed_chatml[-1]['content']['analysis'][0]['issues'] == [
            {
        'cwe_id': 'CWE-119',
        'description': 'Potential buffer overflow due to insecure usage of scanf',
        'line': 3
        },
            {
        'cwe_id': 'CWE-119',
        'description': 'Potential buffer overflow due to insecure usage of scanf',
        'line': 3
        },
            ]

