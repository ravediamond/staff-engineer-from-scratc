"""W12 D5: an existing eval runner (read it first), plus two features to add while pairing."""
from collections import defaultdict


class TransientError(Exception):
    """Timeouts, 429s, 503s: worth retrying."""


def run_case(system, case: dict) -> dict:
    """Existing: run one case. Score 1.0 if the output equals case["expected"], else 0.0.
    Exceptions are recorded, never raised."""
    try:
        out = system(case["input"])
        return {"id": case["id"], "score": float(out == case["expected"]), "error": None, "attempts": 1}
    except Exception as e:
        return {"id": case["id"], "score": 0.0, "error": f"{type(e).__name__}: {e}", "attempts": 1}


def run_case_with_retry(system, case: dict, retries: int) -> dict:
    """NEW: like run_case, but retry up to `retries` extra times when system raises TransientError.
    Any other exception: no retry. Record the total attempts. A final TransientError is recorded as an error."""
    attempts = 0
    while True:
        attempts += 1
        try:
            out = system(case["input"])
            return {"id": case["id"], "score": float(out == case["expected"]), "error": None, "attempts": attempts}
        except TransientError as e:
            if attempts > retries:
                return {"id": case["id"], "score": 0.0, "error": f"TransientError: {e}", "attempts": attempts}
        except Exception as e:
            return {"id": case["id"], "score": 0.0, "error": f"{type(e).__name__}: {e}", "attempts": attempts}


def slice_report(results: list, cases: list) -> dict:
    """NEW: {slice: {"n": count, "mean": mean score, "errors": count of results with an error}} using case["slice"]."""
    by_id = {c["id"]: c for c in cases}
    acc = defaultdict(list)
    for r in results:
        acc[by_id[r["id"]]["slice"]].append(r)
    return {s: {"n": len(rs), "mean": sum(r["score"] for r in rs) / len(rs),
                "errors": sum(1 for r in rs if r["error"])} for s, rs in acc.items()}


def run_all(system, cases: list, retries: int = 0, by_slice: bool = False) -> dict:
    """Existing signature, extended. Returns {"results", "mean"} and, if by_slice, "slices".
    retries > 0 uses run_case_with_retry; retries == 0 keeps the old behaviour (run_case)."""
    if retries > 0:
        results = [run_case_with_retry(system, c, retries) for c in cases]
    else:
        results = [run_case(system, c) for c in cases]
    out = {"results": results, "mean": sum(r["score"] for r in results) / len(results)}
    if by_slice:
        out["slices"] = slice_report(results, cases)
    return out
