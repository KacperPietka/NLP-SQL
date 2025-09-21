import chromadb

chroma_client = chromadb.PersistentClient("./chroma_data")



collections = chroma_client.create_collection(name="my_collection")