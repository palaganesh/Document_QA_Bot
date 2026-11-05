import chromadb
from pathlib import Path
from EMBEDDING import model, embeddings
from CHUNKING import all_chunks

# Create persistent database
DB_PATH = Path(__file__).resolve().parent.parent / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

# Create collection
collection = client.get_or_create_collection(
    name="renewable_energy"
)

# Prepare data
ids = [str(i) for i in range(len(all_chunks))]

documents = [chunk["text"] for chunk in all_chunks]

metadatas = [
    {
        "source": chunk["source"],
        "page": chunk["page"]
    }
    for chunk in all_chunks
]

# Store in ChromaDB
collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)

print("\n================================")
print("   DATABASE STORAGE COMPLETED")
print("================================")

print("Total stored chunks:", collection.count())
print("Database location:", DB_PATH)