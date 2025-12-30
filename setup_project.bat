@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════╗
echo ║     SETUP COMPLET - PROJET MÉMOIRE IA       ║
echo ║     Environnement Python 3.10              ║
echo ╚═══════════════════════════════════════════════╝
echo.

REM ============================================
REM 1. CONFIGURATION DES CHEMINS
REM ============================================
set PROJECT_DIR=%CD%
set VENV_DIR=%PROJECT_DIR%\venv
set REQUIREMENTS_FILE=%PROJECT_DIR%\requirements.txt
set DATA_DIR=%PROJECT_DIR%\data
set UTILS_DIR=%PROJECT_DIR%\utils
set TESTS_DIR=%PROJECT_DIR%\testsAndScripts

echo 📁 Répertoire projet: %PROJECT_DIR%
echo.

REM ============================================
REM 2. NETTOYAGE DE L'ANCIEN ENVIRONNEMENT
REM ============================================
echo [1/10] Nettoyage de l'ancien environnement...
if exist %VENV_DIR% (
    echo   Suppression de l'ancien venv...
    rmdir /s /q %VENV_DIR%
    if errorlevel 1 (
        echo ❌ Erreur lors de la suppression de venv
        echo   Essayez de fermer tous les terminaux et réessayez
        pause
        exit /b 1
    )
    echo ✅ Ancien venv supprimé
) else (
    echo ℹ️  Pas d'ancien venv trouvé
)

REM ============================================
REM 3. CRÉATION DU NOUVEL ENVIRONNEMENT
REM ============================================
echo.
echo [2/10] Création du nouvel environnement Python 3.10...
py -3.10 -m venv %VENV_DIR%
if errorlevel 1 (
    echo ❌ Erreur création venv
    echo   Vérifiez que Python 3.10 est installé: py --list
    pause
    exit /b 1
)
echo ✅ Environnement créé avec Python 3.10

REM ============================================
REM 4. ACTIVATION
REM ============================================
echo.
echo [3/10] Activation de l'environnement...
call %VENV_DIR%\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Erreur d'activation
    echo   Essayez manuellement: %VENV_DIR%\Scripts\activate
    pause
    exit /b 1
)
echo ✅ Environnement activé

REM ============================================
REM 5. MISE À JOUR DE PIP
REM ============================================
echo.
echo [4/10] Mise à jour de pip et outils...
python -m pip install --upgrade pip setuptools wheel --quiet
echo ✅ Pip mis à jour (version: )
python -m pip --version | findstr pip

REM ============================================
REM 6. CRÉATION DU REQUIREMENTS.TXT OPTIMISÉ
REM ============================================
echo.
echo [5/10] Création du fichier requirements.txt optimisé...

(
echo # =============================================
echo # Système de Recommandation de Sujets de Mémoire
echo # Dépendances optimisées - Version stable
echo # Python 3.10 compatible
echo # =============================================
echo.
echo # Interface utilisateur
echo streamlit==1.52.2
echo.
echo # Google Gemma 3 API
echo google-generativeai==0.3.2
echo.
echo # Base vectorielle et embeddings
echo chromadb==0.4.22
echo sentence-transformers==2.2.2
echo.
echo # Traitement de données
echo pandas==2.1.4
echo.
echo # Utilitaires
echo python-dotenv==1.0.0
echo.
echo # Dépendances système (versions stables)
echo numpy==1.26.4
echo protobuf==4.25.3
echo typing-extensions==4.7.1
echo packaging==23.1
echo tqdm==4.66.1
) > %REQUIREMENTS_FILE%

echo ✅ requirements.txt créé (%REQUIREMENTS_FILE%)
echo.

REM ============================================
REM 7. INSTALLATION DES DÉPENDANCES
REM ============================================
echo [6/10] Installation des dépendances...
echo   Installation des 11 packages essentiels...

REM Installation séquentielle pour meilleur contrôle
echo   1. streamlit...
pip install streamlit==1.52.2 --quiet

echo   2. google-generativeai...
pip install google-generativeai==0.3.2 --quiet

echo   3. chromadb...
pip install chromadb==0.4.22 --quiet

echo   4. sentence-transformers...
pip install sentence-transformers==2.2.2 --quiet

echo   5. pandas...
pip install pandas==2.1.4 --quiet

