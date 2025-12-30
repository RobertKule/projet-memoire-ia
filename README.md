# 🎓 Système Intelligent de Recommandation de Sujets de Mémoire

## 📋 Description
Application web utilisant l'IA pour recommander des sujets de mémoire aux étudiants de la Faculté des Sciences et Technologies.

## 🚀 Fonctionnalités
- 🤖 Interface conversationnelle en français
- 🧠 Recherche sémantique avec RAG
- 🎯 Recommandations personnalisées (3 sujets)
- 📊 Adaptation au niveau académique
- 🏫 Support multi-départements

## 🏗️ Architecture
```mermaid
graph TD
    A[Étudiant] --> B[Interface Streamlit]
    B --> C[Traitement NLP]
    C --> D[Base Vectorielle ChromaDB]
    D --> E[Modèle IA Gemini/LLaMA]
    E --> F[Recommandations]
    F --> A

🛠️ Technologies

    Frontend : Streamlit

    Backend : Python

    IA/NLP : LangChain, Sentence-Transformers

    Base vectorielle : ChromaDB

    Modèle LLM : Google Gemini Pro

    Hébergement : Streamlit Cloud (gratuit)

📁 Structure du Projet
text

projet_memoire_ia/
├── app.py                 # Application principale
├── requirements.txt       # Dépendances
├── .env.example          # Variables d'environnement
├── data/                 # Données des sujets
├── utils/                # Modules utilitaires
└── chroma_db/            # Base vectorielle (générée)

⚡ Installation Rapide
1. Cloner le projet
bash

git clone https://github.com/ton-username/projet-memoire-ia.git
cd projet-memoire-ia

2. Installer les dépendances
bash

pip install -r requirements.txt

3. Configurer l'environnement
bash

# Copier le template
cp .env.example .env
# Éditer .env avec vos clés API

4. Lancer l'application
bash

streamlit run app.py

🔧 Configuration API
Google Gemini Pro (Recommandé)

    Visitez Google AI Studio

    Créez un compte et obtenez une clé API gratuite

    Ajoutez-la dans .env :

env

GOOGLE_API_KEY=votre_cle_ici

Alternative : Groq

    Visitez Groq Cloud

    Inscrivez-vous pour une clé API gratuite

    Ajoutez dans .env :

env

GROQ_API_KEY=votre_cle_ici

📊 Départements Supportés

    Génie Informatique

    Génie Civil

    Génie Électrique

    Génie Électronique

    Génie Mécanique

🎯 Utilisation

    Lancez l'application : streamlit run app.py

    Décrivez votre projet en français

    Sélectionnez votre niveau académique

    Recevez 3 recommandations personnalisées

📝 Exemples de Requêtes

    "Je veux un sujet en intelligence artificielle pour débutant"

    "Recherche en cybersécurité des systèmes industriels"

    "Développement d'application mobile avec Python"

    "Projet IoT pour la gestion énergétique"

🤝 Contribution

Ce projet a été développé dans le cadre d'un mémoire de Licence en Génie Informatique.
📄 Licence

Projet académique - Université [Nom de ton Université]
👨‍💻 Auteur

[Ton Nom] - Étudiant en Génie Informatique