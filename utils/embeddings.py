"""
Module de gestion des embeddings et base vectorielle
"""
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import numpy as np
import os

class EmbeddingManager:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialise le modèle d'embeddings
        """
        print(f"🔧 Chargement du modèle d'embeddings: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        
        # Configuration de ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path="chroma_db",
            settings=Settings(anonymized_telemetry=False)
        )
        
    def create_embeddings(self, texts, metadatas=None, collection_name="sujets_memoire"):
        """
        Crée les embeddings et les stocke dans ChromaDB
        """
        try:
            # Vérifier si la collection existe déjà
            existing_collections = [col.name for col in self.chroma_client.list_collections()]
            
            if collection_name in existing_collections:
                print(f"📁 Collection '{collection_name}' déjà existante")
                collection = self.chroma_client.get_collection(collection_name)
            else:
                print(f"🆕 Création de la collection: {collection_name}")
                collection = self.chroma_client.create_collection(
                    name=collection_name,
                    metadata={"description": "Sujets de mémoire académiques"}
                )
                
                # Générer les embeddings
                print(f"⚙️ Génération des embeddings pour {len(texts)} textes...")
                embeddings = self.model.encode(texts, show_progress_bar=True)
                
                # Convertir en listes pour ChromaDB
                embeddings_list = embeddings.tolist()
                
                # Ajouter les documents à la collection
                ids = [f"doc_{i}" for i in range(len(texts))]
                
                if metadatas is None:
                    metadatas = [{} for _ in range(len(texts))]
                
                collection.add(
                    embeddings=embeddings_list,
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )
                
                print(f"✅ {len(texts)} documents ajoutés à la collection")
            
            return collection
            
        except Exception as e:
            print(f"❌ Erreur lors de la création des embeddings: {e}")
            return None
    
    def search_similar(self, query, collection, n_results=5, filters=None):
        """
        Recherche les documents les plus similaires à la requête
        """
        try:
            # Embedding de la requête
            query_embedding = self.model.encode([query]).tolist()[0]
            
            # Recherche dans ChromaDB
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filters
            )
            
            return results
            
        except Exception as e:
            print(f"❌ Erreur lors de la recherche: {e}")
            return None
    
    def get_collection(self, collection_name="sujets_memoire"):
        """
        Récupère une collection existante
        """
        try:
            return self.chroma_client.get_collection(collection_name)
        except:
            return None