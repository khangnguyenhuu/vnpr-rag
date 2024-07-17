# author khangnh
from langfuse.llama_index import LlamaIndexCallbackHandler
from llama_index.core.callbacks import CallbackManager
from llama_index.core.ingestion import (
    DocstoreStrategy,
    IngestionPipeline,
    IngestionCache
)
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache
from llama_index.core import Settings
from src.constants import (cfg,
                           TEXT_EMBEDDING_MODEL)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.vector_stores.redis import RedisVectorStore
from llama_index.core import SimpleDirectoryReader
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
)
import pickle
import torch
import os
import sys
sys.path.insert(0, ".")


# text splitter


class IngestionService:
    '''
    Service class for ingestion pipeline
    '''
    cfg = cfg

    def __init__(self):
        self.device_type = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.splitter = SemanticSplitterNodeParser(
            buffer_size=1, breakpoint_percentile_threshold=95, embed_model=TEXT_EMBEDDING_MODEL,
        )
        self.ingestion_pipeline = self.initialize_ingestion_pipeline()
        self.query_index = VectorStoreIndex.from_vector_store(
            self.ingestion_pipeline.vector_store,
            embed_model = TEXT_EMBEDDING_MODEL
        )
        Settings.embed_model = TEXT_EMBEDDING_MODEL

    def initialize_ingestion_pipeline(self):
        '''
        Init llama index ingestion pipeline
        '''
        _, host, port = os.getenv("REDIS_HOST").split(":")
        host = host.replace("//", "")
        from llama_index.vector_stores.redis import RedisVectorStore
        from redisvl.schema import IndexSchema
        schema = IndexSchema.from_dict({
            "index": {"name": "redis_vector_store", "prefix": "docs"},
            "fields": [
                {"name": "id", "type": "tag"},
                {"name": "doc_id",
                 "type": "tag"},
                {"name": "text",
                 "type": "text"},
                {
                    "name": "vector",
                    "type": "vector",
                    "attrs": {
                        "dims": cfg.EMBEDDING_MODEL.EMBEDDING_DIMS,
                        "algorithm": "flat"
                    }
                }
            ]
        })
        pipeline = IngestionPipeline(
            transformations=[
                self.splitter,
                TEXT_EMBEDDING_MODEL,
            ],
            vector_store=RedisVectorStore(
                schema=schema,
                redis_url=f"redis://{host}:{port}",
            ),
            docstore=RedisDocumentStore.from_host_and_port(
                host, port, namespace="document_store"),
            cache=IngestionCache(
                cache=RedisCache.from_host_and_port(host, port),
                collection="redis_cache",
            ),
            docstore_strategy=DocstoreStrategy.UPSERTS,
        )

        return pipeline

    def insert(self, doc_file_path):
        """Insert new document into global index and vectore store"""
        documents = SimpleDirectoryReader(doc_file_path).load_data()

        # insert progress
        self.ingestion_pipeline.run(
            documents=documents, in_place=True, show_progress=True)
        # reload query_index to update new ingested data
        self.query_index = VectorStoreIndex.from_vector_store(
            self.ingestion_pipeline.vector_store
        )
        torch.cuda.empty_cache()
