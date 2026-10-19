import io
import json
import os
import time
import zipfile
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


def dart_error(payload):
    try:
        root = ET.fromstring(payload)
        return root.findtext("status"), root.findtext("message")
    except ET.ParseError:
        try:
            body = json.loads(payload)
            return body.get("status"), body.get("message")
        except (json.JSONDecodeError, AttributeError):
            return None, "Unrecognized OpenDART response"


def main():
    if not KEY:
        raise RuntimeError("DART_API_KEY is empty.")

    corp_response = api("corpCode.xml")
    archive = io.BytesIO(corp_response.content)
    if not zipfile.is_zipfile(archive):
        status, message = dart_error(corp_response.content)
        raise RuntimeError(f"OpenDART corpCode.xml failed ({status}): {message}")

    archive.seek(0)
    with zipfile.ZipFile(archive) as zf:
        corp = pd.read_xml(zf.open("CORPCODE.xml"), parser="etree")

    stock_code = str(CFG["stock_code"]).zfill(6)
    matches = corp[corp["stock_code"].fillna("").astype(str).str.zfill(6) == stock_code]
    if matches.empty:
        raise RuntimeError(f"Stock code {stock_code} was not found in OpenDART corp codes.")
    corp_code = matches.iloc[0]["corp_code"]

    reports = []
    accounts = []
    report_types = [
        ("11011", "FY", "annual"),
        ("11012", "H1", "half-year"),
        ("11013", "Q1", "quarterly"),
        ("11014", "Q3", "quarterly"),
    ]

    for year in range(int(CFG["start_year"]), pd.Timestamp.now().year + 1):
        for report_code, period, category in report_types:
            response = api(
                "fnlttSinglAcntAll.json",
                corp_code=corp_code,
                bsns_year=year,
                reprt_code=report_code,
                fs_div="CFS",
            )
            result = response.json()
            if result.get("status") == "013":
                response = api(
                    "fnlttSinglAcntAll.json",
                    corp_code=corp_code,
                    bsns_year=year,
                    reprt_code=report_code,
                    fs_div="OFS",
                )
                result = response.json()

            if result.get("status") == "013":
                continue
            if result.get("status") != "000":
                raise RuntimeError(
                    f"OpenDART financial API failed for {year}/{report_code} "
                    f"({result.get('status')}): {result.get('message')}"
                )

            for account in result.get("list", []):
                accounts.append(
                    {
                        "year": year,
                        "period": period,
                        "category": category,
                        "report_code": report_code,
                        **{
                            key: account.get(key)
                            for key in (
                                "fs_div",
                                "account_id",
                                "account_nm",
                                "thstrm_amount",
                                "thstrm_nm",
                            )
                        },
                    }
                )
            reports.append(
                {
                    "year": year,
                    "period": period,
                    "category": category,
                    "report_code": report_code,
                }
            )
            time.sleep(0.12)

    data_dir = ROOT / "data"
    data_dir.mkdir(exist_ok=True)
    pd.DataFrame(reports).to_csv(data_dir / "reports.csv", index=False)
    pd.DataFrame(accounts).to_csv(data_dir / "financial_statements.csv", index=False)


if __name__ == "__main__":
    main()
