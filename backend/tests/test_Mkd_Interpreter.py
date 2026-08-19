#!/usr/bin/python3

import pytest

from Mkd_Interpreter import (
    MkdToLatex_interpreter,
    escape_latex
)

from AST import Node
from Enum_Rule import Rule
from Token import Token

from unittest.mock import patch, Mock


def test_creation_interpreter():
    interpreter = MkdToLatex_interpreter()
    assert interpreter.latex_text == ""
    assert interpreter.packages == []
    assert interpreter.pos_node == 0
    assert interpreter._table_counter == 0



def test_escape_latex():
    texte = r"50% & 10$ # test_text"
    resultat = escape_latex(texte)
    assert resultat == (
        r"50\% \& 10\$ \# test\_text"
    )


def test_escape_latex_accolades():
    texte = "{test}"
    resultat = escape_latex(texte)
    assert resultat == r"\{test\}"


def test_escape_latex_none():
    assert escape_latex(None) == ""


def test_escape_latex_texte_normal():
    assert escape_latex("Bonjour") == "Bonjour"


def test_advance():

    interpreter = MkdToLatex_interpreter()

    assert interpreter.pos_node == 0

    resultat = interpreter.advance()

    assert resultat == 1
    assert interpreter.pos_node == 1



def test_get_node():

    interpreter = MkdToLatex_interpreter()

    arbre = Node(
        Rule.DOCUMENT,
        [
            Node(Rule.PARAGRAPH),
            Node(Rule.EOF)
        ]
    )

    interpreter.pos_node = 0

    assert interpreter.get_node(arbre).valeur == Rule.PARAGRAPH


def test_get_node_deuxieme_noeud():

    interpreter = MkdToLatex_interpreter()

    arbre = Node(
        Rule.DOCUMENT,
        [
            Node(Rule.PARAGRAPH),
            Node(Rule.EOF)
        ]
    )

    interpreter.pos_node = 1

    assert interpreter.get_node(arbre).valeur == Rule.EOF



def test_add_package():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.add_package("graphicx")

    assert resultat == ["graphicx"]
    assert interpreter.packages == ["graphicx"]


def test_add_package_ne_cree_pas_de_doublon():

    interpreter = MkdToLatex_interpreter()

    interpreter.add_package("graphicx")
    interpreter.add_package("graphicx")

    assert interpreter.packages == ["graphicx"]


def test_add_plusieurs_packages():

    interpreter = MkdToLatex_interpreter()

    interpreter.add_package("graphicx")
    interpreter.add_package("hyperref")
    interpreter.add_package("listings")

    assert interpreter.packages == [
        "graphicx",
        "hyperref",
        "listings"
    ]


def test_get_header_sans_package():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.get_header()

    assert resultat == "\\documentclass{article}\n"


def test_get_header_avec_packages():

    interpreter = MkdToLatex_interpreter()

    interpreter.add_package("graphicx")
    interpreter.add_package("hyperref")

    resultat = interpreter.get_header()

    attendu = (
        "\\documentclass{article}\n"
        "\\usepackage{graphicx}\n"
        "\\usepackage{hyperref}\n"
    )

    assert resultat == attendu


def creer_arbre_heading(niveau, texte):

    token = Token(
        "HEADER",
        (niveau, texte),
        0,
        0
    )

    heading = Node(
        Rule.HEADING,
        [token]
    )

    return Node(
        Rule.DOCUMENT,
        [heading]
    )


def test_convert_heading_niveau_1():

    interpreter = MkdToLatex_interpreter()

    arbre = creer_arbre_heading(1, "Titre")

    resultat = interpreter.convert_heading(arbre)

    assert resultat == r"  \section{Titre}"


def test_convert_heading_niveau_2():

    interpreter = MkdToLatex_interpreter()

    arbre = creer_arbre_heading(2, "Sous titre")

    resultat = interpreter.convert_heading(arbre)

    assert resultat == r"  \subsection{Sous titre}"


def test_convert_heading_niveau_3():

    interpreter = MkdToLatex_interpreter()

    arbre = creer_arbre_heading(3, "Sous sous titre")

    resultat = interpreter.convert_heading(arbre)

    assert resultat == r"  \subsubsection{Sous sous titre}"


def test_convert_heading_niveau_4():

    interpreter = MkdToLatex_interpreter()

    arbre = creer_arbre_heading(4, "Titre")

    resultat = interpreter.convert_heading(arbre)

    assert resultat == r"  \paragraph{Titre}"


