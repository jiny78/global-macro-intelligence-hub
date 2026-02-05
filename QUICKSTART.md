# 🚀 빠른 시작 가이드

## 웹 대시보드 실행 (가장 쉬운 방법)

### Windows

1. **run_dashboard.bat** 파일을 더블클릭

2. 자동으로 웹 브라우저가 열립니다 (`http://localhost:8501`)

3. 종목명 입력 후 "분석 시작" 버튼 클릭

---

## 명령줄 실행

### 1. 가상환경 활성화

```bash
cd "C:\Users\User\Projects\Global Macro Intelligence Hub"
.\venv\Scripts\activate
```

### 2. 웹 대시보드 실행

```bash
streamlit run streamlit_app.py
```

### 3. 명령줄 실행 (CLI)

```bash
python main.py --ticker 005930.KS
```

---

## 사용 예시

### 웹 대시보드

1. 검색창에 "삼성전자" 또는 "005930.KS" 입력
2. "🚀 분석 시작" 버튼 클릭
3. 약 1-2분 대기
4. 주가 차트, 뉴스, 분석 보고서 확인

### 명령줄

```bash
# 삼성전자 분석
python main.py --ticker 005930.KS

# 카카오 분석
python main.py --ticker 035720.KS

# SK하이닉스 분석
python main.py -t 000660.KS
```

---

## 지원 종목

| 종목명 | 티커 |
|--------|------|
| 삼성전자 | 005930.KS |
| 카카오 | 035720.KS |
| SK하이닉스 | 000660.KS |
| LG화학 | 051910.KS |
| 현대차 | 005380.KS |
| 삼성SDI | 006400.KS |
| NAVER | 035420.KS |

---

## 출력 결과

- **웹 대시보드**: 브라우저에서 바로 확인
- **보고서**: `reports/[종목명]_[날짜].md`
- **원본 데이터**: `data/data_[티커]_[타임스탬프].json`
- **분석 결과**: `analysis/analysis_[티커]_[타임스탬프].json`

---

## 문제 해결

### 포트가 이미 사용중인 경우

```bash
streamlit run streamlit_app.py --server.port 8502
```

### API 키 오류

`.env` 파일에서 다음 키들이 설정되어 있는지 확인:
- DART_API_KEY
- NEWS_API_KEY
- ANTHROPIC_API_KEY

---

## 다음 단계

- 여러 종목을 비교 분석해보세요
- 히스토리 기능으로 과거 분석 결과를 확인하세요
- 보고서를 저장하여 투자 전략 수립에 활용하세요

**⚠️ 주의:** 본 시스템은 정보 제공 목적이며, 투자 권유가 아닙니다.
