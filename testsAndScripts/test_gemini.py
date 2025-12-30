"""
Test avec Google Gemini - Version corrigée
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

print("🤖 TEST GOOGLE GEMINI (CORRIGÉ)")
print("="*50)

# Vérifier la clé
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY non trouvée dans .env")
    exit(1)

print(f"✅ Clé trouvée: {'*' * 20}{api_key[-6:]}")

try:
    # Configurer Gemini
    genai.configure(api_key=api_key)
    
    # Utiliser un modèle ACTUEL (pas gemini-pro qui est obsolète)
    # Modèles gratuits disponibles :
    # - gemini-2.0-flash-lite : Léger et gratuit
    # - gemini-2.0-flash : Rapide
    # - gemma-3-4b-it : Léger et performant
    
    model_name = "gemini-2.0-flash-lite"  # Modèle gratuit et actuel
    
    print(f"\n🧪 Test avec le modèle: {model_name}")
    model = genai.GenerativeModel(model_name)
    
    prompt = "Recommande un sujet de mémoire simple en informatique. Réponds en une phrase."
    
    response = model.generate_content(prompt)
    
    print(f"\n📋 Réponse Gemini:")
    print(f"   {response.text}")
    print(f"\n🎉 SUCCÈS! Google Gemini fonctionne avec {model_name}!")
    
    # Test plus complet
    print("\n" + "="*50)
    print("🧪 TEST COMPLET (recommandation académique)")
    
    full_prompt = """
    Tu es un conseiller académique à la Faculté des Sciences et Technologies.
    
    Recommande 3 sujets de mémoire en informatique pour un étudiant débutant.
    
    Format:
    1. [Titre]
       📍 Département: 
       🎯 Objectif: 
       ⚙️ Technologies: 
    
    Réponds en français.
    """
    
    print("\n⏳ Génération des recommandations...")
    response2 = model.generate_content(full_prompt)
    
    print(f"\n📋 Recommandations complètes:")
    print(response2.text)
    
except Exception as e:
    print(f"\n❌ Erreur: {str(e)}")
    
    # Essayer avec un autre modèle
    print("\n🔄 Essai avec un autre modèle...")
    try:
        model = genai.GenerativeModel("gemma-3-4b-it")
        response = model.generate_content("Dis bonjour en français.")
        print(f"✅ Autre modèle fonctionne! Réponse: {response.text}")
    except Exception as e2:
        print(f"❌ Échec avec l'autre modèle: {e2}")

print("\n" + "="*50)