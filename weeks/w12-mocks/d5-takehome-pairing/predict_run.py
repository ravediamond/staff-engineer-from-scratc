"""Self-contained. Run after predict.md."""
print("1. real bugs (KeyError, assertion failures) get retried: slower runs and flaky-looking results that hide defects")
print("2. 3 calls (1 + 2 retries), passes on the third")
