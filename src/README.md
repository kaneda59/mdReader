# Markdown Viewer

Une application de bureau légère écrite en Python et PyQt6 permettant de visionner des fichiers Markdown avec la possibilité de basculer entre le mode rendu graphique et le mode code source.

## Fonctionnalités

- **Mode Vue / Code :** Bascule instantanée via le bouton `<-> Code`.
- **Copie rapide :** Bouton pour copier l'intégralité du contenu dans le presse-papiers.
- **Impression :** Impression native du rendu HTML ou du code source.
- **Multiplateforme :** Fonctionne sous Windows, Linux et macOS.

## Installation en développement

1. Créer un environnement virtuel et l'activer :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Linux/macOS
   .\venv\Scripts\activate   # Sur Windows