import chromadb

# Create a Chroma client
client = chromadb.Client()

# Create a multimodal embedding function and image loader
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
embedding_function = OpenCLIPEmbeddingFunction()
data_loader = ImageLoader()

# Create a collection with the multimodal embedding function and image loader
collection = client.create_collection(
    name='multimodal_collection',
    embedding_function=embedding_function,
    data_loader=data_loader
)

# Add documents to the collection
collection.add(
    ids=['id4', 'id5', 'id6'],
    documents=["This is a document", "This is another document", "This is a third document"]
)

# Query the collection with text
results = collection.query(
    query_texts=["This is a query document", "This is another query document"]
)

# Print the results
for result in results:
    print(results)  
