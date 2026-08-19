#!/usr/bin/python3

from Mkd_Interpreter import MkdToLatex_interpreter
import argparse
import sys

"""
Nom ............................................... : Main.py
Role .............................................. : Le programme principale qui réunit toutes les composantes (lexeur, parseur, interpreteur), et permet une interaction avec l'utilisateur. 
Auteur ............................................ : PREMAKUMAR Samya
Version ........................................... : V1.5
Execution de l'interpréteur sans enregistrement ... : python3 Main.py
Execution de l'interpréteur avec enregistrement ... : python3 Main.py FileSave.tex
Execution du compileur ... : python3 Main.py -c FileCompile.md
Execution du compileur avec enregistrement... : python3 Main.py -c FileCompile.md FileSave.tex
Execution affichant les aides : python3 Main.py -h
"""

""" Renvoie le fichier sous forme d'un chaîne de caractère """
def open_file(file) :
	try :
		contenu = ""
		with open(file, 'r') as f :
			contenu += f.read()
		return contenu
	except FileNotFoundError :
		print(f"Erreur : Le fichier {file} n'existe pas.")
		sys.exit(1)
	except IOError as e :
		print(f"Erreur lors de la lecture du fichier : {e}")
		sys.exit(1)


""" Enregistre le résultat de la compilation ou interpréteur dans un fichier """
def save_file(result, file) :
	try : 
		with open(file, "w") as f : 
			f.write(result)
		print("Fin de sauvegarde dans le fichier") 
	except IOError as e :
		print(f"Erreur lors de l'enregistrement du fichier : {e}")
		sys.exit(1)



if __name__ == '__main__' :
	# Crée le parseur pour les arguments : 
	parser = argparse.ArgumentParser(description='Convertir des fichiers Markdown en LaTeX.')

	# Définition des arguments :
	parser.add_argument('input_file', nargs='?', default=None, help='Nom du fichier d’entrée à traduire (si aucun fichier n’est fourni, une entrée interactive est utilisée).')
	parser.add_argument('-c', '--compile', action='store_true', help='Compiler le fichier LaTeX après traduction.')
	parser.add_argument('output_file', nargs='?', default=None, help='Nom du fichier où enregistrer le résultat.')

	# Parse les arguments : 
	args = parser.parse_args()

	# Crée notre interpréteur pour traduire du markdown en latex : 
	traducteur = MkdToLatex_interpreter()

	# Si aucun argument n'est fourni, alors lance l'interpréteur + affiche le résultat à la fin : 
	if args.input_file is None and args.output_file is None and args.compile == False :
		traducteur.interpreter()
		print(traducteur.latex_text)

	# Si un argument (= input_file) est fourni, alors lance l'interpréteur, puis enregistre le résultat dans un fichier :
	elif args.input_file is not None and args.output_file is None and args.compile == False :
		traducteur.interpreter()
		save_file(traducteur.latex_text, args.input_file)
		print(traducteur.latex_text)

	# Si l'option "-c" est fourni ET un argument (= input_file), alors compile le fichier + affiche 
	elif args.input_file is not None and args.output_file is None and args.compile == True :
		traducteur.compiler(open_file(args.input_file))
		print(traducteur.latex_text)

	# Si l'option "-c" est fourni ET deux arguments : un fichier à traduire et un fichier à enregistrer, alors compile le fichier + enregistre + affiche :
	elif args.input_file is not None and args.output_file is not None and args.compile == True :
		traducteur.compiler(open_file(args.input_file))
		save_file(traducteur.latex_text, args.output_file)
		print(traducteur.latex_text)

	# Dans tous les autres cas, alors on affiche l'aide et quitte l'interpréteur :
	else : 
		parser.print_help()
		sys.exit(1)