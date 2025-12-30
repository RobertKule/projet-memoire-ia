"""
Test avec DeepSeek API
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("🤖 TEST DEEPSEEK API")
print("="*50)

# Vérifier la clé
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("❌ DEEPSEEK_API_KEY non trouvée dans .env")
    exit(1)

print(f"✅ Clé trouvée: {'*' * 20}{api_key[-6:]}")

# Test de l'API
url = "https://api.deepseek.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "Tu es un assistant francophone."},
        {"role": "user", "content": "Recommande un sujet de mémoire simple en informatique. Réponds en une phrase."}
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

try:
    print("\n🧪 Envoi de la requête...")
    response = requests.post(url, headers=headers, json=data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        message = result["choices"][0]["message"]["content"]
        
        print(f"\n📋 Réponse DeepSeek:")
        print(f"   {message}")
        print("\n🎉 SUCCÈS! DeepSeek fonctionne!")
        
    elif response.status_code == 401:
        print(f"\n❌ Erreur 401: Clé API invalide")
        print("   Vérifie ta clé sur: https://platform.deepseek.com/api_keys")
        
    else:
        print(f"\n⚠️  Code d'erreur: {response.status_code}")
        print(f"   Réponse: {response.text[:200]}")
        
except Exception as e:
    print(f"\n❌ Erreur: {str(e)}")

print("\n" + "="*50)