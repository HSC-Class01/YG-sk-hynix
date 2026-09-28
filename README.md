# SK hynix DART Financial Dashboard

🔗 [대시보드 바로가기](https://hsc-class01.github.io/YG-sk-hynixl/)

2010년부터 OpenDART의 사업·반기·분기보고서 재무제표를 수집하고 CSV/JSON 및 정적 대시보드를 생성합니다.

## 설정
1. 파일을 대상 저장소 루트에 업로드합니다(.github/workflows 경로 유지).
2. GitHub 저장소 Settings → Secrets and variables → Actions에서 `DART_API_KEY` secret을 등록합니다.
3. Settings → Pages → Build and deployment → Source를 GitHub Actions로 설정합니다.
4. Actions 탭에서 `DART monthly update`를 수동 실행합니다. 이후 매월 1일 02:15 UTC(한국시간 11:15)에 실행됩니다.

기본 종목코드는 SK hynix 000660입니다. 데이터는 `data/`에 저장되고 대시보드는 `docs/index.html`입니다. 재무비율은 매출액 영업이익률, 순이익률, 부채비율, 유동비율, 자기자본비율, ROA, ROE를 산출합니다. 일부 계정은 공시 명칭 차이로 누락될 수 있습니다.
