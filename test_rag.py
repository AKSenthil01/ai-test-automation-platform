from ai_engine.rag_retriever import RAGRetriever

retriever = RAGRetriever()

query = """
Temperature sensor failure.
Defrost cycle not starting.
"""

docs = retriever.retrieve(query, top_k=3)

for i, doc in enumerate(docs, start=1):
    print("=" * 80)
    print(f"Result {i}")
    print("=" * 80)
    print("Metadata:")
    print(doc.metadata)
    print("\nContent:")
    print(doc.page_content)
    print()