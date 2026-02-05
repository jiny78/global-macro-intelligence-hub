"""
Global Macro Intelligence Hub - Main Entry Point
데이터 수집 → 비판적 분석 → 보고서 생성을 한 번에 수행하는 통합 스크립트
"""

import argparse
import os
import sys
from datetime import datetime
from typing import Dict, Any
import json

from data_collector import DataCollector
from critical_analyzer import CriticalAnalyzer
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class IntelligenceHub:
    """전체 워크플로우를 관리하는 메인 클래스"""

    def __init__(self):
        """초기화"""
        self.collector = DataCollector()
        self.analyzer = CriticalAnalyzer()

        # 보고서 디렉토리 생성
        self.reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)

    def get_company_name(self, ticker: str) -> str:
        """
        티커에서 회사명 추출

        Args:
            ticker: 종목 티커 (예: "005930.KS")

        Returns:
            회사명
        """
        # 주요 한국 종목 매핑
        ticker_to_name = {
            "005930.KS": "삼성전자",
            "035720.KS": "카카오",
            "000660.KS": "SK하이닉스",
            "051910.KS": "LG화학",
            "005380.KS": "현대차",
            "006400.KS": "삼성SDI",
            "035420.KS": "NAVER",
            "207940.KS": "삼성바이오로직스",
            "068270.KS": "셀트리온",
            "028260.KS": "삼성물산",
        }

        return ticker_to_name.get(ticker, ticker.split('.')[0])

    def create_enhanced_prompt(self, data: Dict[str, Any]) -> str:
        """
        신뢰도 점수를 포함한 향상된 프롬프트 생성

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

        # 비판적 추론 프롬프트 생성 (신뢰도 점수 포함)
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

### 5. 신뢰도 점수 (Reliability Score)

**점수: [0-100점]**

**평가 기준:**
- 데이터 완전성 (0-25점): 주가, 뉴스, 공시 데이터의 충분성과 품질
- 데이터-내러티브 일관성 (0-25점): 뉴스 내용과 실제 주가 움직임의 일치 정도
- 공시 신뢰성 (0-25점): 공시 내용의 실현 가능성과 과거 실적 대비 합리성
- 분석 근거 강도 (0-25점): 강세론/약세론의 근거가 데이터에 얼마나 명확히 기반하는가

**점수 산정 논리:**
- 데이터 완전성: [점수]점 - [이유]
- 데이터-내러티브 일관성: [점수]점 - [이유]
- 공시 신뢰성: [점수]점 - [이유]
- 분석 근거 강도: [점수]점 - [이유]

**총점: [합계]점**

**신뢰도 해석:**
- 80-100점: 높은 신뢰도 - 데이터 기반 의사결정 가능
- 60-79점: 중간 신뢰도 - 추가 검증 후 의사결정 권장
- 40-59점: 낮은 신뢰도 - 추가 데이터 수집 필요
- 0-39점: 매우 낮은 신뢰도 - 의사결정 보류 권장

**주요 신뢰도 저해 요인:**
- [요인 1]
- [요인 2]
- [요인 3]

---

**중요:** 추측이나 일반론은 배제하고, 오직 제공된 데이터에 기반한 분석만 수행하세요.
데이터가 불충분한 경우 "데이터 부족"이라고 명시하고, 신뢰도 점수에 반영하세요.
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

    def _format_news_data(self, news: list) -> str:
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

    def _format_disclosure_data(self, disclosures: list) -> str:
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

        return "\n".join(lines) if lines else "[ERROR] 유효한 공시 없음"

    def analyze_with_reliability(self, json_file_path: str) -> Dict[str, Any]:
        """
        신뢰도 점수를 포함한 분석 실행

        Args:
            json_file_path: 분석할 JSON 파일 경로

        Returns:
            분석 결과 딕셔너리
        """
        print(f"\n{'='*80}")
        print(f"[START] Critical analysis (with reliability score)")
        print(f"{'='*80}\n")

        # 1. 데이터 로드
        data = self.analyzer.load_data(json_file_path)

        # 2. 향상된 프롬프트 생성
        print("[INFO] Creating critical reasoning prompt (with reliability score)...")
        prompt = self.create_enhanced_prompt(data)

        # 3. Claude API 호출
        print("[INFO] Calling Claude API...")
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8192,  # 신뢰도 점수 포함으로 토큰 증가
                temperature=0.3,
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
            "company_name": data.get('stock_data', {}).get('company_name', 'N/A'),
            "source_file": json_file_path,
            "analysis": analysis_text,
            "metadata": {
                "model": "claude-sonnet-4-20250514",
                "framework": "Critical Reasoning Framework with Reliability Score",
                "rules": [
                    "Data-Narrative Discrepancy Analysis",
                    "Disclosure Credibility Check",
                    "Confirmation Bias Elimination (5:5 Balance)",
                    "Reliability Score (0-100)"
                ]
            }
        }

        return result

    def save_report(self, result: Dict[str, Any], ticker: str) -> str:
        """
        최종 보고서를 reports/ 폴더에 저장

        Args:
            result: 분석 결과
            ticker: 종목 티커

        Returns:
            저장된 파일 경로
        """
        # 회사명 추출
        company_name = self.get_company_name(ticker)

        # 날짜 포맷팅
        date_str = datetime.now().strftime('%Y%m%d')

        # 파일명 생성
        filename = f"{company_name}_{date_str}.md"
        filepath = os.path.join(self.reports_dir, filename)

        # Markdown 보고서 생성
        report_content = f"""# 비판적 분석 보고서 - {company_name}

