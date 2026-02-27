# Calculateur de Superficie - Guide Complet

## 📖 Table des matières
1. [Installation rapide](#installation-rapide)
2. [Prérequis](#prérequis)
3. [Méthode automatique (recommandée)](#méthode-automatique)
4. [Méthode manuelle (si automatique ne marche pas)](#méthode-manuelle)
5. [Utilisation du logiciel](#utilisation)
6. [Dépannage](#dépannage)

---

## 🚀 Installation Rapide

**La plus simple :**
1. Assurez-vous que [Python est installé](#prérequis)
2. Double-cliquez sur **`start.bat`** 
3. Attendez que tout s'installe
4. Le logiciel se lance automatiquement

C'est tout! Le fichier `.bat` fait tout automatiquement.

---

## 📋 Prérequis

### Python 3.9 ou supérieur REQUIS

**Vérifier si Python est déjà installé :**
1. Appuyez sur **Windows + R**
2. Tapez `cmd` et appuyez sur **Entrée**
3. Tapez : `python --version`
4. Si vous voyez une version (ex: `Python 3.11.9`), Python est installé ✓

**Si Python n'est pas installé :**

1. Allez sur : **https://www.python.org/**
2. Cliquez sur le bouton bleu **"Download Python 3.x.x"** (la version la plus récente)
3. Lancez le fichier téléchargé (`.exe`)
4. **⚠️ TRÈS IMPORTANT :** Cochez la case **"Add Python to PATH"** (en bas à gauche)
5. Cliquez sur **"Install Now"**
6. Attendez la fin de l'installation
7. Cliquez sur **"Close"**
8. **Redémarrez votre ordinateur**

Après restart, tapez à nouveau `python --version` pour vérifier.

---

## 🤖 Méthode Automatique (RECOMMANDÉE)

### Etape 1 : S'assurer que Python est installé

Ouvrez `Cmd` (Windows + R → `cmd`)  
Tapez : `python --version`  
Vous devez voir une version (ex: `Python 3.11.9`)

### Etape 2 : Double-cliquer sur start.bat

1. Ouvrez le dossier du calculateur
2. **Double-cliquez sur `start.bat`**
3. Une fenêtre noire s'ouvre
4. Attendez et observez le processus :
   - Etape 1 : Vérification de Python
   - Etape 2 : Création de l'environnement
   - Etape 3 : Activation
   - Etape 4 : Mise à jour PIP
   - Etape 5 : Installation des modules (peut prendre 2-3 min la première fois)

### Etape 3 : Le logiciel se lance

Une fois tout installé, l'interface graphique du calculateur s'ouvre automatiquement.

Si erreurs durant l'installation → voir la [Méthode Manuelle](#méthode-manuelle)

---

## 🖥️ Méthode Manuelle (Si le batch échoue)

### Étape 1 : Ouvrir le Command Prompt

- Appuyez sur **Windows + R**
- Tapez `cmd`
- Appuyez sur **Entrée**

### Étape 2 : Se déplacer dans le dossier

Tapez cette commande (remplacez `[VotreNom]` par votre nom d'utilisateur) :

```
cd C:\Users\[VotreNom]\Documents\PLAN\LOGICIEL_PAPA
```

**Exemple :**
```
cd C:\Users\israel\Documents\PLAN\LOGICIEL_PAPA
```

Appuyez sur **Entrée**

### Étape 3 : Créer l'environnement virtuel (PREMIÈRE FOIS SEULEMENT)

Tapez cette commande :

```
python -m venv env
```

Appuyez sur **Entrée**

Attendez quelques secondes. Vous verrez :
```
C:\Users\israel\Documents\PLAN\LOGICIEL_PAPA>
```

C'est bon, un dossier `env` a été créé.

### Étape 4 : Activer l'environnement

Tapez :

```
env\Scripts\activate.bat
```

Appuyez sur **Entrée**

Vous verrez maintenant au début de la ligne :
```
(env) C:\Users\israel\Documents\PLAN\LOGICIEL_PAPA>
```

Le `(env)` indique que l'environnement est actif. C'est bon!

### Étape 5 : Installer les modules

Tapez :

```
python -m pip install -r requirements.txt
```

Appuyez sur **Entrée**

**Attendez !** Vous verrez s'afficher :
```
Collecting kivy==2.2.1
Downloading kivy-2.2.1-cp311-cp311-win_amd64.whl (...)
Collecting kivymd==1.2.0
...
Successfully installed kivy-2.2.1 kivymd-1.2.0 ...
```

**Si ça prend du temps ou y'a des warnings, c'est normal.** Laissez faire.

**Si ça échoue**, essayez :

```
python -m pip install -r requirements_flexible.txt
```

### Étape 6 : Lancer l'application

Tapez simplement :

```
python calculateur.py
```

Appuyez sur **Entrée**

**L'interface graphique du calculateur doit s'ouvrir !** ✓

---

## 📱 Utilisation du Logiciel

### Interface Principale

**À GAUCHE** - Saisie des coordonnées :
1. Remplissez **"Nom du projet"** (ex: "Terrain Kinshasa")
2. Remplissez **"Propriétaire / Demandeur"** (ex: "Jean Dupont")
3. Le champ **"Localisation"** est défini à "Kananga" (peut être changé)
4. Zone UTM = 33S (fixe)
5. **X (Easting)** : la coordonnée Easting (ex: 500000)
6. **Y (Northing)** : la coordonnée Northing (ex: 9000000)
7. **Commentaires** : Observations optionnelles
8. Cliquez **"AJOUTER LE POINT"**

**À DROITE** - Liste des points :
- S'affiche au fur et à mesure que vous ajoutez des points
- Vous pouvez supprimer un point en cliquant la croix rouge
- **MINIMUM 3 POINTS requis pour générer un rapport**

**EN BAS** - Générer le rapport :
- Cliquez **"GÉNÉRER LE RAPPORT OFFICIEL"**
- Attendez quelques secondes
- Un message s'affiche : "Rapport généré avec succès"
- Cliquez "OUVRIR LE DOSSIER" pour voir le PDF

### Structure du PDF généré

**4 pages professionnelles :**

- **Page 1 : Couverture**
  - Titre "AVIS DE CONFORMITE"
  - Infos du projet
  - RÉFÉRENCE, PROJET, DEMANDEUR, LOCALITÉ, ZONE UTM, DATE

- **Page 2 : Données Techniques**
  - Tableau des coordonnées UTM
  - Distances entre les points
  - Résultats : Surface (m²), Superficie (ha), Périmètre (m)

- **Page 3 : Plan de Situation**
  - Dessin du terrain avec tous les points
  - Graphique planimétrique

- **Page 4 : Validations**
  - Champ d'observations à remplir au stylo (4 lignes)
  - Zone signature + cachet : Chef de Division (Moise Mukaya Tshijuke)

### Où sont sauvegardés les PDFs ?

Tous les rapports sont sauvegardés dans :

```
C:\Users\[VotreNom]\Documents\Rapports_Division_AT_KasaiCentral\
```

Noms des fichiers : `RAPPORT_[NomProjet]_[YYYYMMDD]_[HHMMSS].pdf`

---

## 🐛 Dépannage

### ❌ "Python n'est pas reconnu"

**Cause :** Python n'est pas dans le PATH

**Solution :**
1. Réinstallez Python depuis https://www.python.org/
2. **TRÈS IMPORTANT** : Cochez **"Add Python to PATH"** pendant l'installation
3. Redémarrez l'ordinateur
4. Relancez `start.bat` ou refaites l'installation manuelle

---

### ❌ "Le fichier start.bat s'ouvre puis se ferme immédiatement"

**Cause :** Il y a une erreur

**Solution :**
1. Ouvrez `Cmd` (Windows + R → `cmd`)
2. Allez dans le dossier : `cd C:\Users\[VotreNom]\Documents\PLAN\LOGICIEL_PAPA`
3. Tapez : `start.bat`
4. Cette fois la fenêtre ne se fermera pas et vous verrez l'erreur
5. Consultez le message d'erreur et reportez-vous à ce guide

---

### ❌ "Module not found" ou "Erreur d'installation"

**Cause :** Les modules n'ont pas pu s'installer

**Solution :**
1. Essayez la méthode manuelle (voir étapes above)
2. À l'étape 5, utilisez :

```
python -m pip install --upgrade pip
python -m pip install kivy
python -m pip install kivymd
python -m pip install matplotlib
python -m pip install reportlab
python -m pip install numpy
python -m pip install pillow
```

(Une ligne à la fois)

---

### ❌ "L'interface ne s'affiche pas / reste blanche"

**Cause :** Modules non chargés correctement

**Solution :**
1. Fermez le logiciel
2. Relancez `start.bat`
3. Si ça persiste, réinstallez manuellement les modules via Cmd

---

### ❌ "PDF ne se génère pas"

**Cause :** Minimum 3 points requis

**Solution :**
1. Vérifiez que vous avez **au minimum 3 points**
2. Vérifiez que le **"Nom du projet"** et **"Propriétaire"** sont remplis
3. Vérifiez que le dossier `Documents` existe sur votre ordinateur
4. Si erreur persiste, vérifiez que le fichier `header.jpeg` existe (optionnel mais recommandé)

---

### ❌ "Les coordonnées ne sont pas prises en compte"

**Cause :** Format incorrect

**Solution :**
- X et Y doivent être des **NOMBRES**
- Format : `500000` ou `500000.5` (pas de lettres)
- Pas d'espaces

---

## 📁 Fichiers importants

```
LOGICIEL_PAPA/
├── start.bat                   ← Double-cliquez ( RECOMMANDÉ!)
├── calculateur.py              ← Application principale
├── requirements.txt            ← Liste des modules
├── requirements_flexible.txt   ← Versions flexibles (fallback)
├── README.md                   ← Ce fichier (infos complètes)
├── LIRE_MOI.txt               ← Instructions simples
├── env/                        ← Dossier créé auto après install
├── header.jpeg                 ← Logo en-tête (optionnel)
└── rapports/                   ← PDFs générés (auto créé)
```

**NE SUPPRIMEZ PAS le dossier `env` !** Il contient tous les modules installés.

---

## ⚙️ Paramètres techniques

| Paramètre | Valeur |
|-----------|--------|
| Zone UTM | 33S (Kasaï Central) |
| Format coordonnées | Easting / Northing |
| Unités | Mètres |
| Calcul surface | Formule de Shoelace (polygone fermé) |
| Calcul périmètre | Distance Euclidienne |
| Points minimum | 3 |
| Python requis | 3.9+ |

---

## 🔒 Sécurité & Confidentialité

- ✓ Tous les fichiers restent sur votre ordinateur
- ✓ Aucune donnée n'est envoyée en ligne
- ✓ Les rapports sont stockés localement
- ✓ Vous gardez le contrôle complet

---

## 💡 Conseils d'utilisation

1. **Créer un raccourci :** Clic droit sur `start.bat` → Créer un raccourci → Placer sur le Bureau

2. **Utiliser les mêmes coordonnées :** Si vous travaillez sur le même terrain, gardez les mêmes points pour comparer

3. **Vérifier avant de générer :** Regardez la liste des points à droite avant de générer le rapport

4. **Sauvegarder les PDFs :** Les rapports générés peuvent être imprimés et signés

5. **Remplir les observations :** N'oubliez pas de remplir le champ "Observations" du PDF avant signature

---

## 📞 Problèmes courants

**Q: Ça prend combien de temps la première installation?**  
R: 2-3 minutes selon votre connexion Internet. Laissez faire, ne fermez pas.

**Q: Est-ce que je dois avoir internet?**  
R: OUI pour l'installation initiale. NON pour l'utilisation après.

**Q: Puis-je lancer le logiciel sans le .bat après?**  
R: Oui, tapez `python calculateur.py` dans Cmd (après avoir activé l'env)

**Q: Que faire si j'ai un message d'erreur bizarre?**  
R: Lisez le message, notez-le, et consultez la section Dépannage above

**Q: Comment supprimer et réinstaller?**  
R: Supprimez le dossier `env`, puis relancez `start.bat`

---

## 📊 Exemple complet d'utilisation

1. Double-cliquez `start.bat`
2. Attendez l'installation
3. L'interface s'ouvre
4. Projet : "Terrain Kasangre"
5. Propriétaire : "Mukaya"
6. Localité : "Kananga"
7. Point 1 : X=500000, Y=9000000 → Cliquez "Ajouter"
8. Point 2 : X=501000, Y=9000000 → Cliquez "Ajouter"
9. Point 3 : X=500500, Y=9001000 → Cliquez "Ajouter"
10. Vous voyez 3 points à droite
11. Cliquez "GÉNÉRER LE RAPPORT OFFICIEL"
12. Attendez quelques secondes
13. Message "Succès!"
14. Cliquez "OUVRIR LE DOSSIER"
15. Le PDF `RAPPORT_Terrain_Kasangre_20260227_HHMMSS.pdf` s'ouvre
16. Imprimez et signez!

---

## 📝 Notes finales

- Ce logiciel a été conçu pour la Division AT - Kasaï Central
- Les calculs sont fiables et conformes aux normes topographiques
- Les PDF sont prêts à imprimer et à signer
- Support technique disponible sur demande

---

**Version** : 1.0  
**Date** : 27 février 2026  
**Pour** : Division AT - Kasaï Central  
**Langage** : Python 3.11+  
**Licence** : Gouvernement Provincial Kasaï Central

---

**Besoin d'aide? Relisez ce guide - la réponse s'y trouve probablement!** 😊
