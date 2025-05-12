import os
from typing import List, Dict, Any
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document

class EmbeddingEngine:
    """Handles document embedding and retrieval."""

    def __init__(self, api_key: str = None):
        """Initialize the embedding engine."""

        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None

    def create_embeddings(self, chunks: List[Dict[str, Any]]):
        """Create embeddings from document chunks."""

        documents = [
            Document(page_content=chunk["content"], metadata=chunk["metadata"])
            for chunk in chunks
        ]

        # Creating a vector store from the documents
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )

        return self.vector_store
    
    def retrieve_relevant_chunks(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve the most relevant chinks for a query."""

        if not self.vector_store:
            raise ValueError("No documents have been embedded yet.")
        
        return self.vector_store.similarity_search(query, k=k)
    
    def get_vector_store(self):
        """Return the vector store."""
        return self.vector_store