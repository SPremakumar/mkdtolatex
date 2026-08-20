import sys
import os
import threading
import time
import webbrowser
from werkzeug.serving import make_server


# Chemin vers le dossier backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

sys.path.insert(0, BACKEND_DIR)

# Import de l'application Flask
from app import app

# Ouverture automatique du navigateur
def ouvrir_navigateur():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")

# Lancement
if __name__ == "__main__":
    # Création du serveur Flask/Werkzeug
    server = make_server("127.0.0.1",5000,app)

    # Permet à app.py d'accéder à server.shutdown()
    app.config["SHUTDOWN_SERVER"] = server.shutdown

    # Ouverture automatique du navigateur
    threading.Thread(target=ouvrir_navigateur,daemon=True).start()

    # Démarrage du serveur
    server.serve_forever()