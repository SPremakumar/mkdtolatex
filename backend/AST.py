#!/usr/bin/python3

from Token import Token

class Node : 
	""" Notre arbre AST contient un noeud principal représentant
	les règles (block, inline, ...), et, des branches pour les 
	définitions représentées sous la forme d'une liste (contenant
	d'autres règles, eux-même contenant d'autre ou non) ou non. """
	def __init__(self, valeur, branches=None) : 
		self.valeur = valeur
		self.branches = branches or []

	""" affiche l'arbre en entier """
	def __repr__(self, level=0) : 
		ret = "-" * level + repr(self.valeur) + "\n"
		for item in self.branches :
			if isinstance(item, Node):
				ret += item.__repr__(level + 1)
			elif isinstance(item, Token):
				ret += "-" * (level + 1) + repr(item) + "\n"
		return ret

	""" accède à l'arbre de la même manière d'une liste """
	def __getitem__(self, index) :
		return self.branches[index]

	""" renvoie le nombre de branches dans l'arbre AST """
	def __len__(self) : 
		return len(self.branches)

	""" ajoute des noeuds (qui peuvent être des tokens 
	ou des rules) dans l'arbre """
	def add(self, noeud) :
		# Si c'est un Node
		if isinstance(noeud, Node) : 
			return self.branches.append(noeud)
		
		# Si c'est un token 
		elif isinstance(noeud, Token):
			return self.branches.append(Token(noeud.token_type, noeud.token_value, noeud.coord[0], noeud.coord[1]))
		
		# Les autres cas : (par sécurité ou éviter des erreurs)
		else :
			return self.branches.append(Node(noeud))
