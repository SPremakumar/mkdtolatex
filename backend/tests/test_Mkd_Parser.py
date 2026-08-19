#!/usr/bin/python3

import pytest
from Mkd_Parser import Mkd_Parser
from Enum_Rule import Rule
from AST import Node


def test_creation_parser():
    parser = Mkd_Parser("Bonjour")

    assert parser.Mkd_Lexer is not None
    assert parser.current_token is not None

    assert parser.AST.valeur == Rule.DOCUMENT
    assert len(parser.AST) == 0


def test_advance():
    parser = Mkd_Parser("Bonjour")

    premier_token = parser.current_token

    token = parser.advance()

    assert token is parser.current_token
    assert token is not premier_token


def test_document_vide():
    parser = Mkd_Parser("")

    ast = parser.parse()

    assert ast.valeur == Rule.DOCUMENT
    assert len(ast) == 1

    assert isinstance(ast[0], Node)
    assert ast[0].valeur == Rule.EOF


def test_parse_texte_simple():
    parser = Mkd_Parser("Bonjour")

    ast = parser.parse()

    paragraph = ast[0]
    inline = paragraph[0]
    token = inline[0]

    assert paragraph.valeur == Rule.PARAGRAPH
    assert inline.valeur == Rule.INLINE

    assert token.token_type == "TEXT"
    assert token.token_value == "Bonjour"


def test_parse_ajoute_eof():
    parser = Mkd_Parser("Bonjour")

    ast = parser.parse()

    assert ast[-1].valeur == Rule.EOF


def test_parse_heading():
    parser = Mkd_Parser("# Bonjour\n")

    ast = parser.parse()

    heading = ast[0]

    assert heading.valeur == Rule.HEADING
    assert heading[0].token_type == "HEADER"
    assert heading[0].token_value == (1, "Bonjour")


def test_parse_heading_niveau_2():
    parser = Mkd_Parser("## Bonjour\n")

    ast = parser.parse()

    heading = ast[0]

    assert heading.valeur == Rule.HEADING
    assert heading[0].token_type == "HEADER"
    assert heading[0].token_value == (2, "Bonjour")


def test_parse_heading_niveau_6():
    parser = Mkd_Parser("###### Bonjour\n")

    ast = parser.parse()

    heading = ast[0]

    assert heading.valeur == Rule.HEADING
    assert heading[0].token_type == "HEADER"
    assert heading[0].token_value == (6, "Bonjour")


def test_parse_bold():
    parser = Mkd_Parser("**Bonjour**")

    ast = parser.parse()

    paragraph = ast[0]
    inline = paragraph[0]

    assert paragraph.valeur == Rule.PARAGRAPH
    assert inline.valeur == Rule.INLINE

    assert inline[0].token_type == "BOLD"
    assert inline[0].token_value == ("Bonjour",)


def test_parse_italic():
    parser = Mkd_Parser("*Bonjour*")

    ast = parser.parse()

    paragraph = ast[0]
    inline = paragraph[0]

    assert paragraph.valeur == Rule.PARAGRAPH
    assert inline.valeur == Rule.INLINE

    assert inline[0].token_type == "ITALIC"
    assert inline[0].token_value == ("Bonjour",)


def test_parse_bold_italic():
    parser = Mkd_Parser("***Bonjour***")

    ast = parser.parse()

    paragraph = ast[0]
    inline = paragraph[0]

    assert paragraph.valeur == Rule.PARAGRAPH
    assert inline.valeur == Rule.INLINE

    assert inline[0].token_type == "BOLD_ITALIC"
    assert inline[0].token_value == ("Bonjour",)


def test_parse_link():
    parser = Mkd_Parser(
        "[Google](https://google.com)"
    )

    ast = parser.parse()

    paragraph = ast[0]
    inline = paragraph[0]

    assert paragraph.valeur == Rule.PARAGRAPH
    assert inline.valeur == Rule.INLINE

    assert inline[0].token_type == "LINK"
    assert inline[0].token_value == (
        "Google",
        "https://google.com"
    )


