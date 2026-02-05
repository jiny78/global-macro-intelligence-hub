"""
Global Macro Intelligence Hub - Critical Analyzer
수집된 데이터를 비판적 추론 프레임워크로 분석하는 모듈
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv
from anthropic import Anthropic

# .env 파일 로드
load_dotenv()


class CriticalAnalyzer:
    """비판적 추론 프레임워크를 적용한 데이터 분석 클래스"""

    def __init__(self, anthropic_api_key: str = None):
        """
        Args:
            anthropic_api_key: Claude API 키 (환경변수 ANTHROPIC_API_KEY로도 설정 가능)
        """
        self.api_key = anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")

        self.client = Anthropic(api_key=self.api_key)

    def load_data(self, json_file_path) -> Dict[str, Any]:
        """
        JSON 파일 또는 딕셔너리에서 데이터 로드

        Args:
            json_file_path: JSON 파일 경로 또는 데이터 딕셔너리

        Returns:
            로드된 데이터 딕셔너리
        """
        # 이미 딕셔너리인 경우 그대로 반환
        if isinstance(json_file_path, dict):
            print("[INFO] Using provided data dictionary")
            return json_file_path

        # 파일 경로인 경우 로드
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"[OK] Data loaded: {json_file_path}")
            return data
        except Exception as e:
            print(f"[ERROR] Data load failed: {str(e)}")
            raise

    def create_critical_prompt(self, data: Dict[str, Any]) -> str:
        """
        비판적 추론 프레임워크를 적용한 프롬프트 생성

        Args:
            data: 분석할 데이터

        Returns:
            Claude API용 프롬프트
        """
        # 데이터 요약 추출
        ticker = data.get('ticker', 'N/A')
        stock_data = data.get('stock_data', {})
        news = data.get('news', [])
        disclosures = data.get('disclosures', [])

        # 주가 데이터 포맷팅
        price_data_str = self._format_price_data(stock_data)

        # 뉴스 데이터 포맷팅
        news_str = self._format_news_data(news)

        # 공시 데이터 포맷팅
        disclosure_str = self._format_disclosure_data(disclosures)

        # 비판적 추론 프롬프트 생성
        prompt = f"""
당신은 글로벌 매크로 투자 전문가이자 비판적 데이터 분석가입니다.
다음 데이터를 **비판적 추론 프레임워크**에 따라 철저히 분석하세요.

## 필수 분석 규칙:

### 1. 데이터-내러티브 괴리 분석 (Data-Narrative Discrepancy)
- 뉴스에서 "호재", "긍정적" 등의 표현이 있는데 실제 주가나 거래량이 하락했다면, 그 이유를 **추측이 아닌 데이터상의 모순**으로 지적할 것
- 뉴스에서 "악재", "부정적" 표현이 있는데 주가가 상승했다면 동일하게 분석할 것
- 반드시 구체적인 수치와 함께 모순을 제시할 것

### 2. 공시 진위 판별 (Disclosure Credibility Check)
- 공시된 내용(실적 전망, 투자 계획 등)이 과거 실적 대비 **실현 가능한 수준**인지 검증
- 과거 공시와 실제 실적의 괴리가 있었는지 확인
- 너무 낙관적이거나 비현실적인 목표는 비판적으로 지적

### 3. 확증 편향 제거 (Confirmation Bias Elimination)
- **강세론(Bullish Case)과 약세론(Bearish Case)의 근거를 반드시 5:5 비율로 균형있게 제시**
- 한쪽으로 치우친 분석은 절대 불가
- 각 논거는 데이터에 기반해야 함

---

## 분석 대상 데이터:

### 종목 정보:
- 티커: {ticker}
- 회사명: {stock_data.get('company_name', 'N/A')}

### 주가 데이터 (최근 7일):
{price_data_str}

### 뉴스 헤드라인:
{news_str}

### 공시 정보:
{disclosure_str}

---

## 출력 형식 (반드시 준수):

### 1. 데이터-내러티브 괴리 분석
**발견된 모순:**
- [뉴스 제목 또는 내용] vs [실제 주가/거래량 데이터]
- 구체적 수치 제시
- 가능한 해석 (추측 X, 데이터 기반)

### 2. 공시 진위 판별
**공시 내용 검증:**
- 공시명: [공시명]
- 주요 내용: [요약]
- 실현 가능성 평가: [높음/중간/낮음]
- 근거: [과거 데이터와 비교]

