"""W5 D1: estimation helpers. SI units (1 KB = 1e3 bytes). Seconds per day = 86,400. Hours per month = 730."""
import math

SECONDS_PER_DAY = 86_400
HOURS_PER_MONTH = 730


def qps(dau: float, actions_per_day: float, peak_factor: float) -> tuple:
    """(average QPS, peak QPS)."""
    # TODO
    raise NotImplementedError


def storage_bytes(items_per_day: float, bytes_per_item: float, years: float, replication: int) -> float:
    """Total bytes stored after `years` (365 days/yr), including replicas."""
    # TODO
    raise NotImplementedError


def bandwidth_gbps(qps_: float, bytes_per_request: float) -> float:
    """Gigabits per second (1 Gb = 1e9 bits)."""
    # TODO
    raise NotImplementedError


def llm_gpus(peak_qps: float, in_tokens: float, out_tokens: float, prefill_tok_s: float,
             decode_tok_s: float, headroom: float = 1.0) -> int:
    """GPUs = ceil(peak_qps * (in/prefill + out/decode) * headroom).
    Round to 9 decimals before ceil: 30 * (0.1 + 0.2) is 9.000000000000002 in floating point."""
    # TODO
    raise NotImplementedError


def monthly_cost(gpus: int, usd_per_gpu_hour: float, utilization: float = 1.0) -> float:
    """Cost of keeping `gpus` provisioned a full month. `utilization` is the fraction of time they are
    actually rented (1.0 = reserved 24/7; 0.5 = autoscaled to half the month on average)."""
    # TODO
    raise NotImplementedError


def human_bytes(n: float) -> str:
    """'512 B', '1.5 KB', '40.0 TB', '3.7 PB' (SI, one decimal above bytes)."""
    # TODO
    raise NotImplementedError