def test_parse_code_inline():
    parser = Mkd_Parser(
        "`print('hello')`"
    )

    ast = parser.parse()

    paragraph = ast[0]
    inline = paragraph[0]

    assert paragraph.valeur == Rule.PARAGRAPH
    assert inline.valeur == Rule.INLINE

    assert inline[0].token_type == "CODE_INLINE"
    assert inline[0].token_value == (
        "print('hello')",
    )


def test_parse_image():
    parser = Mkd_Parser(
        "![Chat](chat.jpg)"
    )

    ast = parser.parse()

    image = ast[0]

    assert image.valeur == Rule.IMAGE
    assert image[0].token_type == "IMAGE"
    assert image[0].token_value == (
        "Chat",
        "chat.jpg",
        None
    )



def test_parse_image_avec_caption():
    parser = Mkd_Parser(
        '![Chat](chat.jpg "Mon chat")'
    )

    ast = parser.parse()

    image = ast[0]

    assert image.valeur == Rule.IMAGE
    assert image[0].token_type == "IMAGE"

    assert image[0].token_value == (
        "Chat",
        "chat.jpg",
        "Mon chat"
    )


def test_parse_quote():
    parser = Mkd_Parser(
        "> Bonjour"
    )

    ast = parser.parse()

    quote = ast[0]

    assert quote.valeur == Rule.QUOTE
    assert quote[0].token_type == "QUOTE"
    assert quote[0].token_value == (
        "Bonjour",
    )


def test_parse_code_block():
    parser = Mkd_Parser(
        "```python\n"
        "print('hello')\n"
        "```"
    )

    ast = parser.parse()

    code = ast[0]

    assert code.valeur == Rule.CODE_BLOCK
    assert code[0].token_type == "CODE_BLOCK"


def test_parse_liste_non_ordonnee():
    parser = Mkd_Parser(
        "- Premier\n"
        "- Deuxième\n"
    )

    ast = parser.parse()

    liste = ast[0]

    assert liste.valeur == Rule.LIST

    item = liste[0]

    assert item.valeur == Rule.LIST_ITEM

    assert len(item) == 2

    assert item[0].token_type == "LIST_ITEM"
    assert item[1].token_type == "LIST_ITEM"

    assert item[0].token_value == (
        "-",
        "Premier"
    )

    assert item[1].token_value == (
        "-",
        "Deuxième"
    )


def test_parse_liste_ordonnee():
    parser = Mkd_Parser(
        "1. Premier\n"
        "2. Deuxième\n"
    )

    ast = parser.parse()

    liste = ast[0]

    assert liste.valeur == Rule.LIST

    item = liste[0]

    assert item.valeur == Rule.LIST_NUM

    assert len(item) == 2

    assert item[0].token_type == "LIST_NUM"
    assert item[1].token_type == "LIST_NUM"

    assert item[0].token_value == (
        "1",
        "Premier"
    )

    assert item[1].token_value == (
        "2",
        "Deuxième"
    )


def test_parse_newline():
    parser = Mkd_Parser("\n")

    ast = parser.parse()

    newline = ast[0]

    assert newline.valeur == Rule.NEW_LINE
    assert newline[0].token_type == "NL"


def test_parse_document_complet():

    markdown = (
        "# Mon document\n"
        "Bonjour **tout le monde**.\n"
        "- Premier\n"
        "- Deuxième\n"
    )

    parser = Mkd_Parser(markdown)

    ast = parser.parse()

    assert ast.valeur == Rule.DOCUMENT

    assert ast[0].valeur == Rule.HEADING
    assert ast[1].valeur == Rule.PARAGRAPH
    assert ast[2].valeur == Rule.LIST

    assert ast[-1].valeur == Rule.EOF


def test_error():
    parser = Mkd_Parser("Bonjour")
    with pytest.raises(Exception) as erreur:
        parser.error("Erreur test")
    assert "Erreur de syntaxe: Erreur test" in str(erreur.value)