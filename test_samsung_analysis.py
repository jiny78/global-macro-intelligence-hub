"""
Samsung Electronics Full Analysis Test
삼성전자 전체 시스템 테스트
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from data_collector import DataCollector
from critical_analyzer import CriticalAnalyzer
import json

load_dotenv()

print("=" * 70)
print("Samsung Electronics (005930) - Full System Test")
print("=" * 70)
print()

# 테스트 설정
ticker_kr = "005930.KS"  # 삼성전자 (yfinance용)
ticker_code = "005930"   # 삼성전자 (DART용)
company_name = "삼성전자"

print(f"Target: {company_name} ({ticker_code})")
print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()
print("-" * 70)
print("STEP 1: Data Collection")
print("-" * 70)
print()

try:
    # 데이터 수집
    collector = DataCollector()
    print()

    print("[1/3] Collecting stock data...")
    stock_data = collector.get_stock_data(ticker_kr, days=7)
    print()

    print("[2/3] Collecting news...")
    news_data = collector.get_news_headlines(ticker_kr, company_name, count=5)
    print()

    print("[3/3] Collecting disclosures...")
    disclosures = collector.get_dart_disclosures(ticker_kr, days=30)
    print()

    # 수집 결과 요약
    print("-" * 70)
    print("Data Collection Summary")
    print("-" * 70)

    stock_days = len(stock_data.get('data', []))
    news_count = len([n for n in news_data if 'error' not in n])
    disclosure_count = len([d for d in disclosures if 'error' not in d])

    print(f"Stock Data: {stock_days} days")
    if stock_days > 0:
        latest = stock_data['data'][-1]
        print(f"  Latest: {latest['date']}")
        print(f"  Close: {latest['close']:,.0f} KRW")
        print(f"  Volume: {latest['volume']:,}")

    print(f"\nNews: {news_count} articles")
    if news_count > 0:
        for i, news in enumerate(news_data[:3], 1):
            if 'error' not in news:
                print(f"  [{i}] {news.get('title', 'N/A')[:60]}...")

    print(f"\nDisclosures: {disclosure_count} items")
    if disclosure_count > 0:
        for i, disc in enumerate(disclosures[:3], 1):
            if 'error' not in disc:
                print(f"  [{i}] {disc.get('report_name', 'N/A')}")

    # 전체 데이터 구성
    collected_data = {
        "ticker": ticker_kr,
        "company_name": company_name,
        "collected_at": datetime.now().isoformat(),
        "stock_data": stock_data,
        "news": news_data,
        "disclosures": disclosures
    }

    # 데이터 저장
    output_file = f"data/test_{ticker_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs('data', exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(collected_data, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Data saved to: {output_file}")

    print()
    print("-" * 70)
    print("STEP 2: AI Critical Analysis")
    print("-" * 70)
    print()

    # AI 분석
    analyzer = CriticalAnalyzer()

    print("[INFO] Starting Claude Sonnet 4 analysis...")
    print("[INFO] This may take 10-15 seconds...")
    print()

    analysis_result = analyzer.analyze(collected_data)

    print("-" * 70)
    print("AI Analysis Result")
    print("-" * 70)
    print()

    if analysis_result and 'error' not in analysis_result:
        analysis_text = analysis_result.get('analysis', '')

        # 분석 결과 요약
        lines = analysis_text.split('\n')

        print("[Analysis Preview]")
        print()

        # 처음 30줄만 출력
        for line in lines[:30]:
            if line.strip():
                print(line)

        if len(lines) > 30:
            print()
            print(f"... ({len(lines) - 30} more lines)")

        # 신뢰도 점수 추출
        import re
        reliability_match = re.search(r'점수:\s*(\d+)', analysis_text)
        if reliability_match:
            score = reliability_match.group(1)
            print()
            print(f"[Reliability Score] {score}/100")

        # 분석 저장
        analysis_file = f"reports/test_analysis_{ticker_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        os.makedirs('reports', exist_ok=True)
        with open(analysis_file, 'w', encoding='utf-8') as f:
            f.write(analysis_text)

        print()
        print(f"[OK] Analysis saved to: {analysis_file}")

    else:
        print("[ERROR] Analysis failed")
        if 'error' in analysis_result:
            print(f"Error: {analysis_result['error']}")

    print()
    print("=" * 70)
    print("Test Complete!")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  - Data Collection: {'OK' if stock_days > 0 else 'FAIL'}")
    print(f"  - AI Analysis: {'OK' if analysis_result and 'error' not in analysis_result else 'FAIL'}")
    print(f"  - Stock Data: {stock_days} days")
    print(f"  - News: {news_count} articles")
    print(f"  - Disclosures: {disclosure_count} items")
    print()

    if analysis_result and 'error' not in analysis_result:
        print("[SUCCESS] All systems working properly!")
        print()
        print("Next Steps:")
        print("1. Open http://localhost:8501 in browser")
        print("2. Test PDF report generation")
        print("3. Check email delivery")
    else:
        print("[PARTIAL] Data collection OK, but AI analysis needs checking")

    print()

except Exception as e:
    print()
    print("=" * 70)
    print("[ERROR] Test Failed")
    print("=" * 70)
    print()
    print(f"Error: {str(e)}")
    print()
    import traceback
    traceback.print_exc()
