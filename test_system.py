"""
System Test Script
"""

import os
import sys
from datetime import datetime

print("=" * 60)
print("Global Macro Intelligence Hub - System Test")
print("=" * 60)
print()

# 1. Environment Variables Check
print("1. Environment Variables Check...")
from dotenv import load_dotenv
load_dotenv()

required_keys = ['DART_API_KEY', 'NEWS_API_KEY', 'ANTHROPIC_API_KEY',
                 'SENDER_EMAIL', 'APP_PASSWORD', 'RECIPIENT_EMAIL']

for key in required_keys:
    value = os.getenv(key)
    if value:
        masked = value[:8] + "..." if len(value) > 8 else "***"
        print(f"   [OK] {key}: {masked}")
    else:
        print(f"   [FAIL] {key}: Missing")

print()

# 2. Module Import Test
print("2. Module Import Test...")
try:
    from screener import StockScreener
    print("   [OK] StockScreener")
except Exception as e:
    print(f"   [FAIL] StockScreener: {e}")

try:
    from data_collector import DataCollector
    print("   [OK] DataCollector")
except Exception as e:
    print(f"   [FAIL] DataCollector: {e}")

try:
    from critical_analyzer import CriticalAnalyzer
    print("   [OK] CriticalAnalyzer")
except Exception as e:
    print(f"   [FAIL] CriticalAnalyzer: {e}")

try:
    from report_manager import ExpertReportManager
    print("   [OK] ExpertReportManager")
except Exception as e:
    print(f"   [FAIL] ExpertReportManager: {e}")

print()

# 3. Screener Test
print("3. Screener Test...")
try:
    screener = StockScreener()
    print("   [INFO] Screening KOSPI stocks...")

    # Test with few stocks
    test_tickers = ['005930', '000660', '035420']  # Samsung, SK Hynix, NAVER

    results = []
    for ticker in test_tickers:
        try:
            result = screener.analyze_single_stock(ticker)
            if result:
                results.append(result)
                print(f"   [OK] {result['name']} ({ticker}): {result.get('score', 0)} points")
        except Exception as e:
            print(f"   [WARN] {ticker}: {e}")

    if results:
        print(f"   [OK] Screening complete: {len(results)} stocks")
    else:
        print("   [WARN] No screening results")

except Exception as e:
    print(f"   [FAIL] Screener error: {e}")

print()

# 4. Data Collection Test
print("4. Data Collection Test (Samsung)...")
try:
    collector = DataCollector()
    ticker = "005930"
    print(f"   [INFO] Collecting data for {ticker}...")

    data = collector.collect_all_data(ticker)

    if data:
        print(f"   [OK] Stock data: {len(data.get('stock_data', []))} days")
        print(f"   [OK] News: {len(data.get('news', []))} articles")
        print(f"   [OK] Disclosures: {len(data.get('disclosures', []))} items")
    else:
        print("   [WARN] Data collection failed")

except Exception as e:
    print(f"   [FAIL] Data collection error: {e}")

print()

# 5. AI Analyzer Test
print("5. AI Analyzer Initialization Test...")
try:
    analyzer = CriticalAnalyzer()
    print("   [OK] CriticalAnalyzer initialized")
    print("   [INFO] Full analysis test in Streamlit app (to save API costs)")
except Exception as e:
    print(f"   [FAIL] AI Analyzer error: {e}")

print()

# 6. PDF Report Manager Test
print("6. PDF Report Manager Test...")
try:
    manager = ExpertReportManager()
    print("   [OK] ExpertReportManager initialized")

    # Font detection test
    from report_manager import ProfessionalPDFReport
    pdf = ProfessionalPDFReport()
    has_font, font_path = pdf.find_korean_font()

    if has_font:
        print(f"   [OK] Korean font detected: {font_path}")
    else:
        print("   [WARN] No Korean font (will use English)")

except Exception as e:
    print(f"   [FAIL] PDF Manager error: {e}")

print()

# 7. Directory Structure Check
print("7. Directory Structure Check...")
dirs = ['data', 'reports']
for dir_name in dirs:
    if os.path.exists(dir_name):
        files = len(os.listdir(dir_name))
        print(f"   [OK] {dir_name}/ ({files} files)")
    else:
        print(f"   [WARN] {dir_name}/ not found")

print()

# 8. Streamlit App Status
print("8. Streamlit App Status...")
print("   [INFO] URL: http://localhost:8501")
print("   [INFO] Open the URL in your browser to test the app")

print()
print("=" * 60)
print("Test Complete!")
print("=" * 60)
print()
print("Next Steps:")
print("1. Open http://localhost:8501 in browser")
print("2. Check screening results")
print("3. Click 'Claude Analysis' button")
print("4. Click 'Expert PDF Report' button")
print("5. Check email (starhawk@naver.com)")
print()
