from AST import Node
from Token import Token


def test_creation_node():
    node = Node("document")

    assert node.valeur == "document"
    assert node.branches == []
    assert len(node) == 0


def test_creation_avec_branches():
    enfant1 = Node("paragraph")
    enfant2 = Node("paragraph")

    node = Node("document", [enfant1, enfant2])

    assert node.valeur == "document"
    assert len(node) == 2
    assert node[0] is enfant1
    assert node[1] is enfant2


def test_len():
    node = Node("document")

    assert len(node) == 0

    node.add(Node("paragraph"))
    assert len(node) == 1

    node.add(Node("paragraph"))
    assert len(node) == 2


def test_getitem():
    enfant1 = Node("paragraph")
    enfant2 = Node("heading")

    node = Node("document", [enfant1, enfant2])

    assert node[0] is enfant1
    assert node[1] is enfant2


def test_getitem_index_invalide():
    node = Node("document")

    try:
        node[0]
        assert False
    except IndexError:
        pass


def test_add_node():
    parent = Node("document")
    enfant = Node("paragraph")

    resultat = parent.add(enfant)

    assert resultat is None
    assert len(parent) == 1
    assert parent[0] is enfant


def test_add_token():
    parent = Node("paragraph")

    token = Token(
        "TEXT",
        "Bonjour",
        1,
        5
    )

    parent.add(token)

    assert len(parent) == 1

    token_ajoute = parent[0]

    assert isinstance(token_ajoute, Token)
    assert token_ajoute.token_type == token.token_type
    assert token_ajoute.token_value == token.token_value
    assert token_ajoute.coord == token.coord


def test_add_token_cree_une_copie():
    parent = Node("paragraph")

    token = Token("TEXT", "Bonjour", 1, 5)

    parent.add(token)

    token_ajoute = parent[0]

    assert token_ajoute is not token


def test_add_autre_type():
    parent = Node("document")

    parent.add("paragraph")

    assert len(parent) == 1
    assert isinstance(parent[0], Node)
    assert parent[0].valeur == "paragraph"


def test_repr_node_simple():
    node = Node("document")

    resultat = repr(node)

    assert resultat == "'document'\n"


def test_repr_nodes_imbriques():
    document = Node("document")
    paragraph = Node("paragraph")
    text = Node("text")

    paragraph.add(text)
    document.add(paragraph)

    resultat = repr(document)

    attendu = (
        "'document'\n"
        "-'paragraph'\n"
        "--'text'\n"
    )

    assert resultat == attendu


def test_repr_avec_token():
    paragraph = Node("paragraph")

    token = Token("TEXT", "Bonjour", 1, 1)
    paragraph.add(token)

    resultat = repr(paragraph)

    attendu = (
        "'paragraph'\n"
        "-(TEXT, Bonjour, (1, 1))\n"
    )

    assert resultat == attendu