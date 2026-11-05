# Document Q&A Bot Using Retrieval-Augmented Generation (RAG)

**Author:** Pala Ganesh
**GitHub:** https://github.com/palaganesh

## 1. Project Description

The Document Q&A Bot is a Python-based application that answers questions using information extracted from local PDF documents. It implements Retrieval-Augmented Generation (RAG) by retrieving relevant information from a ChromaDB vector database and passing the retrieved context to Google Gemini to generate answers.

The application provides an interactive Command Line Interface (CLI), displays source filenames and page numbers, and avoids answering questions when the required information is unavailable in the retrieved documents.

## 2. Technology Stack

| Technology            | Version / Model   | Purpose                         |
| --------------------- | ----------------- | ------------------------------- |
| Python                | 3.14.10           | Programming language            |
| PyMuPDF               | 2.1               | PDF text extraction             |
| ChromaDB              | 1.5.9             | Persistent vector database      |
| Sentence Transformers | 6.2.0             | Embedding generation            |
| all-MiniLM-L6-v2      | Pre-trained model | Text embeddings                 |
| Google GenAI          | 2.34.0            | Gemini API integration          |
| python-dotenv         | 1.2.4             | Environment variable management |

## 3. Project Architecture

The application follows a Retrieval-Augmented Generation pipeline.

```text
             PDF Documents
                   |
                   v
          Document Extraction
                   |
                   v
             Text Chunking
          (500 Words, 100 Overlap)
                   |
                   v
          Embedding Generation
           (all-MiniLM-L6-v2)
                   |
                   v
          ChromaDB Vector Database
                   |
                   v
             User Question
                   |
                   v
          Question Embedding
                   |
                   v
          Similarity Search
                   |
                   v
        Relevant Document Context
                   |
                   v
              Google Gemini
                   |
                   v
        Answer with Source Citations
```

### Pipeline Components

* EXTRACT.py: Verifies PDF documents and their extracted text.
* CHUNKING.py: Extracts page text and divides it into smaller chunks.
* EMBEDDING.py: Generates numerical embeddings for the text chunks.
* DATABASE.py: Stores embeddings, text and metadata in ChromaDB.
* RETRIEVAL.py: Demonstrates retrieval of relevant document chunks.
* ANSWER.py: Retrieves relevant context, generates answers using Gemini and displays source information.

## 4. Chunking Strategy

The project uses **fixed-size word-based chunking**.

Configuration:

* Chunk size: 500 words
* Chunk overlap: 100 words

The overlap preserves contextual information between consecutive chunks and reduces information loss at chunk boundaries.

Each chunk stores the following metadata:

* Source filename
* Page number

This metadata allows the application to identify the original PDF document and page associated with retrieved information.

## 5. Embedding Model and Vector Database

### Embedding Model

The project uses `all-MiniLM-L6-v2` from Sentence Transformers.

It converts text chunks into numerical vectors with 384 dimensions.

Embedding generation is performed in batches using a batch size of 32 rather than processing one chunk at a time.

### Vector Database

ChromaDB is used as the persistent vector database.

It stores:

* Text chunks
* Numerical embeddings
* Source filenames
* Page numbers

The database is stored locally in the `chroma_db` directory.

This allows the application to retrieve relevant document information without generating all document embeddings again for every question.

## 6. Installation and Setup

### Prerequisites

* Python 3.14.10 or a compatible Python version.
* Git.
* Google Gemini API key.
* Internet connection for Gemini API access.

### Step 1: Clone the repository

```bash
git clone https://github.com/palaganesh/Document_QA_Bot.git
```

```bash
cd Document_QA_Bot
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure the Gemini API key

Create a `.env` file in the main project directory.

Add the following line:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

Replace `your_actual_gemini_api_key` with your own Gemini API key.

The application uses `python-dotenv` to load the API key.

**Security:** Never upload your actual `.env` file or API key to GitHub.

### Step 5: Index the PDF documents

Open the source directory:

```bash
cd src
```

Run the following scripts in order.

**1. Create text chunks**

```bash
python CHUNKING.py
```

**2. Generate embeddings**

```bash
python EMBEDDING.py
```

**3. Store embeddings in ChromaDB**

```bash
python DATABASE.py
```

After successful indexing, the document chunks and their metadata are stored in the persistent ChromaDB database.

The indexing process should be repeated whenever new PDF documents are added or existing documents are modified.

### Step 6: Run the Document Q&A Bot

While inside the `src` directory, execute:

```bash
python ANSWER.py
```

The interactive CLI will start.

Enter your questions when prompted.

Type `exit` to stop the application.

## 7. Environment Variables

The application requires the following environment variable:

| Variable       | Description                                      |
| -------------- | ------------------------------------------------ |
| GEMINI_API_KEY | Google Gemini API key used for answer generation |

The API key is loaded from the `.env` file using `python-dotenv`.

The `.env` file is excluded from GitHub using `.gitignore`.

A `.env.example` file is provided to show the required environment variable format without exposing any actual API key.

## 8. Example Questions

The following questions can be used to test the application.

| No. | Sample Question                                | Expected Answer Topic              |
| --- | ---------------------------------------------- | ---------------------------------- |
| 1   | What is solar energy?                          | Solar energy and its applications  |
| 2   | What is green hydrogen?                        | Green hydrogen production and uses |
| 3   | What are the advantages of electric vehicles?  | Benefits of electric vehicles      |
| 4   | How does a wind turbine work?                  | Wind energy generation             |
| 5   | What is the purpose of battery energy storage? | Battery storage applications       |

### Unanswerable Question

**Question:** Who is the Prime Minister of India?

**Expected response:**

"The answer is not available in the provided documents."

This test checks whether the application avoids generating answers using information outside the retrieved document context.

## 9. Known Limitations

* The current document ingestion pipeline supports PDF files.
* Scanned PDFs and image-only pages may not provide extractable text without OCR.
* Answer quality depends on the relevance of retrieved document chunks.
* The application requires an internet connection to access the Gemini API.
* Gemini API availability and free-tier usage limits may affect answer generation.
* The application answers using information available in the retrieved document context.
* Information that is not available in the indexed documents may not be answered.
* The current implementation retrieves a limited number of relevant chunks for each question.

## 10. Project Structure

```text
Document_QA_Bot/
│
├── data/
│   ├── Battery Energy Storage System for Renewable Energy Integration.pdf
│   ├── ELECTRIC VEHICLE.pdf
│   ├── GREEN HYDROGEN.pdf
│   ├── Solar Energy.pdf
│   └── WIND.pdf
│
├── src/
│   ├── EXTRACT.py
│   ├── CHUNKING.py
│   ├── EMBEDDING.py
│   ├── DATABASE.py
│   ├── RETRIEVAL.py
│   └── ANSWER.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

The `.env`, `.venv` and `chroma_db` directories are excluded from the GitHub repository.

## Author

**Pala Ganesh**

GitHub Profile: https://github.com/palaganesh

Developed as an AI/ML internship assignment.
