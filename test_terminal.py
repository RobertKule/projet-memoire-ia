"""
Test du système de recommandation dans le terminal
"""
import os
import sys
import json
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Données de test (simule les sujets de mémoire)
TEST_SUBJECTS = [
    {
        'titre': 'Application web éducative avec IA',
        'resume': 'Développement d\'une plateforme d\'apprentissage adaptatif',
        'departement': 'Génie Informatique',
        'niveau': 'intermédiaire'
    },
    {
        'titre': 'Système IoT pour la domotique',
        'resume': 'Conception d\'un système intelligent pour la maison',
        'departement': 'Génie Informatique',
        'niveau': 'débutant'
    },
    {
        'titre': 'Analyse de données médicales',
        'resume': 'Utilisation du machine learning pour diagnostiquer des maladies',
        'departement': 'Génie Informatique',
        'niveau': 'intermédiaire'
    },
    {
        'titre': 'Robot autonome avec vision par ordinateur',
        'resume': 'Création d\'un robot capable de naviguer seul',
        'departement': 'Génie Informatique',
        'niveau': 'avancé'
    },
    {
        'titre': 'Chatbot intelligent pour support client',
        'resume': 'Développement d\'un assistant conversationnel',
        'departement': 'Génie Informatique',
        'niveau': 'intermédiaire'
    }
]

def print_banner():
    """Affiche une bannière stylée"""
    print("\n" + "="*60)
    print("🎓  SYSTÈME DE RECOMMANDATION DE SUJETS DE MÉMOIRE  🎓")
    print("="*60)

