from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import JSONLoader

from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from dotenv import load_dotenv
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.indices.vector_store.base import VectorStoreIndex
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

load_dotenv()



client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))
# for doc in client.sales_database.sales_collection.find():
#     print(doc["storeLocation"])

loader = JSONLoader(file_path="./tinytweets.json", jq_schema=".tweets[]", text_content=False)

documents = loader.load()
db = Chroma.from_documents(documents, embedding_function)
query = "Medical advice for body"

docs = db.similarity_search(query)
print("All the Docs :",docs, type(docs))
print(docs[0].page_content)
