#!/usr/bin/python3

"""
Nom ......... : Token.py
Role ........ : crée un objet token
Auteur ...... : PREMAKUMAR Samya
Version ..... : V1.1 
Execution ... : python3 Token.py
"""

class Token : 
	''' le token (ou lexème) est composé du type, la valeur 
	d'un mot (ou un texte) et éventuellemnt la ligne + la colonne 
	où a été trouvé le token. '''
	def __init__(self, token_type, token_value, x=None, y=None) :
		self.token_type = token_type
		self.token_value = token_value
		self.coord = (x, y)

	''' affiche le token (ou lexeme). '''
	def __repr__(self) : 
		return f"({self.token_type}, {self.token_value}, {self.coord})"
