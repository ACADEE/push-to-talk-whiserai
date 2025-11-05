# 📘 Tutorial Pas à Pas : Mettre à Jour l'Application

Ce guide vous accompagne étape par étape pour installer les dernières mises à jour de l'application de dictée vocale.

---

## 🎯 Trois Méthodes de Mise à Jour

Choisissez la méthode qui correspond à votre situation :

| Méthode | Quand l'utiliser | Avantages |
|---------|------------------|-----------|
| **A - Mise à jour du .exe** | Vous utilisez déjà le .exe | Rapide, simple |
| **B - Mise à jour du code Python** | Vous lancez via Python | Garde vos paramètres |
| **C - Installation propre** | Problèmes persistants | Réinitialisation complète |

---

## 📋 Méthode A : Mise à Jour du .exe (Recommandé)

**Pour qui ?** Vous avez déjà un `SpeechToText.exe` et voulez la nouvelle version.

### Étape A1 : Sauvegarder vos paramètres

**Action** : Trouvez où est votre .exe actuel.

**Fichiers à sauvegarder** (dans le même dossier que le .exe) :
- `api_key.txt` (votre clé API OpenAI)
- `microphone.txt` (votre micro préféré)

**Copie de sauvegarde** :
1. Créez un dossier temporaire sur le Bureau : `Sauvegarde_Dictation`
2. Copiez-y les 2 fichiers ci-dessus

> ⚠️ **IMPORTANT** : Si vous ne trouvez pas ces fichiers, c'est que vous n'avez jamais lancé l'ancienne version. Passez directement à l'étape A2.

---

### Étape A2 : Télécharger la nouvelle version

**Option 1 : Vous avez accès au dossier source**
1. Ouvrez l'invite de commandes (CMD)
2. Naviguez vers le dossier du projet :
   ```bash
   cd C:\Users\VotreNom\Documents\push-to-talk-whiserai
   ```
3. Téléchargez les dernières modifications :
   ```bash
   git pull origin claude/windows-spelling-practice-app-011CUpdgMUU9oSmXbafDWaoE
   ```
4. Régénérez le .exe :
   ```bash
   python build_exe.py
   ```
5. Votre nouveau .exe est dans `dist/SpeechToText.exe`

**Option 2 : Vous recevez le .exe directement**
- Copiez le nouveau `SpeechToText.exe` fourni

---

### Étape A3 : Installer le nouveau .exe

**Action** : Remplacez l'ancien .exe par le nouveau.

**Instructions** :
1. Supprimez (ou renommez) l'ancien `SpeechToText.exe`
2. Copiez le nouveau `SpeechToText.exe` au même endroit
3. Copiez vos fichiers sauvegardés (`api_key.txt` et `microphone.txt`) dans le même dossier que le nouveau .exe

---

### Étape A4 : Tester

**Action** : Lancez le nouveau .exe.

**Vérifications** :
- ✅ La fenêtre s'ouvre normalement
- ✅ Votre clé API est déjà remplie (si vous avez copié `api_key.txt`)
- ✅ Votre micro est déjà sélectionné (si vous avez copié `microphone.txt`)
- ✅ Le **status apparaît EN HAUT** de la fenêtre (nouvelle fonctionnalité !)
- ✅ Push-to-Talk fonctionne plusieurs fois de suite (bug corrigé !)
- ✅ Live Mode affiche rouge/vert selon l'activité vocale (nouveau !)

---

## 📋 Méthode B : Mise à Jour du Code Python

**Pour qui ?** Vous lancez l'application avec `python live_dictation_app.py`.

### Étape B1 : Sauvegarder vos paramètres

**Même principe que Méthode A1** : Sauvegardez `api_key.txt` et `microphone.txt` s'ils existent.

---

### Étape B2 : Mettre à jour le code

**Action** : Téléchargez les dernières modifications depuis Git.

**Commandes** :
```bash
# Naviguez vers le dossier du projet
cd C:\Users\VotreNom\Documents\push-to-talk-whiserai

# Vérifiez qu'il n'y a pas de modifications locales non sauvegardées
git status

# Téléchargez les dernières mises à jour
git pull origin claude/windows-spelling-practice-app-011CUpdgMUU9oSmXbafDWaoE
```

**Résultat attendu** :
```
Updating 01eb84e..cd67a26
Fast-forward
 live_dictation_app.py | 84 +++++++++++++++++++++++++++++-----------
 1 file changed, 43 insertions(+), 41 deletions(-)
```

