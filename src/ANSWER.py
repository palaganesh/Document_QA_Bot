
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv
from google.genai import errors
import os
import time

# ========================================
# PROJECT PATH
# ========================================

ROOT_FOLDER = Path(__file__).resolve().parent.parent

# ========================================
# LOAD GEMINI API KEY
# ========================================

load_dotenv(ROOT_FOLDER / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key not found in .env file")

client_ai = genai.Client(api_key=API_KEY)

# ========================================
# LOAD EMBEDDING MODEL
# ========================================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

# ========================================
# CONNECT CHROMADB
# ========================================

DB_PATH = ROOT_FOLDER / "chroma_db"

client_db = chromadb.PersistentClient(
    path=str(DB_PATH)
)

collection = client_db.get_collection(
    name="renewable_energy"
)

print("\n================================")
print("       DOCUMENT Q&A BOT")
print("================================")

print("Total stored chunks:", collection.count())

# ========================================
# QUESTION ANSWERING FUNCTION
# ========================================

def answer_question(question):

    # Convert question into embedding

    query_embedding = model.encode(
        [question]
    ).tolist()

    # Retrieve relevant documents

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not documents:
        print("\nAnswer not available in the provided documents.")
        return

    # Prepare document context

    context = ""

    for i in range(len(documents)):

        context += f"""
Source: {metadatas[i]['source']}
Page: {metadatas[i]['page']}
Content: {documents[i]}
"""

    # Prepare Gemini prompt

    prompt = f"""
You are a document-based question answering assistant.

Answer the question using ONLY the information
available in the provided document context.

Do not use outside knowledge or your own training data.

If the answer is not available in the context,
respond exactly:

"The answer is not available in the provided documents."

Use clear and simple language.

Include source filename and page number
for the information used in your answer.

DOCUMENT CONTEXT:

{context}

QUESTION:

{question}

ANSWER:
"""

    # ========================================
    # GEMINI RESPONSE WITH RETRY
    # ========================================

    for attempt in range(3):

        try:

            response = client_ai.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            print("\n========== ANSWER ==========")

            if response.text:
                print(response.text)
            else:
                print("Gemini returned an empty response.")

            print("\n========== SOURCES ==========")

            for i in range(len(documents)):

                print(
                    f"{i + 1}. {metadatas[i]['source']} "
                    f"- Page {metadatas[i]['page']}"
                )

            return

        except errors.ServerError as e:

            print(f"\nGemini server error: {e}")

            if attempt < 2:

                print("Retrying in 10 seconds...")

                time.sleep(10)

            else:

                print("\nGemini is currently unavailable.")
                print("Please try again later.")

        except Exception as e:

            print("\nError:", e)
            return


# ========================================
# INTERACTIVE QUESTION LOOP
# ========================================

while True:

    question = input("\nAsk your question (or type exit): ")

    if question.lower().strip() == "exit":

        print("\nThank you for using Document Q&A Bot!")

        break

    if not question.strip():

        print("Please enter a question.")

        continue

    answer_question(question)
