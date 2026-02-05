"""
Global Macro Intelligence Hub - Data Collector
특정 티커의 주가, 뉴스, 공시 정보를 수집하는 모듈
"""

import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import os
import dart_fss as df
from typing import Dict, List, Any
import time
from dotenv import load_dotenv
import feedparser
from urllib.parse import quote

# .env 파일 로드
load_dotenv()


class DataCollector:
    """주가, 뉴스, 공시 데이터를 수집하는 클래스"""

    def __init__(self, dart_api_key: str = None):
        """
        Args:
            dart_api_key: OpenDART API 키 (환경변수 DART_API_KEY로도 설정 가능)
        """
        # .env에서 API 키 읽기
        self.dart_api_key = dart_api_key or os.getenv('DART_API_KEY')

        # DART API 설정
        self.dart_initialized = False
        if self.dart_api_key:
            try:
                # API 키 설정
                df.set_api_key(api_key=self.dart_api_key)

                # API 키 정상 작동 테스트 (corp_list 로드)
                print("   [INFO] DART API initializing...")
                corp_list = df.get_corp_list()

                if corp_list is not None:
                    self.dart_initialized = True
                    print("   [OK] DART API initialized")
                else:
                    print("   [WARN] DART API returned None")

            except Exception as e:
                print(f"   [ERROR] DART API initialization failed: {str(e)}")
                print("   [INFO] Check DART_API_KEY or network connection")
                print(f"   [INFO] API key (first 8): {self.dart_api_key[:8] if self.dart_api_key else 'None'}...")
                self.dart_initialized = False
        else:
            print("   [WARN] DART API key not configured (.env file)")

        # Google News RSS (No API key needed)
        print("   [OK] Google News RSS ready (no API key needed)")

    def get_stock_data(self, ticker: str, days: int = 7) -> Dict[str, Any]:
        """
        yfinance로 주가 데이터 수집

        Args:
            ticker: 종목 티커 (예: '005930.KS')
            days: 수집할 일수 (기본 7일)

        Returns:
            주가 데이터 딕셔너리
        """
        try:
            print(f"[INFO] {ticker} Stock data collection...")
            stock = yf.Ticker(ticker)

            # 최근 N일 데이터 가져오기
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days+5)  # 주말 포함하여 여유있게

            hist = stock.history(start=start_date, end=end_date)

            # 최근 7일 영업일 데이터만 추출
            hist = hist.tail(days)

            stock_data = {
                "ticker": ticker,
                "company_name": stock.info.get('longName', 'N/A'),
                "currency": stock.info.get('currency', 'KRW'),
                "collected_at": datetime.now().isoformat(),
                "data": []
            }

            for date, row in hist.iterrows():
                daily_data = {
                    "date": date.strftime('%Y-%m-%d'),
                    "open": float(row['Open']),
                    "high": float(row['High']),
                    "low": float(row['Low']),
                    "close": float(row['Close']),
                    "volume": int(row['Volume']),
                }
                stock_data["data"].append(daily_data)

            # 외국인 보유 비율 정보 (가능한 경우)
            if 'heldPercentInstitutions' in stock.info:
                stock_data["institutional_holders_pct"] = stock.info.get('heldPercentInstitutions', 0) * 100

            print(f"[OK] Stock data collected: {len(stock_data['data'])} days")
            return stock_data

        except Exception as e:
            print(f"[ERROR] Stock data collection failed: {str(e)}")
            return {"error": str(e), "ticker": ticker}

    def get_news_headlines(self, ticker: str, company_name: str = None, count: int = 5) -> List[Dict[str, str]]:
        """
        Google News RSS로 종목 관련 뉴스 헤드라인 수집

        Args:
            ticker: 종목 티커
            company_name: 회사명 (검색어로 사용)
            count: 가져올 뉴스 개수

        Returns:
            뉴스 헤드라인 리스트
        """
        try:
            print(f"[INFO] {ticker} News collection (Google News RSS)...")

            # 검색어 설정
            if company_name and company_name != 'N/A':
                search_query = company_name
            else:
                # 티커에서 종목 코드 추출
                stock_code = ticker.split('.')[0]
                search_query = stock_code

            # Google News RSS URL
            # hl=ko: 한국어, gl=KR: 한국, ceid=KR:ko: 한국 지역 코드
            encoded_query = quote(search_query)
            rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"

            print(f"   [INFO] Fetching from Google News RSS...")
            print(f"   [INFO] Query: {search_query}")

            # RSS 피드 파싱
            feed = feedparser.parse(rss_url)

            news_list = []

            # 피드 항목 처리
            if feed.entries:
                for entry in feed.entries[:count]:
                    # Google News RSS 항목 파싱
                    news_item = {
                        "title": entry.get('title', 'N/A'),
                        "description": entry.get('summary', 'N/A'),
                        "source": entry.get('source', {}).get('title', 'Google News') if hasattr(entry, 'source') else 'Google News',
                        "published": entry.get('published', 'N/A'),
                        "link": entry.get('link', 'N/A'),
                        "author": entry.get('author', 'N/A')
                    }
                    news_list.append(news_item)

                print(f"[OK] News collected: {len(news_list)} articles")
            else:
                print("[WARN] No news found for query")

            return news_list

        except Exception as e:
            print(f"[ERROR] News collection failed: {str(e)}")
            return [{"error": str(e)}]

    def get_dart_disclosures(self, ticker: str, days: int = 30) -> List[Dict[str, str]]:
        """
        OpenDART API로 최근 공시 정보 수집

        Args:
            ticker: 종목 티커 (예: '005930.KS')
            days: 수집할 기간 (일)

        Returns:
            공시 정보 리스트
        """
        try:
            if not self.dart_api_key:
                print("   [WARN] DART API 키가 설정되지 않았습니다.")
                print("   [INFO] .env 파일에 DART_API_KEY를 설정하세요.")
                return [{"error": "DART API key not configured"}]

            if not self.dart_initialized:
                print("   [WARN] DART API가 초기화되지 않았습니다.")
                print("   [INFO] DART API 키를 확인하거나 네트워크를 점검하세요.")
                return [{"error": "DART API initialization failed"}]

            print(f"   [INFO] {ticker} 공시 정보 수집 중...")

            # 티커에서 종목 코드 추출
            stock_code = ticker.split('.')[0]

            # 날짜 설정
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # OpenDART API 호출
            disclosures = []

            # API 엔드포인트 직접 호출
            base_url = "https://opendart.fss.or.kr/api/list.json"
            params = {
                "crtfc_key": self.dart_api_key,
                "corp_code": stock_code,
                "bgn_de": start_date.strftime('%Y%m%d'),
                "end_de": end_date.strftime('%Y%m%d'),
                "page_count": 100
            }

            response = requests.get(base_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if data.get('status') == '000':
                    items = data.get('list', [])

                    # 주요 공시 필터링
                    important_reports = [
                        '사업보고서', '반기보고서', '분기보고서',
                        '자기주식취득', '자기주식처분',
                        '주요사항보고서', '합병', '분할',
                        '유상증자', '무상증자', '전환사채',
                        '자산양수도', '영업양수도'
                    ]

                    for item in items:
                        report_name = item.get('report_nm', '')

                        # 주요 공시만 필터링
                        if any(keyword in report_name for keyword in important_reports):
                            disclosures.append({
                                "company": item.get('corp_name', 'N/A'),
                                "report_name": report_name,
                                "submitted_date": item.get('rcept_dt', 'N/A'),
                                "report_type": item.get('corp_cls', 'N/A'),
                                "url": f"http://dart.fss.or.kr/dsaf001/main.do?rcpNo={item.get('rcept_no', '')}"
                            })

                else:
                    error_msg = data.get('message', 'Unknown error')
                    print(f"   [ERROR] DART API 오류: {error_msg}")
                    print(f"   [INFO] DART API 키를 확인하거나 네트워크를 점검하세요.")
                    return [{"error": error_msg}]
            else:
                print(f"   [ERROR] DART API HTTP 오류: {response.status_code}")
                print(f"   [INFO] 네트워크 연결을 확인하거나 잠시 후 다시 시도하세요.")
                return [{"error": f"HTTP {response.status_code}"}]

            print(f"   [OK] 공시 정보 수집 완료: {len(disclosures)}건")
            return disclosures

        except requests.exceptions.RequestException as e:
            print(f"   [ERROR] 네트워크 오류: {str(e)}")
            print(f"   [INFO] 인터넷 연결을 확인하세요.")
            return [{"error": f"Network error: {str(e)}"}]
        except Exception as e:
            print(f"   [ERROR] 공시 정보 수집 실패: {str(e)}")
            print(f"   [INFO] DART API 키를 확인하거나 네트워크를 점검하세요.")
            return [{"error": str(e)}]

    def collect_all_data(self, ticker: str, output_file: str = None) -> Dict[str, Any]:
        """
        모든 데이터를 수집하고 JSON으로 저장

        Args:
            ticker: 종목 티커
            output_file: 저장할 파일명 (None이면 자동 생성)

        Returns:
            수집된 모든 데이터
        """
        print(f"\n{'='*60}")
        print(f"[START] Data collection: {ticker}")
        print(f"{'='*60}\n")

        # 1. 주가 데이터 수집
        stock_data = self.get_stock_data(ticker)
        time.sleep(1)  # API 호출 간격

        # 2. 뉴스 수집
        company_name = stock_data.get('company_name', None)
        news_data = self.get_news_headlines(ticker, company_name)
        time.sleep(2)  # 크롤링 간격

        # 3. 공시 정보 수집
        disclosure_data = self.get_dart_disclosures(ticker)

        # 전체 데이터 구성
        result = {
            "ticker": ticker,
            "collected_at": datetime.now().isoformat(),
            "stock_data": stock_data,
            "news": news_data,
            "disclosures": disclosure_data
        }

        # JSON 파일로 저장
        if output_file is None:
            # 자동 파일명 생성
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            stock_code = ticker.replace('.', '_')
            output_file = f"data_{stock_code}_{timestamp}.json"

        output_path = os.path.join(
            os.path.dirname(__file__),
            'data',
            output_file
        )

        # data 디렉토리 생성
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n{'='*60}")
        print(f"[COMPLETE] Data collection finished!")
        print(f"[SAVED] File: {output_path}")
        print(f"{'='*60}\n")

        return result


def main():
    """메인 실행 함수"""
    # 사용 예시
    ticker = "005930.KS"  # 삼성전자

    # API 키 설정 (.env 파일에서 자동으로 로드)
    dart_api_key = os.getenv('DART_API_KEY')

    # 데이터 수집기 생성 (Google News RSS는 API 키 불필요)
    collector = DataCollector(dart_api_key=dart_api_key)

    # 데이터 수집 및 저장
    result = collector.collect_all_data(ticker)

    # 결과 요약 출력
    print("\n[SUMMARY] Collection results:")
    print(f"  - 주가 데이터: {len(result['stock_data'].get('data', []))}일")
    print(f"  - 뉴스: {len(result['news'])}건")
    print(f"  - 공시: {len(result['disclosures'])}건")


if __name__ == "__main__":
    main()
