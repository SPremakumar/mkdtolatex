import React, { useState, useRef } from 'react';
import '../styles/Menu.css';

const Menu = ({darkMode,setDarkMode,texte,setTexte,latex, setLatex}) => {
  const [isOpen, setIsOpen] = useState(false);

  // Référence vers le sélecteur de fichier
  const fileInputRef = useRef(null);

  // Fermer le menu
  const closeMenu = () => { setIsOpen(false); };

  // Créer un nouveau document
  const handleNewDocument = () => {
    setTexte('');
    setLatex('');
    closeMenu();
  };

  // Ouvrir l'explorateur de fichiers
  const handleImport = () => {
    fileInputRef.current.click();
    closeMenu();
  };

  // Lire le fichier Markdown sélectionné
  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    // Vérifier que le fichier est bien un fichier Markdown
    if (!file.name.endsWith('.md') && !file.name.endsWith('.markdown')) {
      alert('Veuillez sélectionner un fichier Markdown (.md).');
      return;
    }

    const reader = new FileReader();

    reader.onload = (event) => {
      // Met le contenu du fichier directement dans l'éditeur
      setTexte(event.target.result);
    };

    reader.onerror = () => {
      console.error('Erreur lors de la lecture du fichier.');
    };

    reader.readAsText(file);

    // Permet de sélectionner à nouveau le même fichier
    event.target.value = '';
  };

  // Télécharger le document Markdown
  // Télécharger le document LaTeX généré
  const handleDownload = () => {
    if (!latex) {
      alert('Aucun code LaTeX à télécharger.');
      return;
    }

    const blob = new Blob([latex], {
      type: 'text/plain;charset=utf-8'
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = 'document.tex';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);

    closeMenu();
};

  // Changer le mode clair / sombre
  const handleDarkMode = () => {
    setDarkMode(!darkMode);
    closeMenu();
  };

  return (
    <div className="menu-container">

      <button
        className="menu-button"
        onClick={() => setIsOpen(!isOpen)}
      >
        ☰
      </button>

      {isOpen && (
        <div className={`menu-dropdown ${darkMode ? 'dark-menu' : ''}`}>

          <button onClick={handleImport}>
            📂 Importer
          </button>

          <button onClick={handleDownload}>
            💾 Télécharger
          </button>

          <button onClick={handleDarkMode}>
            {darkMode ? '☀️ Mode clair' : '🌙 Mode sombre'}
          </button>

          {/* Nouveau document */}
          <button onClick={handleNewDocument}>
            📄 Nouveau document
          </button>


        </div>
      )}

      {/* Sélecteur de fichier caché */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".md,.markdown"
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />

    </div>
  );
};

export default Menu;