def test_convert_heading_niveau_5():

    interpreter = MkdToLatex_interpreter()

    arbre = creer_arbre_heading(5, "Titre")

    resultat = interpreter.convert_heading(arbre)

    assert resultat == r"  \subparagraph{Titre}"


def test_convert_heading_niveau_6():

    interpreter = MkdToLatex_interpreter()

    arbre = creer_arbre_heading(6, "Titre")

    resultat = interpreter.convert_heading(arbre)

    assert resultat == r"  \subparagraph{Titre}"


def test_convert_heading_niveau_invalide():

    interpreter = MkdToLatex_interpreter()

    arbre = creer_arbre_heading(7, "Titre")

    with pytest.raises(Exception):

        interpreter.convert_heading(arbre)



def test_is_valid_url():
    interpreter = MkdToLatex_interpreter()
    assert interpreter.is_valid_url(
        "https://google.com"
    )


def test_is_valid_url_http():
    interpreter = MkdToLatex_interpreter()
    assert interpreter.is_valid_url(
        "http://google.com"
    )


def test_is_valid_url_invalide():
    interpreter = MkdToLatex_interpreter()
    assert not interpreter.is_valid_url(
        "bonjour"
    )


def test_is_valid_url_fichier():

    interpreter = MkdToLatex_interpreter()

    assert not interpreter.is_valid_url(
        "image.png"
    )



def test_all_char_same():
    interpreter = MkdToLatex_interpreter()
    assert interpreter.all_char_same(
        "-----",
        "-"
    )


def test_all_char_same_avec_espaces():
    interpreter = MkdToLatex_interpreter()
    assert interpreter.all_char_same(
        "  -----  ",
        "-"
    )


def test_all_char_same_faux():
    interpreter = MkdToLatex_interpreter()
    assert not interpreter.all_char_same(
        "---x-",
        "-"
    )


def test_convert_newline():
    interpreter = MkdToLatex_interpreter()
    assert interpreter.convert_newline() == r"  \par"


def test_convert_bold():
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.convert_bold(
        ("Bonjour",)
    )
    assert resultat == r" \textbf{Bonjour} "


def test_convert_bold_echappe_latex():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.convert_bold(
        ("50%",)
    )

    assert resultat == r" \textbf{50\%} "



def test_convert_italic():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.convert_italic(
        ("Bonjour",)
    )

    assert resultat == r" \textit{Bonjour} "


def test_convert_bold_italic():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.convert_bold_italic(
        ("Bonjour",)
    )

    assert resultat == (
        r" \textbf{\textit{Bonjour}} "
    )



def test_convert_hline():
    interpreter = MkdToLatex_interpreter()
    assert interpreter.convert_hline() == r"  \hrulefill"



def test_convert_code_inline():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.convert_code_inline(
        ("print()",)
    )

    assert resultat == r"  \texttt{print()} "


def test_convert_code_inline_echappe():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.convert_code_inline(
        ("a_b",)
    )

    assert resultat == r"  \texttt{a\_b} "



def test_convert_link():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.convert_link(
        ("Google", "https://google.com")
    )

    assert resultat == (
        r"  \href{https://google.com}{Google} "
    )

    assert "hyperref" in interpreter.packages


def test_convert_link_echappe_label():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.convert_link(
        ("mon_lien", "https://google.com")
    )

    assert resultat == (
        r"  \href{https://google.com}{mon\_lien} "
    )



def test_convert_quote():

    interpreter = MkdToLatex_interpreter()

    token = Token(
        "QUOTE",
        ("Bonjour",),
        0,
        0
    )

    quote = Node(
        Rule.QUOTE,
        [token]
    )

    arbre = Node(
        Rule.DOCUMENT,
        [quote]
    )

    resultat = interpreter.convert_quote(arbre)

    attendu = (
        "  \\begin{quote}\n"
        "    Bonjour\n"
        "  \\end{quote}\n"
    )

    assert resultat == attendu



