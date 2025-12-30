"""
Application Streamlit principale - Système de Recommandation Intelligent
"""
import streamlit as st
import pandas as pd
import time
from utils.data_loader import load_subjects, filter_by_department, filter_by_level
from utils.embeddings import EmbeddingManager
from utils.recommender import RecommenderSystem
import os

# Configuration de la page
st.set_page_config(
    page_title="Recommandation de Sujets de Mémoire",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #374151;
        margin-top: 1.5rem;
    }
    .recommendation-box {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #3B82F6;
    }
    .stButton button {
        background-color: #3B82F6;
        color: white;
        font-weight: bold;
        width: 100%;
    }
    .info-box {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #93C5FD;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de l'état de session
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'student_level' not in st.session_state:
    st.session_state.student_level = "intermédiaire"

def initialize_system():
    """Initialise le système de recommandation"""
    with st.spinner("🔄 Initialisation du système intelligent..."):
        # Charger les données
        st.session_state.df = load_subjects()
        
        # Initialiser le gestionnaire d'embeddings
        st.session_state.embedding_manager = EmbeddingManager()
        
        # Préparer les métadonnées pour ChromaDB
        texts = st.session_state.df['texte_complet'].tolist()
        metadatas = st.session_state.df[['departement', 'niveau']].to_dict('records')
        
        # Créer les embeddings
        st.session_state.collection = st.session_state.embedding_manager.create_embeddings(
            texts=texts,
            metadatas=metadatas
        )
        
        # Initialiser le système de recommandation
        groq_api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        if not groq_api_key:
            st.error("⚠️ Clé API Groq manquante. Veuillez configurer GROQ_API_KEY")
            st.stop()
        
        st.session_state.recommender = RecommenderSystem(groq_api_key=groq_api_key)
        
        st.session_state.initialized = True
        st.success("✅ Système initialisé avec succès!")

# Interface principale
st.markdown('<h1 class="main-header">🎓 Système Intelligent de Recommandation de Sujets de Mémoire</h1>', unsafe_allow_html=True)

# Barre latérale pour la configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # Section d'information
    with st.expander("ℹ️ À propos du système", expanded=True):
        st.info("""
        **Fonctionnalités:**
        - 📚 Base de 100+ sujets de mémoire
        - 🧠 IA avec LLaMA 3 (Groq)
        - 🔍 Recherche sémantique avancée
        - 🎯 Recommandations personnalisées
        
        **Départements supportés:**
        - Génie Informatique
        - Génie Civil
        - Génie Électrique
        - Génie Électronique
        - Génie Mécanique
        """)
    
    # Sélection du niveau
    st.session_state.student_level = st.selectbox(
        "🎓 Ton niveau académique",
        ["débutant", "intermédiaire"],
        index=1
    )
    
    # Filtre par département
    departments = st.multiselect(
        "🏫 Départements cibles (optionnel)",
        ["Génie Informatique", "Génie Civil", "Génie Électrique", "Génie Électronique", "Génie Mécanique"],
        default=["Génie Informatique"]
    )
    
    # Bouton d'initialisation
    if not st.session_state.initialized:
        if st.button("🚀 Initialiser le système", type="primary"):
            initialize_system()
    else:
        st.success("✅ Système prêt")
        
        # Aperçu des données
        with st.expander("📊 Aperçu des données"):
            filtered_df = filter_by_department(st.session_state.df, departments)
            filtered_df = filter_by_level(filtered_df, st.session_state.student_level)
            
            st.metric("Sujets disponibles", len(filtered_df))
            
            if len(filtered_df) > 0:
                st.dataframe(
                    filtered_df[['titre', 'departement', 'niveau']].head(10),
                    use_container_width=True
                )

# Section principale
if not st.session_state.initialized:
    st.markdown("""
    <div class="info-box">
    <h4>👋 Bienvenue dans le système de recommandation!</h4>
    <p>Pour commencer, cliquez sur <b>"Initialiser le système"</b> dans la barre latérale.</p>
    <p>Le système va charger les sujets de mémoire et préparer l'IA pour vos recommandations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Exemples de requêtes
    st.markdown("### 💡 Exemples de requêtes:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Pour débutants:**
        - "Je veux un sujet simple en programmation"
        - "Projet IoT pas trop complexe"
        - "Application mobile éducative"
        """)
    
    with col2:
        st.markdown("""
        **Pour intermédiaires:**
        - "Sujet en cybersécurité"
        - "Machine learning appliqué"
        - "Optimisation de systèmes"
        """)
    
    with col3:
        st.markdown("""
        **Par domaine:**
        - "Intelligence artificielle"
        - "Développement web"
        - "Automatisation industrielle"
        """)
    
else:
    # Interface de requête
    st.markdown('<h2 class="sub-header">💬 Décris ton projet de mémoire</h2>', unsafe_allow_html=True)
    
    # Exemples rapides
    example_queries = [
        "Je veux un sujet en intelligence artificielle pour débutant",
        "Recherche sur la cybersécurité des systèmes industriels",
        "Développement d'une application mobile innovante",
        "Optimisation énergétique dans les bâtiments intelligents"
    ]
    
    cols = st.columns(4)
    for idx, example in enumerate(example_queries):
        with cols[idx]:
            if st.button(example[:40] + "...", key=f"example_{idx}"):
                st.session_state.user_query = example
    
    # Zone de texte pour la requête
    user_query = st.text_area(
        "Décris tes intérêts, ton niveau, et le domaine souhaité:",
        value=st.session_state.get('user_query', ''),
        height=100,
        placeholder="Ex: 'Je suis débutant en informatique et je m'intéresse à la programmation Python pour créer une application utile...'"
    )
    
    # Bouton de recommandation
    if st.button("🎯 Générer les recommandations", type="primary"):
        if user_query.strip():
            with st.spinner("🧠 Analyse de ta requête et recherche des sujets pertinents..."):
                # Filtrer les données
                filtered_df = filter_by_department(st.session_state.df, departments)
                filtered_df = filter_by_level(filtered_df, st.session_state.student_level)
                
                # Recherche sémantique
                results = st.session_state.embedding_manager.search_similar(
                    query=user_query,
                    collection=st.session_state.collection,
                    n_results=10,
                    filters={"niveau": st.session_state.student_level} if st.session_state.student_level != "intermédiaire" else None
                )
                
                if results and results['documents']:
                    # Préparer le contexte pour l'IA
                    context_docs = []
                    for i in range(len(results['documents'][0])):
                        # Trouver le document correspondant dans le DataFrame
                        doc_text = results['documents'][0][i]
                        # Rechercher le document dans le DataFrame (méthode simplifiée)
                        for _, row in filtered_df.iterrows():
                            if row['texte_complet'] in doc_text:
                                context_docs.append({
                                    'titre': row['titre'],
                                    'resume': row['resume'],
                                    'departement': row['departement'],
                                    'niveau': row['niveau']
                                })
                                break
                    
                    # Générer les recommandations
                    start_time = time.time()
                    recommendations = st.session_state.recommender.generate_recommendations(
                        query=user_query,
                        context=context_docs[:5],  # Prendre les 5 plus pertinents
                        student_level=st.session_state.student_level
                    )
                    generation_time = time.time() - start_time
                    
                    # Stocker les résultats
                    st.session_state.recommendations = recommendations
                    st.session_state.generation_time = generation_time
                    st.session_state.user_query = user_query
                    
                    st.success(f"✅ Recommandations générées en {generation_time:.2f} secondes!")
                else:
                    st.error("❌ Aucun sujet trouvé. Essayez d'élargir vos critères.")
        else:
            st.warning("⚠️ Veuillez décrire votre projet avant de générer des recommandations.")
    
    # Afficher les recommandations si disponibles
    if st.session_state.recommendations:
        st.markdown("---")
        st.markdown(f"### 📋 Résultats pour: *{st.session_state.user_query}*")
        
        # Afficher l'analyse
        with st.expander("🔍 Analyse de ta requête"):
            analysis = st.session_state.recommender.analyze_student_query(st.session_state.user_query)
            st.write(analysis)
        
        # Afficher les recommandations
        st.markdown(st.session_state.recommendations)
        
        # Options supplémentaires
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Générer de nouvelles suggestions"):
                st.session_state.recommendations = None
                st.rerun()
        
        with col2:
            if st.button("💾 Exporter les recommandations"):
                # Créer un texte exportable
                export_text = f"""
                RECOMMANDATIONS DE SUJETS DE MÉMOIRE
                =====================================
                
                Requête: {st.session_state.user_query}
                Niveau: {st.session_state.student_level}
                Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}
                
                {st.session_state.recommendations}
                """
                
                st.download_button(
                    label="📥 Télécharger",
                    data=export_text,
                    file_name=f"recommandations_memoire_{pd.Timestamp.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
    
    # Section d'information sur le fonctionnement
    with st.expander("🔧 Comment fonctionne le système?"):
        st.markdown("""
        ### Architecture RAG (Retrieval-Augmented Generation)
        
        1. **Chargement des données**: 100+ sujets de mémoire réels
        2. **Embeddings**: Conversion en vecteurs numériques (Sentence-Transformers)
        3. **Stockage vectoriel**: ChromaDB pour une recherche rapide
        4. **Recherche sémantique**: Trouve les sujets les plus proches de ta requête
        5. **Génération IA**: LLaMA 3 adapte et personnalise les recommandations
        
        ### Avantages:
        - ✅ **Personnalisé**: Adapté à ton niveau et intérêts
        - ✅ **Rapide**: Réponses en quelques secondes
        - ✅ **Pertinent**: Basé sur de vrais sujets traités
        - ✅ **Gratuit**: Utilise des technologies open-source
        """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6B7280;'>"
    "🎓 Projet de Génie Informatique - Système Intelligent de Recommandation - "
    "Utilise LLaMA 3 via Groq & ChromaDB"
    "</div>",
    unsafe_allow_html=True
)