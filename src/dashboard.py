from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)
metrics_path = ROOT / "data/metrics.csv"
df = pd.read_csv(metrics_path).fillna("")
period_order = {"FY": 1, "H1": 2, "Q1": 3, "Q3": 4}
df["_order"] = df["period"].map(period_order).fillna(9)
df = df.sort_values(["year", "_order"], ascending=[True, True])
cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
def esc(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
def fmt(value):
    try:
        n = float(value)
        return "—" if pd.isna(n) else f"{n:,.1f}" if "%" in str(value) else f"{n:,.0f}"
    except (TypeError, ValueError):
        return "—" if value == "" else esc(value)
metric_labels = {
    "revenue":"매출액 (원)", "operating_income":"영업이익 (원)", "net_income":"당기순이익 (원)",
    "assets":"자산총계 (원)", "liabilities":"부채총계 (원)", "equity":"자본총계 (원)",
    "current_assets":"유동자산 (원)", "current_liabilities":"유동부채 (원)",
    "operating_margin_pct":"영업이익률 (%)", "net_margin_pct":"순이익률 (%)",
    "debt_to_equity_pct":"부채비율 (%)", "current_ratio_pct":"유동비율 (%)",
    "equity_ratio_pct":"자기자본비율 (%)", "roa_pct":"ROA (%)", "roe_pct":"ROE (%)"
}
columns = ["year", "period"] + list(metric_labels)
def table(category, title):
    part = df[df.category == category]
    if part.empty:
        body = '<tr><td colspan="17" class="empty">공시 데이터가 없습니다.</td></tr>'
    else:
        rows = []
        for _, r in part.sort_values(["year","_order"], ascending=False).iterrows():
            cells = [f'<td>{int(r["year"])}</td>', f'<td>{esc(r["period"])}</td>']
            for key in metric_labels:
                val = r.get(key, "")
                try:
                    n = float(val)
                    cells.append(f'<td class="num">{("—" if pd.isna(n) else f"{n:,.1f}" if key.endswith("_pct") else f"{n:,.0f}")}</td>')
                except (TypeError, ValueError):
                    cells.append('<td class="num">—</td>')
            rows.append("<tr>" + "".join(cells) + "</tr>")
        body = "".join(rows)
    heads = "<th>연도</th><th>기간</th>" + "".join(f"<th>{label}</th>" for label in metric_labels.values())
    return f'<section class="card"><div class="section-title"><div><span class="eyebrow">{category.upper()}</span><h2>{title}</h2></div><span class="count">{len(part)}개 기간</span></div><div class="table-wrap"><table><thead><tr>{heads}</tr></thead><tbody>{body}</tbody></table></div></section>'
recent = df.iloc[-1] if len(df) else {}
latest_year = int(recent["year"]) if len(df) else "—"
latest_period = recent["period"] if len(df) else "—"
def kpi(key):
    val = recent.get(key, "")
    try:
        return f"{float(val):,.1f}%" if key.endswith("_pct") else f"{float(val)/1_000_000_000_000:,.2f}조 원"
    except (TypeError, ValueError):
        return "—"
labels = [f'{int(r.year)} {r.period}' for r in df.itertuples()]
def series(key):
    out=[]
    for value in df[key]:
        try: out.append(float(value) if value != "" else None)
        except (ValueError, TypeError): out.append(None)
    return out
peers = "".join(f'<tr><td>{esc(p["name"])}</td><td>{esc(p["stock_code"])}</td><td>{esc(p.get("relationship","국내 반도체 비교기업"))}</td></tr>' for p in cfg["peer_firms"])
generated = pd.Timestamp.now(tz="Asia/Seoul").strftime("%Y-%m-%d %H:%M KST")
html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>SK hynix 재무 대시보드</title><style>
:root{{--bg:#f3f6fb;--ink:#17233a;--muted:#66748b;--line:#e5eaf2;--blue:#2856d8;--cyan:#1c9eac;--card:#fff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.6 Inter,Pretendard,"Noto Sans KR",system-ui,sans-serif}}main{{max-width:1440px;margin:auto;padding:36px 28px 70px}}header{{padding:30px 34px;border-radius:24px;background:linear-gradient(120deg,#13264a,#244a92 65%,#167e9a);color:white;box-shadow:0 18px 42px #243d6b24}}.eyebrow{{font-size:11px;font-weight:800;letter-spacing:.15em;color:#1c9eac}}header .eyebrow{{color:#8de3e8}}h1{{font-size:34px;line-height:1.2;margin:10px 0}}.sub{{color:#d6e1f5;margin:0}}.meta{{margin-top:22px;font-size:12px;color:#c7d5ef}}.kpis{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:18px 0}}.kpi,.card{{background:var(--card);border:1px solid var(--line);border-radius:18px;box-shadow:0 8px 24px #1f36520a}}.kpi{{padding:19px 21px}}.kpi label{{color:var(--muted);font-size:12px}}.kpi strong{{display:block;margin-top:7px;font-size:24px;letter-spacing:-.03em}}.grid{{display:grid;grid-template-columns:1.55fr 1fr;gap:16px;margin:16px 0}}.card{{padding:22px;margin:16px 0}}.grid .card{{margin:0}}h2{{font-size:19px;margin:4px 0 14px}}.section-title{{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}}.count{{font-size:12px;color:var(--muted)}}.chart-box{{height:310px}}.table-wrap{{overflow:auto;border:1px solid var(--line);border-radius:12px}}table{{width:100%;border-collapse:collapse;white-space:nowrap;font-variant-numeric:tabular-nums}}thead th{{position:sticky;top:0;background:#f3f6fb;color:#475772;font-size:11px;text-align:right;padding:11px 12px;border-bottom:1px solid var(--line)}}thead th:first-child,thead th:nth-child(2),tbody td:first-child,tbody td:nth-child(2){{text-align:left}}tbody td{{padding:10px 12px;border-bottom:1px solid #eef1f6;text-align:right;font-size:12px}}tbody tr:hover{{background:#f8faff}}tbody tr:last-child td{{border-bottom:0}}.num{{font-variant-numeric:tabular-nums}}.empty{{text-align:center;color:var(--muted);padding:24px}}.note{{color:var(--muted);font-size:12px}}a{{color:inherit}}footer{{color:var(--muted);font-size:12px;margin-top:26px}}@media(max-width:900px){{.grid{{grid-template-columns:1fr}}.kpis{{grid-template-columns:repeat(2,1fr)}}main{{padding:18px 12px 42px}}header{{padding:24px}}h1{{font-size:27px}}}}
</style></head><body><main><header><span class="eyebrow">OPENDART · FINANCIAL INTELLIGENCE</span><h1>SK hynix 재무 대시보드</h1><p class="sub">공시 재무제표의 흐름과 수익성·안정성 지표를 한눈에 확인합니다.</p><div class="meta">기준 데이터: {latest_year} {latest_period} · 최근 갱신: {generated} · 금액 단위: 원</div></header>
<div class="kpis"><div class="kpi"><label>최근 매출액</label><strong>{kpi("revenue")}</strong></div><div class="kpi"><label>최근 영업이익</label><strong>{kpi("operating_income")}</strong></div><div class="kpi"><label>영업이익률</label><strong>{kpi("operating_margin_pct")}</strong></div><div class="kpi"><label>부채비율</label><strong>{kpi("debt_to_equity_pct")}</strong></div></div>
<div class="grid"><section class="card"><span class="eyebrow">PERFORMANCE</span><h2>매출 및 영업이익 추이</h2><div class="chart-box"><canvas id="financial"></canvas></div></section><section class="card"><span class="eyebrow">PROFITABILITY</span><h2>수익성 지표 추이</h2><div class="chart-box"><canvas id="margins"></canvas></div></section></div>
{table("annual","연간 재무 데이터 · Annual")}{table("half-year","반기 재무 데이터 · Half-year")}{table("quarterly","분기 재무 데이터 · Quarterly")}
<section class="card"><span class="eyebrow">DOMESTIC COMPARABLES</span><h2>국내 Peer firms</h2><p class="note">사업모델이 완전히 같지 않은 반도체 업종 내 국내 비교기업입니다. DB하이텍과 LX세미콘은 각각 파운드리·팹리스 기업으로 사업구조 차이를 감안해 해석해야 합니다.</p><div class="table-wrap"><table><thead><tr><th>기업</th><th>종목코드</th><th>비교 관점</th></tr></thead><tbody>{peers}</tbody></table></div></section>
<footer>출처: 금융감독원 OpenDART 사업·반기·분기보고서. CFS 우선, 미제공 시 OFS 사용. 원자료 계정명의 매칭 및 계산 결과로 일부 지표는 공시 여부에 따라 비어 있을 수 있습니다. 유동비율·부채비율·ROA·ROE는 모두 % 표기입니다. 본 자료는 투자 조언이 아닙니다.</footer></main>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script><script>
const labels={json.dumps(labels, ensure_ascii=False)};
new Chart(document.getElementById("financial"),{{type:"line",data:{{labels,datasets:[{{label:"매출액 (조 원)",data:{json.dumps(series("revenue"))}.map(v=>v==null?null:v/1e12),borderColor:"#2856d8",backgroundColor:"#2856d81b",fill:true,tension:.28,pointRadius:2}},{{label:"영업이익 (조 원)",data:{json.dumps(series("operating_income"))}.map(v=>v==null?null:v/1e12),borderColor:"#1c9eac",tension:.28,pointRadius:2}}]}},options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:"index",intersect:false}},scales:{{y:{{grid:{{color:"#edf0f5"}}}}}}}}}});
new Chart(document.getElementById("margins"),{{type:"line",data:{{labels,datasets:[{{label:"영업이익률",data:{json.dumps(series("operating_margin_pct"))},borderColor:"#2856d8",tension:.3,pointRadius:2}},{{label:"순이익률",data:{json.dumps(series("net_margin_pct"))},borderColor:"#e49b37",tension:.3,pointRadius:2}}]}},options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:"index",intersect:false}},scales:{{y:{{ticks:{{callback:v=>v+"%"}},grid:{{color:"#edf0f5"}}}}}}}}}});
</script></body></html>"""
(DOCS / "index.html").write_text(html, encoding="utf-8")