def test_convert_list_item():
    interpreter = MkdToLatex_interpreter()

    token1 = Token(
        "LIST_ITEM",
        ("-", "Premier"),
        0,
        0
    )

    token2 = Token(
        "LIST_ITEM",
        ("-", "Deuxième"),
        1,
        0
    )

    liste = Node(
        Rule.LIST_ITEM,
        [
            token1,
            token2
        ]
    )

    list_node = Node(
        Rule.LIST,
        [liste]
    )

    arbre = Node(
        Rule.DOCUMENT,
        [list_node]
    )

    interpreter.pos_node = 0

    resultat = interpreter.convert_list_item(arbre)

    assert "\\begin{itemize}" in resultat
    assert "\\item Premier" in resultat
    assert "\\item Deuxième" in resultat
    assert "\\end{itemize}" in resultat


def test_convert_list_num():
    interpreter = MkdToLatex_interpreter()

    token1 = Token(
        "LIST_NUM",
        ("1", "Premier"),
        0,
        0
    )

    token2 = Token(
        "LIST_NUM",
        ("2", "Deuxième"),
        1,
        0
    )

    liste = Node(
        Rule.LIST_NUM,
        [
            token1,
            token2
        ]
    )

    list_node = Node(
        Rule.LIST,
        [liste]
    )

    arbre = Node(
        Rule.DOCUMENT,
        [list_node]
    )

    interpreter.pos_node = 0

    resultat = interpreter.convert_list_num(arbre)

    assert "\\begin{enumerate}" in resultat
    assert "\\item Premier" in resultat
    assert "\\item Deuxième" in resultat
    assert "\\end{enumerate}" in resultat


def test_convert_code_block():
    interpreter = MkdToLatex_interpreter()

    token = Token(
        "CODE_BLOCK",
        (
            "python",
            "print('Bonjour')\n"
        ),
        0,
        0
    )

    code = Node(
        Rule.CODE_BLOCK,
        [token]
    )

    arbre = Node(
        Rule.DOCUMENT,
        [code]
    )

    interpreter.pos_node = 0

    resultat = interpreter.convert_code_block(arbre)

    attendu = (
        "  \\begin{lstlisting}[language=python]\n"
        "print('Bonjour')\n"
        "  \\end{lstlisting}\n"
    )

    assert resultat == attendu
    assert "listings" in interpreter.packages


def test_convert_code_block_sans_langage():

    interpreter = MkdToLatex_interpreter()

    token = Token(
        "CODE_BLOCK",
        (
            None,
            "print('Bonjour')\n"
        ),
        0,
        0
    )

    code = Node(
        Rule.CODE_BLOCK,
        [token]
    )

    arbre = Node(
        Rule.DOCUMENT,
        [code]
    )

    interpreter.pos_node = 0

    resultat = interpreter.convert_code_block(arbre)

    assert "\\begin{lstlisting}" in resultat
    assert "print('Bonjour')" in resultat



def test_convert_image_local():
    interpreter = MkdToLatex_interpreter()

    token = Token(
        "IMAGE",
        (
            "Chat",
            "chat.jpg",
            None
        ),
        0,
        0
    )

    image = Node(
        Rule.IMAGE,
        [token]
    )

    arbre = Node(
        Rule.DOCUMENT,
        [image]
    )

    interpreter.pos_node = 0

    resultat = interpreter.convert_image(arbre)

    assert "\\begin{figure}" in resultat
    assert "\\centering" in resultat
    assert "\\includegraphics" in resultat
    assert "{chat.jpg}" in resultat
    assert "\\caption{Chat}" in resultat
    assert "\\end{figure}" in resultat

    assert "graphicx" in interpreter.packages


def test_convert_image_avec_caption():

    interpreter = MkdToLatex_interpreter()

    token = Token(
        "IMAGE",
        (
            "Chat",
            "chat.jpg",
            "Mon chat"
        ),
        0,
        0
    )

    image = Node(
        Rule.IMAGE,
        [token]
    )

    arbre = Node(
        Rule.DOCUMENT,
        [image]
    )

    interpreter.pos_node = 0

    resultat = interpreter.convert_image(arbre)

    assert "\\caption{Mon chat}" in resultat


def test_convert_image_url():

    interpreter = MkdToLatex_interpreter()

    token = Token(
        "IMAGE",
        (
            "Chat",
            "https://example.com/chat.jpg",
            None
        ),
        0,
        0
    )

    image = Node(
        Rule.IMAGE,
        [token]
    )

    arbre = Node(
        Rule.DOCUMENT,
        [image]
    )

    mock_converter = Mock()

    mock_converter.image_name = "image_temp.jpg"

    mock_converter.convert_link_image.return_value = (
        "image_temp.jpg"
    )

    mock_converter.is_valid_image.return_value = True

    with patch(
        "Mkd_Interpreter.convert_link_to_image",
        return_value=mock_converter
    ):

        interpreter.pos_node = 0

        resultat = interpreter.convert_image(arbre)

    assert "image_temp.jpg" in resultat

    mock_converter.convert_link_image.assert_called_once()
    mock_converter.is_valid_image.assert_called_once()




