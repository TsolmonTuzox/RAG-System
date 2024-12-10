from typing import List, Dict
import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone
from datetime import datetime

class DocumentProcessor:
    def __init__(self):
        # Initialize Pinecone
        self.pc = Pinecone(
            api_key=os.getenv("PINECONE_API_KEY")
        )
        self.index_name = os.getenv("PINECONE_INDEX")
        self.index = self.pc.Index(self.index_name)
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    async def process_documents(self, docs_dir: str = "docs") -> List[Dict]:
        """Process all markdown documents in the docs directory"""
        # Load documents
        loader = DirectoryLoader(docs_dir, glob="*.md")
        documents = loader.load()
        
        # Split documents
        texts = self.text_splitter.split_documents(documents)
        
        # Create embeddings and upload to Pinecone
        for i, text in enumerate(texts):
            embedding = self.embeddings.embed_query(text.page_content)
            
            metadata = {
                "text": text.page_content,
                "source": text.metadata.get("source", ""),
                "created_at": datetime.now().isoformat()
            }
            
            # Upload to Pinecone
            self.index.upsert(
                vectors=[(f"doc_{i}", embedding, metadata)]
            )
        
        return texts