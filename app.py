# app.py - Version complète avec Google Gemma 3
"""
Application Streamlit principale - Système de Recommandation Intelligent
Version finale avec Google Gemma 3 (gemma-3-4b-it)
"""
import streamlit as st
import pandas as pd
import time
import os
from dotenv import load_dotenv
from utils.data_loader import load_subjects
from utils.embeddings import EmbeddingManager
from utils.recommender import RecommenderSystem  # Version Gemma 3

from fpdf import FPDF
from fpdf.enums import XPos, YPos

def create_pdf(recommendation_text, student_name="Étudiant"):
    # Initialisation (Helvetica remplace Arial par défaut pour éviter les warnings)
    pdf = FPDF()
    pdf.add_page()
    
    # Titre du rapport
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(190, 10, "Rapport d'Orientation Académique - FST", 
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(10)
    
    # Infos étudiant
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(190, 10, f"Destinataire : {student_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(190, 10, f"Date : {time.strftime('%d/%m/%Y')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    # Contenu de la recommandation
    pdf.set_font("Helvetica", "", 11)
    
    # Nettoyage des caractères spéciaux (latin-1)
    # Important : latin-1 ne supporte pas tous les emojis, on les remplace par du texte ou on les ignore
    clean_text = recommendation_text.replace('📘', '').replace('🎯', '-').replace('✅', 'OK').replace('⚙️', '*')
    clean_text = clean_text.encode('latin-1', 'ignore').decode('latin-1')
    
    pdf.multi_cell(0, 8, clean_text)
    
    # Sortie en bytes (La nouvelle syntaxe retire le paramètre 'dest')
    return pdf.output()

# Configuration de la page
st.set_page_config(
    page_title="Recommandation de Sujets de Mémoire",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# STYLE CSS AVANCÉ
# ============================================================================
st.markdown("""
<style>
    /* Thème principal */
    :root {
        --primary-color: #3B82F6;
        --secondary-color: #10B981;
        --accent-color: #8B5CF6;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --bg-primary: #FFFFFF;
        --bg-secondary: #F9FAFB;
        --border-color: #E5E7EB;
    }
    
    /* Mode sombre */
    @media (prefers-color-scheme: dark) {
        :root {
            --text-primary: #F9FAFB;
            --text-secondary: #D1D5DB;
            --bg-primary: #111827;
            --bg-secondary: #1F2937;
            --border-color: #374151;
        }
    }
    
    /* Header avec animation */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1rem;
        animation: fadeIn 1s ease-in;
    }
    
    /* Animation d'entrée */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Card moderne */
    .card {
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Bouton primaire */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Zone de texte */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid var(--border-color);
        padding: 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Tags pour départements */
    .department-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
        color: var(--text-primary);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.9rem;
        border: 1px solid var(--border-color);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .department-tag:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: scale(1.05);
    }
    
    /* Recommendations */
    .recommendation-item {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid var(--primary-color);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Spinner personnalisé */
    .stSpinner > div {
        border-color: var(--primary-color) transparent transparent transparent;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: var(--text-secondary);
        font-size: 0.9rem;
        border-top: 1px solid var(--border-color);
        margin-top: 3rem;
    }
    
    /* Badge IA */
    .ai-badge {
        display: inline-block;
        background: linear-gradient(135deg, #FF6B6B, #EE5A24);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALISATION DE SESSION
# ============================================================================
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'student_level' not in st.session_state:
    st.session_state.student_level = "intermédiaire"
if 'selected_departments' not in st.session_state:
    st.session_state.selected_departments = ["Génie Informatique"]
if 'api_initialized' not in st.session_state:
    st.session_state.api_initialized = False

## ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================
@st.cache_resource
def initialize_system():
    """Initialise le système de recommandation avec Google Gemma 3"""
    with st.spinner("🔄 Initialisation du système intelligent..."):
        try:
            # 1. Gestion hybride de la clé API (Local .env vs Streamlit Cloud Secrets)
            load_dotenv() # Tente de charger le .env local
            
            # On cherche dans st.secrets (Cloud) puis dans os.getenv (.env local)
            api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
            
            if not api_key:
                st.error("""
                ❌ Clé API Google non trouvée !
                
                **En local :** Vérifiez votre fichier `.env`.
                **Sur le Cloud :** Ajoutez `GOOGLE_API_KEY` dans les Secrets de votre application.
                """)
                return None, None, None, None
            
            # 2. Chargement des données (CSV)
            # Utilise un chemin relatif robuste
            csv_path = os.path.join(os.path.dirname(__file__), "data/sujets_memoires.csv")
            df = load_subjects(csv_path)
            
            if df.empty:
                st.error("❌ Base de données des sujets vide ou introuvable.")
                return None, None, None, None
            
            # 3. Initialisation des composants NLP
            embedding_manager = EmbeddingManager()
            
            # Préparation des données pour ChromaDB
            texts = df['texte_complet'].tolist()
            metadatas = df[['departement', 'niveau']].to_dict('records')
            
            collection = embedding_manager.create_embeddings(
                texts=texts,
                metadatas=metadatas
            )
            
            # 4. Initialisation du Recommender avec la clé récupérée
            recommender = RecommenderSystem(api_key=api_key)
            
            st.session_state.api_initialized = True
            return df, embedding_manager, collection, recommender
            
        except Exception as e:
            st.error(f"❌ Erreur critique lors de l'initialisation : {str(e)}")
            return None, None, None, None

# Classe de démo fallback
class DemoRecommender:
    """Recommandateur de démo en cas d'erreur API"""
    def generate_recommendations(self, query, context, student_level="intermédiaire"):
        import random
        subjects = [
            "Application web éducative avec Django",
            "Système de recommandation intelligent avec Python",
            "Application mobile de gestion avec Flutter",
            "Analyse de données avec machine learning",
            "Site e-commerce moderne avec React",
            "Chatbot conversationnel avec IA",
            "Système IoT domestique avec Arduino",
            "Jeu éducatif mobile avec Unity"
        ]
        
        selected = random.sample(subjects, 3)
        
        return f"""
        📘 **RECOMMANDATIONS PERSONNALISÉES** (Mode démo)
        
        🎯 **Demande:** {query}
        📊 **Niveau:** {student_level}
        ⚠️ **Note:** Mode démo (l'API rencontre des limitations)
        
        🔵 **1. {selected[0]}**
           📍 Département: Génie Informatique
           🎯 Objectif pédagogique: Développer un projet complet avec les technologies modernes
           ⚙️ Technologies: Adaptées au niveau {student_level}
           ✅ Pourquoi ce sujet: Excellente introduction pratique aux concepts fondamentaux
        
        🟢 **2. {selected[1]}**
           📍 Département: Génie Informatique
           🎯 Objectif pédagogique: Acquérir des compétences en développement logiciel
           ⚙️ Technologies: Adaptées au niveau {student_level}
           ✅ Pourquoi ce sujet: Projet concret avec résultats mesurables
        
        🟡 **3. {selected[2]}**
           📍 Département: Génie Informatique
           🎯 Objectif pédagogique: Maîtriser un domaine spécifique de l'informatique
           ⚙️ Technologies: Adaptées au niveau {student_level}
           ✅ Pourquoi ce sujet: Permet de se spécialiser dans un domaine porteur
        
        💡 *Pour des recommandations personnalisées avec IA, assurez-vous que l'API Google est configurée correctement.*
        """

# ============================================================================
# INTERFACE PRINCIPALE
# ============================================================================

# Header principal
st.markdown('<h1 class="main-header">🎓 Assistant Intelligent de Sujets de Mémoire</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: var(--text-secondary); margin-bottom: 2rem;">Powered by Google Gemma 3 AI <span class="ai-badge">🤖 IA</span></p>', unsafe_allow_html=True)

# Barre latérale
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # Sélection du niveau
    st.session_state.student_level = st.selectbox(
        "**Niveau académique**",
        ["débutant", "intermédiaire", "avancé"],
        index=1,
        help="Sélectionnez votre niveau actuel"
    )
    
    # Sélection des départements
    all_departments = ["Génie Informatique", "Génie Civil", "Génie Électrique", 
                       "Génie Électronique", "Génie Mécanique", "Tous départements"]
    
    st.markdown("**Départements d'intérêt**")
    
    selected_tags = []
    for dept in all_departments:
        if dept == "Tous départements":
            if st.checkbox("Tous départements", value=False, key="all_depts"):
                selected_tags = all_departments[:-1]  # Exclure "Tous départements"
                break
        else:
            if st.checkbox(dept, value=(dept == "Génie Informatique"), key=f"dept_{dept}"):
                selected_tags.append(dept)
    
    if not selected_tags and "Tous départements" not in selected_tags:
        selected_tags = ["Génie Informatique"]
    
    st.session_state.selected_departments = selected_tags
    
    # Information système
    with st.expander("ℹ️ À propos du système", expanded=False):
        st.info("""
        **Technologie utilisée :**
        - 🤖 Google Gemma 3 (gemma-3-4b-it)
        - 🔍 Recherche sémantique avancée
        - 🎯 Recommandations personnalisées
        - 🇫🇷 Interface en français
        
        **Comment ça marche :**
        1. Décrivez vos intérêts
        2. Le système analyse votre demande
        3. Génère 3 sujets adaptés
        4. Propose un accompagnement complet
        """)
        
    if st.button("🔄 Réinitialiser", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key not in ['initialized', 'api_initialized']:
                del st.session_state[key]
        st.rerun()

# Initialisation automatique
if not st.session_state.initialized:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>👋 Bienvenue dans l'Assistant IA !</h3>
            <p>Je suis votre conseiller académique intelligent.</p>
            <p>Je vais vous aider à trouver le sujet de mémoire parfait.</p>
            <div style="margin: 1.5rem 0;">
                <div class="ai-badge" style="margin: 0.5rem;">Google Gemma 3</div>
                <div class="ai-badge" style="background: linear-gradient(135deg, #3B82F6, #1D4ED8); margin: 0.5rem;">IA Gratuite</div>
                <div class="ai-badge" style="background: linear-gradient(135deg, #10B981, #059669); margin: 0.5rem;">Français</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Initialiser le système
    with st.spinner("🚀 Initialisation du moteur IA..."):
        system_data = initialize_system()
    
    if system_data[0] is not None:
        df, embedding_manager, collection, recommender = system_data
        st.session_state.df = df
        st.session_state.embedding_manager = embedding_manager
        st.session_state.collection = collection
        st.session_state.recommender = recommender
        st.session_state.initialized = True
        st.success("✅ Système initialisé avec succès !")
        time.sleep(1)
        st.rerun()
    else:
        st.error("""
        ❌ Échec de l'initialisation
        
        **Solutions possibles :**
        1. Vérifiez votre fichier `.env` avec la clé API Google
        2. Assurez-vous que le fichier `data/sujets_memoires.csv` existe
        3. Vérifiez votre connexion internet
        """)
        
        # Mode démo optionnel
        if st.button("🎮 Activer le mode démonstration", type="secondary"):
            st.session_state.initialized = True
            st.session_state.demo_mode = True
            st.session_state.recommender = DemoRecommender()
            st.session_state.df = pd.DataFrame({
                'titre': ['Sujet démo 1', 'Sujet démo 2'],
                'departement': ['Génie Informatique'],
                'niveau': ['intermédiaire'],
                'texte_complet': ['Contenu démonstration']
            })
            st.rerun()
        
        st.stop()

# ============================================================================
# SECTION DE REQUÊTE PRINCIPALE
# ============================================================================

# Présentation
st.markdown("""
<div class="card">
    <h3>💡 Décrivez votre projet idéal</h3>
    <p>Parlez-moi de vos intérêts, compétences et aspirations. Je vais analyser votre profil et vous proposer <strong>3 sujets personnalisés</strong>.</p>
</div>
""", unsafe_allow_html=True)

# Exemples rapides
st.markdown("**💡 Besoin d'inspiration ? Essayez ces exemples :**")
example_cols = st.columns(4)
examples = [
    {"text": "IA pour débutant", "icon": "🤖"},
    {"text": "Cybersécurité web", "icon": "🔐"},
    {"text": "Application mobile", "icon": "📱"},
    {"text": "IoT intelligent", "icon": "🌐"}
]

for idx, example in enumerate(examples):
    with example_cols[idx]:
        if st.button(
            f"{example['icon']} {example['text']}",
            key=f"ex_{idx}",
            use_container_width=True,
            type="secondary"
        ):
            st.session_state.preset_query = example['text']

# Zone de texte principale
user_query = st.text_area(
    "**Parlez-moi de votre projet :**",
    value=st.session_state.get('preset_query', ''),
    height=150,
    placeholder="Exemple : 'Je suis en informatique, intéressé par l\'IA et le machine learning. J\'aimerais un sujet pas trop complexe mais qui me permette d\'apprendre Python et les bases de l\'intelligence artificielle. J\'ai déjà des notions en programmation.'",
    key="main_query",
    label_visibility="collapsed"
)

# Bouton de génération
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_btn = st.button(
        "🚀 Générer mes recommandations IA",
        type="primary",
        use_container_width=True,
        disabled=not user_query.strip()
    )

# ============================================================================
# TRAITEMENT ET AFFICHAGE DES RÉSULTATS
# ============================================================================

if generate_btn and user_query.strip():
    with st.spinner("🧠 L'IA analyse votre demande..."):
        try:
            # Préparer la recherche
            if hasattr(st.session_state, 'df'):
                # Filtrer par départements
                if st.session_state.selected_departments and "Tous départements" not in st.session_state.selected_departments:
                    filtered_df = st.session_state.df[
                        st.session_state.df['departement'].isin(st.session_state.selected_departments)
                    ]
                else:
                    filtered_df = st.session_state.df
                
                # Recherche sémantique
                results = st.session_state.embedding_manager.search_similar(
                    query=user_query,
                    collection=st.session_state.collection,
                    n_results=6,
                    filters={"niveau": st.session_state.student_level} if st.session_state.student_level != "intermédiaire" else None
                )
                
                # Préparer le contexte
                context_docs = []
                if results and results['documents']:
                    for i in range(min(4, len(results['documents'][0]))):
                        doc_text = results['documents'][0][i]
                        # Chercher correspondance dans les données
                        match_found = False
                        for _, row in filtered_df.iterrows():
                            if row['texte_complet'] in doc_text:
                                context_docs.append({
                                    'titre': row['titre'],
                                    'resume': row.get('resume', ''),
                                    'departement': row['departement'],
                                    'niveau': row['niveau']
                                })
                                match_found = True
                                break
                        
                        # Si pas de correspondance exacte, utiliser le texte brut
                        if not match_found and i < 3:
                            context_docs.append({
                                'titre': f"Sujet référence {i+1}",
                                'resume': doc_text[:200] + "...",
                                'departement': "Génie Informatique",
                                'niveau': st.session_state.student_level
                            })
                
                # Si pas assez de résultats, prendre des sujets aléatoires
                if len(context_docs) < 2:
                    context_docs = filtered_df.sample(min(3, len(filtered_df))).to_dict('records')
            
            else:
                # Mode sans données
                context_docs = [
                    {
                        'titre': 'Projets académiques références',
                        'departement': 'Génie Informatique',
                        'niveau': st.session_state.student_level
                    }
                ]
            
            # Barre de progression
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("🔍 Analyse de votre demande...")
                elif i < 60:
                    status_text.text("🤖 Consultation de la base de connaissances...")
                elif i < 90:
                    status_text.text("🎯 Génération des recommandations...")
                else:
                    status_text.text("✅ Finalisation...")
                time.sleep(0.02)
            
            status_text.text("✨ Recommandations prêtes !")
            time.sleep(0.5)
            
            # Générer les recommandations
            start_time = time.time()
            
            if hasattr(st.session_state, 'recommender'):
                recommendations = st.session_state.recommender.generate_recommendations(
                    query=user_query,
                    context=context_docs,
                    student_level=st.session_state.student_level
                )
            else:
                # Mode démo
                recommendations = DemoRecommender().generate_recommendations(
                    query=user_query,
                    context=context_docs,
                    student_level=st.session_state.student_level
                )
            
            generation_time = time.time() - start_time
            
            # Stocker les résultats
            st.session_state.recommendations = recommendations
            st.session_state.generation_time = generation_time
            st.session_state.user_query = user_query
            st.session_state.context_used = context_docs
            
            progress_bar.empty()
            status_text.empty()
            
            st.success(f"✅ Recommandations générées en {generation_time:.1f} secondes")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération: {str(e)}")
            
            # Fallback vers le mode démo
            st.info("🔄 Activation du mode de secours...")
            st.session_state.recommendations = DemoRecommender().generate_recommendations(
                query=user_query,
                context=[],
                student_level=st.session_state.student_level
            )
            st.session_state.user_query = user_query

# --- BLOC D'AFFICHAGE DES RÉSULTATS ---
if st.session_state.get('recommendations'):
    st.markdown("---")
    
    # Header des résultats
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.markdown(f"### 📋 Vos recommandations personnalisées")
        
        # Afficher le contexte (Expander pour ne pas encombrer l'écran)
        with st.expander("🔍 Voir les critères de recherche", expanded=False):
            st.markdown(f"""
            **Niveau cible :** {st.session_state.student_level}  
            **Départements sélectionnés :** {', '.join(st.session_state.selected_departments)}  
            **Votre requête :** "{st.session_state.user_query}"
            """)
            
            if st.session_state.get('context_used'):
                st.markdown("**Sujets de référence analysés dans la base :**")
                for doc in st.session_state.context_used[:3]:
                    st.markdown(f"- {doc.get('titre', 'Sujet')} *({doc.get('departement', 'Génie')})*")
    
    with col_header2:
        if st.button("🔄 Nouvelle recherche", use_container_width=True, type="secondary"):
            st.session_state.recommendations = None
            # On garde l'historique mais on réinitialise la recherche actuelle
            st.rerun()
    
    # Zone d'affichage de la recommandation (Style "Card")
    st.info("💡 Analyse de l'IA Gemma 3 terminée avec succès.")
    st.markdown(st.session_state.recommendations)
    
    # --- SECTION EXPORT ---
    st.markdown("---")
    st.markdown("### 📤 Exporter vos résultats")
    
    col_export1, col_export2, col_export3 = st.columns(3)
    
    # 1. BOUTON PDF (Logique Réelle)
    with col_export1:
        try:
            # On utilise la fonction create_pdf définie plus tôt
            # Note : Assure-toi que la fonction create_pdf est bien dans ton code
            pdf_bytes = create_pdf(st.session_state.recommendations, st.session_state.get('user_name', 'Étudiant FST'))
            
            st.download_button(
                label="📄 Télécharger en PDF",
                data=pdf_bytes,
                file_name=f"Rapport_Orientation_{pd.Timestamp.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error("Erreur génération PDF")

    # 2. BOUTON TEXTE (.txt)
    with col_export2:
        export_text = f"""
        RECOMMANDATIONS DE SUJETS DE MÉMOIRE - FST
        {'=' * 60}
        Date : {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}
        Niveau : {st.session_state.student_level}
        Départements : {', '.join(st.session_state.selected_departments)}
        
        REQUÊTE : {st.session_state.user_query}
        
        {'-' * 60}
        {st.session_state.recommendations}
        {'-' * 60}
        
        Généré par l'Assistant IA (Gemma 3) - Faculté des Sciences et Technologies
        """
        
        st.download_button(
            label="📝 Télécharger (.txt)",
            data=export_text,
            file_name=f"sujets_memoire_{pd.Timestamp.now().strftime('%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # 3. BOUTON FAVORIS (Logique Session)
    with col_export3:
        if st.button("⭐ Ajouter aux favoris", use_container_width=True):
            if 'favorites' not in st.session_state:
                st.session_state.favorites = []
            
            # On sauvegarde un petit dictionnaire
            fav = {
                "date": pd.Timestamp.now().strftime('%d/%m/%Y'),
                "query": st.session_state.user_query,
                "content": st.session_state.recommendations
            }
            st.session_state.favorites.append(fav)
            st.success("✅ Ajouté à votre profil !")
# ============================================================================
# SECTION D'INFORMATION
# ============================================================================
st.markdown("---")

with st.expander("🤖 En savoir plus sur la technologie utilisée", expanded=False):
    st.markdown("""
    ### 🧠 Google Gemma 3 - Intelligence Artificielle Avancée
    
    Ce système utilise **Google Gemma 3 (gemma-3-4b-it)**, un modèle d'IA open-source performant développé par Google.
    
    **Caractéristiques techniques :**
    - ✅ **Entièrement gratuit** - Pas de limitations de crédits
    - 🚀 **Rapide et efficace** - Génération en quelques secondes
    - 🇫🇷 **Excellente compréhension du français** - Spécialement optimisé
    - 🎯 **Précis et contextuel** - Comprend les nuances académiques
    
    **Architecture RAG (Retrieval-Augmented Generation) :**
    1. **Recherche sémantique** - Trouve les sujets pertinents dans la base
    2. **Analyse contextuelle** - Comprend votre niveau et intérêts
    3. **Génération adaptative** - Crée des recommandations uniques
    4. **Validation académique** - Assure la faisabilité des sujets
    
    **Pour les étudiants :**
    - Suggestions personnalisées selon votre profil
    - Sujets adaptés à votre niveau et durée de projet
    - Technologies modernes et pertinentes
    - Objectifs pédagogiques clairs
    """)

# Footer
st.markdown("""
<div class="footer">
    <p>🎓 <strong>Système Intelligent de Recommandation de Sujets de Mémoire</strong></p>
    <p>Faculté des Sciences et Technologies - Assistant IA Académique</p>
    <p style="font-size: 0.8rem; opacity: 0.7;">
        Technologie Google Gemma 3 • Recherche sémantique avancée • Interface française
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MODE DÉVELOPPEMENT
# ============================================================================
if os.getenv("DEBUG_MODE", "false").lower() == "true":
    if st.button("🔧 Mode développeur : Purger le cache", type="secondary"):
        st.cache_resource.clear()
        st.success("Cache vidé !")
        st.rerun()