---

### Étape B3 : Mettre à jour les dépendances

**Action** : Vérifiez que toutes les bibliothèques sont à jour.

**Commande** :
```bash
pip install -r requirements.txt --upgrade
```

**Temps** : 1-2 minutes

---

### Étape B4 : Restaurer vos paramètres

**Action** : Remettez vos fichiers sauvegardés.

**Instructions** :
- Copiez `api_key.txt` et `microphone.txt` de votre sauvegarde vers le dossier du projet

---

### Étape B5 : Tester

**Action** : Lancez l'application mise à jour.

**Commande** :
```bash
python live_dictation_app.py
```

**Vérifications** : Mêmes que Méthode A4

---

## 📋 Méthode C : Installation Propre (Réinitialisation)

**Pour qui ?** Vous avez des problèmes et voulez tout réinstaller de zéro.

### Étape C1 : Sauvegarder SEULEMENT les paramètres

**Action** : Sauvegardez UNIQUEMENT `api_key.txt` et `microphone.txt`.

**Ne sauvegardez PAS** :
- Les fichiers `.py` (vous allez télécharger les nouveaux)
- Le dossier `build/` (peut être supprimé)
- Le dossier `dist/` (peut être supprimé)
- Les fichiers `__pycache__/` (peut être supprimé)

---

### Étape C2 : Supprimer l'ancienne installation

**Action** : Supprimez le dossier du projet entier.

**Exemple** :
- Supprimez le dossier `C:\Users\VotreNom\Documents\push-to-talk-whiserai`

---

### Étape C3 : Cloner le projet à nouveau

**Action** : Téléchargez une copie fraîche du projet.

**Commandes** :
```bash
# Naviguez où vous voulez installer
cd C:\Users\VotreNom\Documents

# Clonez le repository
git clone [URL_DU_REPOSITORY] push-to-talk-whiserai

# Entrez dans le dossier
cd push-to-talk-whiserai

# Basculez sur la bonne branche
git checkout claude/windows-spelling-practice-app-011CUpdgMUU9oSmXbafDWaoE
```

---

### Étape C4 : Installer les dépendances

**Action** : Installez toutes les bibliothèques nécessaires.

**Commandes** :
```bash
pip install -r requirements.txt
pip install pyinstaller
```

---

### Étape C5 : Restaurer vos paramètres

**Action** : Copiez vos fichiers sauvegardés (`api_key.txt` et `microphone.txt`) dans le nouveau dossier du projet.

---

### Étape C6 : Générer le .exe (optionnel)

**Si vous voulez un .exe** :
```bash
python build_exe.py
```

**Si vous utilisez Python directement** :
```bash
python live_dictation_app.py
```

---

## 🔍 Vérifier Votre Version

**Comment savoir quelle version vous avez ?**

**Méthode 1 : Vérifier Git**
```bash
cd C:\Users\VotreNom\Documents\push-to-talk-whiserai
git log --oneline -5
```

Vous devez voir en premier :
```
cd67a26 Fix push-to-talk second press bug and move status to top
```

**Méthode 2 : Vérifier visuellement**
- Lancez l'application
- Le **Status** doit être EN HAUT de la fenêtre
- Push-to-Talk doit fonctionner plusieurs fois de suite
- Live Mode doit afficher rouge (parole détectée) et vert (silence)

---

## 📦 Nouvelles Fonctionnalités (Dernière Mise à Jour)

Cette mise à jour apporte :

### 🐛 Corrections de Bugs

1. **Push-to-Talk fonctionne maintenant plusieurs fois de suite**
   - Avant : Marchait la 1ère fois, bloqué à la 2ème
   - Maintenant : Fonctionne indéfiniment

2. **API Key visible en haut**
   - Avant : Section API Key disparaissait
   - Maintenant : Toujours visible en haut

3. **Gestion des erreurs améliorée**
   - Avant : Erreurs silencieuses
   - Maintenant : Messages d'erreur visibles dans le status

### ✨ Améliorations UI

1. **Status en haut de la fenêtre**
   - Plus visible, avec police plus grande
   - Affichage immédiat de l'état de l'application

2. **Live Mode : Feedback visuel rouge/vert**
   - 🟢 Vert : Silence détecté, pas d'appel API (économie !)
   - 🔴 Rouge : Parole détectée, appel API en cours (coût)

