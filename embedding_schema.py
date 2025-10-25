import chromadb
import yaml
import os
from sentence_transformers import SentenceTransformer
import snowflake.connector

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


    def add_snowflake_schema(self, user, password, account, warehouse, database, schema):
        """
        Connects to Snowflake and embeds all table schemas (via DESCRIBE TABLE) into ChromaDB.
        """
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        cur = conn.cursor()

        try:
            # Get all tables in schema
            cur.execute(f"SHOW TABLES IN SCHEMA {database}.{schema}")
            tables = [row[1] for row in cur.fetchall()]

            for t in tables:
                cur.execute(f"DESCRIBE TABLE {database}.{schema}.{t}")
                rows = cur.fetchall()

                # Build a text representation of schema
                schema_text = f"Table: {t}\n"
                schema_text += "\n".join([f"  {r[0]} ({r[1]})" for r in rows])

                chunks = self._chunk_text(schema_text)
                embeddings = self.embedder.encode(chunks).tolist()
                ids = [f"{t}_chunk_{i}" for i in range(len(chunks))]
                metadatas = [{"source": t, "chunk_index": i, "type": "snowflake_table"} for i in range(len(chunks))]

                self.collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)

        finally:
            cur.close()
            conn.close()

    def get_context(self, query_text, n_results=1):
        query_embedding = self.embedder.encode([query_text]).tolist()
        results = self.collection.query(query_embeddings=query_embedding, n_results=n_results)
        return results

    def get_schema(self, question, n_results=1):
        results = self.get_context(question, n_results)
        docs = results["documents"][0]
        schema_parts = [doc for doc in docs if any(k in doc.lower() for k in ["table", "model", "columns", "schema"])]
        return "\n\n".join(schema_parts)
