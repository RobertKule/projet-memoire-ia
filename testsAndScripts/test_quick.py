"""
Test rapide et fiable du système
"""
import os
import sys
import requests

print("🚀 TEST RAPIDE DU SYSTÈME")
print("="*50)

# 1. Vérifier Python
print(f"🐍 Python version: {sys.version.split()[0]}")

# 2. Vérifier dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ python-dotenv: OK")
except ImportError:
    print("❌ python-dotenv: NON INSTALLÉ")
    print("   Installez: pip install python-dotenv")

# 3. Vérifier requests
try:
    import requests
    print("✅ requests: OK")
except ImportError:
    print("❌ requests: NON INSTALLÉ")
    print("   Installez: pip install requests")

# 4. Vérifier la clé API
api_key = os.getenv("GROQ_API_KEY")
if api_key and len(api_key) > 20:
    print(f"✅ GROQ_API_KEY: {'*' * 20}{api_key[-6:]}")
    
    # 5. Tester l'API Groq
    print("\n🧪 Test de l'API Groq...")
    
    # Modèle actuel
    models_to_try = [
        "llama3-70b-8192",
        "mixtral-8x7b-32768", 
        "gemma2-9b-it"
    ]
    
    for model in models_to_try:
        print(f"\n🔍 Essai avec le modèle: {model}")
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "Tu es un assistant francophone. Réponds simplement 'Bonjour!'"},
                {"role": "user", "content": "Dis bonjour"}
            ],
            "temperature": 0.1,
            "max_tokens": 10
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                message = result["choices"][0]["message"]["content"]
                print(f"   ✅ {model}: FONCTIONNE! Réponse: {message}")
                working_model = model
                break
            elif response.status_code == 400:
                error = response.json().get("error", {})
                error_msg = error.get("message", "Erreur inconnue")
                print(f"   ❌ {model}: {error_msg[:80]}")
            else:
                print(f"   ⚠️  {model}: Code {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {model}: Erreur - {str(e)[:50]}")
    
    print("\n" + "="*50)
    
    # 6. Test complet si un modèle fonctionne
    if 'working_model' in locals():
        print("\n🎯 TEST COMPLET AVEC LE MODÈLE QUI FONCTIONNE")
        
        prompt = """
        Recommande un sujet de mémoire simple en informatique.
        Réponds en une phrase seulement.
        """
        
        data = {
            "model": working_model,
            "messages": [
                {"role": "system", "content": "Tu es un conseiller académique."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                recommendation = result["choices"][0]["message"]["content"]
                print(f"\n📋 Recommandation test:")
                print(f"   {recommendation}")
                print(f"\n🎉 SUCCÈS! Le système fonctionne avec {working_model}")
            else:
                print(f"\n⚠️  Modèle {working_model} a répondu mais erreur: {response.status_code}")
                
        except Exception as e:
            print(f"\n❌ Erreur lors du test complet: {str(e)}")
    
else:
    print("❌ GROQ_API_KEY: NON TROUVÉE ou INVALIDE")
    print("   Vérifiez votre fichier .env")
    print("   Il doit contenir: GROQ_API_KEY=votre_clé_ici")

print("\n" + "="*50)
print("🔍 VÉRIFICATION TERMINÉE")