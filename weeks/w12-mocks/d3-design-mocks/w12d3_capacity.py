"""W12 D3: arithmetic for the two design prompts. Days per month = 30."""


def online_store_size(entities: float, features: float, bytes_per_feature: float, replication: int) -> float:
    """Bytes."""
    # TODO
    raise NotImplementedError


def serving_qps(predictions_per_s: float, features_per_prediction: int, batch_lookup: bool) -> float:
    """Key-value lookups per second hitting the online store: one per feature, or one per prediction if batched."""
    # TODO
    raise NotImplementedError


def triage_cost_per_month(tickets_per_day: float, in_tokens: float, out_tokens: float, usd_per_m_in: float,
                          usd_per_m_out: float, escalation_rate: float, usd_per_human_ticket: float) -> dict:
    """{"llm": ..., "human": ..., "total": ...} per month."""
    # TODO
    raise NotImplementedError
