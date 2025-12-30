"""
Module de recommandation intelligente utilisant RAG avec LangChain
"""
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class RecommenderSystem:
    def __init__(self, groq_api_key=None):
        """
        Initialise le système de recommandation avec LangChain et Groq
        """
        # Utiliser la clé API fournie ou celle de l'environnement
        self.api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ Clé API Groq manquante. Veuillez fournir GROQ_API_KEY dans .env")
        
        # Initialiser le modèle LLaMA 3 via Groq
        print("🧠 Initialisation du modèle LLaMA 3 via Groq...")
        self.llm = ChatGroq(
            temperature=0.7,
            groq_api_key=self.api_key,
            model_name="llama3-70b-8192"  # Modèle gratuit et performant
        )
        
        # Template du prompt pour la recommandation
        self.recommendation_prompt = PromptTemplate(
            input_variables=["query", "context", "student_level"],
            template="""
            Tu es un assistant académique spécialisé dans la recommandation de sujets de mémoire.
            
            CONTEXTE (anciens sujets de mémoire):
            {context}
            
            REQUÊTE DE L'ÉTUDIANT:
            {query}
            
            NIVEAU DE L'ÉTUDIANT:
            {student_level}
            
            TÂCHE:
            Analyse la requête de l'étudiant et recommande EXACTEMENT 3 sujets de mémoire pertinents.
            
            RÈGLES STRICTES:
            1. Propose EXACTEMENT 3 sujets différents
            2. Adapte les recommandations au niveau spécifié ({student_level})
            3. Pour chaque sujet, fournis:
               - Titre proposé (basé sur les sujets existants mais adapté)
               - Département concerné
               - Brève justification (1-2 phrases)
               - Adaptation au niveau de l'étudiant
            4. Réponds UNIQUEMENT en français
            5. Sois créatif mais réaliste
            
            FORMAT DE RÉPONSE:
            📘 **RECOMMANDATIONS PERSONNALISÉES**
            
            🎯 **Sujet 1: [Titre]**
            📍 Département: [Département]
            ✅ Pourquoi ce sujet: [Justification]
            🎓 Adaptation niveau: [Adaptation au niveau]
            
            🔁 Répète ce format pour les 3 sujets
            
            COMMENCE TA RÉPONSE DIRECTEMENT AVEC "📘 **RECOMMANDATIONS PERSONNALISÉES**"
            """
        )
        
        # Initialiser la chaîne LangChain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.recommendation_prompt,
            verbose=False
        )
    
    def generate_recommendations(self, query, context, student_level="intermédiaire"):
        """
        Génère des recommandations personnalisées
        """
        try:
            print(f"🤔 Génération de recommandations pour: '{query}'")
            
            # Préparer le contexte formaté
            context_str = "\n\n".join([
                f"Titre: {doc['titre']}\n"
                f"Résumé: {doc['resume']}\n"
                f"Département: {doc['departement']}\n"
                f"Niveau: {doc['niveau']}"
                for doc in context
            ])
            
            # Exécuter la chaîne
            response = self.chain.run(
                query=query,
                context=context_str,
                student_level=student_level
            )
            
            return response
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
            return f"Erreur: {str(e)}"
    
    def analyze_student_query(self, query):
        """
        Analyse la requête de l'étudiant pour extraire des informations clés
        """
        analysis_prompt = f"""
        Analyse la requête suivante d'un étudiant cherchant un sujet de mémoire.
        Identifie:
        1. Le domaine/thème principal
        2. Le niveau implicite (débutant/intermédiaire/avancé)
        3. Les mots-clés techniques
        4. Le département concerné (si mentionné)
        
        Requête: "{query}"
        
        Réponds en français avec un format clair.
        """
        
        try:
            messages = [
                SystemMessage(content="Tu es un expert en analyse de requêtes académiques."),
                HumanMessage(content=analysis_prompt)
            ]
            
            response = self.llm(messages)
            return response.content
        except:
            return "Analyse non disponible"