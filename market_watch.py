"""
Global Macro Intelligence Hub - Market Watch
시장 감시 및 주목할 만한 종목 추천 모듈
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import time


class MarketWatch:
    """시장 감시 및 종목 추천 클래스"""

    def __init__(self):
        """초기화"""
        # 주요 한국 종목 리스트
        self.kospi_stocks = {
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

    def calculate_technical_indicators(self, ticker: str, days: int = 30) -> Dict[str, Any]:
        """
        기술적 지표 계산

        Args:
            ticker: 종목 티커
            days: 분석 기간 (일)

        Returns:
            기술적 지표 딕셔너리
        """
        try:
            # 데이터 가져오기
            stock = yf.Ticker(ticker)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days+10)  # 여유있게

            hist = stock.history(start=start_date, end=end_date)

            if len(hist) < 2:
                return None

            # 최신 데이터
            latest = hist.iloc[-1]
            previous = hist.iloc[-2]

            # 가격 변화
            price_change = ((latest['Close'] - previous['Close']) / previous['Close']) * 100

            # 거래량 변화
            avg_volume = hist['Volume'].tail(10).mean()
            volume_change = ((latest['Volume'] - avg_volume) / avg_volume) * 100 if avg_volume > 0 else 0

            # 이동평균선 계산
            hist['MA5'] = hist['Close'].rolling(window=5).mean()
            hist['MA20'] = hist['Close'].rolling(window=20).mean()

            ma5_current = hist['MA5'].iloc[-1]
            ma20_current = hist['MA20'].iloc[-1]
            ma5_prev = hist['MA5'].iloc[-2]
            ma20_prev = hist['MA20'].iloc[-2]

            # 골든크로스/데드크로스 감지
            golden_cross = (ma5_prev <= ma20_prev) and (ma5_current > ma20_current)
            death_cross = (ma5_prev >= ma20_prev) and (ma5_current < ma20_current)

            # 52주 최고/최저
            high_52w = hist['High'].tail(252).max() if len(hist) >= 252 else hist['High'].max()
            low_52w = hist['Low'].tail(252).min() if len(hist) >= 252 else hist['Low'].min()

            distance_from_high = ((high_52w - latest['Close']) / high_52w) * 100
            distance_from_low = ((latest['Close'] - low_52w) / low_52w) * 100

            # RSI 계산 (14일)
            rsi = self._calculate_rsi(hist['Close'], period=14)

            return {
                "ticker": ticker,
                "current_price": latest['Close'],
                "previous_close": previous['Close'],
                "price_change_pct": price_change,
                "volume": latest['Volume'],
                "avg_volume": avg_volume,
                "volume_change_pct": volume_change,
                "ma5": ma5_current,
                "ma20": ma20_current,
                "golden_cross": golden_cross,
                "death_cross": death_cross,
                "high_52w": high_52w,
                "low_52w": low_52w,
                "distance_from_high_pct": distance_from_high,
                "distance_from_low_pct": distance_from_low,
                "rsi": rsi,
            }

        except Exception as e:
            print(f"[WARN] {ticker} analysis failed: {str(e)}")
            return None

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """RSI 계산"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))

            return rsi.iloc[-1]
        except:
            return 50.0  # 중립값

    def generate_recommendation_reason(self, indicators: Dict[str, Any]) -> str:
        """
        추천 사유 생성

        Args:
            indicators: 기술적 지표

        Returns:
            추천 사유 (한 줄)
        """
        reasons = []

        # 급등
        if indicators['price_change_pct'] > 10:
            reasons.append(f"급등 {indicators['price_change_pct']:.1f}%")
        elif indicators['price_change_pct'] > 5:
            reasons.append(f"상승 {indicators['price_change_pct']:.1f}%")

        # 거래량 급증
        if indicators['volume_change_pct'] > 200:
            reasons.append("역대급 거래량")
        elif indicators['volume_change_pct'] > 100:
            reasons.append("거래량 급증")
        elif indicators['volume_change_pct'] > 50:
            reasons.append("거래량 증가")

        # 골든크로스
        if indicators['golden_cross']:
            reasons.append("골든크로스 발생")

        # 52주 최저점 근처
        if indicators['distance_from_low_pct'] < 5:
            reasons.append("52주 최저가 근접")
        # 52주 최고점 돌파
        elif indicators['distance_from_high_pct'] < 1:
            reasons.append("52주 최고가 경신")

        # RSI
        if indicators['rsi'] < 30:
            reasons.append("과매도 구간")
        elif indicators['rsi'] > 70:
            reasons.append("과매수 구간")

        # MA 위치
        if indicators['current_price'] > indicators['ma5'] > indicators['ma20']:
            reasons.append("상승 추세")
        elif indicators['current_price'] < indicators['ma5'] < indicators['ma20']:
            reasons.append("하락 추세")

        if reasons:
            return " | ".join(reasons[:3])  # 최대 3개 사유
        else:
            return "주가 변동 감지"

    def calculate_recommendation_score(self, indicators: Dict[str, Any]) -> float:
        """
        추천 점수 계산 (0-100)

        Args:
            indicators: 기술적 지표

        Returns:
            추천 점수
        """
        score = 50.0  # 기본 점수

        # 가격 변화
        if indicators['price_change_pct'] > 7:
            score += 20
        elif indicators['price_change_pct'] > 5:
            score += 15
        elif indicators['price_change_pct'] > 3:
            score += 10

        # 거래량 변화
        if indicators['volume_change_pct'] > 150:
            score += 15
        elif indicators['volume_change_pct'] > 100:
            score += 12
        elif indicators['volume_change_pct'] > 50:
            score += 8

        # 골든크로스
        if indicators['golden_cross']:
            score += 10

        # RSI
        if 40 <= indicators['rsi'] <= 60:
            score += 5  # 중립적인 RSI는 긍정

        # 데드크로스 페널티
        if indicators['death_cross']:
            score -= 10

        # 과매수 페널티
        if indicators['rsi'] > 80:
            score -= 5

        return min(max(score, 0), 100)  # 0-100 범위 제한

    def get_watchlist(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        주목할 만한 종목 리스트 가져오기

        Args:
            limit: 반환할 종목 수

        Returns:
            추천 종목 리스트
        """
        print("\n" + "="*70)
        print("[WATCH] Market Watch - Monitoring market...")
        print("="*70 + "\n")

        watchlist = []

        for ticker, name in self.kospi_stocks.items():
            print(f"분석 중: {name} ({ticker})...", end=" ")

            indicators = self.calculate_technical_indicators(ticker)

            if indicators:
                # 추천 조건: 5% 이상 상승 또는 거래량 50% 이상 증가
                if (indicators['price_change_pct'] >= 5 or
                    indicators['volume_change_pct'] >= 50):

                    score = self.calculate_recommendation_score(indicators)
                    reason = self.generate_recommendation_reason(indicators)

                    watchlist.append({
                        "ticker": ticker,
                        "company_name": name,
                        "current_price": indicators['current_price'],
                        "price_change_pct": indicators['price_change_pct'],
                        "volume_change_pct": indicators['volume_change_pct'],
                        "score": score,
                        "reason": reason,
                        "indicators": indicators
                    })

                    print(f"[RECOMMEND] Score: {score:.0f}")
                else:
                    print("[SKIP] Below threshold")
            else:
                print("[FAIL] Failed")

            # API 제한 고려
            time.sleep(0.5)

        # 점수 순으로 정렬
        watchlist.sort(key=lambda x: x['score'], reverse=True)

        print(f"\n{'='*70}")
        print(f"[OK] 분석 완료: {len(watchlist)}개 종목 발견")
        print(f"{'='*70}\n")

        return watchlist[:limit]

    def get_market_summary(self) -> Dict[str, Any]:
        """
        시장 전체 요약 정보

        Returns:
            시장 요약 딕셔너리
        """
        try:
            # KOSPI 지수
            kospi = yf.Ticker("^KS11")
            kospi_hist = kospi.history(period="5d")

            if len(kospi_hist) >= 2:
                kospi_current = kospi_hist['Close'].iloc[-1]
                kospi_prev = kospi_hist['Close'].iloc[-2]
                kospi_change = ((kospi_current - kospi_prev) / kospi_prev) * 100
            else:
                kospi_current = kospi_prev = kospi_change = 0

            # KOSDAQ 지수
            kosdaq = yf.Ticker("^KQ11")
            kosdaq_hist = kosdaq.history(period="5d")

            if len(kosdaq_hist) >= 2:
                kosdaq_current = kosdaq_hist['Close'].iloc[-1]
                kosdaq_prev = kosdaq_hist['Close'].iloc[-2]
                kosdaq_change = ((kosdaq_current - kosdaq_prev) / kosdaq_prev) * 100
            else:
                kosdaq_current = kosdaq_prev = kosdaq_change = 0

            return {
                "kospi": {
                    "value": kospi_current,
                    "change_pct": kospi_change
                },
                "kosdaq": {
                    "value": kosdaq_current,
                    "change_pct": kosdaq_change
                },
                "updated_at": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"[WARN] 시장 요약 정보 가져오기 실패: {str(e)}")
            return None


def main():
    """테스트 실행"""
    watch = MarketWatch()

    # 시장 요약
    print("\n[DATA] 시장 요약")
    summary = watch.get_market_summary()
    if summary:
        print(f"KOSPI: {summary['kospi']['value']:.2f} ({summary['kospi']['change_pct']:+.2f}%)")
        print(f"KOSDAQ: {summary['kosdaq']['value']:.2f} ({summary['kosdaq']['change_pct']:+.2f}%)")

    # 주목할 종목
    print("\n\n[TARGET] 주목할 만한 종목")
    watchlist = watch.get_watchlist(limit=5)

    for i, item in enumerate(watchlist, 1):
        print(f"\n{i}. {item['company_name']} ({item['ticker']})")
        print(f"   현재가: {item['current_price']:,.0f}원 ({item['price_change_pct']:+.2f}%)")
        print(f"   거래량: {item['volume_change_pct']:+.1f}% 변화")
        print(f"   점수: {item['score']:.0f}/100")
        print(f"   사유: {item['reason']}")


if __name__ == "__main__":
    main()
