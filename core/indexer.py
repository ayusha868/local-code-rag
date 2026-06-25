import chromadb
from chromadb.utils import embedding_functions

class LocalIndexer:
    def __init__(self, persist_directory="./.vector_db"):
        # Initializes a persistent local folder on your disk to save the vectors
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # This downloads a free, highly optimized embedding model running locally on your CPU
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Get or create a specific collection table inside ChromaDB
        self.collection = self.client.get_or_create_collection(
            name="codebase_index", 
            embedding_function=self.embedding_fn
        )

    def index_code(self, docs, metadatas):
        # Create a unique text string ID for every single code chunk
        ids = [f"id_{meta['source'].replace('/', '_')}_{meta['chunk_id']}" for meta in metadatas]
        
        # Batch upload vectors, text contents, and tracking metadata directly to local disk
        self.collection.add(
            documents=docs,
            metadatas=metadatas,
            ids=ids
        )
        print(f"💾 Successfully stored {len(docs)} chunks into the local Vector DB.")

    def query_code(self, query_text, n_results=2):
        # Performs a cosine similarity vector search
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results["documents"][0], results["metadatas"][0]