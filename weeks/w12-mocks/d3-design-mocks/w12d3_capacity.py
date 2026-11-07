"""W12 D3: arithmetic for the two design prompts. Days per month = 30."""


def online_store_size(entities: float, features: float, bytes_per_feature: float, replication: int) -> float:
    """Bytes."""
    return entities * features * bytes_per_feature * replication


def serving_qps(predictions_per_s: float, features_per_prediction: int, batch_lookup: bool) -> float:
    """Key-value lookups per second hitting the online store: one per feature, or one per prediction if batched."""
    return predictions_per_s if batch_lookup else predictions_per_s * features_per_prediction


def triage_cost_per_month(tickets_per_day: float, in_tokens: float, out_tokens: float, usd_per_m_in: float,
                          usd_per_m_out: float, escalation_rate: float, usd_per_human_ticket: float) -> dict:
    """{"llm": ..., "human": ..., "total": ...} per month."""
    n = tickets_per_day * 30
    llm = n * (in_tokens * usd_per_m_in + out_tokens * usd_per_m_out) / 1e6
    human = n * escalation_rate * usd_per_human_ticket
    return {"llm": llm, "human": human, "total": llm + human}
