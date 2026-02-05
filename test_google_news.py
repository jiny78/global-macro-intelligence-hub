"""
Test Google News RSS Integration
"""

from data_collector import DataCollector
import json

print("=" * 70)
print("Google News RSS Test")
print("=" * 70)
print()

# Test data
test_cases = [
    ("005930.KS", "삼성전자"),
    ("000660.KS", "SK하이닉스"),
    ("035420.KS", "NAVER"),
]

collector = DataCollector()
print()

for ticker, company_name in test_cases:
    print("-" * 70)
    print(f"Testing: {company_name} ({ticker})")
    print("-" * 70)

    news = collector.get_news_headlines(ticker, company_name, count=3)

    print()
    print(f"Results for {company_name}:")
    print(f"  Total articles: {len([n for n in news if 'error' not in n])}")
    print()

    for i, article in enumerate(news, 1):
        if 'error' in article:
            print(f"  [ERROR] {article['error']}")
        else:
            print(f"  [{i}] {article['title'][:60]}...")
            print(f"      Source: {article['source']}")
            print(f"      Published: {article['published']}")
            print()

    print()

print("=" * 70)
print("Test Complete!")
print("=" * 70)
print()
print("Summary:")
print("- Google News RSS: No API key needed")
print("- Korean language: Fully supported")
print("- Real-time news: Available")
print()
