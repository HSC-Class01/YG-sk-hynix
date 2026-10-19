# SK hynix DART Financial Dashboard

🔗 [대시보드 바로가기](https://hsc-class01.github.io/YG-sk-hynix/)

OpenDART에서 SK하이닉스(종목코드 000660)의 사업·반기·분기 재무제표를 수집하고 CSV와 정적 대시보드를 생성합니다. 데이터는 원 단위로 보존하며, 연결재무제표(CFS)를 우선 수집하고 제공되지 않는 보고서는 별도재무제표(OFS)를 대체 조회합니다.

## 자동화

`.github/workflows/dart-monthly.yml`이 매월 1일 02:15 UTC(한국시간 11:15)에 실행됩니다. `Actions` 탭에서 `DART monthly update`를 수동 실행할 수도 있습니다. 이 작업은 공시 자료 수집 → 지표 계산 → 대시보드 생성 → CSV와 HTML 갱신 커밋 → GitHub Pages 배포 순으로 진행합니다.

## 최초 설정

1. 저장소 `Settings → Secrets and variables → Actions`에서 `DART_API_KEY` secret을 등록합니다. 키는 [OpenDART](https://opendart.fss.or.kr/)에서 발급받습니다.
2. 저장소 `Settings → Pages`의 Build and deployment에서 Source를 `GitHub Actions`로 설정합니다.
3. `Actions` 탭에서 `DART monthly update`를 수동 실행해 첫 데이터를 수집하고 대시보드를 배포합니다.

기본 시작 연도는 `config.json`의 `start_year`(2010)이며, OpenDART가 제공하는 보고서부터 저장됩니다. 원자료는 `data/reports.csv`, `data/financial_statements.csv`, 분석 결과는 `data/metrics.csv`, 대시보드는 `docs/index.html`에 저장됩니다. 지표에는 매출액 영업이익률·순이익률, 부채비율, 유동비율, 자기자본비율, ROA, ROE가 포함됩니다. 계정명 차이 또는 미제공 보고서로 일부 값이 비어 있을 수 있습니다. 대시보드 값은 공시 계정 매칭 결과이며 투자 조언이 아닙니다.
