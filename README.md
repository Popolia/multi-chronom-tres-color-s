<p align="center">
  <img src="assets/logo.png" alt="Logo Multi-Chronomètres Colorés" width="160">
</p>

<h1 align="center">Multi-Chronomètres Colorés</h1>

<p align="center">
  <a href="https://github.com/Popolia/multi-chronom-tres-color-s/archive/refs/heads/main.zip">
    <img src="https://img.shields.io/badge/⬇️_T%C3%A9l%C3%A9charger-2ecc71?style=for-the-badge" alt="Télécharger">
  </a>
</p>

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
- **Thème sombre personnalisé** : interface et icône de fenêtre reprennent les couleurs du logo
<img width="822" height="572" alt="image" src="https://github.com/user-attachments/assets/caa54140-b71b-4c17-9a02-1e6c76026b71" />



## Utilisation

1. Double-clique sur `gestionnaire_lignes.exe`
2. Ajoute, renomme et personnalise tes lignes selon tes besoins
3. Démarre/mets en pause chaque chronomètre indépendamment
4. Ferme l'application : tout est sauvegardé automatiquement, tu retrouveras l'état exact à la prochaine ouverture

> ⚠️ Au premier lancement, Windows SmartScreen peut afficher un avertissement (l'exe n'étant pas signé numériquement). Clique sur **Informations complémentaires** puis **Exécuter quand même**.

## Structure des fichiers

```
multi-chronomètres-colorés/
├── assets/
│   ├── logo.png                # Logo (fenêtre + README)
│   ├── logo.ico                # Icône de l'exécutable Windows
│   └── logo.svg                # Source vectorielle du logo
├── gestionnaire_lignes.exe     # Application (à distribuer, avec assets/ à côté)
├── gestionnaire_lignes.py      # Code source
├── sauvegarde_lignes.json      # Généré automatiquement au 1er lancement
├── build.ps1                   # Script de compilation tout-en-un
└── README.md
```

> ⚠️ L'exécutable a besoin du dossier `assets/` juste à côté de lui (pour l'icône de fenêtre au runtime). Ne distribue jamais `gestionnaire_lignes.exe` seul — copie tout le dossier, ou au minimum l'exe + `assets/`.

## Développement

Le projet est écrit en **Python 3** avec **tkinter** (inclus par défaut, aucune dépendance externe pour l'exécution).

### Lancer depuis le code source

```bash
python gestionnaire_lignes.py
```

### Compiler en exécutable Windows autonome

**Méthode rapide — script tout-en-un**

```bash
python -m venv venv
venv\Scripts\activate
pip install pyinstaller
Unblock-File .\build.ps1    # si le fichier vient d'être téléchargé
.\build.ps1
```

`build.ps1` nettoie les anciens fichiers de build, compile avec l'icône, et recopie automatiquement `assets/` à côté de l'exe final dans `dist/`.

**Méthode manuelle**

```bash
python -m venv venv
venv\Scripts\activate
pip install pyinstaller
python -m PyInstaller --onefile --icon=assets\logo.ico gestionnaire_lignes.py
```

Avec cette méthode, pense à recréer `dist\assets\` et à y copier `logo.png` + `logo.ico` manuellement après la compilation.

L'exécutable final se trouve dans le dossier `dist/`.

> 💡 Si la compilation échoue avec une erreur de permission (`PermissionError` / `FileNotFoundError` sur le `.exe`), ajoute une exclusion pour le dossier du projet dans ton antivirus (Windows Defender : *Protection contre les virus et menaces > Gérer les paramètres > Exclusions*).

> 💡 Si PowerShell refuse d'exécuter `build.ps1` (*"n'est pas signé numériquement"*), débloque-le une fois avec `Unblock-File .\build.ps1`, et si besoin autorise les scripts locaux avec `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`.

## Licence

Projet personnel — usage libre.
