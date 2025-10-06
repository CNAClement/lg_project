#!/bin/bash
set -e

echo "🚀 Installation des dépendances Python..."

# Mise à jour de pip
pip install --upgrade pip

# Installation des requirements si le fichier existe
if [ -f requirements.txt ]; then
    echo "📦 Installation des packages depuis requirements.txt..."
    pip install -r requirements.txt
    echo "✅ Installation terminée !"
else
    echo "⚠️  Fichier requirements.txt non trouvé"
fi

echo "🎉 Configuration terminée !"