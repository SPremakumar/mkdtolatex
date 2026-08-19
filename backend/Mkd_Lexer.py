#!/usr/bin/python3

"""
Nom ......... : Mkd_Lexer.py
Role ........ : le lexeur pour notre interpreteur markdown en latex
Auteur ...... : PREMAKUMAR Samya
Version ..... : V1.3 (corrections)
Execution ... : python3 Mkd_Lexer.py
"""

import re
from Token import Token


class Mkd_Lexer:
	""" Le lexeur utilise un dictionnaire pour associer des
	type à des expressions réguliers, afin de repérer des
	commandes markdown dans un text (self.text). """

	# Ancre "début de ligne" : soit le tout début du texte, soit juste après un '\n'.
	_LINE_START = r'(?:(?<=\n)|^)'

	def __init__(self, text):
		self.text = text
		self.pos = 0
		self.line = 0
		self.column = 0
		self.raw_patterns = {
			"ESCAPE": r'\\([\\`*_{}\[\]()#+\-.!>~^$%&])',
			"BOLD_ITALIC": r'\*\*\*(.+?)\*\*\*',  # *** text ***
			"BOLD": r'\*\*(.*?)\*\*',
			"ITALIC": r'\*(.*?)\*',
			"HEADER": self._LINE_START + r'(#{1,6})\s+(.+)(?:\n|\Z)',
			"LIST_ITEM": self._LINE_START + r'([-*\+])\s+(.+)(?:\n|\Z)',
			"LIST_NUM": self._LINE_START + r'(\d+)\.\s+(.+)(?:\n|\Z)',
			"H_LINE": self._LINE_START + r'(?:---+|\*\*\*)(?:\n|\Z)',
			"IMAGE": r'!\[(.*?)\]\((.*?)\s*(?:"(.*?)")?\)',
			"LINK": r'\[(.*?)\]\((.*?)\)',
			"QUOTE": self._LINE_START + r'>\s+(.*?)(?=\n|$)',
			"TABLE": r'(\|(?:[^\|\n]*\|)+)\n(\|(?:[-:| ]*\|)+)\n((?:\|(?:[^\|\n]*\|)+\n?)*)\s*(?:\[(.*?)\])?',
			"CODE_INLINE": r'`([^`]+?)`',
			"CODE_BLOCK": r'```(?:\s*(\w+))?\n([\s\S]*?)```',
			"TEXT": r'([^\*\`\!\[\\\n]+)',
			"NL": r'\n',
			"EOF": "End Of File",
		}
		# précompilation : évite de recompiler chaque motif à chaque token
		self.patterns = {
			name: (re.compile(pattern) if name != "EOF" else pattern)
			for name, pattern in self.raw_patterns.items()
		}

	""" Renvoie une correspondance à partir de la position actuelle dans le texte. """
	def find_match(self, position):
		for token_type, regex in self.patterns.items():
			if token_type == "EOF":
				continue
			match = regex.match(self.text, position)
			if match:
				return token_type, match, len(match.group())
		return None, None, 1

	""" Retourne la valeur à partir de la correspondance trouvée. """
	def get_value(self, token_type, match):
		if token_type != 'TEXT':
			return match.groups()
		else:
			return (match.group(),)

	""" Créer le token en utilisant la classe 'Token' et gère les cas spéciaux """
	def create_token(self, token_type, match):
		value = self.get_value(token_type, match)

		if token_type == 'TEXT':
			value = match.group().strip()

		elif token_type == 'ESCAPE':
			value = value[0]  # le caractère littéral échappé (sans le '\')

		elif token_type == 'HEADER':
			level = len(value[0])
			value = (level, value[1].strip())

		elif token_type == 'LIST_ITEM':
			bullet = match.group(1)
			text = value[1]
			value = (bullet, text)
		elif token_type == 'H_LINE':
			value = match.group().strip()
		elif token_type == 'IMAGE':
			text_alt, image_path, caption = value
			value = (text_alt, image_path, caption)
		elif token_type == 'TABLE':
			titre_col = value[0].strip().split('|')[1:-1]
			sep = value[1].strip().split('|')[1:-1]
			contenu = [row.strip().split('|')[1:-1] for row in value[2].strip().split('\n')]
			caption = value[3] or None
			value = (titre_col, sep, contenu, caption)
		elif token_type == 'NL':
			value = f'\\n'
		return Token(token_type, value, self.line, self.column)

	""" Mettre à jour la position (et compte les lignes traversées par le token) """
	def update_position(self, token_type, match, length):
		consumed = match.group()
		nb_newlines = consumed.count('\n')
		if nb_newlines:
			self.line += nb_newlines
			self.column = len(consumed) - consumed.rfind('\n') - 1
		else:
			self.column += length
		return match.end()

	""" Trouve une correspondance, puis crée ce token, met à jour la position et le retourne. """
	def get_token(self):
		while self.pos < len(self.text):
			token_type, match, length = self.find_match(self.pos)

			if match:
				self.pos = self.update_position(token_type, match, length)
				return self.create_token(token_type, match)

			else:
				# Filet de sécurité : ne devrait plus arriver puisque TEXT couvre
				# désormais tout caractère imprimable hors '*', '`' et '\n'.
				# On avance sans rien perdre silencieusement : on émet quand
				# même un token TEXT pour le caractère isolé.
				char = self.text[self.pos]
				self.pos += 1
				self.column += 1
				return Token("TEXT", char, self.line, self.column)

		return Token("EOF", self.raw_patterns["EOF"], self.line, self.column)