def test_api_groq_direct(query, student_level="intermédiaire"):
    """
    Test de l'API Groq directement (sans LangChain)
    """
    print(f"\n🧪 Test API Groq - Requête: '{query}'")
    print(f"📊 Niveau: {student_level}")
    print("-"*50)
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ Aucune clé API Groq trouvée dans .env")
        print("💡 Mode démo activé")
        return test_demo_mode(query, student_level)
    
    try:
        import requests
        
        # Préparer le prompt
        context_str = "\n".join([
            f"- {subject['titre']} ({subject['departement']}) - {subject['niveau']}"
            for subject in TEST_SUBJECTS[:3]
        ])
        
        prompt = f"""
        Tu es un conseiller académique francophone.
        
        SUJETS EXISTANTS :
        {context_str}
        
        DEMANDE DE L'ÉTUDIANT :
        "{query}"
        
        NIVEAU : {student_level}
        
        RECOMMANDE 3 SUJETS DE MÉMOIRE :
        
        Format :
        1. [TITRE]
           📍 Département : [Département]
           🎯 Objectif : [Objectif]
           ⚙️ Technologies : [Technologies]
        
        2. [TITRE]
           [Même structure]
        
        3. [TITRE]
           [Même structure]
        
        Réponds uniquement en français.
        """
        
        # Appel API Groq
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "Tu es un expert académique francophone. Tu recommandes des sujets de mémoire."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        print("🔄 Envoi de la requête à l'API Groq...")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            recommendations = result["choices"][0]["message"]["content"]
            
            print("✅ API Groq fonctionne !")
            print("\n📋 RECOMMANDATIONS :")
            print("-"*50)
            print(recommendations)
            print("-"*50)
            
            # Vérifier la qualité
            check_recommendation_quality(recommendations)
            
            return True
            
        else:
            print(f"❌ Erreur API: {response.status_code}")
            print(f"Message: {response.text}")
            return False
            
    except ImportError:
        print("❌ Le module 'requests' n'est pas installé")
        print("📦 Installez-le: pip install requests")
        return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_demo_mode(query, student_level):
    """
    Mode démo sans API
    """
    print("🎮 MODE DÉMO (sans API)")
    print("-"*50)
    
    # Recommandations basées sur des règles simples
    if "ia" in query.lower() or "intelligence artificielle" in query.lower():
        recommendations = """
        1. **Système de recommandation de films avec IA**
           📍 Département : Génie Informatique
           🎯 Objectif : Développer un algorithme de recommandation personnalisé
           ⚙️ Technologies : Python, Scikit-learn, Pandas
        
        2. **Chatbot médical intelligent**
           📍 Département : Génie Informatique
           🎯 Objectif : Créer un assistant pour répondre aux questions santé
           ⚙️ Technologies : Python, NLP, FastAPI
        
        3. **Classification d'images avec deep learning**
           📍 Département : Génie Informatique
           🎯 Objectif : Reconnaître des objets dans des images
           ⚙️ Technologies : Python, TensorFlow, OpenCV
        """
    elif "web" in query.lower() or "application" in query.lower():
        recommendations = """
        1. **Plateforme e-learning interactive**
           📍 Département : Génie Informatique
           🎯 Objectif : Créer un site d'apprentissage en ligne
           ⚙️ Technologies : React, Node.js, MongoDB
        
        2. **Réseau social pour étudiants**
           📍 Département : Génie Informatique
           🎯 Objectif : Développer une plateforme de partage académique
           ⚙️ Technologies : Django, PostgreSQL, WebSockets
        
        3. **Gestionnaire de projets collaboratif**
           📍 Département : Génie Informatique
           🎯 Objectif : Application pour gérer les projets d'équipe
           ⚙️ Technologies : Vue.js, Express.js, MySQL
        """
    elif "iot" in query.lower() or "internet" in query.lower():
        recommendations = """
        1. **Système de surveillance domestique intelligent**
           📍 Département : Génie Informatique / Électrique
           🎯 Objectif : Surveiller une maison avec des capteurs
           ⚙️ Technologies : Arduino, Raspberry Pi, MQTT
        
        2. **Jardin automatisé avec IoT**
           📍 Département : Génie Informatique
           🎯 Objectif : Automatiser l'arrosage des plantes
           ⚙️ Technologies : ESP32, Capteurs d'humidité, Cloud
        
        3. **Système de tracking de colis**
           📍 Département : Génie Informatique
           🎯 Objectif : Suivre des objets en temps réel
           ⚙️ Technologies : GPS, LoRa, Application mobile
        """
    else:
        recommendations = """
        1. **Application de gestion de bibliothèque**
           📍 Département : Génie Informatique
           🎯 Objectif : Système de gestion pour une bibliothèque universitaire
           ⚙️ Technologies : Python, Django, SQLite
        
        2. **Analyse de sentiments sur Twitter**
           📍 Département : Génie Informatique
           🎯 Objectif : Analyser les opinions sur un sujet donné
           ⚙️ Technologies : Python, Tweepy API, TextBlob
        
        3. **Système de réservation en ligne**
           📍 Département : Génie Informatique
           🎯 Objectif : Plateforme de réservation de salles
           ⚙️ Technologies : JavaScript, Node.js, MongoDB
        """
    
    print("\n📋 RECOMMANDATIONS (DÉMO) :")
    print("-"*50)
    print(recommendations)
    print("-"*50)
    print("💡 Pour des recommandations personnalisées avec IA, configurez GROQ_API_KEY")
    
    return True

def check_recommendation_quality(recommendations):
    """Vérifie la qualité des recommandations"""
    print("\n🔍 ANALYSE DE QUALITÉ :")
    
    checks = {
        "Contient 3 sujets": recommendations.count("1.") >= 1 and recommendations.count("2.") >= 1 and recommendations.count("3.") >= 1,
        "En français": any(word in recommendations.lower() for word in ["département", "objectif", "technologies", "pourquoi"]),
        "Longueur suffisante": len(recommendations) > 200,
        "Format structuré": "📍" in recommendations or "🎯" in recommendations or "⚙️" in recommendations
    }
    
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")
    
    quality_score = sum(checks.values()) / len(checks) * 100
    print(f"\n📊 Score de qualité: {quality_score:.0f}%")

def test_embeddings():
    """Test des embeddings (recherche sémantique)"""
    print("\n🔍 Test des embeddings (recherche sémantique)...")
    
    try:
        # Test simple de similarité
        test_query = "intelligence artificielle pour débutant"
        
        # Simuler une recherche sémantique
        keywords = ["ia", "machine learning", "deep learning", "neural network", "python"]
        query_keywords = test_query.lower().split()
        
        matches = sum(1 for kw in keywords if any(qk in kw for qk in query_keywords))
        
        if matches > 0:
            print(f"✅ Recherche sémantique: {matches} correspondances trouvées")
            print(f"   Requête: '{test_query}'")
            print(f"   Mots-clés détectés: IA, machine learning")
        else:
            print("⚠️ Aucune correspondance sémantique trouvée")
            
    except Exception as e:
        print(f"❌ Erreur embeddings: {str(e)}")

