# 📖 사용 가이드

## 🎯 앱 선택 가이드

프로젝트에는 **2가지 Streamlit 앱**이 있습니다:

### 1. **app.py** ⭐ 권장 (비용 효율적)

**특징:**
- 💰 **비용 최소화**: 버튼 클릭 시에만 Claude API 호출
- 🔍 **스크리닝 우선**: 무료로 이상 징후 종목 탐지
- 🎯 **선택적 분석**: 관심 종목만 심층 분석

**사용 시나리오:**
- 매일 시장 모니터링
- 비용 관리가 중요한 경우
- 많은 종목 중 일부만 분석

**실행:**
```bash
streamlit run app.py
# 또는
run_app.bat
```

---

### 2. **streamlit_app.py** (풀 기능)

**특징:**
- 🎨 **풍부한 UI**: 모든 기능 통합
- 📊 **Market Watch**: 실시간 추천 종목
- 🔄 **히스토리**: 분석 이력 관리
- 📈 **상세 차트**: 다양한 시각화

**사용 시나리오:**
- 종목 심층 연구
- 여러 분석 비교
- 풀 기능이 필요한 경우

**실행:**
```bash
streamlit run streamlit_app.py
# 또는
run_dashboard.bat
```

---

## 🚀 빠른 시작

### app.py 사용 (권장)

```bash
# 1. 앱 실행
streamlit run app.py

# 2. 웹 브라우저에서 자동으로 열림 (http://localhost:8501)

# 3. "🔄 스크리닝 실행" 클릭
#    → 20개 종목 분석 (약 30초, 무료)

# 4. 이상 징후 종목 확인

# 5. 관심 종목의 "🤖 클로드 비판 분석 시작" 클릭
#    → Claude API 호출 (유료)

# 6. AI 보고서 확인
```

---

## 💰 비용 구조

### 무료 (API 호출 없음)
- ✅ 스크리닝 실행
- ✅ 종목 리스트 확인
- ✅ 기본 지표 확인 (가격, 거래량, RSI)

### 유료 (Claude API 호출)
- 💳 비판적 분석 보고서 생성
- 💳 버튼 클릭 시에만 호출
- 💳 종목당 1회 호출

**예상 비용:**
- 종목 1개 분석: ~$0.10-0.20
- 10개 분석: ~$1-2

---

## 📊 워크플로우 비교

### A. 비용 효율형 (app.py)

```
1. 스크리닝 (무료) → 2. 이상 종목 확인 → 3. 선택 분석 (유료)
```

**장점:**
- 💰 최소 비용
- 🎯 필요한 종목만 분석

**단점:**
- 제한적 UI
- 히스토리 없음

---

### B. 풀 기능형 (streamlit_app.py)

```
1. Market Watch → 2. 종목 검색 → 3. 즉시 분석 → 4. 히스토리 저장
```

**장점:**
- 🎨 풍부한 UI
- 📜 히스토리 관리
- 🔄 재분석 간편

**단점:**
- 💸 API 호출 빈번
- 다소 복잡

---

## 🎯 추천 사용 패턴

### 일일 모니터링
```bash
# 매일 장 마감 후
python screener.py          # CLI로 빠른 스크리닝
# 또는
streamlit run app.py        # 웹으로 확인
```

### 심층 분석
```bash
# 관심 종목 발견 시
streamlit run app.py        # 비판적 분석 실행
```

### 연구/학습
```bash
streamlit run streamlit_app.py  # 모든 기능 활용
```

---

## 🛠️ 명령줄 도구

### 1. 스크리너 (CLI)
```bash
python screener.py
# → watchlist.json 생성
```

### 2. 단일 종목 분석 (CLI)
```bash
python main.py --ticker 005930.KS
# → reports/삼성전자_날짜.md 생성
```

### 3. 데이터 수집만
```bash
python data_collector.py
# → data/*.json 생성
```

---

## 📁 출력 파일

| 파일 | 설명 | 생성 시점 |
|------|------|-----------|
| `watchlist.json` | 스크리닝 결과 | screener.py 실행 |
| `data/*.json` | 원본 데이터 | 분석 실행 시 |
| `reports/*.md` | 보고서 | 분석 완료 시 |
| `analysis/*.json` | 분석 결과 | 분석 완료 시 |
| `analysis_history.json` | 히스토리 | streamlit_app.py 사용 시 |

---

## 🔧 문제 해결

### 포트 충돌
```bash
streamlit run app.py --server.port 8502
```

### API 키 오류
```
.env 파일 확인:
- DART_API_KEY
- NEWS_API_KEY
- ANTHROPIC_API_KEY
```

### 스크리닝 결과 없음
- 정상적인 상황일 수 있음
- 조건이 엄격 (거래량 2배, RSI 극단값)
- 다른 시간대에 재실행

---

## 💡 프로 팁

1. **비용 절감**: app.py로 스크리닝 → 2-3개만 분석
2. **정기 실행**: 매일 같은 시간에 스크리닝
3. **watchlist 보관**: 날짜별로 비교 분석
4. **CLI 활용**: 자동화 스크립트에 screener.py 사용

---

## 🎓 학습 경로

### 초급
1. `python screener.py` 실행
2. watchlist.json 확인
3. `streamlit run app.py` 실행
4. 종목 1개 분석

### 중급
1. 다양한 종목 비교
2. 보고서 분석
3. 신뢰도 점수 이해

### 고급
1. CLI 자동화
2. 커스텀 스크리닝 조건
3. 데이터 분석 및 백테스팅

---

**Happy Trading! 📈**
