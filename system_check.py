"""
System Health Check
전체 시스템 문제점 점검
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("System Health Check")
print("=" * 70)
print()

issues = []
warnings = []

# 1. API Keys Check
print("[1] API Keys Verification")
print("-" * 70)

api_keys = {
    'DART_API_KEY': os.getenv('DART_API_KEY'),
    'NEWS_API_KEY': os.getenv('NEWS_API_KEY'),
    'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
    'SENDER_EMAIL': os.getenv('SENDER_EMAIL'),
    'APP_PASSWORD': os.getenv('APP_PASSWORD'),
    'RECIPIENT_EMAIL': os.getenv('RECIPIENT_EMAIL')
}

for key, value in api_keys.items():
    if value:
        print(f"[OK] {key}: {value[:8]}...")
    else:
        print(f"[FAIL] {key}: NOT SET")
        issues.append(f"{key} not configured")

print()

# 2. Module Import Test
print("[2] Module Import Test")
print("-" * 70)

modules_to_test = [
    ('dart_fss', 'import dart_fss as df'),
    ('yfinance', 'import yfinance as yf'),
    ('newsapi', 'from newsapi import NewsApiClient'),
    ('anthropic', 'import anthropic'),
    ('streamlit', 'import streamlit'),
    ('plotly', 'import plotly.graph_objects as go'),
    ('fpdf', 'from fpdf import FPDF'),
]

for module_name, import_stmt in modules_to_test:
    try:
        exec(import_stmt)
        print(f"[OK] {module_name}")
    except Exception as e:
        print(f"[FAIL] {module_name}: {e}")
        issues.append(f"{module_name} import failed")

print()

# 3. DART API Test
print("[3] DART API Connection Test")
print("-" * 70)

try:
    import dart_fss as df
    dart_key = os.getenv('DART_API_KEY')

    if dart_key:
        df.set_api_key(api_key=dart_key)
        corp_list = df.get_corp_list()

        if corp_list:
            print(f"[OK] DART API working - {len(corp_list)} corporations loaded")
        else:
            print("[WARN] DART API returned None")
            warnings.append("DART API returns None")
    else:
        print("[FAIL] DART API key not set")
        issues.append("DART API key missing")

except Exception as e:
    print(f"[FAIL] DART API error: {e}")
    issues.append(f"DART API: {str(e)}")

print()

# 4. News API Test
print("[4] News API Test")
print("-" * 70)

try:
    from newsapi import NewsApiClient
    news_key = os.getenv('NEWS_API_KEY')

    if news_key:
        newsapi = NewsApiClient(api_key=news_key)

        # Test with English query
        print("[TEST 1] English query test...")
        try:
            test_en = newsapi.get_everything(
                q='Samsung',
                language='en',
                page_size=1
            )
            if test_en['status'] == 'ok':
                print(f"[OK] English query works - {test_en['totalResults']} results")
            else:
                print(f"[WARN] English query status: {test_en['status']}")
        except Exception as e:
            print(f"[FAIL] English query: {e}")

        # Test with Korean query
        print("[TEST 2] Korean query test...")
        try:
            test_ko = newsapi.get_everything(
                q='삼성전자',
                language='ko',
                page_size=1
            )
            if test_ko['status'] == 'ok':
                print(f"[OK] Korean query works - {test_ko['totalResults']} results")
            else:
                print(f"[WARN] Korean query status: {test_ko['status']}")
        except Exception as e:
            print(f"[FAIL] Korean query failed: {e}")
            issues.append(f"News API Korean language not supported: {str(e)}")

        # Test without language filter
        print("[TEST 3] No language filter test...")
        try:
            test_no_lang = newsapi.get_everything(
                q='삼성전자 OR Samsung Electronics',
                page_size=5
            )
            if test_no_lang['status'] == 'ok':
                articles = test_no_lang.get('articles', [])
                print(f"[OK] No language filter works - {len(articles)} articles")
                if articles:
                    print(f"    Sample: {articles[0].get('title', 'N/A')[:50]}...")
            else:
                print(f"[WARN] No language filter status: {test_no_lang['status']}")
        except Exception as e:
            print(f"[FAIL] No language filter: {e}")

    else:
        print("[FAIL] News API key not set")
        issues.append("News API key missing")

except Exception as e:
    print(f"[FAIL] News API error: {e}")
    issues.append(f"News API: {str(e)}")

print()

# 5. Claude API Test
print("[5] Claude API Test")
print("-" * 70)

try:
    import anthropic
    claude_key = os.getenv('ANTHROPIC_API_KEY')

    if claude_key:
        client = anthropic.Anthropic(api_key=claude_key)

        # Simple test
        try:
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=50,
                messages=[{"role": "user", "content": "Hello"}]
            )
            print(f"[OK] Claude API working")
            print(f"    Response: {message.content[0].text[:50]}...")
        except Exception as e:
            print(f"[FAIL] Claude API call failed: {e}")
            issues.append(f"Claude API: {str(e)}")
    else:
        print("[FAIL] Claude API key not set")
        issues.append("Claude API key missing")

except Exception as e:
    print(f"[FAIL] Claude API error: {e}")
    issues.append(f"Claude API: {str(e)}")

print()

# 6. Font Check
print("[6] Korean Font Check")
print("-" * 70)

from report_manager import ProfessionalPDFReport

pdf = ProfessionalPDFReport()
has_font, font_path = pdf.find_korean_font()

if has_font:
    print(f"[OK] Korean font found: {font_path}")
else:
    print("[WARN] No Korean font found - will use English")
    warnings.append("No Korean font (PDF will use English)")

print()

# Summary
print("=" * 70)
print("Summary")
print("=" * 70)
print()

if not issues:
    print("[SUCCESS] No critical issues found!")
else:
    print(f"[CRITICAL] {len(issues)} issue(s) found:")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")

print()

if warnings:
    print(f"[WARNINGS] {len(warnings)} warning(s):")
    for i, warning in enumerate(warnings, 1):
        print(f"  {i}. {warning}")

print()

# Recommendations
print("=" * 70)
print("Recommendations")
print("=" * 70)
print()

if "News API Korean language not supported" in str(issues):
    print("[NEWS API ISSUE]")
    print("  Problem: News API doesn't support Korean language parameter")
    print()
    print("  Solutions:")
    print("  1. Use English query instead (q='Samsung Electronics')")
    print("  2. Remove language filter (works but gets mixed languages)")
    print("  3. Switch to alternative news source:")
    print("     - Google News RSS (Free, no API key needed)")
    print("     - Naver News Search API (Free, requires registration)")
    print("     - Direct web scraping with BeautifulSoup")
    print()
    print("  Recommended: Google News RSS (easiest and free)")
    print()

print("=" * 70)
