"""
Test du flux complet de l'application
"""
import os
import sys
from dotenv import load_dotenv

# Ajouter le chemin du projet
sys.path.append('.')

load_dotenv()

print("🧪 TEST DU FLUX COMPLET")
print("="*60)

# 1. Vérifier l'environnement
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY manquante")
    exit()

print(f"✅ Clé API: ...{api_key[-10:]}")

# 2. Tester le chargement des données
try:
    from utils.data_loader import load_subjects
    df = load_subjects("data/sujets_memoires.csv")
    print(f"✅ Données chargées: {len(df)} sujets")
except Exception as e:
    print(f"❌ Erreur chargement données: {e}")

# 3. Tester le recommandateur
try:
    from utils.recommender import RecommenderSystem
    
    # Créer un contexte de test
    test_context = [
        {
            'titre': 'Application web avec Django',
            'departement': 'Génie Informatique',
            'niveau': 'intermédiaire'
        },
        {
            'titre': 'Système IoT avec Arduino',
            'departement': 'Génie Informatique',
            'niveau': 'débutant'
        },
        {
            'titre': 'Analyse de données avec Python',
            'departement': 'Génie Informatique',
            'niveau': 'intermédiaire'
        }
    ]
    
    # Initialiser
    recommender = RecommenderSystem(api_key=api_key)
    
    # Test simple
    print("\n🧪 Test de recommandation...")
    test_query = "Je veux un sujet en programmation web"
    
    recommendations = recommender.generate_recommendations(
        query=test_query,
        context=test_context,
        student_level="débutant"
    )
    
    print("\n📋 RÉSULTATS DU TEST:")
    print("-"*50)
    print(recommendations[:500] + "..." if len(recommendations) > 500 else recommendations)
    print("-"*50)
    
    # Vérifier la qualité
    if "RECOMMANDATIONS" in recommendations and "Sujet" in recommendations:
        print("\n✅ TEST RÉUSSI ! Le système fonctionne correctement.")
    else:
        print("\n⚠️  Format de réponse inhabituel")
        
except Exception as e:
    print(f"\n❌ Erreur: {str(e)}")

print("\n" + "="*60)
print("🎉 Prêt pour Streamlit !")
print("Commande: streamlit run app.py")