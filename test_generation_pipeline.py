from ai_engine.generation_pipeline import GenerationPipeline

pipeline = GenerationPipeline()

result = pipeline.generate(
    requirement="Verify A2L leak alarm during compressor startup"
)

print("\nPipeline Completed\n")

print(result["quality"])

print(result["execution"])

print(result["report"])