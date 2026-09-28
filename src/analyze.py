from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1]; d=pd.read_csv(R/'data/financial_statements.csv').fillna('')
aliases={'revenue':['매출액','수익(매출액)'],'operating_income':['영업이익','영업이익(손실)'],'net_income':['당기순이익','당기순이익(손실)'],'assets':['자산총계'],'liabilities':['부채총계'],'equity':['자본총계'],'current_assets':['유동자산'],'current_liabilities':['유동부채']}
def n(x):
 try:return float(str(x).replace(',',''))
 except:return None
rows=[]
for (y,p,c),g in d.groupby(['year','period','category']):
 v={}
 for k,names in aliases.items():
  a=g[g.account_nm.isin(names)]; v[k]=n(a.iloc[0].thstrm_amount) if len(a) else None
 def ratio(a,b):return a/b*100 if a is not None and b not in (None,0) else None
 v.update(operating_margin_pct=ratio(v['operating_income'],v['revenue']),net_margin_pct=ratio(v['net_income'],v['revenue']),debt_to_equity_pct=ratio(v['liabilities'],v['equity']),current_ratio_pct=ratio(v['current_assets'],v['current_liabilities']),equity_ratio_pct=ratio(v['equity'],v['assets']),roa_pct=ratio(v['net_income'],v['assets']),roe_pct=ratio(v['net_income'],v['equity']))
 rows.append(dict(year=y,period=p,category=c,**v))
pd.DataFrame(rows).to_csv(R/'data/metrics.csv',index=False)
