// URL de l'API flask
const API_URL = '/api';

// gère les communication avec le backend
export const sendMarkdown = async (texte) => {
  
  try {
  
    // Vérification du contenu
    if (typeof texte !== 'string') {
      throw new Error('Le texte envoyé doit être une chaîne de caractères.');
    }

    // envoie le texte markdwon à l'api Flask /api/markdown
    const response = await fetch(`${API_URL}/markdown`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        texte,
      }),
    });

    // Si une Erreur HTTP ALORS affiche un message d'erreur 
    if (!response.ok) {
      let message = `Erreur HTTP ${response.status}`;

      // essaie de récuperer le msg d'erreur par le flask
      try {
        const errorData = await response.json();
        if (errorData.message) { message = errorData.message; }
      } catch {
        // La réponse n'est pas du JSON
      }
      throw new Error(message);
    }

    // Récupère et convertit la réponse JSON de Flask.
    const data = await response.json();

    // Vérifie que le serveur a bien retourné des données.
    if (!data) {
      throw new Error('Le serveur a retourné une réponse vide.');
    }

    // retourne les données (dans app.jsx)
    return data;

  // gestion des erreurs avec le serveur flask
  } catch (error) {

    // Serveur inaccessible / problème réseau
    if (error instanceof TypeError) {
      console.error('Impossible de contacter le serveur Flask.');
      throw new Error(
        'Le serveur Flask est inaccessible. Vérifiez qu’il est démarré.'
      );
    }

    console.error('Erreur lors de la communication avec Flask :', error);

    throw error;
  }
};