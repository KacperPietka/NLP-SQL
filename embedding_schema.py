import chromadb
import yaml
import os
from sentence_transformers import SentenceTransformer

class ChromaSchemaManager:
    def __init__(self, data_dir="./chroma_data", collection_name="schema_collection", model_name="all-mpnet-base-v2"):
        self.chroma_client = chromadb.PersistentClient(path=data_dir)
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)
        self.embedder = SentenceTransformer(model_name)

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
        """Split long text into overlapping chunks (safe for transformer models)."""
        chunks = []
        start = 0
        while start < len(text):
            end = min(len(text), start + chunk_size)
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def add_yml(self, file_path: str):
        if not file_path.endswith((".yml", ".yaml")):
            raise ValueError("Only .yml or .yaml files are allowed.")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        text = yaml.dump(data)

        chunks = self._chunk_text(text)
        embeddings = self.embedder.encode(chunks).tolist()

        file_id = os.path.basename(file_path)
        ids = [f"{file_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": file_id, "chunk_index": i} for i in range(len(chunks))]
                     
        self.collection.add(documents=chunks,embeddings=embeddings,ids=ids,metadatas=metadatas)
        return

    def get_context(self, query_text, n_results=3):
        query_embedding = self.embedder.encode([query_text]).tolist()
        results = self.collection.query(query_embeddings=query_embedding, n_results=n_results)
        return results

    def get_schema(self, question, n_results=3):
        results = self.get_context(question, n_results)
        docs = results["documents"][0]
        schema_parts = [doc for doc in docs if any(k in doc.lower() for k in ["table", "model", "columns", "schema"])]
        return "\n\n".join(schema_parts)
