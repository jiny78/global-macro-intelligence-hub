"""
Global Macro Intelligence Hub - Streamlit Web Dashboard
웹 기반 주식 데이터 수집 및 비판적 분석 대시보드
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
import glob
from pathlib import Path

from data_collector import DataCollector
from main import IntelligenceHub
from market_watch import MarketWatch

# 페이지 설정
st.set_page_config(
    page_title="Global Macro Intelligence Hub",
    page_icon="[DATA]",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================
# 비밀번호 보호 기능
# ============================================
def check_password():
    """비밀번호 확인. 맞으면 True 반환."""

    def password_entered():
        """비밀번호 입력 확인"""
        # Streamlit Secrets에서 비밀번호 가져오기 (배포 시)
        # 로컬에서는 환경변수에서 가져오기
        correct_password = os.getenv("APP_PASSWORD", "macro2026")  # 기본값: macro2026

        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    # 첫 실행이거나 비밀번호가 확인되지 않은 경우
    if "password_correct" not in st.session_state:
        st.markdown("""
        <div style='text-align: center; padding: 50px 0;'>
            <h1>[LOCK] Global Macro Intelligence Hub</h1>
            <p>이 앱은 비밀번호로 보호되어 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)

        st.text_input(
            "비밀번호를 입력하세요",
            type="password",
            on_change=password_entered,
            key="password",
            help="배포 시 Streamlit Secrets의 APP_PASSWORD 사용 / 로컬: macro2026"
        )
        return False

    elif not st.session_state["password_correct"]:
        st.markdown("""
        <div style='text-align: center; padding: 50px 0;'>
            <h1>[LOCK] Global Macro Intelligence Hub</h1>
            <p>이 앱은 비밀번호로 보호되어 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)

        st.text_input(
            "비밀번호를 입력하세요",
            type="password",
            on_change=password_entered,
            key="password",
            help="배포 시 Streamlit Secrets의 APP_PASSWORD 사용 / 로컬: macro2026"
        )
        st.error("[ERROR] 비밀번호가 틀렸습니다.")
        return False

    else:
        # 비밀번호 맞음
        return True


# 비밀번호 체크 - 틀리면 여기서 멈춤
if not check_password():
    st.stop()

# ============================================
# 여기서부터 원래 앱 코드
# ============================================

# 커스텀 CSS (모바일 반응형 포함)
st.markdown("""
<style>
    /* 기본 스타일 */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .search-box {
        text-align: center;
        margin: 2rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .recent-item {
        padding: 0.5rem;
        margin: 0.5rem 0;
        background: #f8f9fa;
        border-radius: 5px;
        cursor: pointer;
    }
    .recent-item:hover {
        background: #e9ecef;
    }

    /* ========================================
       모바일 반응형 스타일 (768px 이하)
       ======================================== */
    @media (max-width: 768px) {
        /* 메인 컨테이너 */
        .main .block-container {
            padding: 1rem 0.5rem !important;
            max-width: 100% !important;
        }

        /* 헤더 */
        .main-header {
            padding: 1rem 0.5rem !important;
            margin-bottom: 1rem !important;
        }
        .main-header h1 {
            font-size: 1.3rem !important;
        }
        .main-header p {
            font-size: 0.85rem !important;
        }

        /* 검색박스 */
        .search-box {
            margin: 1rem 0 !important;
        }

        /* 버튼 */
        .stButton>button {
            padding: 0.6rem !important;
            font-size: 0.9rem !important;
        }

        /* 메트릭 카드 */
        .metric-card {
            padding: 0.75rem !important;
            font-size: 0.85rem !important;
        }

        /* Streamlit 기본 요소 */
        .stMarkdown {
            font-size: 0.9rem !important;
        }

        /* 사이드바 */
        section[data-testid="stSidebar"] {
            width: 280px !important;
        }
        section[data-testid="stSidebar"] .stMarkdown {
            font-size: 0.85rem !important;
        }

        /* 탭 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.85rem !important;
            padding: 0.5rem 0.75rem !important;
        }

        /* 차트 */
        .js-plotly-plot {
            width: 100% !important;
            height: auto !important;
        }

        /* 테이블 */
        .dataframe {
            font-size: 0.75rem !important;
        }

        /* 입력 필드 */
        .stTextInput input {
            font-size: 0.9rem !important;
        }

        /* 선택박스 */
        .stSelectbox {
            font-size: 0.9rem !important;
        }

        /* 컬럼 간격 조정 */
        [data-testid="column"] {
            padding: 0.25rem !important;
        }

        /* Expander */
        .streamlit-expanderHeader {
            font-size: 0.9rem !important;
        }

        /* 메트릭 */
        [data-testid="stMetric"] {
            font-size: 0.85rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.75rem !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 1rem !important;
        }
    }

    /* ========================================
       작은 모바일 (480px 이하)
       ======================================== */
    @media (max-width: 480px) {
        .main .block-container {
            padding: 0.5rem 0.25rem !important;
        }

        .main-header h1 {
            font-size: 1.1rem !important;
        }
        .main-header p {
            font-size: 0.75rem !important;
        }

        .stButton>button {
            padding: 0.5rem !important;
            font-size: 0.85rem !important;
        }

        section[data-testid="stSidebar"] {
            width: 240px !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 0.9rem !important;
        }
    }

    /* ========================================
       터치 최적화
       ======================================== */
    @media (hover: none) and (pointer: coarse) {
        /* 터치 디바이스용 버튼 크기 증가 */
        .stButton>button {
            min-height: 44px !important;
        }

        /* 입력 필드 크기 증가 */
        .stTextInput input,
        .stSelectbox select {
            min-height: 44px !important;
        }

        /* 클릭 영역 증가 */
        .recent-item {
            padding: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


class AnalysisHistory:
    """분석 히스토리 관리 클래스"""

    def __init__(self):
        self.history_file = os.path.join(
            os.path.dirname(__file__),
            'analysis_history.json'
        )

    def load_history(self):
        """히스토리 로드"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_history(self, history):
        """히스토리 저장"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def add_analysis(self, ticker, company_name):
        """새 분석 추가"""
        history = self.load_history()

        # 기존 항목 제거 (중복 방지)
        history = [h for h in history if h['ticker'] != ticker]

        # 새 항목 추가
        history.insert(0, {
            'ticker': ticker,
            'company_name': company_name,
            'analyzed_at': datetime.now().isoformat()
        })

        # 최대 20개까지만 유지
        history = history[:20]

        self.save_history(history)

    def get_recent(self, limit=10):
        """최근 분석 목록 가져오기"""
        history = self.load_history()
        return history[:limit]


def get_ticker_mapping():
    """종목명-티커 매핑 반환"""
    return {
        "삼성전자": "005930.KS",
        "005930.KS": "005930.KS",
        "005930": "005930.KS",
        "SK하이닉스": "000660.KS",
        "000660.KS": "000660.KS",
        "000660": "000660.KS",
        "NAVER": "035420.KS",
        "네이버": "035420.KS",
        "035420.KS": "035420.KS",
        "035420": "035420.KS",
        "LG화학": "051910.KS",
        "051910.KS": "051910.KS",
        "051910": "051910.KS",
        "현대차": "005380.KS",
        "005380.KS": "005380.KS",
        "005380": "005380.KS",
        "삼성SDI": "006400.KS",
        "006400.KS": "006400.KS",
        "006400": "006400.KS",
        "카카오": "035720.KS",
        "035720.KS": "035720.KS",
        "035720": "035720.KS",
        "삼성바이오로직스": "207940.KS",
        "207940.KS": "207940.KS",
        "207940": "207940.KS",
        "셀트리온": "068270.KS",
        "068270.KS": "068270.KS",
        "068270": "068270.KS",
        "삼성물산": "028260.KS",
        "028260.KS": "028260.KS",
        "028260": "028260.KS",
        "포스코홀딩스": "003670.KS",
        "003670.KS": "003670.KS",
        "003670": "003670.KS",
        "현대모비스": "012330.KS",
        "012330.KS": "012330.KS",
        "012330": "012330.KS",
        "기아": "000270.KS",
        "000270.KS": "000270.KS",
        "000270": "000270.KS",
        "KB금융": "105560.KS",
        "105560.KS": "105560.KS",
        "105560": "105560.KS",
        "신한지주": "055550.KS",
        "055550.KS": "055550.KS",
        "055550": "055550.KS",
        "SK텔레콤": "017670.KS",
        "017670.KS": "017670.KS",
        "017670": "017670.KS",
        "SK이노베이션": "096770.KS",
        "096770.KS": "096770.KS",
        "096770": "096770.KS",
        "두산에너빌리티": "034020.KS",
        "034020.KS": "034020.KS",
        "034020": "034020.KS",
        "삼성전기": "009150.KS",
        "009150.KS": "009150.KS",
        "009150": "009150.KS",
        "삼성에스디에스": "018260.KS",
        "018260.KS": "018260.KS",
        "018260": "018260.KS",
    }


def resolve_ticker(input_text):
    """입력값을 티커로 변환 (티커 형식이면 그대로 허용)"""
    input_text = input_text.strip()

    # 먼저 매핑 테이블에서 찾기
    ticker_map = get_ticker_mapping()
    if input_text in ticker_map:
        return ticker_map[input_text]

    # 티커 형식 (6자리.KS 또는 6자리.KQ)이면 그대로 허용
    import re
    if re.match(r'^\d{6}\.(KS|KQ)$', input_text):
        return input_text

    # 6자리 숫자만 입력한 경우 .KS 추가
    if re.match(r'^\d{6}$', input_text):
        return f"{input_text}.KS"

    return None


def create_stock_chart(stock_data):
    """주가 인터랙티브 차트 생성"""
    data_list = stock_data.get('data', [])

    if not data_list:
        st.warning("주가 데이터가 없습니다.")
        return

    # 데이터 준비
    dates = [d['date'] for d in data_list]
    opens = [d['open'] for d in data_list]
    highs = [d['high'] for d in data_list]
    lows = [d['low'] for d in data_list]
    closes = [d['close'] for d in data_list]
    volumes = [d['volume'] for d in data_list]

    # 캔들스틱 차트 생성
    fig = go.Figure()

    # 캔들스틱
    fig.add_trace(go.Candlestick(
        x=dates,
        open=opens,
        high=highs,
        low=lows,
        close=closes,
        name='주가',
        increasing_line_color='#26a69a',
        decreasing_line_color='#ef5350'
    ))

    # 레이아웃 설정
    fig.update_layout(
        title={
            'text': f"<b>{stock_data.get('company_name', 'N/A')} 주가 추이</b>",
            'font': {'size': 24, 'color': '#2c3e50'}
        },
        xaxis_title="날짜",
        yaxis_title="주가 (원)",
        template="plotly_white",
        height=500,
        hovermode='x unified',
        xaxis=dict(
            rangeslider=dict(visible=False),
            type='category'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # 거래량 차트
    fig_volume = go.Figure()

    fig_volume.add_trace(go.Bar(
        x=dates,
        y=volumes,
        name='거래량',
        marker_color='rgba(102, 126, 234, 0.6)'
    ))

    fig_volume.update_layout(
        title="<b>거래량</b>",
        xaxis_title="날짜",
        yaxis_title="거래량",
        template="plotly_white",
        height=250,
        showlegend=False
    )

    st.plotly_chart(fig_volume, use_container_width=True)

    # 주가 통계
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("시가", f"{opens[0]:,.0f}원")

    with col2:
        change = closes[-1] - closes[0]
        change_pct = (change / closes[0]) * 100
        st.metric(
            "종가",
            f"{closes[-1]:,.0f}원",
            f"{change:+,.0f}원 ({change_pct:+.2f}%)"
        )

    with col3:
        st.metric("최고가", f"{max(highs):,.0f}원")

    with col4:
        st.metric("최저가", f"{min(lows):,.0f}원")


def display_analysis_result(report_path):
    """분석 결과 표시"""
    if not os.path.exists(report_path):
        st.error("보고서 파일을 찾을 수 없습니다.")
        return

    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Markdown 렌더링
    st.markdown(content)


def main():
    """메인 함수"""

    # 히스토리 관리자 초기화
    history_manager = AnalysisHistory()

    # 헤더
    st.markdown("""
    <div class="main-header">
        <h1>[DATA] Global Macro Intelligence Hub</h1>
        <p>AI 기반 비판적 주식 분석 시스템</p>
    </div>
    """, unsafe_allow_html=True)

    # 사이드바
    with st.sidebar:
        st.markdown("### [SETTINGS] 설정")

        # API 키 확인 (Streamlit Secrets 또는 환경변수)
        def check_api_key(key_name):
            """Streamlit Secrets 또는 환경변수에서 API 키 확인"""
            try:
                # Streamlit Secrets 확인
                if key_name in st.secrets:
                    return bool(st.secrets[key_name])
            except:
                pass
            # 환경변수 확인
            return bool(os.getenv(key_name))

        api_keys_ok = all([
            check_api_key('DART_API_KEY'),
            check_api_key('ANTHROPIC_API_KEY')
        ])

        if api_keys_ok:
            st.success("[OK] API 키 설정 완료")
        else:
            st.error("[ERROR] API 키 확인 필요")
            st.info("Streamlit Secrets 또는 .env 파일에서 API 키를 설정하세요.")

        st.markdown("---")

        # 최근 분석 목록
        st.markdown("### [HISTORY] 최근 분석 종목")

        recent_analyses = history_manager.get_recent(10)

        if recent_analyses:
            for item in recent_analyses:
                analyzed_date = datetime.fromisoformat(item['analyzed_at']).strftime('%Y-%m-%d %H:%M')

                if st.button(
                    f"[REFRESH] {item['company_name']} ({item['ticker']})\n[DATE] {analyzed_date}",
                    key=f"recent_{item['ticker']}_{item['analyzed_at']}",
                    use_container_width=True
                ):
                    st.session_state.ticker_input = item['ticker']
                    st.rerun()
        else:
            st.info("아직 분석한 종목이 없습니다.")

        st.markdown("---")

        # 사용 가이드
        st.markdown("### [GUIDE] 사용 가이드")
        st.markdown("""
        1. 종목명 또는 티커 입력
        2. '분석 시작' 버튼 클릭
        3. 데이터 수집 및 분석 대기
        4. 결과 확인
        """)

        st.markdown("---")

        # 지원 종목
        with st.expander("[LIST] 지원 종목 목록"):
            st.markdown("""
            - 삼성전자 (005930.KS)
            - 카카오 (035720.KS)
            - SK하이닉스 (000660.KS)
            - LG화학 (051910.KS)
            - 현대차 (005380.KS)
            - 삼성SDI (006400.KS)
            - NAVER (035420.KS)
            """)

    # Market Watch 섹션
    st.markdown("---")
    st.markdown("### [TARGET] Market Watch - 주목할 만한 종목")

    # Market Watch 캐시 (세션 상태 사용)
    if 'market_watch_data' not in st.session_state:
        st.session_state.market_watch_data = None
        st.session_state.market_watch_time = None

    col_refresh, col_auto = st.columns([3, 1])

    with col_refresh:
        if st.button("[REFRESH] 시장 분석 새로고침", use_container_width=True):
            with st.spinner("시장 분석 중... 약 30초 소요됩니다..."):
                try:
                    watch = MarketWatch()
                    watchlist = watch.get_watchlist(limit=5)
                    st.session_state.market_watch_data = watchlist
                    st.session_state.market_watch_time = datetime.now()
                    st.success("[OK] 분석 완료!")
                except Exception as e:
                    st.error(f"[ERROR] 시장 분석 실패: {str(e)}")

    # Market Watch 데이터 표시
    if st.session_state.market_watch_data:
        watchlist = st.session_state.market_watch_data

        if watchlist:
            # 업데이트 시간 표시
            if st.session_state.market_watch_time:
                update_time = st.session_state.market_watch_time.strftime('%Y-%m-%d %H:%M:%S')
                st.caption(f"[DATE] 마지막 업데이트: {update_time}")

            st.markdown("")

            # 추천 종목 카드 형식으로 표시
            for i, item in enumerate(watchlist):
                col_info, col_button = st.columns([4, 1])

                with col_info:
                    # 종목 정보
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
                                padding: 1rem; border-radius: 10px; border-left: 4px solid #667eea;'>
                        <h4 style='margin: 0; color: #2c3e50;'>
                            {i+1}. {item['company_name']}
                            <span style='color: #7f8c8d; font-size: 0.9em;'>({item['ticker']})</span>
                        </h4>
                        <p style='margin: 0.5rem 0; font-size: 1.1em;'>
                            <strong>{item['current_price']:,.0f}원</strong>
                            <span style='color: {"#e74c3c" if item["price_change_pct"] < 0 else "#27ae60"};
                                         font-weight: bold;'>
                                {item['price_change_pct']:+.2f}%
                            </span>
                        </p>
                        <p style='margin: 0; color: #34495e; font-size: 0.9em;'>
                            [TIP] {item['reason']}
                        </p>
                        <p style='margin: 0.3rem 0 0 0; color: #7f8c8d; font-size: 0.85em;'>
                            거래량: {item['volume_change_pct']:+.1f}% | 추천점수: {item['score']:.0f}/100
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                with col_button:
                    if st.button(
                        "[START] 즉시 분석",
                        key=f"analyze_watch_{item['ticker']}",
                        use_container_width=True
                    ):
                        st.session_state.ticker_input = item['ticker']
                        st.session_state.trigger_analysis = True
                        st.rerun()

                st.markdown("")

        else:
            st.info("현재 주목할 만한 종목이 없습니다. (조건: 전일 대비 +5% 또는 거래량 50% 이상 증가)")

    else:
        st.info("'[REFRESH] 시장 분석 새로고침' 버튼을 클릭하여 주목할 만한 종목을 찾아보세요.")

    # 메인 영역
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.markdown("### [SEARCH] 종목 검색")

        # 검색창
        ticker_input = st.text_input(
            "",
            placeholder="종목명 또는 티커를 입력하세요 (예: 삼성전자, 005930.KS)",
            key="ticker_input",
            label_visibility="collapsed"
        )

        # 분석 버튼
        analyze_button = st.button(
            "[START] 분석 시작",
            type="primary",
            use_container_width=True
        )

    # 분석 트리거 확인 (버튼 또는 Market Watch에서 트리거)
    trigger_analysis = st.session_state.get('trigger_analysis', False)

    if trigger_analysis:
        # 트리거 플래그 리셋
        st.session_state.trigger_analysis = False

    # 분석 실행
    if (analyze_button and ticker_input) or trigger_analysis:
        ticker = resolve_ticker(ticker_input)

        if not ticker:
            st.error(f"[ERROR] '{ticker_input}'는 지원하지 않는 종목입니다. 지원 종목 목록을 확인하세요.")
        else:
            # 진행 상태 표시
            progress_container = st.container()

            with progress_container:
                st.markdown("---")
                st.markdown(f"### [DATA] {ticker} 분석 중...")

                progress_bar = st.progress(0)
                status_text = st.empty()

                try:
                    # 1. 데이터 수집
                    status_text.text("1/3 데이터 수집 중...")
                    progress_bar.progress(33)

                    collector = DataCollector()
                    data_result = collector.collect_all_data(ticker)

                    company_name = data_result['stock_data'].get('company_name', ticker)

                    # 2. 분석
                    status_text.text("2/3 비판적 분석 중...")
                    progress_bar.progress(66)

                    hub = IntelligenceHub()

                    # 최신 데이터 파일 찾기
                    data_dir = os.path.join(os.path.dirname(__file__), 'data')
                    json_files = glob.glob(os.path.join(data_dir, f"data_{ticker.replace('.', '_')}*.json"))

                    if json_files:
                        latest_file = max(json_files, key=os.path.getmtime)
                        analysis_result = hub.analyze_with_reliability(latest_file)

                        # 3. 보고서 저장
                        status_text.text("3/3 보고서 생성 중...")
                        progress_bar.progress(100)

                        report_path = hub.save_report(analysis_result, ticker)

                        # 히스토리 추가
                        history_manager.add_analysis(ticker, company_name)

                        # 완료
                        status_text.success("[OK] 분석 완료!")

                        # 세션에 저장
                        st.session_state.latest_analysis = {
                            'report_path': report_path,
                            'data_result': data_result,
                            'ticker': ticker,
                            'company_name': company_name
                        }

                        st.rerun()

                except Exception as e:
                    status_text.error(f"[ERROR] 오류 발생: {str(e)}")
                    st.exception(e)

    # 결과 표시
    if 'latest_analysis' in st.session_state:
        analysis = st.session_state.latest_analysis

        st.markdown("---")

        # 헤더
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"## [CHART] {analysis['company_name']} ({analysis['ticker']})")
        with col2:
            if st.button("[REFRESH] 새로운 분석", use_container_width=True):
                del st.session_state.latest_analysis
                st.rerun()

        # 탭으로 구성
        tab1, tab2, tab3 = st.tabs(["[DATA] 주가 차트", "[LIST] 분석 보고서", "[FILE] 원본 데이터"])

        with tab1:
            st.markdown("### 주가 추이")
            create_stock_chart(analysis['data_result']['stock_data'])

            # 뉴스 요약
            st.markdown("### [NEWS] 주요 뉴스")
            news_list = analysis['data_result'].get('news', [])

            if news_list and 'error' not in news_list[0]:
                for i, news in enumerate(news_list[:5], 1):
                    with st.expander(f"[{news.get('source', 'N/A')}] {news.get('title', 'N/A')}"):
                        st.write(news.get('description', 'N/A'))
                        st.caption(f"[DATE] {news.get('published', 'N/A')}")
                        if news.get('link') != 'N/A':
                            st.markdown(f"[[LINK] 기사 보기]({news.get('link')})")
            else:
                st.info("뉴스 데이터가 없습니다.")

            # 공시 요약
            st.markdown("### [LIST] 주요 공시")
            disclosures = analysis['data_result'].get('disclosures', [])

            if disclosures and 'error' not in disclosures[0]:
                for i, disc in enumerate(disclosures[:5], 1):
                    with st.expander(f"{disc.get('report_name', 'N/A')} ({disc.get('submitted_date', 'N/A')})"):
                        st.write(f"**회사:** {disc.get('company', 'N/A')}")
                        if disc.get('url') != 'N/A':
                            st.markdown(f"[[LINK] 공시 보기]({disc.get('url')})")
            else:
                st.info("공시 데이터가 없습니다.")

        with tab2:
            display_analysis_result(analysis['report_path'])

        with tab3:
            st.json(analysis['data_result'])

    # 푸터
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><b>Global Macro Intelligence Hub</b></p>
        <p>Powered by Claude Sonnet 4 | yfinance | News API | OpenDART</p>
        <p>[WARN] 본 보고서는 정보 제공 목적이며, 투자 권유가 아닙니다.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
