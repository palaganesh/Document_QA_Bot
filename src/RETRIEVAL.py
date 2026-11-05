import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to existing database
DB_PATH = Path(__file__).resolve().parent.parent / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_collection(
    name="renewable_energy"
)

print("================================")
print("     DOCUMENT RETRIEVAL")
print("================================")

# Ask user question
question = input("\nEnter your question: ")

# Convert question into embedding
query_embedding = model.encode([question]).tolist()

# Search database
results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

print("\n========== RETRIEVED RESULTS ==========")

for i in range(len(results["documents"][0])):

    print("\nResult:", i + 1)

    print("Source:", results["metadatas"][0][i]["source"])

    print("Page:", results["metadatas"][0][i]["page"])

    print("Text:", results["documents"][0][i])

print("\n================================")
print("     RETRIEVAL COMPLETED")
print("================================")