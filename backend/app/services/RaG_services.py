from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index import ServiceContext as Settings
from llama_index.core import (
    StorageContext,
    SimpleDirectoryReader, 
    VectorStoreIndex
    )

ollama_embedding = OllamaEmbedding("llama3.2", base_url="http://localhost:11434")
Settings.embed_model = ollama_embedding
Settings.llm = Ollama("llama3.2")

storage_context = StorageContext()

documents = SimpleDirectoryReader("app/data").load_data()


index = VectorStoreIndex.from_documents(
    documents
)

query_engine = index.as_query_engine()

resp = query_engine.query("Summarize the main topic.")

print(resp)