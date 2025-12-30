"""
Script de nettoyage de l'environnement Python
Supprime les packages inutiles pour optimiser le projet
"""
import subprocess
import sys

def get_installed_packages():
    """Retourne la liste des packages installés"""
    result = subprocess.run([sys.executable, "-m", "pip", "freeze"], 
                          capture_output=True, text=True)
    return result.stdout.strip().split('\n')

def uninstall_packages(package_list):
    """Désinstalle une liste de packages"""
    for package in package_list:
        try:
            package_name = package.split('==')[0]
            print(f"🗑️  Désinstallation de {package_name}...")
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", package_name], 
                         capture_output=True)
        except Exception as e:
            print(f"⚠️  Erreur avec {package}: {e}")

def main():
    print("🧹 NETTOYAGE DE L'ENVIRONNEMENT")
    print("="*50)
    
    # Packages ESSENTIELS à garder
    essential = [
        "streamlit",
        "google-generativeai",
        "chromadb",
        "sentence-transformers",
        "pandas",
        "python-dotenv",
        "numpy"
    ]
    
    # Packages INUTILES à supprimer
    to_remove = [
        "langchain", "langchain-community", "langchain-core",
        "langchain-google-genai", "langchain-groq", "langchain-openai",
        "groq", "openai", "tiktoken",
        "transformers", "torch", "onnxruntime",
        "kubernetes", "pulsar-client", "pydeck",
        "fastapi", "uvicorn", "starlette",
        "opentelemetry", "httpx", "aiohttp"
    ]
    
    print(f"📦 Packages installés: {len(get_installed_packages())}")
    
    # Trouver les packages à supprimer
    all_packages = get_installed_packages()
    packages_to_remove = []
    
    for pkg in all_packages:
        pkg_name = pkg.split('==')[0].lower()
        should_remove = False
        
        # Vérifier si c'est un package à supprimer
        for remove_pkg in to_remove:
            if remove_pkg in pkg_name:
                should_remove = True
                break
        
        # Ne pas supprimer les essentiels
        for essential_pkg in essential:
            if essential_pkg in pkg_name:
                should_remove = False
                break
        
        if should_remove:
            packages_to_remove.append(pkg)
    
    print(f"\n🗑️  Packages à supprimer: {len(packages_to_remove)}")
    for pkg in packages_to_remove[:10]:  # Montrer les 10 premiers
        print(f"  - {pkg}")
    
    if len(packages_to_remove) > 10:
        print(f"  ... et {len(packages_to_remove) - 10} autres")
    
    # Demander confirmation
    response = input("\n⚠️  Continuer la désinstallation ? (o/n): ")
    if response.lower() != 'o':
        print("❌ Annulé.")
        return
    
    # Désinstaller
    uninstall_packages(packages_to_remove)
    
    print("\n✅ Nettoyage terminé !")
    print(f"📦 Packages restants: {len(get_installed_packages())}")
    
    # Réinstaller si besoin
    print("\n🔧 Réinstallation des essentiels...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", 
                   "streamlit", "google-generativeai", "chromadb", 
                   "sentence-transformers", "pandas", "python-dotenv"])

if __name__ == "__main__":
    main()