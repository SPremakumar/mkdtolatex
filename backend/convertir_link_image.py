#!/usr/bin/python3

import requests
import base64
import tempfile
import os
from PIL import Image 

"""
Nom ......... : convertir_link_image.py
Role ........ : convertir un lien en une image (png)
Auteur ...... : PREMAKUMAR Samya
Version ..... : V1.1 
"""

class convert_link_to_image : 
	""" le constructeur est composé d'un lien, 
	deux chaines : nom du fichier + code binaire """
	def __init__(self, url) :
		self.url = url
		self.image_name = ""
		self.image_code = b""


	""" convertir un lien en image (jpg) """
	def convert_link_image(self) : 
		# accède au lien + enregistre le contenu (l'image) dans image.code : 
		response = requests.get(self.url)
		self.image_code = response.content

		# convertir l'image à partir du lien en base 64 : 
		encoded_image = base64.b64encode(self.image_code).decode('utf-8')

		# convertir l'image encodée en base64 en une image : 
		self.image_code = base64.b64decode(encoded_image)

		# créer un fichier temporaire :
		with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
			temp_file.write(self.image_code)
			self.image_name = temp_file.name

		return self.image_name

	   

	""" supprime l'image temporaire générée """
	def delete_image_temp(self) :
		if self.image_name and os.path.isfile(self.image_name):
			os.remove(self.image_name)
			print(f"Fichier temporaire supprimé : {self.image_name}")
			self.image_name = ""
		else:
			print("Aucun fichier temporaire à supprimer ou le fichier n'existe pas.")



	
	""" renvoie une valeur boolean selon si une image est valide (ouvrable ou non) """
	def is_valid_image(self) : 
		try:
			with Image.open(self.image_name) as img:
				img.load()
			return True
		except (IOError, SyntaxError) as e:
			print(f"Erreur : {e}") # pour le DÉBUG.
			return False
