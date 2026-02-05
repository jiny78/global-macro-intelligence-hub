# Global Macro Intelligence Hub - 시스템 현황

**마지막 업데이트**: 2026-02-05
**버전**: 2.0 (전문가급 PDF 리포팅 시스템)

---

## 시스템 완성도

### ✅ 완료된 기능

#### 1. 데이터 수집 모듈 (`data_collector.py`)
- [x] yfinance를 통한 주가 데이터 수집 (7일)
- [x] News API를 통한 뉴스 수집
- [x] OpenDART API를 통한 공시 수집
- [x] JSON 형식으로 데이터 저장

#### 2. AI 비판적 분석 (`critical_analyzer.py`)
- [x] Claude Sonnet 4 API 연동
- [x] Critical Reasoning Framework 구현
- [x] 데이터-내러티브 괴리 분석
- [x] 공시 진위 판별
- [x] 강세론 vs 약세론 (5:5 균형)
- [x] 신뢰도 점수 (0-100)

#### 3. 스크리닝 모듈 (`screener.py`)
- [x] LLM 미사용 (비용 절감)
- [x] 기술적 지표 계산 (RSI, MA)
- [x] 거래량 이상 징후 탐지
- [x] watchlist.json 출력

#### 4. 마켓 워치 (`market_watch.py`)
- [x] KOSPI 주요 종목 모니터링
- [x] 골든크로스/데드크로스 감지
- [x] 추천 점수 계산

#### 5. Streamlit 웹 앱 (`app.py`)
- [x] 실시간 스크리닝 결과 표시
- [x] 온디맨드 AI 분석 (버튼 클릭 시)
- [x] 인터랙티브 차트 (Plotly)
- [x] 분석 히스토리 관리
- [x] **전문가급 PDF 리포트 생성 버튼**

#### 6. **전문가급 PDF 리포팅 시스템** (`report_manager.py`) ⭐ NEW
- [x] 한글 폰트 자동 탐지
- [x] 4-Section 전문가급 레이아웃
  - [x] Section 1: 데이터 기반 팩트 체크
  - [x] Section 2: Claude 비판적 분석
  - [x] Section 3: 기술적 지표 요약
  - [x] **Section 4: AI 자기 비판 (필수)**
- [x] 차트 이미지 삽입
- [x] AI Risk Score 계산 (0-100)
- [x] 3-line 핵심 요약 생성
- [x] HTML 지능형 메일
- [x] 리스크 레벨 배지 (Low/Medium/High)
- [x] 14단계 실시간 진행 상황 표시
- [x] SMTP를 통한 Gmail 전송

#### 7. CLI 인터페이스 (`main.py`)
- [x] argparse 기반 커맨드라인
- [x] --ticker 파라미터
- [x] Markdown 리포트 생성

#### 8. 자동 실행 스크립트
- [x] `run_analyzer.bat` (Streamlit 앱 실행)
- [x] `run_app.bat` (대체 실행 방법)
- [x] 가상 환경 자동 생성
- [x] 패키지 자동 설치

#### 9. 문서화
- [x] `README.md` - 프로젝트 개요
- [x] `SETUP.md` - 설치 가이드
- [x] `USAGE.md` - 사용법
- [x] `QUICKSTART.md` - 빠른 시작
- [x] `EMAIL_SETUP.md` - 이메일 설정
- [x] **`PDF_REPORT_GUIDE.md` - PDF 리포팅 가이드** ⭐ NEW

---

## 핵심 혁신 - "혹독한 완성도 기준" 충족

### 1. PDF 엔진
✅ **한글 폰트 자동 탐지**
- 나눔고딕, 맑은 고딕, 나눔바른고딕, 굴림 자동 탐색
- 폰트 없어도 영문으로 정상 작동

✅ **4-Section 전문가급 레이아웃**
- Section 1: 데이터 팩트 체크 (객관적 사실)
- Section 2: Claude 분석 (AI 의견)
- Section 3: 기술적 지표 (수치 요약)
- **Section 4: AI 자기 비판** (AI 한계 명시) ⚠️

✅ **차트 이미지 삽입**
- Plotly → Kaleido → PNG → PDF
- 주가 추이 7일 차트

### 2. 지능형 메일러
✅ **HTML 포맷**
- 전문적인 그라디언트 헤더
- 색상별 섹션 구분
- 반응형 디자인

✅ **3-line 핵심 요약**
- 공시 분석 1줄
- 기술적 지표 1줄
- AI 자기 비판 1줄

✅ **AI Risk Score 강조**
- 0-100점 척도
- 리스크 레벨 배지
- 키워드 기반 자동 계산

### 3. 가혹한 로직 검증
✅ **AI 자기 비판 섹션 (필수)**

모든 리포트에 다음 내용 포함:
```
1. 데이터 불완전성
   - 7일 데이터만 사용
   - 공시 전체 내용 미확인

2. 시점 차이 문제
   - 데이터 수집 시점 ≠ 현재 시점

3. AI 할루시네이션 가능성
   - 존재하지 않는 패턴 인식 가능

4. 맥락 부족
   - 산업 전체 맥락 미고려

5. 감정과 편향
   - 학습 데이터의 편향 반영 가능
```

