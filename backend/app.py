from Mkd_Interpreter import MkdToLatex_interpreter # notre interpréteur
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os 
import sys
import threading


# Chemins du frontend React
if getattr(sys, "frozen", False):
    # Application lancée depuis l'exécutable PyInstaller
    BASE_DIR = sys._MEIPASS
else:
    # Application lancée normalement avec Python
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend", "dist")



# Création de l'application flask
app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)

CORS(app, origins=["http://localhost:5173"])


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

# Quitter l'application
@app.route("/api/shutdown", methods=["POST"])
def shutdown():
    shutdown_func = app.config.get("SHUTDOWN_SERVER")

    if shutdown_func is None:
        return jsonify({
            "message": "Impossible d'arrêter le serveur."
        }), 500

    # Arrêter le serveur après avoir envoyé la réponse
    threading.Timer(0.2, shutdown_func).start()

    return jsonify({
        "message": "Application arrêtée."
    })

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    file_path = os.path.join(app.static_folder, path)

    if path and os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)

    return send_from_directory(app.static_folder, "index.html")



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
