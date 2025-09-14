from typing import List, Dict, Optional
import os
from datetime import datetime

from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    Docx2txtLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone


class DocumentProcessor:
    def __init__(self):
        # Initialize Pinecone
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_INDEX")
        self.index = self.pc.Index(self.index_name)

        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

    async def process_documents(
        self,
        docs_dir: str = "docs",
        allowed_file_types: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Process documents in the docs directory.

        Args:
            docs_dir: Directory containing documents.
            allowed_file_types: List of file extensions to load. Defaults to
                ["md", "pdf", "docx"].
        """
        if allowed_file_types is None:
            allowed_file_types = ["md", "pdf", "docx"]

        documents = []
        for file_type in allowed_file_types:
            glob_pattern = f"*.{file_type}"
            if file_type == "pdf":
                loader = DirectoryLoader(
                    docs_dir, glob=glob_pattern, loader_cls=PyPDFLoader
                )
            elif file_type == "docx":
                loader = DirectoryLoader(
                    docs_dir, glob=glob_pattern, loader_cls=Docx2txtLoader
                )
            else:
                loader = DirectoryLoader(docs_dir, glob=glob_pattern)
            documents.extend(loader.load())

        # Split documents
        texts = self.text_splitter.split_documents(documents)

        # Create embeddings and upload to Pinecone
        for i, text in enumerate(texts):
            embedding = self.embeddings.embed_query(text.page_content)

            metadata = {
                "text": text.page_content,
                "source": text.metadata.get("source", ""),
                "created_at": datetime.now().isoformat(),
            }

            # Upload to Pinecone
            self.index.upsert(vectors=[(f"doc_{i}", embedding, metadata)])

        return texts

