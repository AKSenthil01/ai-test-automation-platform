from ai_engine.rag_engine import RAGEngine

rag = RAGEngine()

result = rag.retrieve(
    "Verify A2L leak alarm during compressor startup"
)

print(result)