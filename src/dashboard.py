from pathlib import Path
import pandas as pd,json
R=Path(__file__).resolve().parents[1]; D=R/'docs';D.mkdir(exist_ok=True)
df=pd.read_csv(R/'data/metrics.csv').sort_values(['year','period'],ascending=False)
cfg=json.loads((R/'config.json').read_text(encoding='utf-8'))
def section(cat,title):
 x=df[df.category==cat]
 return '<h2>'+title+'</h2>'+x.to_html(index=False,classes='data',border=0,na_rep='—') if len(x) else '<h2>'+title+'</h2><p>데이터 없음</p>'
peer=''.join('<tr><td>'+p['name']+'</td><td>'+p['stock_code']+'</td></tr>' for p in cfg['peer_firms'])
html='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SK hynix DART Dashboard</title><style>body{font:15px system-ui;background:#0b1220;color:#e8eef8;margin:0;padding:30px}main{max-width:1400px;margin:auto}h1{font-size:36px}.panel{background:#142238;padding:18px;border-radius:14px;overflow:auto;margin:16px 0}h2{margin-top:38px;color:#69d4c2}table{border-collapse:collapse;width:100%;white-space:nowrap}td,th{padding:9px;border-bottom:1px solid #34445c;text-align:right}td:first-child,th:first-child{text-align:left}th{color:#69d4c2}canvas{max-height:300px}</style><main><p>OPENDART · FINANCIAL INTELLIGENCE</p><h1>SK hynix 재무 대시보드</h1><p>2010년 이후 사업·반기·분기보고서 | 매월 1일 자동 갱신</p><div class="panel"><h2>매출액 및 영업이익 추이</h2><canvas id="c"></canvas></div>'''+section('annual','Annual · 사업보고서')+section('half-year','Half-year · 반기보고서')+section('quarterly','Quarterly · 분기보고서')+'<h2>국내 Peer firms</h2><div class="panel"><table><tr><th>기업</th><th>종목코드</th></tr>'+peer+'</table></div><p>출처: 금융감독원 OpenDART. 값은 공시 계정명 매칭 결과이며 투자 조언이 아닙니다.</p></main><script src="https://cdn.jsdelivr.net/npm/chart.js"></script><script>new Chart(document.getElementById("c"),{type:"line",data:{labels:'+json.dumps([str(int(y))+" "+p for y,p in zip(df.year,df.period)])+',datasets:[{label:"매출액",data:'+json.dumps(df.revenue.fillna(0).tolist())+',borderColor:"#69d4c2"},{label:"영업이익",data:'+json.dumps(df.operating_income.fillna(0).tolist())+',borderColor:"#8da9ff"}]},options:{responsive:true}});</script></html>'
(D/'index.html').write_text(html,encoding='utf-8')
