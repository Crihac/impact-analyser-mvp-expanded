def calculate_risk(dist: int, meta: dict) -> float:
    impact_prob = {0: 1.0, 1: 0.7, 2: 0.4}.get(dist, 0.2)
    coverage_pct = meta.get("coverage", 50) / 100.0
    criticality = meta.get("criticality", 0.5)
    churn = meta.get("churn", 0)
    churn_norm = min(churn / 10.0, 1.0)
    risk = (
        0.45 * impact_prob +            # directness
        0.25 * (1.0 - coverage_pct) +   # low coverage increases risk
        0.20 * churn_norm +             # recent churn
        0.10 * criticality              # critical modules score higher
    )
    return round(risk * 100.0, 2)
