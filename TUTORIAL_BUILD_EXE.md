# 📘 Tutorial Pas à Pas : Générer le .exe

Ce guide vous accompagne étape par étape pour créer un fichier exécutable Windows (.exe) de votre application de dictée vocale.

## ⚠️ Pré-requis OBLIGATOIRES

Avant de commencer, vous DEVEZ avoir :
- ✅ Un ordinateur **Windows** (Windows 10 ou 11)
- ✅ Python 3.8 ou plus récent installé
- ✅ Une connexion Internet active

> **IMPORTANT** : On ne peut créer un .exe Windows QUE sur un ordinateur Windows !

---

## 📋 Étape 1 : Vérifier Python

**Action** : Ouvrez l'invite de commandes (CMD)
- Appuyez sur `Windows + R`
- Tapez `cmd`
- Appuyez sur `Entrée`

**Vérification** : Dans la fenêtre noire qui s'ouvre, tapez :
```bash
python --version
```

**Résultat attendu** : Vous devez voir quelque chose comme :
```
Python 3.11.5
```

> ❌ **Si vous voyez une erreur** : Python n'est pas installé. Téléchargez-le depuis https://www.python.org/downloads/

---

## 📋 Étape 2 : Naviguer vers le dossier du projet

**Action** : Dans la même fenêtre CMD, allez dans le dossier du projet.

**Exemple** : Si votre projet est dans `C:\Users\VotreNom\Documents\push-to-talk-whiserai`, tapez :
```bash
cd C:\Users\VotreNom\Documents\push-to-talk-whiserai
```

**Vérification** : Tapez `dir` et appuyez sur Entrée. Vous devez voir la liste des fichiers incluant :
- `live_dictation_app.py`
- `build_exe.py`
- `requirements.txt`

---

## 📋 Étape 3 : Installer les dépendances

**Action** : Installez toutes les bibliothèques nécessaires.

**Commande 1** : Installer les dépendances de l'application
```bash
pip install -r requirements.txt
```

**Attendez...** : Cela peut prendre 2-5 minutes. Vous verrez défiler du texte.

