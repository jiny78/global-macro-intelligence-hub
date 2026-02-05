"""
Test DART API Fix
"""

import os
from dotenv import load_dotenv
from data_collector import DataCollector

load_dotenv()

print("=" * 60)
print("DART API Fix Test")
print("=" * 60)
print()

# API 키 확인
dart_key = os.getenv('DART_API_KEY')
if dart_key:
    print(f"[OK] DART API Key found: {dart_key[:8]}...")
else:
    print("[FAIL] DART API Key not found in .env")
    exit(1)

print()
print("Initializing DataCollector...")
print()

try:
    collector = DataCollector()
    print()
    print("=" * 60)
    print("Test Result")
    print("=" * 60)
    print()

    if collector.dart_initialized:
        print("[SUCCESS] DART API initialized successfully!")
        print("[INFO] dart-fss import method: 'import dart_fss as df'")
        print("[INFO] API key setting: df.set_api_key(api_key=...)")
        print("[INFO] corp_list loaded successfully")
    else:
        print("[FAIL] DART API initialization failed")
        print("[INFO] Check your DART_API_KEY or network connection")

    print()

except Exception as e:
    print(f"[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
