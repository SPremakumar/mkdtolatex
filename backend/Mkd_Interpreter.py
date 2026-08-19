#!/usr/bin/python3

"""
Nom ......... : Mkd_Interpreter.py
Role ........ : l'évaluateur (ou l'intepréteur) réalisation la traduction entre le langage markdown et latex.
Auteur ...... : PREMAKUMAR Samya
Version ..... : V1.2 (corrections)
Execution ... : python3 Main.py
"""

from AST import Node
from Enum_Rule import Rule
from Mkd_Lexer import Mkd_Lexer
from Mkd_Parser import Mkd_Parser
from convertir_link_image import convert_link_to_image
import sys
import re


# --------------------------------------------------------------------------- #
# Échappement des caractères spéciaux LaTeX
# --------------------------------------------------------------------------- #
_LATEX_SPECIAL_CHARS = {
	'\\': r'\textbackslash{}',
	'&': r'\&',
	'%': r'\%',
	'$': r'\$',
	'#': r'\#',
	'_': r'\_',
	'{': r'\{',
	'}': r'\}',
	'~': r'\textasciitilde{}',
	'^': r'\textasciicircum{}',
}
_LATEX_SPECIAL_RE = re.compile(r'([\\&%$#_{}~^])')


def escape_latex(text):
	""" échappe les caractères ayant un sens spécial en LaTeX, pour que
	le texte markdown d'origine soit affiché tel quel (et pas interprété
	comme du code LaTeX ou, pire, casse la compilation). """
	if text is None:
		return ""
	return _LATEX_SPECIAL_RE.sub(lambda m: _LATEX_SPECIAL_CHARS[m.group(1)], text)


