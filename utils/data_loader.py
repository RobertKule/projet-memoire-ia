"""
Module de chargement et prétraitement des données
"""
import pandas as pd
import re

def load_subjects(file_path="data/sujets_memoires.csv"):
    """
    Charge les sujets de mémoire depuis un fichier CSV
    """
    try:
        df = pd.read_csv(file_path)
        print(f"✅ {len(df)} sujets chargés depuis {file_path}")
        
        # Nettoyage des textes
        df['texte_complet'] = df.apply(
            lambda row: f"Titre: {row['titre']}. Résumé: {row['resume']}. Département: {row['departement']}. Niveau: {row['niveau']}.",
            axis=1
        )
        
        return df
    except Exception as e:
        print(f"❌ Erreur lors du chargement des données: {e}")
        return pd.DataFrame()

def filter_by_department(df, departments=None):
    """
    Filtre les sujets par département
    """
    if departments and len(departments) > 0:
        return df[df['departement'].isin(departments)]
    return df

def filter_by_level(df, level):
    """
    Filtre les sujets par niveau (débutant/intermédiaire)
    """
    if level == "débutant":
        return df[df['niveau'] == "débutant"]
    elif level == "intermédiaire":
        return df[df['niveau'].isin(["intermédiaire", "avancé"])]
    return df