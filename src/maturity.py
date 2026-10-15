"""
Модель зрелости Data Governance по 5 уровням (по DAMA/IBM):
1. Initial — ad-hoc
2. Developing — базовые процессы
3. Defined — формализованные процессы
4. Managed — измеряется и управляется
5. Optimized — continuous improvement
"""

DIMENSIONS = [
    "ownership", "metadata", "quality", "privacy",
    "lineage", "access_control", "compliance",
]

def assess_dimension(value, thresholds):
    """
    thresholds: [t1, t2, t3, t4] — границы уровней 2, 3, 4, 5
    """
    for i, t in enumerate(thresholds):
        if value < t:
            return i + 1
    return 5

def overall_maturity(df):
    metrics = {
        "ownership": df["has_owner"].mean() * 100,
        "metadata": df["has_description"].mean() * 100,
        "stewardship": df["has_steward"].mean() * 100,
        "quality": df["quality_score"].mean(),
        "privacy": df["has_pii_flag"].mean() * 100,
        "lineage": df["has_lineage"].mean() * 100,
        "contracts": df["has_contract"].mean() * 100,
    }

    dimensions = {
        "ownership": assess_dimension(metrics["ownership"], [40, 60, 80, 95]),
        "metadata": assess_dimension(metrics["metadata"], [40, 60, 80, 95]),
        "quality": assess_dimension(metrics["quality"], [50, 65, 80, 92]),
        "privacy": assess_dimension(metrics["privacy"], [30, 50, 70, 90]),
        "lineage": assess_dimension(metrics["lineage"], [30, 50, 70, 90]),
        "access_control": assess_dimension(metrics["ownership"], [40, 60, 80, 95]),
        "compliance": assess_dimension(metrics["privacy"], [30, 50, 70, 90]),
    }

    avg = sum(dimensions.values()) / len(dimensions)
    return {
        "metrics": {k: round(v, 1) for k, v in metrics.items()},
        "dimensions": dimensions,
        "overall_level": round(avg, 2),
        "overall_label": label_of(avg),
    }

def label_of(level):
    labels = {1: "Initial", 2: "Developing", 3: "Defined",
              4: "Managed", 5: "Optimized"}
    return labels.get(round(level), "Unknown")
