from Mkd_Lexer import Mkd_Lexer
from Token import Token

def test_creation_lexer():
    lexer = Mkd_Lexer("Bonjour")

    assert lexer.text == "Bonjour"
    assert lexer.pos == 0
    assert lexer.line == 0
    assert lexer.column == 0


def test_texte_simple():
    lexer = Mkd_Lexer("Bonjour")

    token = lexer.get_token()

    assert isinstance(token, Token)
    assert token.token_type == "TEXT"
    assert token.token_value == "Bonjour"


def test_eof():
    lexer = Mkd_Lexer("Bonjour")

    lexer.get_token()

    token = lexer.get_token()

    assert token.token_type == "EOF"
    assert token.token_value == "End Of File"