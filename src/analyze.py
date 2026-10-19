from pathlib import Path
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "data/financial_statements.csv"
if not source.exists() or source.stat().st_size == 0:
    raise RuntimeError("financial_statements.csv is missing or empty; run src/collect.py first.")
d = pd.read_csv(source).fillna("")
if d.empty:
    raise RuntimeError("OpenDART returned no financial statement rows; review the collector log.")

aliases = {
    "revenue": ["매출액", "수익(매출액)", "매출", "영업수익"],
    "operating_income": ["영업이익", "영업이익(손실)"],
    "net_income": ["당기순이익", "당기순이익(손실)", "분기순이익", "분기순이익(손실)", "반기순이익", "반기순이익(손실)"],
    "assets": ["자산총계"], "liabilities": ["부채총계"], "equity": ["자본총계"],
    "current_assets": ["유동자산"], "current_liabilities": ["유동부채"],
}
preferred_ids = {
    "revenue": ["ifrs-full_Revenue", "ifrs_Revenue"],
    "operating_income": ["ifrs-full_OperatingIncomeLoss", "ifrs_OperatingIncomeLoss"],
    "net_income": ["ifrs-full_ProfitLoss", "ifrs_ProfitLoss"],
    "assets": ["ifrs-full_Assets", "ifrs_Assets"],
    "liabilities": ["ifrs-full_Liabilities", "ifrs_Liabilities"],
    "equity": ["ifrs-full_Equity", "ifrs_Equity"],
    "current_assets": ["ifrs-full_CurrentAssets", "ifrs_CurrentAssets"],
    "current_liabilities": ["ifrs-full_CurrentLiabilities", "ifrs_CurrentLiabilities"],
}
def number(value):
    try: return float(str(value).replace(",", ""))
    except (TypeError, ValueError): return None
def ratio(a, b):
    return a / b * 100 if a is not None and b not in (None, 0) else None
def extract(group, key):
    preferred = group[group.account_id.isin(preferred_ids[key])]
    candidates = preferred if not preferred.empty else group[
        group.account_nm.map(lambda value: re.sub(r"\s+", "", str(value))).isin(
            [re.sub(r"\s+", "", name) for name in aliases[key]]
        )
    ]
    for amount in candidates.thstrm_amount:
        parsed = number(amount)
        if parsed is not None:
            return parsed
    return None

rows = []
for (year, period, category), group in d.groupby(["year", "period", "category"]):
    values = {key: extract(group, key) for key in aliases}
    values.update(
        operating_margin_pct=ratio(values["operating_income"], values["revenue"]),
        net_margin_pct=ratio(values["net_income"], values["revenue"]),
        debt_to_equity_pct=ratio(values["liabilities"], values["equity"]),
        current_ratio_pct=ratio(values["current_assets"], values["current_liabilities"]),
        equity_ratio_pct=ratio(values["equity"], values["assets"]),
        roa_pct=ratio(values["net_income"], values["assets"]),
        roe_pct=ratio(values["net_income"], values["equity"]),
    )
    rows.append({"year": year, "period": period, "category": category, **values})
out = ROOT / "data/metrics.csv"
pd.DataFrame(rows).to_csv(out, index=False)
print(f"Wrote {len(rows)} financial metric rows to {out}.")
