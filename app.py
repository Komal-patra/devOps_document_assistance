import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# it list down the files and loads data inside directory
documents = SimpleDirectoryReader('./documentation').load_data()

#initialisng the chromadb
chroma_client = chromadb.PersistentClient(path="./storage")

#load a chroma collection

collection_name="dev_docs_collection"

try:
    chroma_collection = chroma_client.get_collection(collection_name)
except Exception:
    chroma_collection = chroma_client.create_collection(collection_name)
    print(f"Collection {collection_name} created")

# wrap the chromadb as a vector store
vector_store = ChromaVectorStore(chroma_collection)

# create vector index
index = VectorStoreIndex.from_documents(documents, vector_store=vector_store)

# save the context storage 
index.storage_context.persist('./storage')

print("Documents indexed successfully")

