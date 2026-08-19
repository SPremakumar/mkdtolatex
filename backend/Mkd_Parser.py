#!/usr/bin/python3

"""
Nom ......... : Mkd_Parser.py
Role ........ : le parseur pour notre interpreteur markdown en latex (= créer un arbre AST)
Auteur ...... : PREMAKUMAR Samya
Version ..... : V1.1 
Execution ... : python3 Mkd_Parser.py
"""

from AST import Node 
from Mkd_Lexer import Mkd_Lexer
from Enum_Rule import Rule


class Mkd_Parser : 
	""" le parseur utilise le lexeur pour tokeniser 
	(séparer les mots en lexemes) le texte d'entrée pour
	les re-organiser en arbre syntaxique """
	def __init__(self, text) : 
		self.Mkd_Lexer = Mkd_Lexer(text)
		self.current_token = self.Mkd_Lexer.get_token()
		self.AST = Node(Rule.DOCUMENT)
		self.all_token_type = ["HEADER", "ITALIC", 
		"BOLD", "BOLD_ITALIC", "LIST_ITEM", "LIST_NUM", 
		"H_LINE", "TEXT", "IMAGE", "LINK", "QUOTE", 
		"TABLE", "CODE_BLOCK", "CODE_INLINE" ]


	""" Avance dans les tokens """
	def advance(self) : 
		self.current_token = self.Mkd_Lexer.get_token()
		return self.current_token


	""" Affiche un message d'erreur """
	def error(self, message) :
		raise Exception(f"Erreur de syntaxe: {message}. Token actuel: {self.current_token}")


	""" parse() : construit l'arbre AST """
	def parse(self) : 
		return self.document()


	""" document = { newline }, { block }, { newline } ; """
	def document(self) :
		while self.current_token.token_type != "EOF" :

			if self.current_token.token_type == "NL" :
				self.AST.add(self.newline())
				self.advance()
			
			elif self.current_token.token_type in self.all_token_type :
				self.AST.add(self.block())
			
			else :
				self.advance()

		# ajoute un EOF dans l'arbre
		self.AST.add(Node(Rule.EOF))
		return self.AST


	""" block = heading | list | horizontalrule | paragraph ; """
	def block(self) : 
		node = Node(Rule.BLOCK)
		# pour les titres
		if self.current_token.token_type == "HEADER": 
			node = self.heading()
			self.advance()

		# pour les listes
		elif self.current_token.token_type in ["LIST_ITEM", "LIST_NUM"]: 
			node = self.markdown_list()
		
		# pour les lignes horizontales
		elif self.current_token.token_type == "H_LINE": 
			node = self.horizontal_line()
			self.advance()

		# pour l'inclusion des images : 
		elif self.current_token.token_type == "IMAGE":
			node = self.image()
			self.advance()

		# pour l'inclusion des citations : 
		elif self.current_token.token_type == "QUOTE" : 
			node = self.quote()
			self.advance()

		# pour l'inclusion des tableaux : 
		elif self.current_token.token_type == "TABLE" : 
			node = self.table()
			self.advance()

		# pour l'inclusion des codes en block : 
		elif self.current_token.token_type == "CODE_BLOCK" : 
			node = self.code_block()
			self.advance()

		# # sinon c'est un paragraphe : ()
		else: 
			node = self.paragraph()
			self.advance()
		
		return node


	""" newline = "\n" ; """    
	def newline(self) :
		node = Node(Rule.NEW_LINE)     
		node.add(self.current_token)
		return node


	""" heading = ("#" | "##" | "###" | "####" | "#####" | "######"), " ", text, newline ; """
	def heading(self) : 
		node = Node(Rule.HEADING)
		node.add(self.current_token)
		return node


	""" horizontalrule  =  "***", newline ; """
	def horizontal_line(self) : 
		node = Node(Rule.H_LINE)
		node.add(self.current_token)
		return node


	""" image = "![", text, "](", text, ")"; """
	def image(self) : 
		node = Node(Rule.IMAGE)
		node.add(self.current_token)
		return node


	""" quote  = ">", " ", text, newline ; """
	def quote(self) : 
		node = Node(Rule.QUOTE)
		node.add(self.current_token)
		return node


	""" table = tableheader, tabledivider, { tablerow } ; """
	def table(self) : 
		node = Node(Rule.TABLE)
		node.add(self.current_token)
		return node


	""" codeblock = codeblockstart, { codeblockline }, codeblockend ; """
	def code_block(self) :
		node = Node(Rule.CODE_BLOCK)
		node.add(self.current_token)
		return node


	""" paragraph = { inline }, newline, { newline } ; """
	def paragraph(self) :
		node = Node(Rule.PARAGRAPH)
		
		while self.current_token.token_type in ["TEXT", "BOLD", "ITALIC", "BOLD_ITALIC", "LINK", "CODE_INLINE"]:
			node.add(self.inline())
			self.advance()
		
		if self.current_token.token_type == "NL": 
			node.add(self.newline())
		
		return node


	""" inline = { text | bold | italic | bold_italic | liens | code en ligne } ; """
	def inline(self) :
		node = Node(Rule.INLINE)
		while self.current_token.token_type in ["TEXT", "BOLD", "ITALIC", "BOLD_ITALIC", "LINK", "CODE_INLINE"] :
			if self.current_token.token_type == "TEXT":
				node.add(self.current_token)		
			elif self.current_token.token_type == "BOLD":
				node.add(self.current_token)
			elif self.current_token.token_type == "ITALIC":
				node.add(self.current_token)
			elif self.current_token.token_type == "BOLD_ITALIC" :
				node.add(self.current_token)
			elif self.current_token.token_type == "LINK" :
				node.add(self.current_token)
			elif self.current_token.token_type == "CODE_INLINE" :
				node.add(self.current_token)
			else : return self.error("Token non reconnu")
			self.advance()
		return node


	""" list = unorderedlist | orderedlist ; """
	def markdown_list(self) : 
		node = Node(Rule.LIST)        
		if self.current_token.token_type == "LIST_ITEM": 
			node.add(self.unordereditem())
		elif self.current_token.token_type == "LIST_NUM": 
			node.add(self.ordereditem())
		else : self.error("Token non reconnu")
		return node


	""" ordereditem = digit, ".", " ", inline, newline, { indenteditem } ; """
	def ordereditem(self) : 
		node = Node(Rule.LIST_NUM)
		while self.current_token.token_type == "LIST_NUM":
			node.add(self.current_token)
			self.advance()
		return node


	""" unordereditem   = "*", " ", inline, newline, { indenteditem } ; """
	def unordereditem(self) :
		node = Node(Rule.LIST_ITEM)
		while self.current_token.token_type == "LIST_ITEM":
			node.add(self.current_token)
			self.advance()
		return node
