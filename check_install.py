"""
Vérifie toutes les dépendances
"""
import importlib
import sys

def check_package(package_name, import_name=None):
    """Vérifie si un package est installé"""
    try:
        if import_name:
            importlib.import_module(import_name)
        else:
            importlib.import_module(package_name)
        return True, f"✅ {package_name}"
    except ImportError:
        return False, f"❌ {package_name}"

# Packages à vérifier
packages = [
    ("streamlit", None),
    ("pandas", None),
    ("langchain", None),
    ("langchain_core", "langchain_core"),
    ("sentence_transformers", "sentence_transformers"),
    ("chromadb", None),
    ("google.generativeai", "google.generativeai"),
    ("langchain_google_genai", "langchain_google_genai"),
    ("langchain_openai", "langchain_openai"),
    ("langchain_groq", "langchain_groq"),
    ("openai", None),
    ("groq", None),
]

print("🔍 Vérification des dépendances...\n")

all_ok = True
for package, import_name in packages:
    ok, message = check_package(package, import_name)
    print(message)
    if not ok:
        all_ok = False

print("\n" + "="*50)
if all_ok:
    print("🎉 Toutes les dépendances sont installées !")
    print("\nPour lancer l'application :")
    print("streamlit run app.py")
else:
    print("⚠️ Certaines dépendances manquent.")
    print("\nInstallez-les avec :")
    print("pip install -r requirements.txt")