import chromadb
import os
import yaml
from sentence_transformers import SentenceTransformer

chroma_client = chromadb.PersistentClient("./chroma_data")

collection = chroma_client.create_collection(name="my_collection")

### Embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

### Adding a file to chrome (only yaml files are allowed)
def add_yml_to_chroma(file_path):
    if not (file_path.endswith(".yml") or file_path.endswith(".yaml")):
        raise ValueError("Only .yml or .yaml files are allowed.")
    with open(file_path, 'r', encoding='UTF-8') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML file: {e}")

    # Convert YAML data to text
    text = yaml.dump(data)

    embedding = embedder.encode([text]).tolist()

    collection.add(
        documents=[text],
        embeddings=embedding,
        ids=[os.path.basename(file_path)],
        metadatas=[{"source": os.path.basename(file_path)}]
    )


def get_context_from_chroma(query_text, n_results=3):
    query_embedding = embedder.encode([query_text]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"📄 From {meta['source']}:\n{doc[:400]}...\n")

    return results

def get_schema_from_chroma(question, n_results=3):
    results = get_context_from_chroma(question, n_results)
    docs = results["documents"][0]

    # Optional: try to extract schema sections from YAML text
    schema_parts = []
    for doc in docs:
        if any(k in doc.lower() for k in ["table", "model", "columns", "schema"]):
            schema_parts.append(doc)

    schema_text = "\n\n".join(schema_parts)
    return schema_text






