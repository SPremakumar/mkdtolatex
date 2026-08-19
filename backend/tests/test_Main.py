import pytest
from unittest.mock import patch, mock_open

from Main import open_file, save_file


def test_open_file():
    contenu = "Bonjour Markdown"
    with patch("builtins.open",mock_open(read_data=contenu)):
        resultat = open_file("test.md")
    assert resultat == contenu


def test_open_file_fichier_vide():
    with patch("builtins.open",mock_open(read_data="")):
        resultat = open_file("test.md")
    assert resultat == ""


def test_open_file_multiligne():
    contenu = "# Titre\n\nBonjour **tout le monde**.\n"
    with patch("builtins.open",mock_open(read_data=contenu)):
        resultat = open_file("test.md")
    assert resultat == contenu


def test_open_file_fichier_inexistant():
    with patch("builtins.open",side_effect=FileNotFoundError):
        with pytest.raises(SystemExit) as erreur:
            open_file("inexistant.md")
    assert erreur.value.code == 1


def test_open_file_erreur_io():
    with patch("builtins.open",side_effect=IOError("Erreur lecture")):
        with pytest.raises(SystemExit) as erreur:
            open_file("test.md")
    assert erreur.value.code == 1


def test_save_file():
    contenu = "Bonjour LaTeX"
    fichier = mock_open()

    with patch("builtins.open",fichier):
        resultat = save_file(contenu,"resultat.tex")

    assert resultat is None
    fichier.assert_called_once_with("resultat.tex","w")
    fichier().write.assert_called_once_with(contenu)


def test_save_file_latex():
    contenu = "\\documentclass{article}\n\\begin{document}\nBonjour\n\\end{document}"
    fichier = mock_open()

    with patch("builtins.open",fichier):
        save_file(contenu,"resultat.tex")

    assert fichier().write.call_count == 1
    fichier().write.assert_called_once_with(contenu)


def test_save_file_erreur_io():
    with patch("builtins.open",side_effect=IOError("Erreur écriture")):
        with pytest.raises(SystemExit) as erreur:
            save_file("Bonjour","resultat.tex")
    assert erreur.value.code == 1