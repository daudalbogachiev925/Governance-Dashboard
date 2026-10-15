import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data import generate_governance_data
from src.maturity import overall_maturity
from src.scorecard import build_scorecard, recommendations
from src.reports import summary_text

st.set_page_config(page_title="Governance Dashboard", layout="wide")
st.title("📈 Data Governance Dashboard")

@st.cache_data
def load():
    return generate_governance_data(200)

df = load()
maturity = overall_maturity(df)
scorecard = build_scorecard(df, maturity)
recs = recommendations(maturity, scorecard)

# Top KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Datasets", scorecard["datasets_total"])
c2.metric("Maturity", f"{scorecard['maturity_label']} ({scorecard['maturity_level']}/5)")
c3.metric("Avg Quality", scorecard["avg_quality_score"])
c4.metric("Stale >30d", scorecard["stale_datasets_30d"])

tab1, tab2, tab3, tab4 = st.tabs(
    ["🎯 Maturity", "📊 Scorecard", "🎨 Домены", "💡 Рекомендации"])

with tab1:
    st.subheader("Уровень зрелости по измерениям")
    dims = maturity["dimensions"]
    fig = go.Figure(data=go.Scatterpolar(
        r=list(dims.values()),
        theta=list(dims.keys()),
        fill="toself",
        name="Maturity"))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                      showlegend=False,
                      title=f"Overall: {maturity['overall_label']}")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Метрики")
    st.dataframe(pd.DataFrame([maturity["metrics"]]).T.rename(columns={0: "value"}))

with tab2:
    st.subheader("Scorecard")
    for k, v in scorecard.items():
        st.write(f"- **{k}**: {v}")

with tab3:
    st.subheader("Датасеты по доменам")
    domain_stats = df.groupby("domain").agg(
        count=("dataset_id", "count"),
        avg_quality=("quality_score", "mean"),
        with_owner=("has_owner", "sum"),
        critical=("classification", lambda x: (x.isin(["confidential","restricted"])).sum()),
    ).round(1)
    st.dataframe(domain_stats)

    st.subheader("Quality distribution")
    st.plotly_chart(px.histogram(df, x="quality_score", color="domain"),
                    use_container_width=True)

    st.subheader("Classification")
    st.plotly_chart(px.pie(df, names="classification"),
                    use_container_width=True)

with tab4:
    st.subheader("Рекомендации")
    for r in recs:
        st.warning(f"🔧 {r}")

    st.subheader("Summary")
    st.code(summary_text(scorecard, maturity))

    st.download_button(
        "Скачать отчёт (JSON)",
        data=pd.DataFrame([scorecard]).to_json(force_ascii=False),
        file_name="governance_report.json")
