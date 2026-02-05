# 📧 이메일 설정 가이드

## PDF 리포트 자동 전송 기능 설정

---

## 🎯 Gmail 설정 (권장)

### 1단계: 2단계 인증 활성화

1. https://myaccount.google.com/security 접속
2. **"2단계 인증"** 찾기
3. 화면 지시에 따라 활성화

### 2단계: 앱 비밀번호 생성

1. https://myaccount.google.com/apppasswords 접속
2. **"앱 선택"** → **"기타(맞춤 이름)"** 선택
3. 이름 입력: `Global Macro Hub`
4. **"생성"** 클릭
5. **16자리 비밀번호** 표시됨 (예: `abcd efgh ijkl mnop`)
6. 이 비밀번호를 복사 (공백 제거: `abcdefghijklmnop`)

### 3단계: .env 파일 설정

`.env` 파일을 열어서 다음과 같이 설정:

```env
# 이메일 설정
SENDER_EMAIL=your-gmail@gmail.com
APP_PASSWORD=abcdefghijklmnop
RECIPIENT_EMAIL=recipient@gmail.com
```

**예시:**
```env
SENDER_EMAIL=hong.gildong@gmail.com
APP_PASSWORD=abcdefghijklmnop
RECIPIENT_EMAIL=hong.gildong@gmail.com
```

---

## 📝 설정 항목 설명

| 항목 | 설명 | 예시 |
|------|------|------|
| **SENDER_EMAIL** | 발신자 이메일 (Gmail 계정) | `myemail@gmail.com` |
| **APP_PASSWORD** | 앱 비밀번호 (16자리, 공백 제거) | `abcdefghijklmnop` |
| **RECIPIENT_EMAIL** | 수신자 이메일 (PDF 받을 주소) | `myemail@gmail.com` |

**💡 팁:** 발신자와 수신자를 같은 주소로 설정하면 자기 자신에게 전송됩니다.

---

## ✅ 설정 확인

### 테스트 방법

1. 앱 실행
   ```bash
   streamlit run app.py
   ```

2. 종목 분석 실행

3. **"📧 PDF 리포트 메일로 받기"** 버튼 클릭

4. 이메일 확인

### 성공 메시지
```
✅ PDF 리포트가 이메일로 전송되었습니다!
```

### 실패 시
```
❌ 이메일 전송 실패. .env 파일의 이메일 설정을 확인하세요.
```

---

## 🔧 문제 해결

### 1. "앱 비밀번호 메뉴가 없습니다"

**원인:** 2단계 인증이 활성화되지 않음

**해결:**
1. https://myaccount.google.com/security
2. 2단계 인증 활성화
3. 다시 앱 비밀번호 메뉴 접속

---

### 2. "인증 실패" 오류

**원인:** 앱 비밀번호가 잘못됨

**해결:**
1. 앱 비밀번호 재생성
2. **공백 제거** 확인
3. .env 파일에 정확히 입력

---

### 3. "SMTP 연결 실패"

**원인:** 방화벽 또는 네트워크 문제

**해결:**
1. 방화벽 설정 확인
2. 다른 네트워크 시도
3. VPN 비활성화

---

### 4. "수신자 주소 오류"

**원인:** 이메일 주소 형식 오류

**해결:**
- 올바른 형식: `example@gmail.com`
- 잘못된 형식: `example@gmailcom`, `example gmail.com`

---

## 📧 수신 이메일 예시

### 제목
```
[Global Macro] report_삼성전자_20260205_143000.pdf
```

### 본문
```
안녕하세요,

Global Macro Intelligence Hub에서 생성한 분석 리포트를 전송합니다.

리포트 파일: report_삼성전자_20260205_143000.pdf
생성 시간: 2026-02-05 14:30:00

첨부된 PDF 파일을 확인하시기 바랍니다.

---
이 이메일은 자동으로 발송되었습니다.
Global Macro Intelligence Hub
Powered by Claude Sonnet 4
```

### 첨부 파일
```
📎 report_삼성전자_20260205_143000.pdf (약 500KB)
```

---

## 🎨 PDF 리포트 구성

### 1. 헤더
- **Global Macro Intelligence Report**
- 전문적인 그라디언트 디자인

### 2. Overview
- 회사명, 티커
- 리포트 생성 날짜
- 분석 모델 정보

### 3. 주가 요약
- 기간, 시가, 종가
- 변동률, 최고가, 최저가

### 4. 주가 차트
- 7일 추이 그래프 이미지

### 5. AI 비판적 분석
- 데이터-내러티브 괴리
- 공시 진위 판별
- 강세론 vs 약세론
- 신뢰도 점수

### 6. 면책 조항
- 법적 고지사항

---

## 🔐 보안 주의사항

### ⚠️ 중요!

1. **앱 비밀번호는 절대 공유하지 마세요**
2. **.env 파일을 Git에 커밋하지 마세요**
3. **사용하지 않는 앱 비밀번호는 삭제하세요**

### 앱 비밀번호 삭제

1. https://myaccount.google.com/apppasswords
2. 사용하지 않는 비밀번호 옆 **"삭제"** 클릭

---

## 💡 고급 활용

### 다른 사람에게 전송

`.env` 파일의 `RECIPIENT_EMAIL`을 변경:

```env
RECIPIENT_EMAIL=colleague@company.com
```

### 여러 명에게 전송

현재는 1명만 지원합니다. 여러 명에게 보내려면:

1. 같은 리포트를 여러 번 전송하거나
2. Gmail에서 자동 전달 규칙 설정

---

## 📞 추가 도움

### Gmail 고객센터
- https://support.google.com/mail

### 2단계 인증 문제
- https://support.google.com/accounts/answer/185839

### 앱 비밀번호 문제
- https://support.google.com/accounts/answer/185833

---

## ✅ 설정 완료 체크리스트

- [ ] 2단계 인증 활성화
- [ ] 앱 비밀번호 생성
- [ ] .env 파일 설정
- [ ] 테스트 전송 성공
- [ ] 이메일 수신 확인

---

**이제 PDF 리포트를 이메일로 받을 준비가 완료되었습니다!** 📧✨
