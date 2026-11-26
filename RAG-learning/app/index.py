from dotenv import load_dotenv

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
# from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

load_dotenv()

pdf_path = Path(__file__).parent / "data" / "sample.pdf"

# PDF loader
loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

# Spliting the documents into the chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

chunks = text_splitter.split_documents(documents=docs)

# Embedding the chunks using OpenAI Embeddings
# embedding_model = OpenAIEmbeddings(
#     model="text-embedding-3-large"
# )

# Embedding the chunks using FastEmbed Embeddings
embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# Create a Qdrant vector store
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="sample_collection",
    url="http://localhost:6333",
    force_recreate=True
) 

print("Vector store created and documents embedded successfully.")


