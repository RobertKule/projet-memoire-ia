"""
Script pour réparer les problèmes d'installation
"""
import subprocess
import sys

def run_command(cmd):
    """Exécute une commande"""
    print(f"▶ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Erreur: {result.stderr}")
    return result.returncode

print("🔧 Réparation du projet...")

# 1. Désinstaller les problèmes
packages_to_remove = [
    "langchain", "langchain-core", "langchain-openai",
    "langchain-groq", "langchain-google-genai"
]

for pkg in packages_to_remove:
    run_command(f"pip uninstall {pkg} -y")

# 2. Installer les versions stables
packages_to_install = [
    "streamlit==1.52.2",
    "pandas==2.3.3",
    "python-dotenv==1.2.1",
    "sentence-transformers==5.2.0",
    "chromadb==0.4.24",
    "torch==2.9.1",
    "requests==2.32.5",
    "numpy==1.26.4",
    "scikit-learn==1.7.2",
    "openai==1.6.1",
    "groq==0.37.1"
]

for pkg in packages_to_install:
    run_command(f"pip install {pkg}")

print("✅ Réparation terminée!")
print("\nPour lancer : streamlit run app.py")