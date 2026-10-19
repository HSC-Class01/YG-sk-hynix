from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "metrics.csv"
PEERS = ROOT / "data" / "peers.csv"

st.set_page_config(
    page_title="SK hynix DART Financial Dashboard", page_icon="📊", layout="wide"
)
st.title("SK hynix DART Financial Dashboard")
st.caption("OpenDART · 연결재무제표 우선 · 사업/반기/분기보고서 · 월간 자동 업데이트")

if not DATA.exists() or DATA.stat().st_size == 0:
    st.warning("아직 분석 데이터가 없습니다. GitHub Actions에서 수집 워크플로를 실행하세요.")
    st.stop()

df = pd.read_csv(DATA)
if df.empty:
    st.warning("분석 데이터가 비어 있습니다. OpenDART Secret과 Actions 로그를 확인하세요.")
    st.stop()

df = df.sort_values(["year", "period_order"]).copy()
df["label"] = df["year"].astype(str) + " " + df["period"].astype(str)
latest = df[df["category"] == "annual"].iloc[-1] if (df["category"] == "annual").any() else df.iloc[-1]

def won(value: float) -> str:
    return f"{value / 1e12:,.1f}조원" if pd.notna(value) else "—"

def percent(value: float) -> str:
    return f"{value:,.1f}%" if pd.notna(value) else "—"

c1, c2, c3, c4 = st.columns(4)
c1.metric("최근 매출", won(latest["revenue"]))
c2.metric("최근 영업이익", won(latest["operating_income"]))
c3.metric("영업이익률", percent(latest["operating_margin_pct"]))
c4.metric("부채비율", percent(latest["debt_to_equity_pct"]))

left, right = st.columns(2)
with left:
    figure = px.line(
        df, x="label", y=["revenue", "operating_income", "net_income"],
        markers=True, title="매출·영업이익·순이익 추이",
    )
    figure.update_yaxes(tickformat=".2s")
    st.plotly_chart(figure, use_container_width=True)
with right:
    figure = px.line(
        df, x="label", y=["operating_margin_pct", "net_margin_pct", "roe_pct"],
        markers=True, title="수익성 추이(%)",
    )
    st.plotly_chart(figure, use_container_width=True)

for category, title in (
    ("annual", "Annual"), ("half-year", "Half-year"), ("quarterly", "Quarterly")
):
    st.subheader(title)
    subset = df[df["category"] == category].sort_values(
        ["year", "period_order"], ascending=False
    )
    st.dataframe(subset.reset_index(drop=True), use_container_width=True, hide_index=True)

st.subheader("국내 비교 기업")
if PEERS.exists():
    st.dataframe(pd.read_csv(PEERS), use_container_width=True, hide_index=True)

st.caption(
    "자료: 금융감독원 OpenDART. 구조화 재무제표 API에 없는 과거 기간은 수집 현황에 미제공으로 표시됩니다."
)
