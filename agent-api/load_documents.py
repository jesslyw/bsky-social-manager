from langchain_community.document_loaders import TextLoader
from nodes.rag.vectorstore import get_vectorstore

loader = TextLoader("data/red-books-faq.txt")
docs = loader.load()  # Lädt den Inhalt als verarbeitbare Objekte.
# Gibt ein Chroma-Objekt zurück, das Embeddings speichern kann.
vectorstore = get_vectorstore()
# Wandelt  Texte in Vektoren um und speichert sie.
vectorstore.add_documents(docs, ids=["redbooks"])

print("Vektorstore erfolgreich erstellt.")
print(vectorstore._collection.get()["ids"])
# vectorstore.delete(ids=['red-books-0']) # delete specific database entries by id
