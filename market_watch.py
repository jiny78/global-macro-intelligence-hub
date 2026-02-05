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
        # 주요 한국 종목 리스트 (KOSPI 100 + KOSDAQ 100 = 200개)
        self.kospi_stocks = {
            # KOSPI 100개
            "005930.KS": "삼성전자", "000660.KS": "SK하이닉스", "035420.KS": "NAVER",
            "051910.KS": "LG화학", "005380.KS": "현대차", "006400.KS": "삼성SDI",
            "035720.KS": "카카오", "207940.KS": "삼성바이오로직스", "068270.KS": "셀트리온",
            "028260.KS": "삼성물산", "003670.KS": "포스코홀딩스", "012330.KS": "현대모비스",
            "000270.KS": "기아", "105560.KS": "KB금융", "055550.KS": "신한지주",
            "017670.KS": "SK텔레콤", "096770.KS": "SK이노베이션", "034020.KS": "두산에너빌리티",
            "009150.KS": "삼성전기", "018260.KS": "삼성에스디에스", "066570.KS": "LG전자",
            "086790.KS": "하나금융지주", "032830.KS": "삼성생명", "000810.KS": "삼성화재",
            "267250.KS": "현대중공업지주", "051900.KS": "LG생활건강", "241560.KS": "두산밥캣",
            "034730.KS": "SK", "138040.KS": "메리츠금융지주", "267260.KS": "HD현대",
            "402340.KS": "SK스퀘어", "003550.KS": "LG", "010130.KS": "고려아연",
            "015760.KS": "한국전력", "012450.KS": "한화에어로스페이스", "011200.KS": "HMM",
            "011170.KS": "롯데케미칼", "036460.KS": "한국가스공사", "010950.KS": "S-Oil",
            "004370.KS": "농심", "271560.KS": "오리온", "097950.KS": "CJ제일제당",
            "009540.KS": "한국조선해양", "030200.KS": "KT", "003490.KS": "대한항공",
            "090430.KS": "아모레퍼시픽", "000720.KS": "현대건설", "032640.KS": "LG유플러스",
            "086280.KS": "현대글로비스", "004020.KS": "현대제철", "010140.KS": "삼성중공업",
            "047050.KS": "POSCO인터내셔널", "161390.KS": "한국타이어앤테크놀로지", "000670.KS": "영풍",
            "011780.KS": "금호석유", "011210.KS": "현대위아", "028050.KS": "삼성엔지니어링",
            "078930.KS": "GS", "023530.KS": "롯데쇼핑", "001040.KS": "CJ",
            "282330.KS": "BGF리테일", "004170.KS": "신세계", "005300.KS": "롯데칠성",
            "049770.KS": "동원F&B", "026960.KS": "동서", "006260.KS": "LS",
            "120110.KS": "코오롱인더", "011070.KS": "LG이노텍", "285130.KS": "SK케미칼",
            "009830.KS": "한화솔루션", "298020.KS": "효성티앤씨", "000210.KS": "대림산업",
            "006360.KS": "GS건설", "042660.KS": "대우조선해양", "002380.KS": "KCC",
            "004000.KS": "롯데정밀화학", "021240.KS": "코웨이", "069620.KS": "대웅제약",
            "000100.KS": "유한양행", "185750.KS": "종근당", "006280.KS": "녹십자",
            "008930.KS": "한미약품", "249420.KS": "일동제약", "170900.KS": "동아에스티",
            "009290.KS": "광동제약", "020560.KS": "아시아나항공", "272450.KS": "진에어",
            "008770.KS": "호텔신라", "032350.KS": "롯데관광개발", "034230.KS": "파라다이스",
            "114090.KS": "GKL", "089590.KS": "제주항공", "001740.KS": "SK네트웍스",
            "001120.KS": "LG상사", "069960.KS": "현대백화점", "031430.KS": "신세계인터내셔날",
            "139480.KS": "이마트", "027410.KS": "BGF", "079160.KS": "CJ CGV",
            "071840.KS": "롯데하이마트", "088350.KS": "한화생명", "005830.KS": "DB손해보험",
            "016360.KS": "삼성증권", "071050.KS": "한국투자금융지주",

            # KOSDAQ 100개
            "091990.KQ": "셀트리온헬스케어", "247540.KQ": "에코프로비엠", "086520.KQ": "에코프로",
            "196170.KQ": "알테오젠", "066970.KQ": "엘앤에프", "278280.KQ": "천보",
            "058470.KQ": "리노공업", "140860.KQ": "파크시스템스", "214150.KQ": "클래시스",
            "145020.KQ": "휴젤", "348370.KQ": "엔켐", "001570.KQ": "금양",
            "095700.KQ": "제넥신", "277810.KQ": "레인보우로보틱스", "352820.KQ": "하이브",
            "293490.KQ": "카카오게임즈", "263750.KQ": "펄어비스", "259960.KQ": "크래프톤",
            "036570.KQ": "엔씨소프트", "112040.KQ": "위메이드", "078340.KQ": "컴투스",
            "069080.KQ": "웹젠", "251270.KQ": "넷마블", "323410.KQ": "카카오뱅크",
            "377300.KQ": "카카오페이", "336260.KQ": "두산퓨얼셀", "036490.KQ": "SK머티리얼즈",
            "361610.KQ": "SK아이이테크놀로지", "041510.KQ": "에스엠", "035900.KQ": "JYP",
            "096530.KQ": "씨젠", "086900.KQ": "메디톡스", "084990.KQ": "헬릭스미스",
            "215600.KQ": "신라젠", "064550.KQ": "바이오니아", "014570.KQ": "코오롱티슈진",
            "122870.KQ": "YG엔터테인먼트", "037270.KQ": "와이지플러스", "182360.KQ": "큐브엔터테인먼트",
            "173940.KQ": "FNC엔터테인먼트", "253450.KQ": "스튜디오드래곤", "095660.KQ": "네오위즈",
            "067000.KQ": "조이시티", "192080.KQ": "더블유게임즈", "123420.KQ": "선데이토즈",
            "052790.KQ": "액토즈소프트", "063080.KQ": "게임빌", "225570.KQ": "넥슨게임즈",
            "041620.KQ": "그라비티", "042420.KQ": "망고스틴", "067160.KQ": "아프리카TV",
            "299900.KQ": "위지윅스튜디오", "263720.KQ": "디앤씨미디어", "237820.KQ": "플레이디",
            "194480.KQ": "데브시스터즈", "136510.KQ": "마블러스", "035760.KQ": "CJ ENM",
            "206560.KQ": "덱스터", "122350.KQ": "초록뱀미디어", "240810.KQ": "원익IPS",
            "265520.KQ": "AP시스템", "067310.KQ": "하나마이크론", "036540.KQ": "SFA반도체",
            "089030.KQ": "테크윙", "074600.KQ": "원익QnC", "086390.KQ": "유니테스트",
            "053610.KQ": "프로텍", "122990.KQ": "와이솔", "060850.KQ": "큐알티",
            "213420.KQ": "덕산네오룩스", "357780.KQ": "솔브레인", "208710.KQ": "제노레이",
            "094170.KQ": "동운아나텍", "007660.KQ": "이수페타시스", "056190.KQ": "에스에프에이",
            "108320.KQ": "실리콘웍스", "347860.KQ": "알체라", "134580.KQ": "수퍼빈",
            "121800.KQ": "에이피알", "010780.KQ": "아이에스동서", "015750.KQ": "성우하이텍",
            "118990.KQ": "모트렉스", "068240.KQ": "다원시스", "272290.KQ": "이녹스첨단소재",
            "079980.KQ": "휴비스", "183300.KQ": "코미코", "104830.KQ": "원익머트리얼즈",
            "064760.KQ": "티씨케이", "034120.KQ": "SBS", "033630.KQ": "SK브로드밴드",
            "037560.KQ": "LG헬로비전", "190510.KQ": "나무가", "016740.KQ": "두올",
            "049070.KQ": "인탑스", "060590.KQ": "유니퀘스트",
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
            # 데이터 가져오기 (오늘 종가 포함)
            stock = yf.Ticker(ticker)

            # period 파라미터로 최신 데이터 가져오기
            hist = stock.history(period="2mo", interval="1d")

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