def test_convert_image_url_invalide():

    interpreter = MkdToLatex_interpreter()

    token = Token(
        "IMAGE",
        (
            "Chat",
            "https://example.com/chat.jpg",
            None
        ),
        0,
        0
    )

    image = Node(
        Rule.IMAGE,
        [token]
    )

    arbre = Node(
        Rule.DOCUMENT,
        [image]
    )

    mock_converter = Mock()

    mock_converter.image_name = ""

    mock_converter.convert_link_image.side_effect = (
        Exception("Erreur téléchargement")
    )

    with patch(
        "Mkd_Interpreter.convert_link_to_image",
        return_value=mock_converter
    ):

        interpreter.pos_node = 0

        resultat = interpreter.convert_image(arbre)

    assert "image_error.png" in resultat


def test_convert_table():

    interpreter = MkdToLatex_interpreter()

    token = Token(
        "TABLE",
        (
            ["Nom", "Age"],
            ["---", "---"],
            [
                ["Samya", "20"],
                ["Alice", "21"]
            ],
            None
        ),
        0,
        0
    )

    table = Node(
        Rule.TABLE,
        [token]
    )

    arbre = Node(
        Rule.DOCUMENT,
        [table]
    )

    interpreter.pos_node = 0

    resultat = interpreter.convert_table(arbre)

    assert "\\begin{table}" in resultat
    assert "\\begin{tabular}" in resultat
    assert "Nom & Age" in resultat
    assert "Samya & 20" in resultat
    assert "Alice & 21" in resultat
    assert "\\end{tabular}" in resultat
    assert "\\end{table}" in resultat


def test_convert_table_avec_caption():

    interpreter = MkdToLatex_interpreter()

    token = Token(
        "TABLE",
        (
            ["Nom", "Age"],
            ["---", "---"],
            [
                ["Samya", "20"]
            ],
            "Informations"
        ),
        0,
        0
    )

    table = Node(
        Rule.TABLE,
        [token]
    )

    arbre = Node(
        Rule.DOCUMENT,
        [table]
    )

    interpreter.pos_node = 0

    resultat = interpreter.convert_table(arbre)

    assert "\\caption{Informations}" in resultat
    assert "\\label{tab:table-1}" in resultat
    assert "caption" in interpreter.packages


def test_compiler_texte_simple():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.compiler(
        "Bonjour"
    )

    assert "\\documentclass{article}" in resultat
    assert "\\begin{document}" in resultat
    assert "Bonjour" in resultat
    assert "\\end{document}" in resultat


def test_compiler_titre():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.compiler(
        "# Bonjour\n"
    )

    assert "\\section{Bonjour}" in resultat


def test_compiler_gras():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.compiler(
        "**Bonjour**"
    )

    assert "\\textbf{Bonjour}" in resultat


def test_compiler_italic():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.compiler(
        "*Bonjour*"
    )

    assert "\\textit{Bonjour}" in resultat


def test_compiler_lien():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.compiler(
        "[Google](https://google.com)"
    )

    assert "\\href{https://google.com}" in resultat
    assert "\\usepackage{hyperref}" in resultat


def test_compiler_image():

    interpreter = MkdToLatex_interpreter()

    resultat = interpreter.compiler(
        "![Chat](chat.jpg)"
    )

    assert "\\includegraphics" in resultat
    assert "chat.jpg" in resultat
    assert "\\usepackage{graphicx}" in resultat


def test_run():

    interpreter = MkdToLatex_interpreter()

    token = Token(
        "TEXT",
        "Bonjour",
        0,
        0
    )

    inline = Node(
        Rule.INLINE,
        [token]
    )

    paragraph = Node(
        Rule.PARAGRAPH,
        [inline]
    )

    arbre = Node(
        Rule.DOCUMENT,
        [
            paragraph,
            Node(Rule.EOF)
        ]
    )

    resultat = interpreter.run(arbre)

    assert "Bonjour" in resultat