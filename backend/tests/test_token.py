from Token import Token

def test_token_creation():
    token = Token("TEXT", "Bonjour", 1, 5)

    assert token.token_type == "TEXT"
    assert token.token_value == "Bonjour"
    assert token.coord == (1, 5)