"""Self-contained. Run after predict.md."""
print("1. reject before executing; return an observation listing the errors (missing 'path', unexpected 'pth')")
print("2. exactly 5, then status 'max_steps' with no answer")
print("3. retries (bounded) belong in the executor; after that, return an error observation so the model can adapt")
