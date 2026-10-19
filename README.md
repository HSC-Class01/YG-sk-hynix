# SK hynix OpenDART Financial Dashboard

[![🔗 대시보드 바로가기](https://img.shields.io/badge/🔗-대시보드_바로가기-2456D8?style=for-the-badge)](https://hsc-class01.github.io/YG-sk-hynix/)

SK하이닉스(000660)의 OpenDART 사업·반기·분기보고서를 수집하고 주요 재무 수치와 비율을 분석해 GitHub Pages에서 보여줍니다.

## 대시보드

**[🔗 대시보드 바로가기](https://hsc-class01.github.io/YG-sk-hynix/)** · [GitHub 저장소](https://github.com/HSC-Class01/YG-sk-hynix)

## 기능

- 매출·영업이익·순이익 추이, 수익성·안정성 비율을 상단 차트와 KPI로 표시
- Annual, Half-year, Quarterly를 각각 별도 상세 테이블로 제공
- 공시 수집 현황 및 국내 peer firms 표 제공
- CFS(연결) 우선 수집, 연결 자료가 없을 때 OFS(별도) 대체
- 매월 1일 00:15 UTC (한국시간 09:15) 자동 수집·분석·Pages 배포
- 수동 실행은 GitHub 저장소의 `Actions → SK hynix DART dashboard → Run workflow`

## 최초 설정과 OpenDART API 키 입력

1. [OpenDART](https://opendart.fss.or.kr/)에서 인증키를 발급합니다.
2. GitHub 저장소의 `Settings → Secrets and variables → Actions → New repository secret`으로 이동합니다.
3. Secret 이름에 `OPENDART_API_KEY`, 값에 발급받은 인증키를 입력하고 저장합니다. 키를 소스 파일에 직접 입력하지 마세요.
4. `Settings → Pages → Build and deployment`에서 Source를 **GitHub Actions**로 설정합니다.
5. `Actions`에서 **SK hynix DART dashboard**를 열고 **Run workflow**를 한 번 실행합니다.

저장소 관리자가 Secret 등록을 마쳐야 실제 DART 수집과 첫 데이터 생성이 가능합니다. API 키는 GitHub Actions의 환경변수로만 전달됩니다. 기존 설정에서 `DART_API_KEY`를 사용하고 있다면 그대로 사용할 수 있으며, 새 설정은 `OPENDART_API_KEY` 이름을 권장합니다.

## 주요 데이터와 계산 기준

금액 수치는 원 단위 원자료를 저장하고 대시보드에서 억원 단위로 표시합니다. 영업이익률·순이익률·부채비율·유동비율·자기자본비율·ROA·ROE를 계산합니다. 분기보고서의 누적 손익 및 현금흐름은 반기 누적액을 차감하여 Q3 단독 분기값으로 표시합니다. 자산·부채·자본은 보고기간 말 잔액입니다. ROA·ROE는 평균 잔액이 아닌 보고기간 말 잔액을 분모로 사용합니다.

OpenDART 구조화 재무제표 API에서 제공하지 않는 기간은 `data/reports.csv`에 `missing`으로 기록됩니다. 계정명 차이에 따라 일부 값이 비어 있을 수 있습니다. 분석 데이터는 공시 원문을 재분류·계산한 참고 정보이며 투자 조언이 아닙니다.

## 국내 Peer firms

| 기업 | 종목코드 | 비교 관점 |
|---|---:|---|
| 삼성전자 | 005930 | 메모리·시스템 반도체 종합 경쟁사이며 직접 비교에 가장 가까움 |
| DB하이텍 | 000990 | 국내 파운드리 비교기업, 사업구조 차이 유의 |
| LX세미콘 | 108320 | 국내 팹리스 비교기업, 사업구조 차이 유의 |

기업과 비교 설명은 `data/peers.csv`에서 관리합니다.

## 로컬 실행

```powershell
python -m pip install -r requirements.txt
$env:OPENDART_API_KEY = "발급받은_OpenDART_인증키"
python -m src.collect
python -m src.analyze
python -m src.dashboard
python -m http.server 8000 --directory docs
```

브라우저에서 `http://localhost:8000`을 여세요. `requirements-app.txt`를 설치하면 보조 Streamlit 화면도 실행할 수 있습니다.

## 주요 파일

- `src/collect.py`: DART API 수집
- `src/analyze.py`: 계정 추출과 재무비율 계산
- `src/dashboard.py`, `docs/`: 대시보드 데이터와 정적 화면
- `data/financial_statements.csv`: OpenDART 계정 원자료
- `data/reports.csv`: 기간별 수집·누락 상태
- `data/metrics.csv`: 분석 수치와 재무비율
- `data/peers.csv`: 국내 비교기업 목록

## Agent 개발용 ZIP

함께 제공하는 `SK_hynix_DART_Agent.zip`은 숨김 파일 없이 개발용 파일을 포함합니다. Actions 워크플로는 ZIP 내부의 `github_workflows/update_dart.yml`을 저장소의 `.github/workflows/update_dart.yml`로 복사해 등록합니다. 자세한 절차는 `docs/SETUP.md`를 참고하세요.
