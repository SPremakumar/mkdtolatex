from Mkd_Interpreter import MkdToLatex_interpreter


def test_integration_titre_paragraphe():
    markdown = "# Bonjour\n\nCeci est un texte."
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)

    attendu = (
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "  \\section{Bonjour}\n"
        "  \\par\n"
        "  Ceci est un texte.\n"
        "\n"
        "\\end{document}"
    )
    assert resultat == attendu


def test_integration_titres():
    markdown = (
        "# Titre 1\n"
        "## Titre 2\n"
        "### Titre 3\n"
        "#### Titre 4\n"
        "##### Titre 5\n"
        "###### Titre 6\n"
    )
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\section{Titre 1}" in resultat
    assert "\\subsection{Titre 2}" in resultat
    assert "\\subsubsection{Titre 3}" in resultat
    assert "\\paragraph{Titre 4}" in resultat
    assert "\\subparagraph{Titre 5}" in resultat
    assert "\\subparagraph{Titre 6}" in resultat


def test_integration_gras():
    markdown = "Ceci est **important**.\n"
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\textbf{important}" in resultat


def test_integration_italique():
    markdown = "Ceci est *important*.\n"
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\textit{important}" in resultat


def test_integration_gras_italique():
    markdown = "Ceci est ***important***.\n"
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\textbf{\\textit{important}}" in resultat


def test_integration_lien():
    markdown = "[Google](https://google.com)\n"
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\usepackage{hyperref}" in resultat
    assert "\\href{https://google.com}{Google}" in resultat


def test_integration_code_inline():
    markdown = "Utiliser `print()` en Python.\n"
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\texttt{print()}" in resultat


def test_integration_liste_non_ordonnee():
    markdown = (
        "* Premier élément\n"
        "* Deuxième élément\n"
        "* Troisième élément\n"
    )
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\begin{itemize}" in resultat
    assert "\\item Premier élément" in resultat
    assert "\\item Deuxième élément" in resultat
    assert "\\item Troisième élément" in resultat
    assert "\\end{itemize}" in resultat



def test_integration_liste_ordonnee():
    markdown = (
        "1. Premier élément\n"
        "2. Deuxième élément\n"
        "3. Troisième élément\n"
    )
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\begin{enumerate}" in resultat
    assert "\\item Premier élément" in resultat
    assert "\\item Deuxième élément" in resultat
    assert "\\item Troisième élément" in resultat
    assert "\\end{enumerate}" in resultat

def test_integration_citation():
    markdown = "> Ceci est une citation.\n"
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\begin{quote}" in resultat
    assert "Ceci est une citation." in resultat
    assert "\\end{quote}" in resultat


def test_integration_image():
    markdown = "![Mon image](image.png)\n"
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\usepackage{graphicx}" in resultat
    assert "\\begin{figure}" in resultat
    assert "\\includegraphics" in resultat
    assert "image.png" in resultat
    assert "\\caption{Mon image}" in resultat
    assert "\\end{figure}" in resultat



def test_integration_image_avec_legende():
    markdown = '![Mon image](image.png "Une légende")\n'
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\usepackage{graphicx}" in resultat
    assert "\\includegraphics" in resultat
    assert "image.png" in resultat
    assert "\\caption{Une légende}" in resultat


def test_integration_tableau_avec_legende():
    markdown = (
        "| Nom | Age |\n"
        "| --- | --- |\n"
        "| Alice | 20 |\n"
        "| Bob | 25 |\n"
        "[Informations]\n"
    )
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\begin{table}" in resultat
    assert "\\usepackage{caption}" in resultat
    assert "\\caption{Informations}" in resultat
    assert "\\label{tab:table-1}" in resultat


def test_integration_code_block():
    markdown = (
        "```python\n"
        "print('Bonjour')\n"
        "```\n"
    )
    interpreter = MkdToLatex_interpreter()
    resultat = interpreter.compiler(markdown)
    assert "\\usepackage{listings}" in resultat
    assert "\\begin{lstlisting}[language=python]" in resultat
    assert "print('Bonjour')" in resultat
    assert "\\end{lstlisting}" in resultat



# !PB avec tableau sans légende et ligne horizontale.