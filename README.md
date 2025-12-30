# 🎓 Système Intelligent de Recommandation de Sujets de Mémoire

## ✨ Application IA Académique avec Google Gemma 3

**Assistant IA intelligent** qui génère des recommandations personnalisées de sujets de mémoire pour les étudiants de la Faculté des Sciences et Technologies. Utilise **Google Gemma 3 (gemma-3-4b-it)** pour des suggestions adaptées, contextualisées et en français.

🚀 **Lien de démo** : [Disponible sur Streamlit Cloud](#)

---

## 📊 Table des Matières

- [✨ Fonctionnalités](#-fonctionnalités)
- [🏗️ Architecture Technique](#️-architecture-technique)
- [📁 Structure du Projet](#-structure-du-projet)
- [⚡ Installation Rapide](#-installation-rapide)
- [🔧 Configuration API](#-configuration-api)
- [🎮 Utilisation](#-utilisation)
- [🧪 Tests et Développement](#-tests-et-développement)
- [📊 Performance](#-performance)
- [🤝 Contribution](#-contribution)
- [📄 Licence](#-licence)

---

## ✨ Fonctionnalités

### 🤖 Intelligence Artificielle
- **Google Gemma 3** (gemma-3-4b-it) - Modèle IA gratuit et performant
- **Recommandations personnalisées** - 3 sujets adaptés à votre profil
- **Compréhension contextuelle** - Analyse sémantique avancée
- **Support français complet** - Interface et réponses en français académique

### 🎯 Personnalisation
- **Adaptation au niveau** : Débutant, Intermédiaire, Avancé
- **Filtrage par département** : Génie Informatique, Civil, Électrique, etc.
- **Recherche sémantique** : Basée sur vos intérêts et compétences
- **Sujets réalisables** : Projets concrets pour 4-6 mois de travail

### 💻 Interface Utilisateur
- **Interface moderne** avec animations CSS
- **Mode clair/sombre** automatique
- **Export des résultats** en format texte
- **Responsive design** adapté à tous les écrans

---

## 🏗️ Architecture Technique

```mermaid
graph TD
    A[Étudiant] --> B[Interface Streamlit]
    B --> C[Chargement des données]
    C --> D[Embeddings Sentence-Transformers]
    D --> E[Base Vectorielle ChromaDB]
    B --> F[Analyse de la requête]
    F --> G[Recherche sémantique]
    E --> G
    G --> H[Contexte enrichi]
    H --> I[Google Gemma 3 API]
    I --> J[Génération IA]
    J --> K[3 Recommandations]
    K --> L[Formatage académique]
    L --> M[Résultats à l'étudiant]
```

### 🛠️ Stack Technologique

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **Frontend** | Streamlit | 1.29.0 | Interface utilisateur |
| **IA/LLM** | Google Gemma 3 | gemma-3-4b-it | Génération des recommandations |
| **Embeddings** | Sentence-Transformers | 2.2.2 | Recherche sémantique |
| **Base Vectorielle** | ChromaDB | 0.4.22 | Stockage et recherche |
| **Traitement** | Python | 3.10+ | Backend et logique |
| **Gestion API** | google-generativeai | 0.3.2 | Communication avec Google |

---

## 📁 Structure du Projet

```
projet-memoire-ia/
├── 📄 app.py                    # Application Streamlit principale
├── 📄 requirements.txt          # Dépendances Python
├── 📄 .env                     # Configuration API (NON COMMIT)
├── 📄 .gitignore               # Fichiers ignorés par Git
├── 📄 README.md                # Documentation
├── 📄 Dockerfile               # Containerisation (optionnel)
│
├── 📂 data/
│   └── 📄 sujets_memoires.csv  # Base de sujets de mémoire
│
├── 📂 utils/                   # Modules utilitaires
│   ├── 📄 __init__.py
│   ├── 📄 data_loader.py       # Chargement des données CSV
│   ├── 📄 embeddings.py        # Gestion des embeddings
│   └── 📄 recommender.py       # Module Gemma 3 (cœur IA)
│
├── 📂 testsAndScripts/         # Tests et utilitaires
│   ├── 📄 check_install.py     # Vérification de l'installation
│   ├── 📄 fix_problems.py      # Correction des problèmes
│   ├── 📄 test_app_simple.py   # Test du flux complet
│   ├── 📄 test_gemma.py        # Test spécifique Gemma 3
│   ├── 📄 test_quick.py        # Tests rapides
│   └── 📄 test_terminal.py     # Interface terminal
│
├── 📂 chroma_db/               # Base vectorielle (générée)
│   └── 📄 chroma.sqlite3
│
└── 📂 venv/                    # Environnement virtuel (NON COMMIT)
```

---

## ⚡ Installation Rapide

### 1. Prérequis
- Python 3.10 ou supérieur
- Compte Google (pour l'API)
- Git (pour cloner le projet)

### 2. Cloner le projet
```bash
git clone https://github.com/RobertKule/projet-memoire-ia.git
cd projet-memoire-ia
```

### 3. Créer l'environnement virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 5. Configurer l'API
```bash
# Créer le fichier .env
echo "GOOGLE_API_KEY=AIzaSyCATUzWAdFJysadR7ZMU1E09zsAnSFu7Zo" > .env
```

> **Note** : Utilisez votre propre clé API Google pour de meilleures performances.

### 6. Lancer l'application
```bash
streamlit run app.py
```

Accédez à : http://localhost:8501

---

## 🔧 Configuration API

### Google Gemma 3 (Recommandé)
1. **Visitez** [Google AI Studio](https://aistudio.google.com/)
2. **Connectez-vous** avec votre compte Google
3. **Générez** une clé API gratuite
4. **Ajoutez-la** dans votre fichier `.env` :
```env
GOOGLE_API_KEY=votre_clé_api_ici
```

### Clé de test (disponible)
```env
GOOGLE_API_KEY=AIzaSyCATUzWAdFJysadR7ZMU1E09zsAnSFu7Zo
```

> **Important** : Cette clé est partagée et peut atteindre ses limites. Pour une utilisation personnelle, obtenez votre propre clé.

---

## 🎮 Utilisation

### Étape 1 : Lancer l'application
```bash
streamlit run app.py
```

### Étape 2 : Configuration
1. **Sélectionnez votre niveau** : Débutant, Intermédiaire ou Avancé
2. **Choisissez les départements** : Cochez vos domaines d'intérêt
3. **Décrivez votre projet** : Soignez la description pour de meilleurs résultats

### Étape 3 : Génération
1. **Cliquez** sur "🚀 Générer mes recommandations IA"
2. **Attendez** l'analyse (environ 7 secondes)
3. **Consultez** vos 3 recommandations personnalisées

### Étape 4 : Export
- **Téléchargez** les résultats en format texte
- **Partagez** avec vos encadrants
- **Archivez** pour votre mémoire

---

## 📝 Exemples de Requêtes

### Pour débutants
> "Je suis débutant en programmation, je veux un sujet en développement web avec Python"

### Pour intermédiaires
> "Je maîtrise Python, je cherche un sujet en IA ou machine learning avec des applications pratiques"

### Pour avancés
> "Je veux travailler sur un projet complexe en cybersécurité ou IoT avec Arduino et cloud"

### Par domaine
- **IA/ML** : "Sujet en intelligence artificielle avec TensorFlow"
- **Web** : "Développement d'application web moderne"
- **Mobile** : "Application mobile avec Flutter"
- **IoT** : "Système intelligent avec capteurs"
- **Données** : "Analyse de données avec Python"

---

## 🧪 Tests et Développement

### Vérifier l'installation
```bash
python testsAndScripts/check_install.py
```

### Tester Gemma 3
```bash
python testsAndScripts/test_gemma.py
```

### Tester le flux complet
```bash
python testsAndScripts/test_app_simple.py
```

### Mode développement
```bash
# Tests rapides
python testsAndScripts/test_quick.py

# Interface terminal
python testsAndScripts/test_terminal.py

# Résoudre les problèmes
python testsAndScripts/fix_problems.py
```

### Variables d'environnement de développement
```env
DEBUG_MODE=true
GOOGLE_API_KEY=votre_clé
```

---

## 📊 Performance

### Métriques
- ⏱️ **Temps de génération** : 5-8 secondes
- 🎯 **Précision** : Recommandations contextuelles et pertinentes
- 💾 **Mémoire utilisée** : ~500MB (modèle léger)
- 🌐 **Latence API** : 2-4 secondes

### Optimisations
- **Cache des embeddings** : Réduction du temps de chargement
- **Prompt engineering** : Format optimisé pour Gemma 3
- **Fallback automatique** : Mode démo en cas d'erreur
- **Gestion d'erreurs** : Robustesse améliorée

### Limitations connues
- ⚠️ **Clé API partagée** : Peut atteindre les limites de quota
- 📶 **Connexion internet** : Requise pour l'API Google
- 🔄 **Latence** : Dépend de la vitesse de connexion

---

## 🤝 Contribution

### Pour les contributeurs
1. **Fork** le projet
2. **Créez une branche** :
   ```bash
   git checkout -b feature/nouvelle-fonctionnalite
   ```
3. **Commitez vos changements** :
   ```bash
   git commit -m "feat: ajout de [fonctionnalité]"
   ```
4. **Push vers la branche** :
   ```bash
   git push origin feature/nouvelle-fonctionnalite
   ```
5. **Ouvrez une Pull Request**

### Guide de style
- **Code** : PEP 8 avec Black
- **Commits** : Conventional Commits
- **Documentation** : En français ou anglais
- **Tests** : Inclure des tests pour les nouvelles fonctionnalités

### Améliorations possibles
- [ ] Interface multi-langues
- [ ] Export PDF automatisé
- [ ] Intégration avec Google Scholar
- [ ] Système de feedback
- [ ] Dashboard analytique

---

## 📄 Licence

### Licence Académique
Ce projet a été développé dans le cadre d'un **mémoire de Licence en Génie Informatique** à l'**Université de ULPGL-Goma**.

### Conditions d'utilisation
- ✅ **Usage académique** autorisé
- ✅ **Modification** permise
- ✅ **Distribution** libre
- ✅ **Citation** requise
- ❌ **Usage commercial** restreint

### Citation
Si vous utilisez ce projet dans vos travaux académiques, merci de citer :
```
[Système Intelligent de Recommandation de Sujets de Mémoire]. 
Développé par RK, Étudiant en Génie Informatique. 
Université de ULPGL, 2024.
```

---

## 👨‍💻 Auteur

**Robert Kule**  
🎓 Étudiant en Génie Informatique  
🏫 Faculté des Sciences et Technologies  
📧 [ton-email@universite.edu](mailto:ton-email@universite.edu)  
🔗 [GitHub](https://github.com/RobertKule)  
💼 [LinkedIn](#)

### Remerciements
- **Google** pour l'API Gemma 3 gratuite
- **Streamlit** pour l'interface intuitive
- **La communauté open source** pour les outils utilisés
- **Mes encadrants** pour leur soutien académique

---

## 🔗 Liens utiles

- 📚 **Documentation Streamlit** : https://docs.streamlit.io/
- 🤖 **Google AI Studio** : https://aistudio.google.com/
- 🐍 **Python Documentation** : https://docs.python.org/
- 💾 **GitHub Repository** : https://github.com/RobertKule/projet-memoire-ia
- ☁️ **Déploiement Streamlit** : https://streamlit.io/cloud

---

## ⭐ Support

Si ce projet vous a été utile :
1. **Donnez une étoile** ⭐ sur GitHub
2. **Partagez** avec d'autres étudiants
3. **Contribuez** aux améliorations
4. **Signalez** les problèmes rencontrés
