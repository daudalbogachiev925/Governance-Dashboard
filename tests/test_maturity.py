from src.maturity import assess_dimension, overall_maturity, label_of
from src.data import generate_governance_data

def test_assess_dimension():
    assert assess_dimension(30, [40, 60, 80, 95]) == 1
    assert assess_dimension(50, [40, 60, 80, 95]) == 2
    assert assess_dimension(100, [40, 60, 80, 95]) == 5

def test_overall_maturity_range():
    df = generate_governance_data(100)
    m = overall_maturity(df)
    assert 1 <= m["overall_level"] <= 5
    assert m["overall_label"] in ("Initial","Developing","Defined","Managed","Optimized")

def test_label_of():
    assert label_of(1) == "Initial"
    assert label_of(5) == "Optimized"
