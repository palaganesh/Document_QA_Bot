from sentence_transformers import SentenceTransformer
from CHUNKING import all_chunks

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [chunk["text"] for chunk in all_chunks]

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True
)

print("\n================================")
print("    EMBEDDINGS COMPLETED")
print("================================")

print("Total chunks:", len(texts))
print("Embedding shape:", embeddings.shape)
print("First embedding:", embeddings[0][:10])