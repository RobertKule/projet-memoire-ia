"""
Module de recommandation avec Google Gemma 3
Version finale avec gestion d'erreurs robuste
"""
import os
import google.generativeai as genai
import time
from typing import List, Dict, Optional

class RecommenderSystem:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise avec Google Gemma 3 (gemma-3-4b-it)
        
        Args:
            api_key: Clé API Google (sinon depuis GOOGLE_API_KEY)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError("""
            ❌ Clé API Google manquante !
            
            Configurez GOOGLE_API_KEY dans votre fichier .env
            Exemple: GOOGLE_API_KEY=AIzaSyCATUzWAdFJysadR7ZMU1E09zsAnSFu7Zo
            """)
        
        try:
            # Configurer l'API Google
            genai.configure(api_key=self.api_key)
            
            # Utiliser Gemma 3 (modèle gratuit qui fonctionne)
            self.model_name = "gemma-3-4b-it"
            self.model = genai.GenerativeModel(self.model_name)
            
            print(f"✅ Modèle {self.model_name} initialisé avec succès")
            
        except Exception as e:
            print(f"❌ Erreur d'initialisation: {e}")
            raise
    
    def generate_recommendations(self, 
                                query: str, 
                                context: List[Dict], 
                                student_level: str = "intermédiaire") -> str:
        """
        Génère 3 recommandations personnalisées
        
        Args:
            query: Requête de l'étudiant
            context: Contexte des sujets existants
            student_level: Niveau académique
            
        Returns:
            str: Recommandations formatées
        """
        try:
            # Préparer le contexte formaté
            context_str = self._format_context(context)
            
            # Créer le prompt optimisé
            prompt = self._create_prompt(query, context_str, student_level)
            
            # Configuration de génération
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 1200,
            }
            
            start_time = time.time()
            
            # Générer la réponse
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings={
                    "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
                }
            )
            
            elapsed_time = time.time() - start_time
            
            # Traiter la réponse
            result = response.text.strip()
            
            # Formater la réponse finale
            final_output = self._format_output(result, query, student_level, elapsed_time)
            
            print(f"✅ Recommandations générées en {elapsed_time:.1f}s")
            return final_output
            
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Erreur API: {error_msg}")
            return self._get_fallback_recommendations(query, student_level, error_msg)
    
    def _format_context(self, context: List[Dict]) -> str:
        """Formate le contexte pour le prompt"""
        if not context:
            return "Aucun sujet de référence disponible."
        
        context_lines = []
        for i, doc in enumerate(context[:4], 1):
            titre = doc.get('titre', f'Sujet {i}')
            departement = doc.get('departement', 'Génie Informatique')
            niveau = doc.get('niveau', 'intermédiaire')
            resume = doc.get('resume', '')
            
            line = f"{i}. {titre}"
            line += f" | Département: {departement}"
            line += f" | Niveau: {niveau}"
            if resume and len(resume) > 10:
                line += f" | Description: {resume[:100]}..."
            
            context_lines.append(line)
        
        return "\n".join(context_lines)
    
    def _create_prompt(self, query: str, context_str: str, student_level: str) -> str:
        """Crée le prompt pour l'IA"""
        return f"""Tu es un conseiller académique expert à la Faculté des Sciences et Technologies.

BASE DE CONNAISSANCES - SUJETS EXISTANTS:
{context_str}

DEMANDE DE L'ÉTUDIANT:
"{query}"

NIVEAU ACADÉMIQUE:
{student_level}

TÂCHE:
Générer EXACTEMENT 3 recommandations de sujets de mémoire adaptées.

FORMAT OBLIGATOIRE (en français uniquement):

📘 **RECOMMANDATIONS PERSONNALISÉES**

🎯 **Sujet 1: [Titre technique en français]**
   📍 Département: [Département pertinent]
   🎯 Objectif pédagogique: [Ce que l'étudiant apprendra - 1-2 phrases]
   ⚙️ Technologies recommandées: [2-3 technologies adaptées]
   ✅ Pourquoi ce sujet: [Lien avec la demande + avantages pour l'étudiant]

🎯 **Sujet 2: [Titre technique différent]**
   📍 Département: [Département pertinent]
   🎯 Objectif pédagogique: [Apprentissages spécifiques]
   ⚙️ Technologies recommandées: [Stack technique adaptée]
   ✅ Pourquoi ce sujet: [Valeur ajoutée pour le parcours académique]

🎯 **Sujet 3: [Titre innovant]**
   📍 Département: [Département pertinent]
   🎯 Objectif pédagogique: [Compétences à développer]
   ⚙️ Technologies recommandées: [Outils modernes]
   ✅ Pourquoi ce sujet: [Perspectives professionnelles]

RÈGLES STRICTES:
1. Réponds UNIQUEMENT en français académique
2. Adapte la difficulté technique au niveau "{student_level}"
3. Sois précis et concret dans les propositions
4. Propose des sujets réalisables en 4-6 mois
5. Inspire-toi des sujets existants mais sois créatif
6. Utilise EXACTEMENT le format ci-dessus avec les émojis
7. Commence directement par "📘 **RECOMMANDATIONS PERSONNALISÉES**"

Ta réponse:"""
    
    def _format_output(self, response: str, query: str, level: str, time_taken: float) -> str:
        """Formate la sortie finale"""
        if not response.startswith("📘"):
            response = f"📘 **RECOMMANDATIONS PERSONNALISÉES**\n\n{response}"
        
        header = f"""
🎯 **Demande analysée:** {query}
📊 **Niveau cible:** {level}
⏱️ **Temps de génération:** {time_taken:.1f}s
🤖 **Modèle IA:** Google Gemma 3 (gemma-3-4b-it)

"""
        
        return header + response
    
    def _get_fallback_recommendations(self, query: str, student_level: str, error: str = "") -> str:
        """Retourne des recommandations de secours"""
        return f"""
📘 **RECOMMANDATIONS PERSONNALISÉES** (Mode basique)

🎯 **Demande:** {query}
📊 **Niveau:** {student_level}
⚠️ **Note:** L'IA rencontre des limitations techniques

🔵 **1. Application web éducative interactive**
   📍 Département: Génie Informatique
   🎯 Objectif pédagogique: Maîtriser le développement full-stack moderne
   ⚙️ Technologies recommandées: Python (Django), React.js, PostgreSQL, Docker
   ✅ Pourquoi ce sujet: Projet complet avec des résultats concrets, excellent pour un portfolio

🟢 **2. Système de recommandation intelligent pour ressources académiques**
   📍 Département: Génie Informatique
   🎯 Objectif pédagogique: Introduction pratique au machine learning et aux algorithmes
   ⚙️ Technologies recommandées: Python, Scikit-learn, Pandas, FastAPI, Jupyter
   ✅ Pourquoi ce sujet: Compétence très recherchée, permet d'aborder l'IA de façon accessible

🟡 **3. Application mobile de gestion de projets étudiants**
   📍 Département: Génie Informatique
   🎯 Objectif pédagogique: Développer des compétences en mobile, backend et UX/UI
   ⚙️ Technologies recommandées: Flutter/Dart, Firebase, REST APIs, Git, Figma
   ✅ Pourquoi ce sujet: Projet moderne couvrant toutes les étapes du développement

💡 *Suggestions génériques - L'API rencontre: {error[:80] if error else "des limitations"}*
"""