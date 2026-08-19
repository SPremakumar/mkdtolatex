import { useState, useEffect } from 'react';
import { sendMarkdown } from './components/BackendConnection';
import MarkdownEditor from './components/MarkdownEditor';
import LivePreview from './components/LivePreview';
import Menu from './components/Menu';
import './App.css';


function App() {
  const [texte, setTexte] = useState(''); // le texte saisi par l'utilisateur
  const [latex, setLatex] = useState(''); // la sortie renvoyée par flask de python
  const [darkMode, setDarkMode] = useState(false); // option activée par l'utilisée (à partir du menu)

  // récupere et enregistre texte dans texte.
  const handleChange = ({ text }) => { setTexte(text); }; // remet à jour

  // envoie le texte (converti en mkd) au flask
  useEffect(() => {
    // attendre 500 ms avant d'exécuter la conversion. 
    const timer = setTimeout(async () => {
      try {
        // envoie text Markdown au flask
        const data = await sendMarkdown(texte);

        // Récupération du LaTeX envoyé par Flask et remet à jour Latex
        setLatex(data.latex);

      // gestion des erreurs
      } catch (error) {
        console.error(error); // todebug : affiche l'erreur 
      }
    }, 500);

    // Annule le timer précédent si le texte est modifié avant la fin des 500 ms.
    return () => clearTimeout(timer);
  }, [texte]);


  // le composant principale contenant editeur de markdown et latex, et le menu.
  return (
    <div className={`editor-page ${darkMode ? 'dark-mode' : ''}`}>

      <Menu
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        texte={texte}
        setTexte={setTexte}
        latex={latex}
        setLatex={setLatex}
      />

      <h1 className="main-title">
        Éditeur de Markdown en LaTeX
      </h1>

      <div className="editor-layout">

        <div className="editor-panel">
          <MarkdownEditor
            texte={texte}
            onChange={handleChange}
          />
        </div>

        <div className="preview-panel">
          <LivePreview texte={latex} />
        </div>

      </div>
    </div>
  );
}

export default App;