### 4. UI/UX 통합
✅ **실시간 진행 상황 표시**

14단계 진행 바:
1. PDF 문서 초기화
2. 표지 생성
3. 섹션 1 작성
4. 차트 이미지 생성
5. 섹션 2 작성
6. 섹션 3 작성
7. **섹션 4 작성 (AI 자기 비판)**
8. 면책 조항 추가
9. PDF 저장
10. 이메일 준비
11. PDF 첨부
12. HTML 본문 생성
13. SMTP 연결
14. 이메일 전송 완료

✅ **사용자 친화적 버튼**
- "🎯 전문가급 PDF 리포트 생성 및 전송"
- 명확한 액션 유도

---

## 시스템 아키텍처

```
┌─────────────────────────────────────────────────────┐
│                   User Interface                     │
│              (Streamlit Web App)                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  [스크리닝 결과 표시] → [AI 분석 버튼]               │
│                         ↓                            │
│                   [분석 결과 표시]                    │
│                         ↓                            │
│           [🎯 전문가급 PDF 리포트 생성 버튼]          │
│                         ↓                            │
│                 [14단계 진행 바]                      │
│                         ↓                            │
│                  [완료 메시지]                        │
│                                                      │
├─────────────────────────────────────────────────────┤
│                  Backend Modules                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │   Screener   │  │Data Collector│                 │
│  │  (LLM-Free)  │  │ (yf/News/    │                 │
│  │              │  │  DART API)   │                 │
│  └──────────────┘  └──────────────┘                 │
│         │                  │                         │
│         └─────────┬────────┘                         │
│                   ↓                                  │
│          ┌──────────────────┐                        │
│          │Critical Analyzer │                        │
│          │  (Claude API)    │                        │
│          └──────────────────┘                        │
│                   │                                  │
│                   ↓                                  │
│    ┌─────────────────────────────┐                  │
│    │  ExpertReportManager        │                  │
│    │  (PDF + Email)              │                  │
│    ├─────────────────────────────┤                  │
│    │ • ProfessionalPDFReport     │                  │
│    │ • AI Self-Criticism Gen     │                  │
│    │ • Risk Score Calculator     │                  │
│    │ • HTML Email Creator        │                  │
│    │ • SMTP Mailer               │                  │
│    └─────────────────────────────┘                  │
│                   │                                  │
│                   ↓                                  │
│         ┌──────────────────┐                         │
│         │  PDF + Email     │                         │
│         │  Delivery        │                         │
│         └──────────────────┘                         │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 파일 구조

```
C:\Users\User\Projects\Global Macro Intelligence Hub\
│
├── app.py                          # Streamlit 웹 앱 (메인)
├── main.py                         # CLI 인터페이스
├── data_collector.py               # 데이터 수집
├── critical_analyzer.py            # AI 비판적 분석
├── screener.py                     # 스크리닝 (LLM-Free)
├── market_watch.py                 # 마켓 워치
├── report_manager.py               # ⭐ 전문가급 PDF 리포팅
│
├── .env                            # API 키 및 설정
├── .env.example                    # 설정 예시
├── requirements.txt                # 패키지 의존성
│
├── run_analyzer.bat                # Streamlit 실행 스크립트
├── run_app.bat                     # 대체 실행 스크립트
│
├── README.md                       # 프로젝트 개요
├── SETUP.md                        # 설치 가이드
├── USAGE.md                        # 사용법
├── QUICKSTART.md                   # 빠른 시작
├── EMAIL_SETUP.md                  # 이메일 설정
├── PDF_REPORT_GUIDE.md             # ⭐ PDF 리포팅 가이드
├── SYSTEM_STATUS.md                # 이 파일
│
├── data/                           # 수집된 데이터
│   ├── {ticker}_data.json
│   └── watchlist.json
│
├── reports/                        # 생성된 리포트
│   ├── report_{종목}_{날짜}.pdf
│   └── {ticker}_{날짜}.md
│
└── venv/                           # Python 가상 환경
```

---

## 환경 설정 확인

### .env 파일 상태
```env
✅ DART_API_KEY         (OpenDART 공시)
✅ NEWS_API_KEY         (News API 뉴스)
✅ ANTHROPIC_API_KEY    (Claude Sonnet 4)
✅ SENDER_EMAIL         (Gmail 발신)
✅ APP_PASSWORD         (Gmail 앱 비밀번호)
✅ RECIPIENT_EMAIL      (수신자)
```

### 설치된 패키지
```
✅ yfinance             # 주가 데이터
✅ newsapi-python       # 뉴스
✅ dart-fss             # 공시
✅ anthropic            # Claude API
✅ streamlit            # 웹 앱
✅ plotly               # 차트
✅ kaleido              # 차트 → 이미지
✅ fpdf2                # PDF 생성
✅ Pillow               # 이미지 처리
✅ pandas, numpy        # 데이터 분석
✅ python-dotenv        # 환경 변수
```

---

## 사용 가능 명령어

### 웹 앱 실행
```bash
# 방법 1: 배치 파일 (권장)
run_analyzer.bat

