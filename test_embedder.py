from ingestion.embedder import embedder

vec = embedder.embed(
    "hello world"
)

print(
    "Vector size:",
    len(vec[0])
)