class MkdToLatex_interpreter:
	""" l'intrepréteur contient une liste vide de package qui est
	rempli au fur et à mesure, un document latex et la position courant
	d'un noeud. """
	def __init__(self):
		self.latex_text = ""
		self.packages = []
		self.pos_node = 0
		self._table_counter = 0
		# self.level_indentation = " " ou int || À FAIRE !!


	""" avance dans l'arbre en incrémentant self.pos_node """
	def advance(self):
		self.pos_node += 1
		return self.pos_node


	""" renvoie un noeud courant de l'arbre pour """
	def get_node(self, tree):
		return tree[self.pos_node]


	""" ajoute à la liste des packages """
	def add_package(self, package):
		if package not in self.packages:
			self.packages.append(package)
		return self.packages


	""" construit l'entête d'un document latex,
	à savoir le type de document + ajoute les packages
	si nécessaire """
	def get_header(self):
		header = "\\documentclass{article}\n"
		for package in self.packages:
			header += f"\\usepackage{{{package}}}\n"
		return header


	""" créer une interpréteur """
	def interpreter(self):
		code_line = ""
		document_content = "\\begin{document}\n"

		while code_line.lower() != 'exit' + '\n':
			code_line = input(">>> ") + '\n'

			# Le mode multi-lignes :
			if code_line.strip() == '```' or code_line.strip() == "[~list]" or code_line.strip() == "[~table]":
				code_line = self.multi_lines(code_line)

			''' Le mode ligne et le mode multi-lines sont passés
			dans le parseur, qui construit un arbre AST, puis nous
			le traduisant en utilisant la fonction run(). '''
			interpreter = Mkd_Parser(code_line)
			interpreter.parse()
			self.run(interpreter.AST)

		# renvoie le document latex avec les en-têtes + la fin :
		document_content += self.latex_text + "\n\\end{document}"
		self.latex_text = self.get_header() + document_content

		# FIN de l'interprète.
		print("À bientôt")


	""" converter - convertir un texte écris en markdown en latex """
	def compiler(self, text):
		document_content = "\\begin{document}\n"

		compiler = Mkd_Parser(text)
		compiler.parse()
		self.run(compiler.AST)

		document_content += self.latex_text + "\n\\end{document}"
		self.latex_text = self.get_header() + document_content
		return self.latex_text


	""" fonction auxiliaire pour gérer le mode multi-lignes.
	Renvoie une chaine de charactère """
	def multi_lines(self, code_line):
		code_multiline = ""
		start_pat = code_line[:-1]  # le pattern qui déclenche une multilignes
		mode_multilines = True

		while mode_multilines:
			code_line = input("... ") + '\n'

			if code_line.strip() == start_pat:
				mode_multilines = False

			else:
				code_multiline += code_line

		# re-format la chaine de caractère + renvoie la chaine :
		if start_pat == "```":
			code_multiline = "```" + code_multiline + "```"
		elif start_pat == "[~list]" or start_pat == "[~table]":
			code_multiline = code_multiline

		return code_multiline


	""" Parcours l'arbre AST pour traduire chaque ligne
	(jusqu'à le token EOF) """
	def run(self, tree):
		self.pos_node = 0
		while self.get_node(tree).valeur != Rule.EOF:
			self.evaluate(tree)
			self.advance()
		return self.latex_text


	""" évalue chaque noeud et renvoie des fonctions pour convertir """
	def evaluate(self, tree):
		match self.get_node(tree).valeur:

			case Rule.HEADING:
				self.latex_text += self.convert_heading(tree)
				self.latex_text += '\n'

			case Rule.NEW_LINE:
				self.latex_text += self.convert_newline()
				self.latex_text += '\n'

			case Rule.PARAGRAPH:
				self._paragraph(tree)
				self.latex_text += '\n'

			case Rule.H_LINE:
				self.latex_text += self.convert_hline()
				self.latex_text += '\n'

			case Rule.LIST:
				self._mdk_list(tree)
				self.latex_text += '\n'

			case Rule.IMAGE:
				self.latex_text += self.convert_image(tree)
				self.latex_text += '\n'

			case Rule.QUOTE:
				self.latex_text += self.convert_quote(tree)
				self.latex_text += '\n'

			case Rule.TABLE:
				self.latex_text += self.convert_table(tree)
				self.latex_text += '\n'

			case Rule.CODE_BLOCK:
				self.latex_text += self.convert_code_block(tree)
				self.latex_text += '\n'


	""" selon les noeuds (inline ou new_lines), renvoie à des fonctions de convertions """
	def _paragraph(self, tree):
		for node in self.get_node(tree).branches:
			if isinstance(node, Node) and node.valeur == Rule.INLINE:
				self._inline(node.branches)
			elif isinstance(node, Node) and node.valeur == Rule.NEW_LINE:
				self.latex_text += self.convert_newline()


	""" selon les noeuds (text, bold, italic et bold_italic), renvoie à des fonctions de convertions """
	def _inline(self, node):
		self.latex_text += "  "
		for i in node:
			match i.token_type:
				case "TEXT":
					self.latex_text += escape_latex(i.token_value)
				case "BOLD":
					self.latex_text += self.convert_bold(i.token_value)
				case "ITALIC":
					self.latex_text += self.convert_italic(i.token_value)
				case "BOLD_ITALIC":
					self.latex_text += self.convert_bold_italic(i.token_value)
				case "LINK":
					self.latex_text += self.convert_link(i.token_value)
				case "CODE_INLINE":
					self.latex_text += self.convert_code_inline(i.token_value)

		return self.latex_text


	""" convertir en liste (à puces ou numérotées)"""
	def _mdk_list(self, tree):
		if self.get_node(tree).branches[0].valeur == Rule.LIST_ITEM:
			self.convert_list_item(tree)
		elif self.get_node(tree).branches[0].valeur == Rule.LIST_NUM:
			self.convert_list_num(tree)


	""" convertir une liste numérotée """
	def convert_list_num(self, tree):
		self.latex_text += "  \\begin{enumerate}\n"
		for item in self.get_node(tree).branches[0]:
			self.latex_text += f"    \\item {escape_latex(item.token_value[1])}\n"
		self.latex_text += "  \\end{enumerate}"
		return self.latex_text + '\n'


	""" convertir une liste à puces """
	def convert_list_item(self, tree):
		self.latex_text += "  \\begin{itemize}\n"
		for item in self.get_node(tree).branches[0]:
			self.latex_text += f"    \\item {escape_latex(item.token_value[1])}\n"
		self.latex_text += "  \\end{itemize}"
		return self.latex_text + '\n'


	""" convertir les titres  """
	def convert_heading(self, tree, num=""):
		sub = "sub"
		section = "section"
		paragraph = "paragraph"

		token = self.get_node(tree).branches[0].token_value
		level, text = token[0], escape_latex(token[1])

		if level in (1, 2, 3):
			return f"  \\{sub * (level - 1) + section + num}{{{text}}}"
		elif level in (4, 5, 6):
			# LaTeX standard n'a pas de niveau plus profond que \subparagraph :
			# les niveaux 5 et 6 markdown sont donc tous les deux mappés dessus.
			return f"  \\{sub * min(level - 4, 1) + paragraph}{{{text}}}"
		else:
			raise Exception(f"Erreur : niveau de titre inattendu ({level})")


	""" fonction auxiliaie pour vérifie si une chaine est un url """
	def is_valid_url(self, url):
		url_regex = re.compile(r'https?://(?:www\.)?[a-zA-Z0-9./]+')
		return bool(url_regex.match(url))


	""" convertir une inclusion image """
	def convert_image(self, tree):
		self.add_package("graphicx")

		# extraire les informations (légende, le chemin de l'image.)
		alt_txt = self.get_node(tree).branches[0].token_value[0]
		path = self.get_node(tree).branches[0].token_value[1]
		caption = self.get_node(tree).branches[0].token_value[2] or None

		# vérifie si le path est un lien (url) ou le chemin d'un image
		# si OUI alors convertir le lien en image en utilisant la classe "convert_link_to_image" :
		if self.is_valid_url(path):
			clti = convert_link_to_image(path)
			try:
				clti.convert_link_image()
				valid = clti.is_valid_image()
			except Exception:
				valid = False
			path = clti.image_name if valid else "image_error.png"

		# résultat en latex :
		latex_image = f"  \\begin{{figure}}[h!]\n"
		latex_image += f"    \\centering\n"
		latex_image += f"    \\includegraphics[width=\\textwidth]{{{path}}}\n"
		if caption is not None:
			latex_image += f"    \\caption{{{escape_latex(caption)}}}\n"
		else:
			latex_image += f"    \\caption{{{escape_latex(alt_txt)}}}\n"
		latex_image += f"  \\end{{figure}}\n"

		# renvoie le latex_text :
		return latex_image


	""" fonction auxiliaire : vérifie si une chaine contient les même charactère, utilise pour trouver '----' """
	def all_char_same(self, str, char):
		str = str.strip()
		return all(c == char for c in str)


	""" convertir les tableaux """
	def convert_table(self, tree, opt=0):
		col_title = self.get_node(tree).branches[0].token_value[0]
		table_content = self.get_node(tree).branches[0].token_value[2]
		column_format = '|'.join(['c'] * len(col_title))
		caption = self.get_node(tree).branches[0].token_value[3] or None

		self._table_counter += 1

		# début du tableau LaTeX
		latex_table = f"\n  \\begin{{table}}[h!]\n"
		latex_table += f"    \\centering\n"
		latex_table += f"     \\begin{{tabular}}{{|{column_format}|}}\n"
		latex_table += f"       \\hline\n"
		latex_table += '         ' + ' & '.join(escape_latex(c) for c in col_title) + ' \\\\' + '\n'
		latex_table += f"       \\hline\n"

		# le contenu du tableau :
		for ligne in range(len(table_content)):
			# si le contenu de la ligne (toute) contient "----" alors on le transforme en ligne \hline.
			if len(set(table_content[ligne])) == 1 and self.all_char_same(table_content[ligne][0], '-'):
				latex_table += f"       \\hline\n"
			# Sinon met le contenu :
			else:
				latex_table += '         ' + ' & '.join(escape_latex(c) for c in table_content[ligne]) + ' \\\\' + '\n'

		# fin du tableau :
		latex_table += f"       \\hline\n"
		latex_table += f"     \\end{{tabular}}\n"

		# ajoute une légende :
		if caption is not None:
			self.add_package("caption")
			latex_table += f"   \\caption{{{escape_latex(caption)}}}\n"
			latex_table += f"   \\label{{tab:table-{self._table_counter}}}\n"

		latex_table += f"   \\end{{table}}\n"

		# renvoie la latex_text
		return latex_table


	""" convertir les citations """
	def convert_quote(self, tree):
		quote_text = escape_latex(self.get_node(tree).branches[0].token_value[0])
		return (
			"  \\begin{quote}\n"
			f"    {quote_text}\n"
			"  \\end{quote}\n"
		)


	""" convertir les sauts à la ligne """
	def convert_newline(self):
		return "  \\par"


	''' convertir un text en gras '''
	def convert_bold(self, text):
		return f" \\textbf{{{escape_latex(text[0])}}} "


	''' convertir un text en italic '''
	def convert_italic(self, text):
		return f" \\textit{{{escape_latex(text[0])}}} "


	''' convertir un text en gras et italic '''
	def convert_bold_italic(self, text):
		return f" \\textbf{{\\textit{{{escape_latex(text[0])}}}}} "


	""" convertir une ligne horizontale """
	def convert_hline(self):
		return "  \\hrulefill"


	""" convertir un lien """
	def convert_link(self, text):
		self.add_package("hyperref")
		label, url = escape_latex(text[0]), text[1]
		return f"  \\href{{{url}}}{{{label}}} "


	""" convertir en code en ligne """
	def convert_code_inline(self, text):
		return f"  \\texttt{{{escape_latex(text[0])}}} "


	""" convertir du code en block """
	def convert_code_block(self, tree):
		self.add_package("listings")
		lang = self.get_node(tree).branches[0].token_value[0]
		code = self.get_node(tree).branches[0].token_value[1]
		opts = f"[language={lang}]" if lang else ""
		code_block = f"  \\begin{{lstlisting}}{opts}\n"
		code_block += code
		code_block += f"  \\end{{lstlisting}}"
		return code_block + '\n'