# 방법 2: 직접 실행
cd "C:\Users\User\Projects\Global Macro Intelligence Hub"
venv\Scripts\activate
streamlit run app.py
```

### CLI 실행
```bash
cd "C:\Users\User\Projects\Global Macro Intelligence Hub"
venv\Scripts\activate
python main.py --ticker 005930
```

---

## 테스트 시나리오

### 1. 기본 분석 테스트
1. `run_analyzer.bat` 실행
2. 스크리닝 결과 확인
3. "🤖 클로드 비판 분석 시작" 클릭
4. 분석 결과 확인

### 2. PDF 리포트 테스트
1. 분석 완료 후
2. "🎯 전문가급 PDF 리포트 생성 및 전송" 클릭
3. 14단계 진행 바 확인
4. 이메일 수신 확인
5. PDF 파일 열어서 4개 섹션 확인:
   - ✅ Section 1: Data-Based Fact Check
   - ✅ Section 2: Claude Critical Analysis
   - ✅ Section 3: Technical Indicators
   - ⚠️ **Section 4: AI SELF-CRITICISM**

### 3. 이메일 수신 테스트
1. 받은 메일함 확인
2. HTML 포맷 확인
3. 리스크 배지 확인
4. 3-line 요약 확인
5. PDF 첨부 파일 다운로드

---

## 성능 지표

### 비용 최적화
- ✅ 스크리닝: LLM 미사용 (무료)
- ✅ 분석: 온디맨드 (클릭 시에만 API 호출)
- ✅ PDF 생성: 로컬 처리 (무료)
- ✅ 이메일: SMTP (무료)

### 처리 시간 (예상)
- 스크리닝: ~5초 (20개 종목)
- AI 분석: ~10-15초 (Claude API)
- PDF 생성: ~2-3초
- 이메일 전송: ~1-2초
- **총 소요 시간: ~20초**

### API 호출 비용 (예상)
- Claude Sonnet 4: $3 per million input tokens
- 1회 분석당: ~5,000 tokens
- 1회 비용: ~$0.015 (약 20원)

---

## 향후 개선 가능 사항 (선택)

### 단기
- [ ] 여러 종목 배치 PDF 생성
- [ ] PDF 템플릿 커스터마이징 UI
- [ ] 이메일 여러 수신자 지원
- [ ] 리포트 스케줄링 (매일 자동 생성)

### 중기
- [ ] 영문 리포트 지원
- [ ] 모바일 최적화
- [ ] 데이터베이스 연동 (SQLite)
- [ ] 사용자 인증 시스템

### 장기
- [ ] 실시간 알림 시스템
- [ ] 포트폴리오 관리 기능
- [ ] 백테스팅 시뮬레이션
- [ ] API 서버 구축 (REST API)

---

## 시스템 상태 요약

| 항목 | 상태 | 비고 |
|------|------|------|
| 데이터 수집 | ✅ 완료 | yfinance, News API, DART |
| AI 분석 | ✅ 완료 | Claude Sonnet 4 |
| 스크리닝 | ✅ 완료 | LLM-Free |
| 웹 인터페이스 | ✅ 완료 | Streamlit |
| **PDF 리포팅** | ✅ **완료** | **4-Section, AI 자기 비판** |
| **HTML 메일** | ✅ **완료** | **리스크 스코어, 3-line 요약** |
| 문서화 | ✅ 완료 | 6개 가이드 문서 |
| 자동 실행 | ✅ 완료 | 배치 파일 |
| 테스트 | ⏳ 대기 | 사용자 테스트 필요 |

---

## 사용자 액션 아이템

### 즉시 실행 가능
1. ✅ `run_analyzer.bat` 더블클릭
2. ✅ 종목 분석 실행
3. ✅ PDF 리포트 생성 및 이메일 수신

### 선택적 커스터마이징
- `report_manager.py` 수정하여 PDF 레이아웃 조정
- `app.py` 수정하여 UI 변경
- `.env` 수정하여 수신자 변경

---

## 중요 알림

### ⚠️ AI 자기 비판 섹션 (Section 4)
**모든 리포트에 필수적으로 포함됩니다.**

이 섹션은:
- AI의 한계를 투명하게 공개
- 투자자 보호 목적
- 법적 리스크 경감
- 윤리적 AI 사용 원칙 준수

### 🔒 보안 주의사항
- `.env` 파일을 Git에 커밋하지 마세요
- Gmail 앱 비밀번호를 공유하지 마세요
- PDF 리포트에는 민감한 정보가 포함될 수 있습니다

---

**시스템 준비 완료!**

이제 `run_analyzer.bat`를 실행하여 전문가급 PDF 리포트를 생성하고 이메일로 받을 수 있습니다.

**차별화 포인트:**
1. ⚠️ AI가 스스로 한계를 인정 (Section 4)
2. 🎯 리스크 스코어 투명 공개
3. 📧 HTML 지능형 메일
4. 📊 14단계 실시간 진행 상황

---

*Global Macro Intelligence Hub v2.0*
*Powered by Claude Sonnet 4*
