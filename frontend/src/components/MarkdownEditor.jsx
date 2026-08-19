import React from 'react';
import ReactMarkdownEditorLite from 'react-markdown-editor-lite';
import MarkdownIt from 'markdown-it';
import 'react-markdown-editor-lite/lib/index.css';
import '../styles/MarkdownEditor.css';


// Composant permettant à l'utilisateur d'écrire et de modifier du texte au format Markdown.
const MarkdownEditor = ({ texte, onChange }) => {
  // Initialise le parseur Markdown
  const mdParser = new MarkdownIt();

  // le composant pour l'éditeur de markdwon
  return (
    <div className="markdown-editor">

      {/* Titre de l'éditeur */}
      <h2 className="editor-title">
        Éditeur de texte
      </h2>

      {/* Conteneur de l'éditeur */}
      <div className="markdown-editor-container">
        <ReactMarkdownEditorLite
          className="react-markdown-editor-lite" // pour personnaliser le style de l'éditeur dans css
          value={texte}
          onChange={onChange} 
          view={{
            menu: true, // la barre outil
            md: true, // la zone d'écriture
            html: false // d'écriture en html
          }}
          renderHTML={(text) => mdParser.render(text)}
          placeholder="Écrivez quelque chose..."
        />
      </div>

    </div>
  );
};

export default MarkdownEditor;