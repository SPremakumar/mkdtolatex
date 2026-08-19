import React from 'react';
import '../styles/LivePreview.css';

const LivePreview = ({ texte }) => {

  // Composant pour la prévisualisation de latex 
  return (
    <div className="live-preview">
      <h2 className="preview-title">Prévisualisation</h2>
      {/* la zone pour afficher la sortie de latex (le style est définit dans css.*/}
      <div className="preview-content">
        {texte || 'Aucun texte à afficher...'}
      </div>
    </div>
  );
};

export default LivePreview;