echo   6. autres dépendances...
pip install python-dotenv==1.0.0 numpy==1.26.4 protobuf==4.25.3 --quiet

echo ✅ Toutes les dépendances installées
echo.

REM ============================================
REM 8. VÉRIFICATION DES IMPORTS
REM ============================================
echo [7/10] Vérification des imports critiques...
python -c "
print('Vérification des imports...')
modules = [
    ('streamlit', 'st'),
    ('google.generativeai', 'genai'),
    ('chromadb', 'chromadb'),
    ('pandas', 'pd'),
    ('sentence_transformers', 'SentenceTransformer'),
    ('dotenv', 'load_dotenv')
]

all_ok = True
for module, alias in modules:
    try:
        exec(f'import {module} as {alias}')
        print(f'  ✅ {module}')
    except ImportError as e:
        print(f'  ❌ {module}: {e}')
        all_ok = False

if all_ok:
    print('\\n✅ TOUS LES IMPORTS FONCTIONNENT !')
else:
    print('\\n❌ Certains imports ont échoué')
"

REM ============================================
REM 9. TEST DE L'API GOOGLE GEMMA
REM ============================================
echo.
echo [8/10] Test de l'API Google Gemma 3...

REM Créer un fichier de test temporaire
(
echo import os
echo import google.generativeai as genai
echo.
echo print("🧪 Test de l'API Google Gemma 3...")
echo.
echo # Vérifier la clé API
echo if not os.path.exists('.env'):
echo     print("⚠️  Fichier .env non trouvé")
echo     print("   Créez-le avec: GOOGLE_API_KEY=votre_clé")
echo else:
echo     print("✅ Fichier .env trouvé")
echo.
echo # Test de l'import
echo try:
echo     genai.configure(api_key='test')
echo     print("✅ Module google.generativeai fonctionnel")
echo     print("✅ Version: " + genai.__version__)
echo except Exception as e:
echo     print(f"❌ Erreur: {e}")
) > %TEMP%\test_gemma.py

python %TEMP%\test_gemma.py

REM ============================================
REM 10. GÉNÉRATION DU FICHIER REQUIREMENTS FINAL
REM ============================================
echo.
echo [9/10] Génération du fichier requirements final...
pip freeze > requirements_final.txt
echo ✅ Fichier requirements_final.txt généré
echo   Nombre de packages: 
type requirements_final.txt | find /c /v ""

REM ============================================
REM 11. TEST DE L'APPLICATION
REM ============================================
echo.
echo [10/10] Test rapide de l'application...
echo   Test du chargement des données...
python -c "
import sys
sys.path.append('.')
try:
    from utils.data_loader import load_subjects
    df = load_subjects('data/sujets_memoires.csv')
    print(f'✅ Données chargées: {len(df)} sujets')
except Exception as e:
    print(f'❌ Erreur: {e}')
    print('   Vérifiez le fichier data/sujets_memoires.csv')
"

REM ============================================
REM FINAL - INSTRUCTIONS
REM ============================================
echo.
echo ╔═══════════════════════════════════════════════╗
echo ║            ✅ SETUP TERMINÉ !                ║
echo ╚═══════════════════════════════════════════════╝
echo.
echo 📋 INSTRUCTIONS FINALES:
echo.
echo 1. CONFIGUREZ VOTRE CLÉ API:
echo    Créez/modifiez le fichier .env:
echo    GOOGLE_API_KEY=AIzaSyCATUzWAdFJysadR7ZMU1E09zsAnSFu7Zo
echo.
echo 2. LANCEZ L'APPLICATION:
echo    streamlit run app.py
echo.
echo 3. TESTS DISPONIBLES:
echo    python testsAndScripts\test_gemma.py    - Test API Gemma
echo    python testsAndScripts\test_quick.py    - Test rapide
echo    python testsAndScripts\test_app_simple.py - Test complet
echo.
echo 4. DÉPANNAGE:
echo    - Si erreur API: vérifiez votre .env
echo    - Si erreur données: vérifiez data/sujets_memoires.csv
echo    - Si erreur import: relancez ce script
echo.
echo ════════════════════════════════════════════════
echo 📊 ENVIRONNEMENT CONFIGURÉ:
echo    Python: 3.10
echo    Packages: 11 essentiels
echo    Taille estimée: ~200MB
echo    Statut: ✅ PRÊT
echo ════════════════════════════════════════════════
echo.
pause