### 3. 강세론 vs 약세론 (5:5 균형)

**강세론 근거 (Bullish Case):**
1. [데이터 기반 근거 1]
2. [데이터 기반 근거 2]
3. [데이터 기반 근거 3]

**약세론 근거 (Bearish Case):**
1. [데이터 기반 근거 1]
2. [데이터 기반 근거 2]
3. [데이터 기반 근거 3]

### 4. 종합 판단
- 확증 편향을 배제한 객관적 종합 의견
- 투자 시 주의사항
- 추가 확인이 필요한 사항

---

**중요:** 추측이나 일반론은 배제하고, 오직 제공된 데이터에 기반한 분석만 수행하세요.
데이터가 불충분한 경우 "데이터 부족"이라고 명시하세요.
"""

        return prompt

    def _format_price_data(self, stock_data: Dict[str, Any]) -> str:
        """주가 데이터 포맷팅"""
        if 'error' in stock_data:
            return "[ERROR] 주가 데이터 없음"

        data_list = stock_data.get('data', [])
        if not data_list:
            return "[ERROR] 주가 데이터 없음"

        # 테이블 형태로 포맷팅
        lines = ["날짜       | 시가    | 고가    | 저가    | 종가    | 거래량"]
        lines.append("-" * 70)

        for day in data_list:
            line = f"{day['date']} | {day['open']:7.0f} | {day['high']:7.0f} | {day['low']:7.0f} | {day['close']:7.0f} | {day['volume']:,}"
            lines.append(line)

        # 주가 변동률 계산
        if len(data_list) >= 2:
            first_close = data_list[0]['close']
            last_close = data_list[-1]['close']
            change_pct = ((last_close - first_close) / first_close) * 100
            lines.append(f"\n[DATA] 7일 변동률: {change_pct:+.2f}%")

        return "\n".join(lines)

    def _format_news_data(self, news: List[Dict[str, str]]) -> str:
        """뉴스 데이터 포맷팅"""
        if not news or (len(news) == 1 and 'error' in news[0]):
            return "[ERROR] 뉴스 데이터 없음"

        lines = []
        for i, article in enumerate(news, 1):
            if 'error' in article:
                continue

            lines.append(f"\n[뉴스 {i}]")
            lines.append(f"제목: {article.get('title', 'N/A')}")
            lines.append(f"설명: {article.get('description', 'N/A')}")
            lines.append(f"출처: {article.get('source', 'N/A')}")
            lines.append(f"날짜: {article.get('published', 'N/A')}")

        return "\n".join(lines) if lines else "[ERROR] 유효한 뉴스 없음"

    def _format_disclosure_data(self, disclosures: List[Dict[str, str]]) -> str:
        """공시 데이터 포맷팅"""
        if not disclosures or (len(disclosures) == 1 and 'error' in disclosures[0]):
            return "[ERROR] 공시 데이터 없음"

        lines = []
        for i, disc in enumerate(disclosures, 1):
            if 'error' in disc:
                continue

            lines.append(f"\n[공시 {i}]")
            lines.append(f"회사: {disc.get('company', 'N/A')}")
            lines.append(f"공시명: {disc.get('report_name', 'N/A')}")
            lines.append(f"제출일: {disc.get('submitted_date', 'N/A')}")
            lines.append(f"URL: {disc.get('url', 'N/A')}")

        return "\n".join(lines) if lines else "[WARN] No valid disclosures"

    def analyze(self, json_file_path) -> Dict[str, Any]:
        """
        데이터 분석 실행

        Args:
            json_file_path: 분석할 JSON 파일 경로 또는 데이터 딕셔너리

        Returns:
            분석 결과 딕셔너리
        """
        print(f"\n{'='*70}")
        print(f"[START] Critical Analysis")
        print(f"{'='*70}\n")

        # 1. 데이터 로드
        data = self.load_data(json_file_path)

        # 2. 프롬프트 생성
        print("[INFO] Creating critical reasoning prompt...")
        prompt = self.create_critical_prompt(data)

        # 3. Claude API 호출
        print("[INFO] Calling Claude API...")
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",  # 최신 Sonnet 모델
                max_tokens=4096,
                temperature=0.3,  # 낮은 temperature로 객관적 분석 유도
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            analysis_text = message.content[0].text
            print("[OK] Analysis complete!\n")

        except Exception as e:
            print(f"[ERROR] Claude API call failed: {str(e)}")
            analysis_text = f"분석 실패: {str(e)}"

        # 4. 결과 구성
        result = {
            "analyzed_at": datetime.now().isoformat(),
            "ticker": data.get('ticker', 'N/A'),
            "source_file": json_file_path,
            "analysis": analysis_text,
            "metadata": {
                "model": "claude-sonnet-4-20250514",
                "framework": "Critical Reasoning Framework",
                "rules": [
                    "Data-Narrative Discrepancy Analysis",
                    "Disclosure Credibility Check",
                    "Confirmation Bias Elimination (5:5 Balance)"
                ]
            }
        }

        return result

    def save_analysis(self, result: Dict[str, Any], output_format: str = "both") -> str:
        """
        분석 결과 저장

        Args:
            result: 분석 결과
            output_format: 출력 형식 ("json", "markdown", "both")

        Returns:
            저장된 파일 경로
        """
        ticker = result['ticker'].replace('.', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 분석 결과 디렉토리 생성
        analysis_dir = os.path.join(
            os.path.dirname(__file__),
            'analysis'
        )
        os.makedirs(analysis_dir, exist_ok=True)

        saved_files = []

        # JSON 저장
        if output_format in ["json", "both"]:
            json_path = os.path.join(
                analysis_dir,
                f"analysis_{ticker}_{timestamp}.json"
            )
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            saved_files.append(json_path)
            print(f"[SAVED] JSON: {json_path}")

        # Markdown 저장
        if output_format in ["markdown", "both"]:
            md_path = os.path.join(
                analysis_dir,
                f"analysis_{ticker}_{timestamp}.md"
            )
            markdown_content = self._generate_markdown(result)
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            saved_files.append(md_path)
            print(f"[SAVED] Markdown: {md_path}")

        return saved_files[0] if saved_files else None

    def _generate_markdown(self, result: Dict[str, Any]) -> str:
        """분석 결과를 Markdown 형식으로 변환"""
        md = f"""# 비판적 분석 보고서

