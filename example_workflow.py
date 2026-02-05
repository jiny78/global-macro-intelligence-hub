"""
Global Macro Intelligence Hub - Example Workflow
데이터 수집 → 비판적 분석 전체 워크플로우 예시
"""

from data_collector import DataCollector
from critical_analyzer import CriticalAnalyzer
import os
import time


def run_full_analysis(ticker: str):
    """
    특정 종목에 대한 전체 분석 워크플로우 실행

    Args:
        ticker: 종목 티커 (예: "005930.KS")
    """
    print(f"\n{'='*80}")
    print(f"[START] {ticker} full analysis workflow")
    print(f"{'='*80}\n")

    # 1단계: 데이터 수집
    print("\n[STEP 1] Data collection starting...")
    print("-" * 80)

    collector = DataCollector()
    data_result = collector.collect_all_data(ticker)

    # 수집 결과 요약
    print("\n[OK] Data collection complete:")
    print(f"   - 주가 데이터: {len(data_result['stock_data'].get('data', []))}일")
    print(f"   - 뉴스: {len(data_result['news'])}건")
    print(f"   - 공시: {len(data_result['disclosures'])}건")

    # 잠시 대기
    time.sleep(2)

    # 2단계: 비판적 분석
    print(f"\n{'='*80}")
    print("[STEP 2] Critical analysis starting...")
    print("-" * 80)

    # 방금 생성된 JSON 파일 경로 찾기
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    import glob
    json_files = glob.glob(os.path.join(data_dir, f"data_{ticker.replace('.', '_')}*.json"))

    if not json_files:
        print("[ERROR] Collected data file not found")
        return

    latest_file = max(json_files, key=os.path.getmtime)

    # 분석 실행
    analyzer = CriticalAnalyzer()
    analysis_result = analyzer.analyze(latest_file)

    # 3단계: 결과 저장
    print(f"\n{'='*80}")
    print("[SAVE] 3단계: 분석 결과 저장...")
    print("-" * 80)

    analyzer.save_analysis(analysis_result, output_format="both")

    # 4단계: 결과 미리보기
    print(f"\n{'='*80}")
    print("[LIST] 4단계: 분석 결과 미리보기")
    print(f"{'='*80}\n")

    print(analysis_result['analysis'])

    print(f"\n{'='*80}")
    print("[OK] 전체 워크플로우 완료!")
    print(f"{'='*80}\n")


def main():
    """메인 실행 함수"""
    # 분석할 종목 리스트
    tickers = [
        "005930.KS",  # 삼성전자
        # "035720.KS",  # 카카오
        # "000660.KS",  # SK하이닉스
    ]

    for ticker in tickers:
        try:
            run_full_analysis(ticker)
        except Exception as e:
            print(f"[ERROR] {ticker} 분석 중 오류 발생: {str(e)}")
            continue

        # 다음 종목 분석 전 잠시 대기 (API 제한 고려)
        if ticker != tickers[-1]:
            print("\n[WAIT] 다음 종목 분석 전 10초 대기...\n")
            time.sleep(10)


if __name__ == "__main__":
    main()
