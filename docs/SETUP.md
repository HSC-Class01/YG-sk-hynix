# GitHub 배포와 API 키 설정

## 1. OpenDART 인증키 등록

1. [OpenDART](https://opendart.fss.or.kr/)에서 인증키를 발급합니다.
2. GitHub 저장소 `Settings → Secrets and variables → Actions → New repository secret`으로 이동합니다.
3. Name은 `OPENDART_API_KEY`, Secret 값은 발급받은 인증키로 입력하고 저장합니다.
4. API 키를 README, `config.json`, `.env` 커밋에 넣지 마세요. `.env`는 `.gitignore`에 포함돼 있습니다.

## 2. Pages 설정 및 초기 배포

1. 저장소 `Settings → Pages → Build and deployment`에서 Source를 **GitHub Actions**로 선택합니다.
2. API 키 Secret 등록 후 `Actions → SK hynix DART dashboard → Run workflow`를 실행합니다.
3. 워크플로가 데이터를 수집하고 분석한 뒤 `docs`를 Pages에 배포합니다.
4. Actions 실행이 성공하면 대시보드는 [https://hsc-class01.github.io/YG-sk-hynix/](https://hsc-class01.github.io/YG-sk-hynix/)에서 확인할 수 있습니다.

GitHub Pages가 처음 활성화될 때 저장소 설정 단계가 필요합니다. Actions 탭의 워크플로 결과에서 오류가 나면 해당 실행의 로그에서 인증키·Pages 권한 상태를 확인합니다.

## 3. 매월 자동 업데이트

`.github/workflows/update_dart.yml`은 매월 1일 00:15 UTC(한국시간 09:15)에 실행합니다. OpenDART API 수집, 핵심 수치/비율 분석, CSV와 대시보드 데이터 생성, 갱신 파일 커밋, Pages 배포 순으로 처리합니다. GitHub Actions의 일정 실행은 부하가 높을 때 지연될 수 있습니다.

Agent 개발용 ZIP에는 숨김 파일을 넣지 않기 위해 워크플로 파일을 `github_workflows/update_dart.yml`에 둡니다. ZIP을 저장소에 적용할 때는 해당 파일을 저장소의 `.github/workflows/update_dart.yml`로 복사해야 GitHub가 인식합니다.

## 4. 로컬 실행

```powershell
python -m pip install -r requirements.txt
$env:OPENDART_API_KEY = "발급받은_OpenDART_인증키"
python -m src.collect
python -m src.analyze
python -m src.dashboard
python -m http.server 8000 --directory docs
```

브라우저에서 `http://localhost:8000`을 엽니다. 분석 파이프라인 확인은 `python -m unittest discover -s tests`로 실행합니다.

## 데이터 해석

분기보고서 Q3의 손익·현금흐름 누적액은 H1 누적액을 차감해 단독 3분기 값으로 계산합니다. FY와 H1은 각각 연간/반기 누적값입니다. 자산·부채·자본은 기간말 잔액이며 ROA·ROE는 평균잔액 대신 기간말 잔액을 이용한 단순 비율입니다. 계정명 차이가 있거나 공시 구조화 데이터가 없는 기간은 일부 수치가 비거나 `missing`으로 기록될 수 있습니다.
