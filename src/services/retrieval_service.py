from typing import List, Dict
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings

import os

class RetrievalService:
    def __init__(self):
        # Initialize Pinecone
        self.pc = Pinecone(
            api_key=os.getenv("PINECONE_API_KEY")
        )
        self.index = self.pc.Index(os.getenv("PINECONE_INDEX"))
        self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

    async def get_relevant_context(self, query: str, top_k: int = 3) -> str:
        """Get relevant document chunks for a query"""
        # Create query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # Search Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        # Extract and combine relevant texts
        contexts = [result.metadata["text"] for result in results.matches]
        return "\n\n".join(contexts)