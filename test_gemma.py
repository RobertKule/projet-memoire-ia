"""
Test spécifique pour Google Gemma 3
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

print("🤖 TEST GOOGLE GEMMA 3")
print("="*50)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY manquante")
    print("Configurez .env avec: GOOGLE_API_KEY=AIzaSyCATUzWAdFJysadR7ZMU1E09zsAnSFu7Zo")
    exit()

print(f"✅ Clé trouvée: ...{api_key[-10:]}")

try:
    genai.configure(api_key=api_key)
    
    # Test avec gemma-3-4b-it
    model_name = "gemma-3-4b-it"
    print(f"\n🧪 Test avec: {model_name}")
    
    model = genai.GenerativeModel(model_name)
    
    # Test 1: Simple salutation
    print("\n1. Test de salutation...")
    response1 = model.generate_content("Dis bonjour en français et présente-toi comme assistant académique.")
    print(f"   ✅ Réponse: {response1.text[:100]}...")
    
    # Test 2: Recommandation académique
    print("\n2. Test académique complet...")
    prompt = """Tu es un conseiller académique. Recommande un sujet de mémoire en informatique pour un étudiant intermédiaire.

Format requis:
🎯 **Sujet 1: [Titre]**
   📍 Département: [Département]
   🎯 Objectif pédagogique: [Description]
   ⚙️ Technologies: [Liste]

Réponds en français uniquement."""
    
    response2 = model.generate_content(prompt)
    print(f"   📚 Résultat:\n{response2.text[:300]}...")
    
    print(f"\n{'='*50}")
    print(f"🎉 {model_name} FONCTIONNE PARFAITEMENT !")
    print(f"💡 Le modèle est prêt pour l'application.")
    print(f"{'='*50}")
    
except Exception as e:
    print(f"\n❌ Erreur: {str(e)[:200]}")