## [DATA] 기본 정보
- **종목명**: {company_name}
- **티커**: {result['ticker']}
- **분석 일시**: {result['analyzed_at']}
- **분석 모델**: Claude Sonnet 4 (2025-05-14)

---

## [TARGET] 분석 프레임워크
- [OK] 데이터-내러티브 괴리 분석
- [OK] 공시 진위 판별
- [OK] 확증 편향 제거 (강세론 5:5 약세론)
- [OK] 신뢰도 점수 평가

---

## [CHART] 분석 결과

{result['analysis']}

---

## [WARN] 면책 조항

이 보고서는 Claude AI의 비판적 추론 프레임워크를 통해 생성된 데이터 분석 결과입니다.

**투자 시 유의사항:**
- 본 보고서는 투자 권유가 아닌 정보 제공 목적입니다
- 실제 투자 결정 시 반드시 추가적인 실사(Due Diligence)를 수행하세요
- 신뢰도 점수가 낮은 경우 추가 데이터 수집을 권장합니다
- 과거 데이터 기반 분석이므로 미래 수익을 보장하지 않습니다

---

*Generated by Global Macro Intelligence Hub*
*Powered by Claude Sonnet 4*
"""

        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)

        return filepath

    def run(self, ticker: str) -> str:
        """
        전체 워크플로우 실행

        Args:
            ticker: 종목 티커 (예: "005930.KS")

        Returns:
            최종 보고서 파일 경로
        """
        company_name = self.get_company_name(ticker)

        print(f"\n{'='*80}")
        print(f"[START] Global Macro Intelligence Hub")
        print(f"{'='*80}")
        print(f"[INFO] 종목: {company_name} ({ticker})")
        print(f"[TIME] 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")

        # 1단계: 데이터 수집
        print("\n" + "="*80)
        print("[DATA] 1단계: 데이터 수집")
        print("="*80 + "\n")

        data_result = self.collector.collect_all_data(ticker)

        print("\n[OK] 데이터 수집 완료:")
        print(f"   - 주가 데이터: {len(data_result['stock_data'].get('data', []))}일")
        print(f"   - 뉴스: {len(data_result['news'])}건")
        print(f"   - 공시: {len(data_result['disclosures'])}건")

        # 2단계: 비판적 분석
        print("\n" + "="*80)
        print("[SEARCH] 2단계: 비판적 분석 (신뢰도 점수 포함)")
        print("="*80 + "\n")

        # 방금 생성된 JSON 파일 찾기
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        import glob
        json_files = glob.glob(os.path.join(data_dir, f"data_{ticker.replace('.', '_')}*.json"))

        if not json_files:
            print("[ERROR] 수집된 데이터 파일을 찾을 수 없습니다.")
            return None

        latest_file = max(json_files, key=os.path.getmtime)
        analysis_result = self.analyze_with_reliability(latest_file)

        # 3단계: 보고서 저장
        print("\n" + "="*80)
        print("[SAVE] 3단계: 최종 보고서 생성")
        print("="*80 + "\n")

        report_path = self.save_report(analysis_result, ticker)

        print(f"[OK] 보고서 저장 완료: {report_path}")

        # 완료 메시지
        print(f"\n{'='*80}")
        print("[COMPLETE] 전체 워크플로우 완료!")
        print(f"{'='*80}")
        print(f"\n[FILE] 최종 보고서 위치:")
        print(f"   {report_path}")
        print(f"\n[TIME] 완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")

        return report_path


def main():
    """메인 실행 함수"""
    # 명령줄 인자 파싱
    parser = argparse.ArgumentParser(
        description='Global Macro Intelligence Hub - 주식 데이터 수집 및 비판적 분석',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python main.py --ticker 005930.KS           # 삼성전자 분석
  python main.py --ticker 035720.KS           # 카카오 분석
  python main.py -t 000660.KS                 # SK하이닉스 분석 (축약형)

지원 종목:
  005930.KS  삼성전자
  035720.KS  카카오
  000660.KS  SK하이닉스
  051910.KS  LG화학
  005380.KS  현대차
  006400.KS  삼성SDI
  035420.KS  NAVER
        """
    )

    parser.add_argument(
        '--ticker', '-t',
        type=str,
        required=True,
        help='종목 티커 (예: 005930.KS)'
    )

    args = parser.parse_args()

    # API 키 확인
    required_keys = ['DART_API_KEY', 'NEWS_API_KEY', 'ANTHROPIC_API_KEY']
    missing_keys = [key for key in required_keys if not os.getenv(key)]

    if missing_keys:
        print("[ERROR] 다음 API 키가 .env 파일에 설정되지 않았습니다:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\n.env 파일을 확인하고 필요한 API 키를 추가하세요.")
        sys.exit(1)

    # 워크플로우 실행
    try:
        hub = IntelligenceHub()
        report_path = hub.run(args.ticker)

        if report_path:
            print(f"\n[DONE] 보고서를 확인하세요: {report_path}\n")
            sys.exit(0)
        else:
            print("\n[ERROR] 보고서 생성 실패\n")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n[WARN]  사용자에 의해 중단되었습니다.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