## 기본 정보
- **종목**: {result['ticker']}
- **분석 일시**: {result['analyzed_at']}
- **분석 모델**: {result['metadata']['model']}
- **분석 프레임워크**: {result['metadata']['framework']}

## 적용된 분석 규칙
"""
        for rule in result['metadata']['rules']:
            md += f"- {rule}\n"

        md += f"""
---

## 분석 결과

{result['analysis']}

---

*이 보고서는 Claude API의 비판적 추론 프레임워크를 통해 생성되었습니다.*
*투자 결정 시 반드시 추가적인 실사(Due Diligence)를 수행하시기 바랍니다.*
"""
        return md


def main():
    """메인 실행 함수"""
    import sys
    import glob

    # API 키 확인
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("[ERROR] ANTHROPIC_API_KEY not set in .env file")
        print("   .env 파일에 다음을 추가하세요:")
        print("   ANTHROPIC_API_KEY=your-api-key-here")
        return

    # 분석기 생성
    analyzer = CriticalAnalyzer(anthropic_api_key=api_key)

    # data 폴더에서 가장 최근 JSON 파일 찾기
    data_dir = os.path.join(os.path.dirname(__file__), 'data')

    if not os.path.exists(data_dir):
        print(f"[ERROR] data folder not found: {data_dir}")
        print("   먼저 data_collector.py를 실행하여 데이터를 수집하세요.")
        return

    json_files = glob.glob(os.path.join(data_dir, "*.json"))

    if not json_files:
        print(f"[ERROR] No JSON files in data folder")
        print("   먼저 data_collector.py를 실행하여 데이터를 수집하세요.")
        return

    # 가장 최근 파일 선택
    latest_file = max(json_files, key=os.path.getmtime)
    print(f"[FILE] 분석 대상 파일: {latest_file}\n")

    # 분석 실행
    result = analyzer.analyze(latest_file)

    # 결과 저장
    print(f"\n{'='*70}")
    print("[SAVE] 분석 결과 저장 중...")
    print(f"{'='*70}\n")
    saved_path = analyzer.save_analysis(result, output_format="both")

    print(f"\n{'='*70}")
    print("[OK] 모든 분석 완료!")
    print(f"{'='*70}\n")

    # 분석 결과 일부 출력
    print("\n[DATA] 분석 결과 미리보기:\n")
    print(result['analysis'][:500] + "...\n")
    print(f"전체 결과는 analysis 폴더를 확인하세요.")


if __name__ == "__main__":
    main()
