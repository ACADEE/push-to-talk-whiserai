# 🏗️ Guide de Build - Speech-to-Text App

## Pré-requis

- **Windows 10/11** (obligatoire pour créer un .exe Windows)
- **Python 3.8+** installé
- **Connexion Internet** (pour télécharger les dépendances)

## 🚀 Build Rapide (Recommandé)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt
pip install pyinstaller

# 2. Lancer le build
python build_exe.py

# 3. Votre .exe est prêt !
# → dist/SpeechToText.exe
```

## 📦 Résultat

Après le build, vous obtenez :
- **`dist/SpeechToText.exe`** : Application standalone (15-30 MB)
- Aucune autre dépendance nécessaire
- Fonctionne sur n'importe quel PC Windows

## 🎯 Distribution

### Distribuer à vos utilisateurs :

1. **Donnez uniquement** : `SpeechToText.exe`
2. **L'utilisateur** :
   - Double-clique sur le .exe
   - Entre sa clé API OpenAI
   - Commence à dicter !

### Fichiers créés automatiquement :
- `api_key.txt` : Stocke la clé API
- `microphone.txt` : Mémorise le micro sélectionné

## 🛠️ Options de Build

### Build Standard (1 fichier)
```bash
python build_exe.py
```
- ✅ 1 seul fichier .exe
- ✅ Facile à distribuer
- ⚠️ Démarrage légèrement plus lent

### Build Optimisé (dossier)
```bash
python build_exe_optimized.py
```
- ✅ Démarrage plus rapide
- ✅ .exe plus petit
- ⚠️ Doit distribuer tout le dossier

## 🔧 Personnalisation

### Ajouter une icône

1. Créez/téléchargez un fichier `.ico`
2. Modifiez `build_exe.py` :
   ```python
   '--icon=mon_icone.ico',
   ```

### Changer le nom
```python
'--name=MonAppDictee',
```

### Ajouter des fichiers
```python
'--add-data=licence.txt;.',
'--add-data=manuel.pdf;.',
```

## 🐛 Résolution de Problèmes

### Le build échoue

**Erreur** : "No module named 'PyInstaller'"
```bash
pip install pyinstaller
```

**Erreur** : "Module not found" dans le .exe
- Ajoutez le module dans `build_exe.py` :
  ```python
  '--hidden-import=nom_du_module',
  ```

### Windows Defender bloque le .exe

C'est normal pour les .exe non signés. Solutions :

1. **Pour tester** : Cliquez "Plus d'infos" → "Exécuter quand même"
2. **Pour distribuer** : Ajoutez une exclusion Windows Defender
3. **Professionnel** : Signez le .exe avec un certificat code signing

### Le .exe est trop gros (>50MB)

```bash
# Créer un environnement virtuel propre
python -m venv venv_clean
venv_clean\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
python build_exe.py
```

## 📊 Tailles Attendues

| Build | Taille |
|-------|--------|
| `--onefile` | 20-35 MB |
| `--onedir` | 40-60 MB (dossier total) |
| Optimisé | 15-25 MB (dossier) |

## ✅ Checklist Avant Distribution

- [ ] Testé le .exe sur Windows 10
- [ ] Testé le .exe sur Windows 11
- [ ] Vérifié que l'API key se sauvegarde
- [ ] Vérifié que le micro se mémorise
- [ ] Testé push-to-talk mode
- [ ] Testé live mode
- [ ] Testé les deux langues (FR/EN)
- [ ] Vérifié la ponctuation française
- [ ] README inclus pour l'utilisateur

## 📝 Notes

- Le build doit être fait **sur Windows** pour créer un .exe Windows
- Le .exe inclut Python et toutes les dépendances
- Pas besoin d'installer Python chez l'utilisateur
- Compatible Windows 10 et 11 (64-bit)

## 🆘 Support

En cas de problème :
1. Vérifiez les messages d'erreur dans la console
2. Testez d'abord avec `--console` au lieu de `--windowed`
3. Vérifiez que toutes les dépendances sont installées
