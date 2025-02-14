import faiss
import numpy as np
from app.core.logger import logger

class FaissMemoryHelper:
    def __init__(self, embedding_dim=768, faiss_index_path="faiss_index.bin"):
        self.embedding_dim = embedding_dim
        self.faiss_index_path = faiss_index_path
        self.index = self._create_hnsw_index()
        self.message_ids = []  # Store message IDs separately
        self._load_index()

    def _create_hnsw_index(self):
        """Create an HNSW FAISS index for faster similarity search."""
        index = faiss.IndexHNSWFlat(self.embedding_dim, 32)  # 32 neighbors
        index.hnsw.efConstruction = 200  # High quality graph
        index.hnsw.efSearch = 64  # Controls search accuracy
        return index

    def _load_index(self):
        """Load FAISS index from file if it exists."""
        try:
            self.index = faiss.read_index(self.faiss_index_path)
            # Load the stored message IDs as well
            self.message_ids = np.load(self.faiss_index_path.replace(".bin", "_ids.npy"), allow_pickle=True).tolist()
        except Exception:
            print("No existing FAISS index found. Creating a new one.")

    def add_message_to_index(self, message_id, vector):
        """Add embedding to FAISS index and store message ID."""
        vector = vector.reshape(1, -1)  # Ensure correct shape
        self.index.add(vector)  # Add to FAISS
        self.message_ids.append(message_id)  # Store the corresponding message ID
        self._save_index()  # Save FAISS index and message IDs
        print(f"Added message {message_id} to FAISS index.")

    def search_similar_messages(self, query_vector, top_k=5):
        """Find top K similar messages using FAISS HNSW."""
        query_vector = query_vector.reshape(1, -1)  # Ensure 2D
        
        if query_vector.shape[1] != self.index.d:
            raise ValueError(f"Dimension mismatch: query vector has {query_vector.shape[1]}, but FAISS index expects {self.index.d}")
        
        # Check if FAISS index is empty
        if self.index.ntotal == 0:
            logger.warning("FAISS index is empty. Cannot perform search.")
            return [], []

        distances, indices = self.index.search(query_vector, top_k)
        
        # Filter out invalid indices (-1)
        valid_indices = [i for i in indices[0] if i >= 0]
        # Retrieve corresponding message IDs for the search results
        result_message_ids = [self.message_ids[i] for i in valid_indices]
        # Ensure result_message_ids never None
        result_message_ids = result_message_ids if result_message_ids else []
        # Return message IDs and distances
        return result_message_ids, distances[0]  

    def _save_index(self):
        """Save FAISS index and message IDs to files."""
        faiss.write_index(self.index, self.faiss_index_path)
        # Store the message IDs as a numpy file for easy retrieval
        np.save(self.faiss_index_path.replace(".bin", "_ids.npy"), np.array(self.message_ids))