3. **Organisation des sections améliorée**
   - Ordre logique : Status → API Key → Cost → Price → Mode → Prompt → Mic → Lang → Hotkey → Level
   - Plus de chevauchements de sections

### 🇫🇷 Ponctuation Française

- Espaces automatiques avant : `;` `:` `?` `!`
- Guillemets français : `« texte »` au lieu de `"texte"`
- Pas de virgule avant "et"

---

## 🛠️ Résolution de Problèmes

### ❌ Erreur : "Your local changes would be overwritten"

**Cause** : Vous avez modifié des fichiers localement.

**Solution** :
```bash
# Voir quels fichiers sont modifiés
git status

# Option 1 : Sauvegarder vos modifications
git stash

# Télécharger les mises à jour
git pull origin claude/windows-spelling-practice-app-011CUpdgMUU9oSmXbafDWaoE

# Option 2 : Abandonner vos modifications (⚠️ attention !)
git reset --hard HEAD
git pull origin claude/windows-spelling-practice-app-011CUpdgMUU9oSmXbafDWaoE
```

### ❌ Mes paramètres API/micro ont disparu

**Cause** : Vous n'avez pas sauvegardé `api_key.txt` et `microphone.txt`.

**Solution** :
1. Relancez l'application
2. Entrez à nouveau votre clé API
3. Sélectionnez à nouveau votre microphone
4. Les fichiers seront recréés automatiquement

### ❌ Le nouveau .exe ne démarre pas

**Solution** : Créez une version avec console pour voir l'erreur.

**Dans `build_exe.py`**, changez :
```python
'--windowed',  # Remplacez par :
'--console',
```

Relancez le build et exécutez le .exe. Vous verrez les erreurs dans la console.

### ❌ "Module not found" après la mise à jour

**Cause** : Nouvelles dépendances ajoutées.

**Solution** :
```bash
pip install -r requirements.txt --upgrade
```

---

## ✅ Checklist Post-Mise à Jour

Vérifiez que tout fonctionne :

- [ ] L'application démarre sans erreur
- [ ] Le status est EN HAUT de la fenêtre (nouvelle feature)
- [ ] API Key visible et sauvegardée
- [ ] Micro sélectionné et mémorisé
- [ ] Push-to-Talk fonctionne 5+ fois de suite (bug corrigé)
- [ ] Live Mode affiche rouge (parole) et vert (silence)
- [ ] La transcription s'insère dans Word/Notepad
- [ ] Langue française avec ponctuation correcte (espaces avant ? !)
- [ ] Coût API s'affiche en temps réel

---

## 📊 Temps de Mise à Jour Estimés

| Méthode | Durée |
|---------|-------|
| **A - Mise à jour .exe** | 5-15 min |
| **B - Mise à jour Python** | 3-5 min |
| **C - Installation propre** | 15-25 min |

---

## 💡 Conseils pour les Mises à Jour Futures

✅ **Sauvegardez toujours** `api_key.txt` et `microphone.txt` avant toute mise à jour

✅ **Testez avant de distribuer** : Si vous distribuez le .exe, testez-le sur votre PC avant de l'envoyer

✅ **Lisez les notes de version** : Vérifiez `git log` pour voir les changements

✅ **Gardez un backup** : Gardez l'ancien .exe dans un dossier "Old_Versions" au cas où

✅ **Mettez à jour régulièrement** : Exécutez `git pull` une fois par semaine pour avoir les dernières corrections

---

## 🎉 Mise à Jour Terminée !

Votre application est maintenant à jour avec toutes les dernières corrections et fonctionnalités.

**Questions fréquentes** :

**Q : Dois-je redistribuer le .exe à tous mes utilisateurs ?**
R : Oui, si vous avez des utilisateurs qui utilisent le .exe. Envoyez-leur la nouvelle version.

**Q : La mise à jour va-t-elle supprimer mes enregistrements ou paramètres ?**
R : Non, tant que vous sauvegardez `api_key.txt` et `microphone.txt`, tous vos paramètres sont préservés.

**Q : À quelle fréquence dois-je mettre à jour ?**
R : Vérifiez une fois par semaine, ou quand vous rencontrez un bug qui pourrait avoir été corrigé.

---

**Prochaine étape** : Consultez `TUTORIAL_BUILD_EXE.md` si vous voulez recréer le .exe avec les dernières modifications.
