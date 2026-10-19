# SK hynix DART Financial Dashboard

[![🔗 대시보드 바로가기](https://img.shields.io/badge/🔗-대시보드_바로가기-2456D8?style=for-the-badge)](https://hsc-class01.github.io/YG-sk-hynix/)

OpenDART에서 SK하이닉스(종목코드 000660)의 사업·반기·분기 재무제표를 수집해 재무지표를 계산하고 GitHub Pages 대시보드로 제공합니다.

## 자동 업데이트와 배포

GitHub Actions가 매월 1일 02:15 UTC(한국시간 11:15)에 실행됩니다. 수집 → 재무비율 계산 → 대시보드 생성 → 데이터 커밋 → GitHub Pages 배포를 자동 수행합니다. `Actions → DART monthly update → Run workflow`에서 수동 실행할 수 있습니다.

첫 설정 또는 포크한 저장소에서 다음을 확인하세요.

1. [OpenDART](https://opendart.fss.or.kr/)에서 API 인증키를 발급합니다.
2. 저장소 `Settings → Secrets and variables → Actions`에 `DART_API_KEY`라는 이름으로 키를 **Secret** 등록합니다. 키를 소스 코드나 공개 파일에 적지 마세요.
3. 저장소 `Settings → Pages`의 Build and deployment Source를 `GitHub Actions`로 설정합니다.
4. `Actions` 탭에서 `DART monthly update`를 한 번 수동 실행합니다.

## 대시보드 구성

상단에는 매출액·영업이익과 이익률 차트를 배치하고, 아래에는 공시주기별 수치 테이블을 제공합니다.

- Annual: 사업보고서 (FY)
- Half-year: 반기보고서 (H1)
- Quarterly: 분기보고서 (Q1, Q3)
- 국내 Peer firms: 업종과 사업모델의 차이를 표시한 비교기업 표

수집 범위는 `config.json`의 `start_year`(현재 2015년)부터입니다. SK하이닉스 DART 고유번호는 `00164779`입니다. 연결재무제표(CFS)를 우선하고, 해당 보고서가 제공되지 않을 경우 별도재무제표(OFS)를 조회합니다.

## 계산 지표

매출액, 영업이익, 당기순이익, 자산총계, 부채총계, 자본총계, 유동자산, 유동부채 및 영업이익률, 순이익률, 부채비율, 유동비율, 자기자본비율, ROA, ROE를 표시합니다. 금액은 원 단위이며 비율은 %입니다. ROA·ROE는 기간말 자산·자본을 사용한 단순 계산값입니다. 보고서 계정명 차이나 해당 기간 공시 누락으로 일부 값은 비어 있을 수 있습니다.

## 국내 Peer firms

| 기업 | 종목코드 | 비교 관점 |
|---|---:|---|
| 삼성전자 | 005930 | 메모리·시스템 반도체 종합 경쟁사 |
| DB하이텍 | 000990 | 국내 파운드리 비교기업 |
| LX세미콘 | 108320 | 국내 팹리스 비교기업 |

삼성전자는 메모리 사업이 있어 직접적인 비교에 가장 가깝습니다. DB하이텍과 LX세미콘은 파운드리·팹리스 중심으로 사업구조와 수익모델이 다르므로 산업 내 참고기업으로 해석해야 합니다. peer 목록과 설명은 `config.json`에서 관리합니다.

## 파일

- `data/reports.csv`: 수집한 보고기간과 공시 구분
- `data/financial_statements.csv`: OpenDART 계정 원자료
- `data/metrics.csv`: 분석 지표 데이터
- `docs/index.html`: GitHub Pages 대시보드
- `src/collect.py`, `src/analyze.py`, `src/dashboard.py`: 수집·분석·화면 생성 코드

출처: 금융감독원 OpenDART. 대시보드는 공시 데이터의 계정 매칭 및 계산 결과이며 투자 조언이 아닙니다.