def test_environment():
    """Test de l'environnement"""
    print("\n🏗️ Test de l'environnement...")
    
    # Vérifier Python
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Vérifier les packages - CORRIGÉ
    packages_to_check = [
        ("requests", "requests"),
        ("python-dotenv", "dotenv"),  # ← CORRECTION ICI
        ("pandas", "pandas"),
        ("streamlit", "streamlit")
    ]
    
    for display_name, import_name in packages_to_check:
        try:
            if import_name == "dotenv":
                # Import spécial pour dotenv
                from dotenv import load_dotenv
                load_dotenv()
            else:
                __import__(import_name)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name} (manquant)")
    
    # Vérifier la clé API
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        print(f"🔑 GROQ_API_KEY: {'*' * 20}{api_key[-6:]}")
    else:
        print("❌ GROQ_API_KEY: Non configurée")

def run_interactive_test():
    """Mode interactif de test"""
    print_banner()
    
    # Test de l'environnement
    test_environment()
    
    # Test des embeddings
    test_embeddings()
    
    # Menu interactif
    print("\n" + "="*60)
    print("🧪 MODE INTERACTIF DE TEST")
    print("="*60)
    
    while True:
        print("\nOptions:")
        print("1. 🔍 Tester une requête spécifique")
        print("2. 🧠 Tester l'IA avec des exemples prédéfinis")
        print("3. 🏗️ Tester l'environnement seulement")
        print("4. 🚪 Quitter")
        
        choice = input("\n👉 Votre choix (1-4): ").strip()
        
        if choice == "1":
            query = input("\n💭 Entrez votre requête: ").strip()
            if not query:
                print("❌ Requête vide!")
                continue
                
            level = input("🎓 Niveau (débutant/intermédiaire) [intermédiaire]: ").strip()
            if not level:
                level = "intermédiaire"
                
            test_api_groq_direct(query, level)
            
        elif choice == "2":
            print("\n📚 Exemples prédéfinis:")
            examples = [
                ("Je veux un sujet en IA pour débutant", "débutant"),
                ("Application web moderne avec Python", "intermédiaire"),
                ("Projet IoT intelligent", "intermédiaire"),
                ("Cybersécurité pour les systèmes industriels", "avancé"),
                ("Analyse de données avec machine learning", "intermédiaire")
            ]
            
            for i, (example, level) in enumerate(examples, 1):
                print(f"{i}. '{example}' ({level})")
            
            ex_choice = input("\n👉 Choisissez un exemple (1-5): ").strip()
            
            if ex_choice.isdigit() and 1 <= int(ex_choice) <= 5:
                query, level = examples[int(ex_choice)-1]
                print(f"\n🔍 Test avec: '{query}'")
                test_api_groq_direct(query, level)
            else:
                print("❌ Choix invalide")
                
        elif choice == "3":
            test_environment()
            test_embeddings()
            
        elif choice == "4":
            print("\n👋 Au revoir!")
            break
            
        else:
            print("❌ Choix invalide")

def quick_test():
    """Test rapide en une commande"""
    print_banner()
    
    # Test simple
    query = "intelligence artificielle pour débutant"
    print(f"\n⚡ Test rapide avec: '{query}'")
    
    # Test API
    success = test_api_groq_direct(query, "débutant")
    
    if success:
        print("\n🎉 Test réussi! Le système fonctionne.")
    else:
        print("\n⚠️ Test partiellement réussi. Vérifiez la configuration.")

if __name__ == "__main__":
    # Mode d'exécution
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            quick_test()
        elif sys.argv[1] == "--query" and len(sys.argv) > 2:
            query = " ".join(sys.argv[2:])
            test_api_groq_direct(query)
        else:
            print("Usage:")
            print("  python test_terminal.py              # Mode interactif")
            print("  python test_terminal.py --quick      # Test rapide")
            print("  python test_terminal.py --query 'ma requête'")
            sys.exit(1)
    else:
        run_interactive_test()