**Commande 2** : Installer PyInstaller (l'outil qui crée le .exe)
```bash
pip install pyinstaller
```

**Résultat attendu** : Le dernier message doit être similaire à :
```
Successfully installed pyinstaller-X.X.X
```

---

## 📋 Étape 4 : Lancer la génération du .exe

**Action** : Lancez le script de build automatique.

**Commande** :
```bash
python build_exe.py
```

**Ce qui va se passer** :
1. Vous verrez beaucoup de texte défiler (c'est normal !)
2. PyInstaller va analyser tous les fichiers
3. Il va créer un dossier `build` (temporaire)
4. Il va créer un dossier `dist` (votre .exe final sera là)
5. Cela prend environ **2-10 minutes** selon votre ordinateur

**Résultat attendu** : À la fin, vous verrez :
```
========================================================
Build complete!
Your .exe file is in the 'dist' folder:
  → dist/SpeechToText.exe
========================================================
```

---

## 📋 Étape 5 : Trouver votre .exe

**Action** : Naviguez dans l'explorateur Windows vers votre dossier de projet.

**Chemin** : Ouvrez le dossier `dist` qui a été créé.

**Résultat** : Vous devez voir un fichier nommé **`SpeechToText.exe`**

**Taille attendue** : Entre 20 MB et 35 MB (c'est normal, il contient Python et toutes les bibliothèques !)

---

## 📋 Étape 6 : Tester le .exe

**Action** : Testez que votre application fonctionne.

**Double-cliquez** sur `SpeechToText.exe`

**Résultat attendu** :
- ✅ Une fenêtre s'ouvre avec l'interface de l'application
- ✅ Vous pouvez entrer votre clé API
- ✅ Vous pouvez sélectionner votre microphone
- ✅ Le push-to-talk fonctionne

> ⚠️ **Windows Defender peut bloquer** : Si Windows affiche un avertissement, cliquez sur "Plus d'infos" puis "Exécuter quand même". C'est normal pour les .exe non signés.

---

## 📋 Étape 7 : Distribuer votre .exe

**Action** : Partagez votre application.

**Ce qu'il faut distribuer** :
- ✅ **Seulement** le fichier `dist/SpeechToText.exe`
- ✅ C'est tout ! Un seul fichier suffit.

**Instructions pour l'utilisateur final** :
1. Copiez `SpeechToText.exe` sur n'importe quel PC Windows
2. Double-cliquez sur le fichier
3. Entrez votre clé API OpenAI
4. Commencez à dicter !

**Fichiers créés automatiquement** :
- `api_key.txt` : Stocke la clé API (créé au premier lancement)
- `microphone.txt` : Mémorise le micro sélectionné (créé au premier lancement)

---

## 🎯 Option Alternative : Build Optimisé

Si vous voulez un démarrage plus rapide (mais plusieurs fichiers à distribuer) :

**Commande** :
```bash
python build_exe_optimized.py
```

**Résultat** :
- Dossier `dist/SpeechToText/` contenant plusieurs fichiers
- Exécutable : `dist/SpeechToText/SpeechToText.exe`
- **Plus rapide** au démarrage
- **Plus petit** en taille
- **Mais** vous devez distribuer TOUT le dossier `SpeechToText/`

---

## 🛠️ Résolution de Problèmes

### ❌ Erreur : "No module named 'PyInstaller'"

**Solution** :
```bash
pip install pyinstaller
```

### ❌ Erreur : "Module not found" dans le .exe

**Diagnostic** : Une bibliothèque n'a pas été incluse dans le build.

**Solution** : Ouvrez `build_exe.py` avec un éditeur de texte et ajoutez la ligne :
```python
'--hidden-import=nom_du_module',
```
dans la liste des arguments de PyInstaller, puis relancez le build.

### ❌ Le .exe est trop gros (>50 MB)

**Solution** : Créez un environnement virtuel propre :
```bash
# Créer un environnement virtuel
python -m venv venv_clean

# Activer l'environnement
venv_clean\Scripts\activate

# Installer uniquement ce qui est nécessaire
pip install -r requirements.txt
pip install pyinstaller

# Build
python build_exe.py

# Désactiver l'environnement
deactivate
```

### ❌ Windows Defender bloque le .exe

**C'est normal !** Les .exe non signés sont souvent bloqués.

**Pour tester** :
1. Clic droit sur le fichier
2. "Plus d'infos"
3. "Exécuter quand même"

**Pour distribuer** :
- Option 1 : Ajoutez une exclusion dans Windows Defender
- Option 2 : Signez le .exe avec un certificat de signature de code (coûteux, pour usage professionnel)

### ❌ L'application ne démarre pas (aucune fenêtre)

**Solution de diagnostic** : Créez une version avec console pour voir les erreurs.

**Modifiez `build_exe.py`** : Changez `--windowed` en `--console` :
```python
'--console',  # Au lieu de --windowed
```

Relancez le build. Maintenant le .exe ouvrira une console qui affichera les erreurs.

---

## ✅ Checklist Finale

Avant de distribuer, vérifiez :

- [ ] Le .exe s'ouvre sans erreur
- [ ] Vous pouvez entrer une clé API et elle se sauvegarde
- [ ] Vous pouvez sélectionner un microphone et il se mémorise
- [ ] Le mode Push-to-Talk fonctionne (plusieurs fois de suite)
- [ ] Le mode Live fonctionne avec feedback rouge/vert
- [ ] La transcription s'insère dans Notepad/Word
- [ ] Les deux langues (FR/EN) fonctionnent
- [ ] La ponctuation française fonctionne (espaces avant ? ! :)
- [ ] Le coût API s'affiche correctement

---

## 📊 Temps Estimés

| Étape | Durée |
|-------|-------|
| Installer Python | 5-10 min |
| Installer dépendances | 3-5 min |
| Build .exe | 2-10 min |
| Test | 2-3 min |
| **TOTAL** | **12-28 minutes** |

---

## 💡 Conseils

✅ **Faites un build propre** : Si vous modifiez le code, refaites un build complet :
```bash
python build_exe.py
```

✅ **Testez sur plusieurs PC** : Testez le .exe sur un autre PC Windows pour vérifier qu'il fonctionne vraiment en standalone.

✅ **Gardez les sources** : Ne distribuez JAMAIS vos fichiers `.py` avec le .exe. Le .exe est autonome !

✅ **Versioning** : Renommez votre .exe avec un numéro de version : `SpeechToText_v1.0.exe`

---

## 🎉 Félicitations !

Vous avez créé votre premier exécutable Windows ! Votre application de dictée vocale est maintenant prête à être distribuée à n'importe quel utilisateur Windows, même sans Python installé.

**Prochaine étape** : Consultez `TUTORIAL_UPDATE_APP.md` pour apprendre à mettre à jour l'application facilement.
