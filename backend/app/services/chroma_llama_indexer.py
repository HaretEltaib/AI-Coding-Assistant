# app/services/chroma_llama_indexer.py

import os
import chromadb
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.settings import Settings

# Step 3: Define a class that watches a directory or file for changes
class DataDirWatcher(FileSystemEventHandler):
    def __init__(self, callback):  
        super().__init__()
        self.callback = callback

    def on_any_event(self, event):  
        # Ignore directory changes and temp file edits
        if not event.is_directory and not event.src_path.endswith(("~", ".swp")):
            print(f"[watcher] Detected change: {event.event_type} - {event.src_path}")
            self.callback()  # Run the callback (e.g., rebuild the index)

# Step 4: Define the main class to handle Chroma + LlamaIndex logic
class ChromaLlamaIndexer:

    def __init__(self, llm_model="llama3.2", chroma_dir="./chroma_db", collection_name="default"):
        self.embedding_model = OllamaEmbedding(model_name=llm_model)
        self.model = Ollama(model=llm_model)

        self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
        self.collection_name = self.chroma_client.get_or_create_collection(name=collection_name)

        Settings.llm = self.model
        Settings.embed_model = self.embedding_model

        self.vector_store = ChromaVectorStore(chroma_collection=self.collection_name)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

        self.index = None
        self.query_engine = None

    def build_index(self, data_path):
        print(f"[indexer] Loading documents from {data_path}…")

        docs = []
        for root, dirs, files in os.walk(data_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    docs.append(f.read())  

        self.index = VectorStoreIndex.from_documents(documents=docs, storage_context=self.storage_context)
        self.query_engine = self.index.as_query_engine()

        print(f"[indexer] Index built: {len(docs)} documents ingested.")

    def query(self, prompt):
        if self.query_engine is None:
            raise RuntimeError("Index not built yet. Call build_index() first.")
        return self.query_engine.query(prompt)


def main():
    DATA_DIR = "app/data"  

    indexer = ChromaLlamaIndexer(collection_name="my_docs")
    indexer.build_index(data_path=DATA_DIR)

    event_handler = DataDirWatcher(lambda: indexer.build_index(data_path=DATA_DIR))
    observer = Observer()
    observer.schedule(event_handler=event_handler, path=DATA_DIR, recursive=True)
    observer.daemon = True
    observer.start()
    print("[watcher] Watching for changes in", DATA_DIR)

    try:
        while True:
            user_query = input("\n🔍 Your query> ").strip()
            if not user_query:
                continue
            resp = indexer.query(user_query)
            print("\n📄 Response:\n", resp, "\n")
    except KeyboardInterrupt:
        print("\n[shutdown] Stopping watcher and exiting.")
        observer.stop()  
    observer.join()

if __name__ == "__main__":
    main()
