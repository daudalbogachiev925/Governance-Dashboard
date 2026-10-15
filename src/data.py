import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_governance_data(seed=42):
    np.random.seed(seed)
    n = 100
    df = pd.DataFrame({
        "dataset_id": [f"ds{i:04d}" for i in range(n)],
        "domain": np.random.choice(["customer", "product", "finance", "hr"], n),
        "has_owner": np.random.random(n) > 0.1,
        "has_description": np.random.random(n) > 0.2,
        "has_steward": np.random.random(n) > 0.15,
        "has_quality_rules": np.random.random(n) > 0.35,
        "has_pii_flag": np.random.random(n) > 0.25,
        "has_lineage": np.random.random(n) > 0.3,
        "has_contract": np.random.random(n) > 0.4,
        "classification": np.random.choice(
            ["public", "internal", "confidential", "restricted"], n,
            p=[0.1, 0.5, 0.3, 0.1]),
        "quality_score": np.random.uniform(50, 100, n).round(1),
        "last_updated_days": np.random.exponential(30, n).round(0),
        "consumers": np.random.randint(0, 20, n),
    })
    return df
