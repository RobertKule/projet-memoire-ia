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
        # Utiliser st.secrets en priorité si disponible, sinon os.getenv
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ Clé API Google manquante ! Configurez-la dans les secrets de déploiement.")
        
        try:
            genai.configure(api_key=self.api_key)
            self.model_name = "gemma-3-4b-it"
            self.model = genai.GenerativeModel(self.model_name)
            print(f"✅ Modèle {self.model_name} initialisé")
        except Exception as e:
            print(f"❌ Erreur d'initialisation: {e}")
            raise

    def generate_recommendations(self, 
                                query: str, 
                                context: List[Dict], 
                                student_level: str = "intermédiaire") -> str:
        try:
            context_str = self._format_context(context)
            prompt = self._create_prompt(query, context_str, student_level)
            
            generation_config = {
                "temperature": 0.4, # Baissée pour plus de rigueur académique
                "max_output_tokens": 1500,
            }
            
            start_time = time.time()
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            elapsed_time = time.time() - start_time
            result = response.text.strip()
            
            return self._format_output(result, query, student_level, elapsed_time)
            
        except Exception as e:
            return self._get_fallback_recommendations(query, student_level, str(e))

    def _format_context(self, context: List[Dict]) -> str:
        if not context:
            return "Aucun sujet de référence disponible."
        
        context_lines = []
        for i, doc in enumerate(context[:5], 1): # On peut monter à 5 sujets
            line = f"- {doc.get('titre')} (Dept: {doc.get('departement')})"
            context_lines.append(line)
        return "\n".join(context_lines)

    def _create_prompt(self, query: str, context_str: str, student_level: str) -> str:
        return f"""Tu es le Professeur Virtuel de la FST, expert en méthodologie de recherche. 
Ton objectif est de guider l'étudiant vers un sujet de mémoire INNOVANT, RÉALISABLE et ACADÉMIQUEMENT VALIDE.

### CONTEXTE DES ARCHIVES (Sujets déjà traités) :
{context_str}

### PROFIL DE L'ÉTUDIANT :
- Intérêt : {query}
- Niveau : {student_level}

### DIRECTIVES :
1. ANALYSE DE FAISABILITÉ : Évalue si le sujet est réalisable en 4 mois pour un étudiant de niveau {student_level}.
2. ÉVITEMENT DU PLAGIAT : Propose une ÉVOLUTION ou une VARIANTE des archives, jamais un titre identique.
3. STRUCTURE : Chaque proposition doit inclure une problématique centrale.

### FORMAT DE SORTIE (Markdown strict) :
# 🎓 PROPOSITIONS DE RECHERCHE PERSONNALISÉES

---
## 🏆 Option 1 : [Titre Scientifique Précis]
* **Problématique :** [Question scientifique résolue]
* **Lien avec les archives :** [Pourquoi c'est une amélioration des anciens travaux]
* **Méthodologie suggérée :** [Étude/Prototypage/Analyse]
* **Mots-clés :** [3 mots techniques]

---
## 🏆 Option 2 : [Titre Scientifique Précis]
... (Répéter le format)

---
## 🏆 Option 3 : [Titre Scientifique Précis]
... (Répéter le format)

---
## 💡 CONSEIL DU PROFESSEUR
[Conseil sur la gestion du temps ou le choix du directeur]

Réponse (en français) :"""

    def _format_output(self, response: str, query: str, level: str, time_taken: float) -> str:
        header = f"""
---
**Analyse pour :** {query} | **Niveau :** {level} | **Temps :** {time_taken:.1f}s
---
"""
        return header + response

    def _get_fallback_recommendations(self, query: str, student_level: str, error: str = "") -> str:
        return f"# 🎓 PROPOSITIONS (MODE SECOURS)\n\nL'IA est indisponible ({error[:50]})...\n\n1. Étude de l'impact du numérique en Génie Civil\n2. Optimisation de réseaux locaux\n3. Analyse des systèmes automatisés."