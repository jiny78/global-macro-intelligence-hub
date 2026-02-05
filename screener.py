"""
Global Macro Intelligence Hub - Stock Screener
순수 파이썬 수치 계산 기반 종목 스크리닝 (LLM 호출 없음)
"""

import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import time


class StockScreener:
    """
    순수 수치 계산 기반 종목 스크리너
    - LLM(Claude) 호출 없음
    - 거래량, RSI 등 기술적 지표만 계산
    """

    def __init__(self):
        """초기화"""
        # KOSPI 상위 20개 종목
        self.watch_stocks = {
            "005930.KS": "삼성전자",
            "000660.KS": "SK하이닉스",
            "035420.KS": "NAVER",
            "051910.KS": "LG화학",
            "005380.KS": "현대차",
            "006400.KS": "삼성SDI",
            "035720.KS": "카카오",
            "207940.KS": "삼성바이오로직스",
            "068270.KS": "셀트리온",
            "028260.KS": "삼성물산",
            "003670.KS": "포스코홀딩스",
            "012330.KS": "현대모비스",
            "000270.KS": "기아",
            "105560.KS": "KB금융",
            "055550.KS": "신한지주",
            "017670.KS": "SK텔레콤",
            "096770.KS": "SK이노베이션",
            "034020.KS": "두산에너빌리티",
            "009150.KS": "삼성전기",
            "018260.KS": "삼성에스디에스",
        }

    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """
        RSI (Relative Strength Index) 계산

        Args:
            prices: 가격 시리즈
            period: RSI 계산 기간

        Returns:
            RSI 값 (0-100)
        """
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))

            return rsi.iloc[-1]
        except Exception as e:
            print(f"   [WARN] RSI calculation failed: {str(e)}")
            return 50.0  # 중립값

    def analyze_stock(self, ticker: str, days: int = 20) -> Dict[str, Any]:
        """
        개별 종목 분석 (순수 수치 계산)

        Args:
            ticker: 종목 티커
            days: 분석 기간

        Returns:
            분석 결과 딕셔너리
        """
        try:
            # 데이터 가져오기
            stock = yf.Ticker(ticker)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days+20)  # 여유있게

            hist = stock.history(start=start_date, end=end_date)

            if len(hist) < 2:
                return None

            # 최신 데이터
            latest = hist.iloc[-1]
            previous = hist.iloc[-2]

            # 1. 현재가 및 등락률
            current_price = latest['Close']
            previous_close = previous['Close']
            price_change_pct = ((current_price - previous_close) / previous_close) * 100

            # 2. 거래량 분석
            current_volume = latest['Volume']

            # 최근 20일 평균 거래량
            avg_volume_20d = hist['Volume'].tail(days).mean()

            # 거래량 변화율
            volume_change_pct = ((current_volume - avg_volume_20d) / avg_volume_20d) * 100 if avg_volume_20d > 0 else 0

            # 거래량이 평균 대비 몇 배인지
            volume_ratio = current_volume / avg_volume_20d if avg_volume_20d > 0 else 1.0

            # 3. RSI 계산
            rsi = self.calculate_rsi(hist['Close'], period=14)

            # 4. 주목 조건 체크
            noteworthy = False
            reasons = []

            # 조건 1: 거래량이 평균 대비 2배 이상
            if volume_ratio >= 2.0:
                noteworthy = True
                reasons.append(f"거래량 {volume_ratio:.1f}배 급증")

            # 조건 2: RSI 30 이하 (과매도)
            if rsi <= 30:
                noteworthy = True
                reasons.append(f"과매도 (RSI {rsi:.1f})")

            # 조건 3: RSI 70 이상 (과매수)
            if rsi >= 70:
                noteworthy = True
                reasons.append(f"과매수 (RSI {rsi:.1f})")

            return {
                "ticker": ticker,
                "current_price": float(current_price),
                "previous_close": float(previous_close),
                "price_change_pct": float(price_change_pct),
                "current_volume": int(current_volume),
                "avg_volume_20d": float(avg_volume_20d),
                "volume_change_pct": float(volume_change_pct),
                "volume_ratio": float(volume_ratio),
                "rsi": float(rsi),
                "noteworthy": noteworthy,
                "reasons": reasons
            }

        except Exception as e:
            print(f"   [WARN] Analysis failed: {str(e)}")
            return None

    def screen_stocks(self) -> List[Dict[str, Any]]:
        """
        전체 종목 스크리닝

        Returns:
            주목할 종목 리스트
        """
        print("\n" + "="*70)
        print("[SCAN] Stock Screener - Scanning stocks...")
        print("="*70)
        print("\n[CRITERIA] Screening conditions:")
        print("  1. 거래량이 20일 평균 대비 2배 이상")
        print("  2. RSI 30 이하 (과매도)")
        print("  3. RSI 70 이상 (과매수)")
        print("\n" + "="*70 + "\n")

        noteworthy_stocks = []

        for ticker, name in self.watch_stocks.items():
            print(f"분석 중: {name} ({ticker})...", end=" ")

            result = self.analyze_stock(ticker)

            if result and result['noteworthy']:
                result['company_name'] = name
                noteworthy_stocks.append(result)
                print(f"[ALERT] Watch - {', '.join(result['reasons'])}")
            elif result:
                print("[SKIP]  일반")
            else:
                print("[ERROR] 실패")

            # API 제한 고려
            time.sleep(0.5)

        print(f"\n{'='*70}")
        print(f"[OK] 스크리닝 완료: {len(noteworthy_stocks)}개 종목 발견")
        print(f"{'='*70}\n")

        return noteworthy_stocks

    def save_to_json(self, watchlist: List[Dict[str, Any]], filename: str = "watchlist.json"):
        """
        watchlist를 JSON 파일로 저장

        Args:
            watchlist: 주목할 종목 리스트
            filename: 저장할 파일명
        """
        output = {
            "generated_at": datetime.now().isoformat(),
            "total_analyzed": len(self.watch_stocks),
            "noteworthy_count": len(watchlist),
            "screening_criteria": {
                "volume_threshold": "2x average (20 days)",
                "rsi_oversold": 30,
                "rsi_overbought": 70
            },
            "stocks": []
        }

        for stock in watchlist:
            output["stocks"].append({
                "ticker": stock['ticker'],
                "company_name": stock['company_name'],
                "price": {
                    "current": stock['current_price'],
                    "previous_close": stock['previous_close'],
                    "change_pct": stock['price_change_pct']
                },
                "volume": {
                    "current": stock['current_volume'],
                    "avg_20d": stock['avg_volume_20d'],
                    "change_pct": stock['volume_change_pct'],
                    "ratio": stock['volume_ratio']
                },
                "indicators": {
                    "rsi": stock['rsi']
                },
                "reasons": stock['reasons']
            })

        # 파일 저장
        filepath = os.path.join(os.path.dirname(__file__), filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"[SAVE] watchlist 저장 완료: {filepath}\n")

        return filepath

    def print_summary(self, watchlist: List[Dict[str, Any]]):
        """
        주목할 종목 요약 출력

        Args:
            watchlist: 주목할 종목 리스트
        """
        if not watchlist:
            print("[DATA] 주목할 종목이 없습니다.\n")
            return

        print("\n" + "="*70)
        print(f"[DATA] 주목할 종목 요약 ({len(watchlist)}개)")
        print("="*70 + "\n")

        for i, stock in enumerate(watchlist, 1):
            print(f"{i}. {stock['company_name']} ({stock['ticker']})")
            print(f"   현재가: {stock['current_price']:,.0f}원 ({stock['price_change_pct']:+.2f}%)")
            print(f"   거래량: {stock['current_volume']:,} (평균 대비 {stock['volume_ratio']:.2f}배)")
            print(f"   RSI: {stock['rsi']:.1f}")
            print(f"   [INFO] 사유: {', '.join(stock['reasons'])}")
            print()


def main():
    """메인 실행 함수"""
    import os  # main 내부에서 import

    # 스크리너 생성
    screener = StockScreener()

    # 스크리닝 실행
    watchlist = screener.screen_stocks()

    # 결과 출력
    screener.print_summary(watchlist)

    # JSON 저장
    if watchlist:
        screener.save_to_json(watchlist, filename="watchlist.json")

        print("="*70)
        print("[OK] 모든 작업 완료!")
        print("="*70)
        print("\n[TIP] 다음 단계:")
        print("  1. watchlist.json 파일 확인")
        print("  2. 주목할 종목에 대해 main.py로 심층 분석 실행")
        print("     예: python main.py --ticker 005930.KS")
        print()
    else:
        print("[WARN]  현재 주목할 만한 종목이 없습니다.\n")


if __name__ == "__main__":
    main()
