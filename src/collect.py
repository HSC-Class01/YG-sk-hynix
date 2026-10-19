import json
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
API = "https://opendart.fss.or.kr/api"
KEY = os.environ.get("DART_API_KEY", "").strip()
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))

def api(path, **params):
    params["crtfc_key"] = KEY
    response = requests.get(f"{API}/{path}", params=params, timeout=60)
    response.raise_for_status()
    return response

def main():
    if not KEY:
        raise RuntimeError("DART_API_KEY is empty.")
    corp_code = str(CFG.get("corp_code", "")).strip()
    if len(corp_code) != 8 or not corp_code.isdigit():
        raise RuntimeError("config.json corp_code must be an 8-digit OpenDART company code.")

    reports, accounts, skipped = [], [], []
    report_types = [
        ("11011", "FY", "annual"),
        ("11012", "H1", "half-year"),
        ("11013", "Q1", "quarterly"),
        ("11014", "Q3", "quarterly"),
    ]
    for year in range(int(CFG["start_year"]), pd.Timestamp.now().year + 1):
        for report_code, period, category in report_types:
            params = dict(corp_code=corp_code, bsns_year=year, reprt_code=report_code)
            result = api("fnlttSinglAcntAll.json", **params, fs_div="CFS").json()
            fs_div = "CFS"
            if result.get("status") == "013":
                result = api("fnlttSinglAcntAll.json", **params, fs_div="OFS").json()
                fs_div = "OFS"
            status = result.get("status")
            if status == "013":
                skipped.append(f"{year}/{period}: no data in CFS or OFS")
                continue
            if status != "000":
                raise RuntimeError(
                    f"OpenDART financial API failed for {year}/{report_code} "
                    f"({status}): {result.get('message')}"
                )
            items = result.get("list", [])
            if not items:
                skipped.append(f"{year}/{period}: status 000 but empty list")
                continue
            for account in items:
                accounts.append({
                    "year": year, "period": period, "category": category,
                    "report_code": report_code, "fs_div": account.get("fs_div", fs_div),
                    "account_id": account.get("account_id"),
                    "account_nm": account.get("account_nm"),
                    "thstrm_amount": account.get("thstrm_amount"),
                    "thstrm_nm": account.get("thstrm_nm"),
                })
            reports.append({
                "year": year, "period": period, "category": category,
                "report_code": report_code, "fs_div": fs_div, "account_count": len(items)
            })
            time.sleep(0.12)

    data_dir = ROOT / "data"
    data_dir.mkdir(exist_ok=True)
    pd.DataFrame(reports, columns=["year","period","category","report_code","fs_div","account_count"]).to_csv(data_dir / "reports.csv", index=False)
    pd.DataFrame(accounts, columns=["year","period","category","report_code","fs_div","account_id","account_nm","thstrm_amount","thstrm_nm"]).to_csv(data_dir / "financial_statements.csv", index=False)
    print(f"Collected {len(reports)} reports and {len(accounts)} account rows for corp_code={corp_code}.")
    print(f"Unavailable report periods: {len(skipped)}")
    if skipped:
        print("First unavailable periods: " + "; ".join(skipped[:12]))
    if not accounts:
        raise RuntimeError("No financial statement rows were returned. Check DART_API_KEY, corp_code, and DART report availability.")

if __name__ == "__main__":
    main()
