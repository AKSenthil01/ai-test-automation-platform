from ai_engine.rag_retriever import RAGRetriever

retriever = RAGRetriever()

docs = retriever.retrieve(
    "BACnet timeout during controller restart",
    top_k=5
)

for i, doc in enumerate(docs, start=1):
    print(f"\n===== Result {i} =====")
    print("Source :", doc.metadata.get("source"))
    print("Module :", doc.metadata.get("module"))
    print(doc.page_content)