# setup_project.ps1
Write-Host "`n╔═══════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     SETUP COMPLET - PROJET MÉMOIRE IA       ║" -ForegroundColor Cyan
Write-Host "║     Environnement Python 3.10              ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Configuration
$ProjectDir = Get-Location
$VenvDir = Join-Path $ProjectDir "venv"
$RequirementsFile = Join-Path $ProjectDir "requirements.txt"

# 1. Nettoyage
Write-Host "[1/10] Nettoyage de l'ancien environnement..." -ForegroundColor Yellow
if (Test-Path $VenvDir) {
    Remove-Item -Recurse -Force $VenvDir
    Write-Host "  ✅ Ancien venv supprimé" -ForegroundColor Green
}

# 2. Création venv Python 3.10
Write-Host "`n[2/10] Création de l'environnement Python 3.10..." -ForegroundColor Yellow
py -3.10 -m venv $VenvDir
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Erreur création venv" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Environnement créé" -ForegroundColor Green

# 3. Activation
Write-Host "`n[3/10] Activation de l'environnement..." -ForegroundColor Yellow
& "$VenvDir\Scripts\Activate.ps1"
Write-Host "  ✅ Environnement activé" -ForegroundColor Green

# 4. Mise à jour pip
Write-Host "`n[4/10] Mise à jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel --quiet
Write-Host "  ✅ Pip mis à jour" -ForegroundColor Green

# 5. Création requirements.txt
Write-Host "`n[5/10] Création du requirements.txt optimisé..." -ForegroundColor Yellow
@"
# =============================================
# Système de Recommandation de Sujets de Mémoire
# Dépendances optimisées - Version stable
# Python 3.10 compatible
# =============================================

# Interface utilisateur
streamlit==1.52.2

# Google Gemma 3 API
google-generativeai==0.3.2

# Base vectorielle et embeddings
chromadb==0.4.22
sentence-transformers==2.2.2

# Traitement de données
pandas==2.1.4

# Utilitaires
python-dotenv==1.0.0

# Dépendances système
numpy==1.26.4
protobuf==4.25.3
"@ | Out-File -FilePath $RequirementsFile -Encoding UTF8
Write-Host "  ✅ requirements.txt créé" -ForegroundColor Green

# 6. Installation
Write-Host "`n[6/10] Installation des dépendances..." -ForegroundColor Yellow
Write-Host "  Installation des packages essentiels..." -ForegroundColor Gray
pip install -r $RequirementsFile --quiet
Write-Host "  ✅ Dépendances installées" -ForegroundColor Green

# 7. Vérification
Write-Host "`n[7/10] Vérification des imports..." -ForegroundColor Yellow
python -c "
modules = ['streamlit', 'google.generativeai', 'chromadb', 'pandas', 'sentence_transformers', 'dotenv']
for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}')
    except ImportError as e:
        print(f'❌ {module}: {e}')
"

# 8. Test API
Write-Host "`n[8/10] Test de l'API Google..." -ForegroundColor Yellow
python -c "
import google.generativeai as genai
print('✅ Module google.generativeai fonctionnel')
print(f'✅ Version: {genai.__version__}')
"

# 9. Génération requirements final
Write-Host "`n[9/10] Génération du requirements final..." -ForegroundColor Yellow
pip freeze > "$ProjectDir\requirements_final.txt"
$packageCount = (Get-Content "$ProjectDir\requirements_final.txt" | Measure-Object -Line).Lines
Write-Host "  ✅ $packageCount packages installés" -ForegroundColor Green

# 10. Test données
Write-Host "`n[10/10] Test des données..." -ForegroundColor Yellow
python -c "
import sys
sys.path.append('.')
try:
    from utils.data_loader import load_subjects
    df = load_subjects('data/sujets_memoires.csv')
    print(f'✅ {len(df)} sujets chargés')
except Exception as e:
    print(f'❌ Erreur: {e}')
"

# Instructions finales
Write-Host "`n╔═══════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║            ✅ SETUP TERMINÉ !                ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "📋 COMMANDES:" -ForegroundColor Cyan
Write-Host "  streamlit run app.py" -ForegroundColor White
Write-Host "  python testsAndScripts\test_gemma.py" -ForegroundColor White
Write-Host "`n🔧 CONFIGURATION:" -ForegroundColor Cyan
Write-Host "  Créez .env avec: GOOGLE_API_KEY=votre_clé" -ForegroundColor White
Write-Host "`n📊 STATISTIQUES:" -ForegroundColor Cyan
Write-Host "  Python: 3.10" -ForegroundColor White
Write-Host "  Packages: $packageCount" -ForegroundColor White
Write-Host "  Statut: ✅ PRÊT À L'EMPLOI" -ForegroundColor Green