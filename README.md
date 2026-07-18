# Multi-Chronomètres Colorés

[![Télécharger](https://img.shields.io/badge/⬇️_T%C3%A9l%C3%A9charger-2ecc71?style=for-the-badge)](https://github.com/Popolia/multi-chronom-tres-color-s/archive/refs/heads/main.zip)

Application de bureau (Windows) pour gérer plusieurs lignes indépendantes, chacune avec sa propre couleur, un compteur et un chronomètre. Pensée pour suivre plusieurs opérations, postes ou tâches en parallèle.

## Fonctionnalités

- **Lignes illimitées** : ajoute autant de lignes que nécessaire via le bouton `+ Ajouter une ligne`
- **Couleur personnalisable** : clique sur la pastille de couleur pour la changer
- **Nom personnalisable** : double-clic sur le nom de la ligne pour le renommer
- **Compteur** : boutons `+` / `-` pour incrémenter/décrémenter
- **Chronomètre indépendant par ligne** : un seul bouton Démarrer/Pause
- **Reset avec confirmation** : remet le chrono et le compteur à zéro, après demande de confirmation pour éviter les erreurs
- **Suppression de ligne** (`✕`), avec confirmation
- **Sauvegarde automatique** : toutes les données (noms, couleurs, compteurs, temps) sont enregistrées dans `sauvegarde_lignes.json`, à côté de l'exécutable, et rechargées automatiquement au démarrage
- **Console masquée** : aucune fenêtre noire ne s'affiche au lancement

## Utilisation

1. Double-clique sur `gestionnaire_lignes.exe`
2. Ajoute, renomme et personnalise tes lignes selon tes besoins
3. Démarre/mets en pause chaque chronomètre indépendamment
4. Ferme l'application : tout est sauvegardé automatiquement, tu retrouveras l'état exact à la prochaine ouverture

> ⚠️ Au premier lancement, Windows SmartScreen peut afficher un avertissement (l'exe n'étant pas signé numériquement). Clique sur **Informations complémentaires** puis **Exécuter quand même**.

## Structure des fichiers

```
multi-chronomètres-colorés/
├── gestionnaire_lignes.exe     # Application (à distribuer)
├── sauvegarde_lignes.json      # Généré automatiquement au 1er lancement
├── gestionnaire_lignes.py      # Code source
└── README.md
```

## Développement

Le projet est écrit en **Python 3** avec **tkinter** (inclus par défaut, aucune dépendance externe pour l'exécution).

### Lancer depuis le code source

```bash
python gestionnaire_lignes.py
```

### Compiler en exécutable Windows autonome

```bash
python -m venv venv
venv\Scripts\activate
pip install pyinstaller
python -m PyInstaller --onefile gestionnaire_lignes.py
```

L'exécutable final se trouve dans le dossier `dist/`.

> 💡 Si la compilation échoue avec une erreur de permission (`PermissionError` / `FileNotFoundError` sur le `.exe`), ajoute une exclusion pour le dossier du projet dans ton antivirus (Windows Defender : *Protection contre les virus et menaces > Gérer les paramètres > Exclusions*).

## Licence

Projet personnel — usage libre.
