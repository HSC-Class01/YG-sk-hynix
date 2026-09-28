import os,io,zipfile,time
from pathlib import Path
import requests,pandas as pd
ROOT=Path(__file__).resolve().parents[1]; API='https://opendart.fss.or.kr/api'; KEY=os.environ['DART_API_KEY']
CFG=__import__('json').loads((ROOT/'config.json').read_text(encoding='utf-8'))
def api(path,**p):
 p['api_key']=KEY; r=requests.get(API+'/'+path,params=p,timeout=60); r.raise_for_status(); return r
def main():
 with zipfile.ZipFile(io.BytesIO(api('corpCode.xml').content)) as z: corp=pd.read_xml(z.open('CORPCODE.xml'))
 code=corp[corp.stock_code.astype(str).str.zfill(6)==CFG['stock_code']].iloc[0].corp_code
 rows=[]; accounts=[]
 for y in range(CFG['start_year'],pd.Timestamp.now().year+1):
  for rc,period,cat in [('11011','FY','annual'),('11012','H1','half-year'),('11013','Q1','quarterly'),('11014','Q3','quarterly')]:
   j=api('fnlttSinglAcntAll.json',corp_code=code,bsns_year=y,reprt_code=rc,fs_div='CFS').json()
   if j.get('status')=='013': j=api('fnlttSinglAcntAll.json',corp_code=code,bsns_year=y,reprt_code=rc,fs_div='OFS').json()
   if j.get('status')!='000': continue
   for a in j.get('list',[]): accounts.append(dict(year=y,period=period,category=cat,report_code=rc,**{k:a.get(k) for k in ['fs_div','account_id','account_nm','thstrm_amount','thstrm_nm']}))
   rows.append(dict(year=y,period=period,category=cat,report_code=rc))
   time.sleep(.12)
 d=ROOT/'data'; d.mkdir(exist_ok=True)
 pd.DataFrame(rows).to_csv(d/'reports.csv',index=False); pd.DataFrame(accounts).to_csv(d/'financial_statements.csv',index=False)
if __name__=='__main__': main()
