from Mkd_Interpreter import MkdToLatex_interpreter # notre interpréteur
from flask import Flask, request, jsonify
from flask_cors import CORS

# URL du FrontEnd React
lien = "http://localhost:5173"

# Création de l'application flask
app = Flask(__name__)

# Autorise le front-end (React) à faire des requêtes vers cette API
CORS(app, origins=[lien])


# Réception, traitement et renvoie du Markdown envoyé par le frontend : 
@app.route("/api/markdown", methods=["POST"])
def convert_markdown_to_latex():
    # Réception du texte saisi par l'utilisateur dans le frontend React.
    data = request.get_json()
    texte = data.get("texte", "")

    # Compilation du texte en markdown en latex.
    traducteur = MkdToLatex_interpreter()
    traducteur.compiler(texte)

    # Renvoie le texte compilé en Latex au frontend.
    return jsonify({
        "latex" : traducteur.latex_text,
    })


# à effacer pour une production 
if __name__ == "__main__":
    app.run(port=5000, debug=True)