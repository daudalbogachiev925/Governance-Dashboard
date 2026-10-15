import json
from datetime import datetime

def to_json(scorecard, maturity, recs, path="governance_report.json"):
    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "scorecard": scorecard,
        "maturity": maturity,
        "recommendations": recs,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return report

def summary_text(scorecard, maturity):
    return f"""
Data Governance Report
======================
Датасетов: {scorecard['datasets_total']}
Уровень зрелости: {maturity['overall_label']} ({maturity['overall_level']}/5)
Средний quality score: {scorecard['avg_quality_score']}
С критической классификацией: {scorecard['critical_classification_ratio']}%
Устаревших (>30 дней): {scorecard['stale_datasets_30d']}
"""
