def build_scorecard(df, maturity):
    return {
        "datasets_total": len(df),
        "datasets_with_owner": int(df["has_owner"].sum()),
        "datasets_with_description": int(df["has_description"].sum()),
        "datasets_with_steward": int(df["has_steward"].sum()),
        "datasets_with_quality_rules": int(df["has_quality_rules"].sum()),
        "datasets_with_pii_flag": int(df["has_pii_flag"].sum()),
        "datasets_with_lineage": int(df["has_lineage"].sum()),
        "datasets_with_contract": int(df["has_contract"].sum()),
        "avg_quality_score": round(df["quality_score"].mean(), 1),
        "critical_classification_ratio": round(
            (df["classification"].isin(["confidential", "restricted"]).mean()) * 100, 1),
        "stale_datasets_30d": int((df["last_updated_days"] > 30).sum()),
        "maturity_level": maturity["overall_level"],
        "maturity_label": maturity["overall_label"],
    }

def recommendations(maturity, scorecard):
    recs = []
    if scorecard["datasets_with_owner"] / scorecard["datasets_total"] < 0.9:
        recs.append("Назначить владельцев для всех датасетов (ownership)")
    if scorecard["datasets_with_description"] / scorecard["datasets_total"] < 0.9:
        recs.append("Заполнить описания (metadata)")
    if scorecard["datasets_with_quality_rules"] / scorecard["datasets_total"] < 0.8:
        recs.append("Добавить quality rules (data quality)")
    if scorecard["datasets_with_lineage"] / scorecard["datasets_total"] < 0.8:
        recs.append("Построить lineage (lineage)")
    if scorecard["datasets_with_contract"] / scorecard["datasets_total"] < 0.7:
        recs.append("Внедрить data contracts")
    if scorecard["stale_datasets_30d"] > scorecard["datasets_total"] * 0.3:
        recs.append("Обновить устаревшие датасеты (>30 дней)")
    if maturity["overall_level"] < 3.5:
        recs.append("Поднять общий уровень зрелости до Managed (4)")
    return recs
