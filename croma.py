import chromadb

class ChromaClient:
    chroma_client: chromadb.Client
    _persistent_client = None  # Class-level variable to store the persistent client instance

    def __init__(self):
        if not ChromaClient._persistent_client:
            ChromaClient._persistent_client = chromadb.PersistentClient()
        self.chroma_client = ChromaClient._persistent_client

    def get_collection(self, collection_name):
        try:
            collection = self.chroma_client.get_collection(collection_name)
            print("collection exists", collection.count())
            return collection
        except Exception as e:
            print("creating collection")
            collection = self.chroma_client.create_collection(collection_name)
            return collection

    def add_data_to_collection(self, collection_name, ids, text, metadata):
        collection = self.get_collection(collection_name)
        res = collection.add(
            ids= ids,
            documents= text,
            metadatas= metadata,
        )
        print("added data to collection", collection.count())
        return res

    def get_data(self, query, collection_name):
        collection = self.get_collection(collection_name)
        files = collection.query(query_texts=query,n_results=20)
        return files
    

