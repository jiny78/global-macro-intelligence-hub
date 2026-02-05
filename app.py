"""
Global Macro Intelligence Hub - Streamlit App
실시간 이상 징후 종목 + 온디맨드 비판적 분석
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import time
import plotly.graph_objects as go

from screener import StockScreener
from data_collector import DataCollector
from main import IntelligenceHub
from report_manager import ExpertReportManager

# 페이지 설정
st.set_page_config(
    page_title="Global Macro Intelligence Hub",
    page_icon="[TARGET]",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .anomaly-card {
        background: linear-gradient(135deg, #ff6b6b22 0%, #ee5a6f22 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff6b6b;
        margin: 0.5rem 0;
    }
    .analysis-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        font-weight: bold;
    }
    .metric-positive {
        color: #27ae60;
        font-weight: bold;
    }
    .metric-negative {
        color: #e74c3c;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def load_watchlist():
    """watchlist.json 로드"""
    watchlist_path = os.path.join(os.path.dirname(__file__), 'watchlist.json')

    if os.path.exists(watchlist_path):
        with open(watchlist_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def run_screener():
    """스크리너 실행"""
    screener = StockScreener()
    watchlist = screener.screen_stocks()

    if watchlist:
        screener.save_to_json(watchlist, filename='watchlist.json')

    return watchlist


def create_stock_mini_chart(ticker: str):
    """미니 주가 차트 생성"""
    try:
        import yfinance as yf
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")

        if len(hist) == 0:
            return None

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=hist.index,
            y=hist['Close'],
            mode='lines',
            line=dict(color='#667eea', width=2),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))

        fig.update_layout(
            height=150,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=True, gridcolor='#e0e0e0'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )

        return fig
    except:
        return None


def analyze_stock(ticker: str, company_name: str):
    """종목 비판적 분석 실행"""

    # 1단계: 데이터 수집
    st.markdown("### [DATA] 1단계: 데이터 수집")
    progress_bar = st.progress(0)
    status = st.empty()

    status.info("[SEARCH] 주가, 뉴스, 공시 데이터를 수집하고 있습니다...")

    try:
        collector = DataCollector()
        data_result = collector.collect_all_data(ticker)

        progress_bar.progress(33)
        status.success("[OK] 데이터 수집 완료")

        # 수집 결과 요약
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("주가 데이터", f"{len(data_result['stock_data'].get('data', []))}일")
        with col2:
            st.metric("뉴스", f"{len(data_result['news'])}건")
        with col3:
            st.metric("공시", f"{len(data_result['disclosures'])}건")

        time.sleep(1)

        # 2단계: AI 비판적 분석
        st.markdown("### [AI] 2단계: AI 비판적 분석")
        status.info("[AI] AI 분석관이 공시와 뉴스를 대조 중입니다...")
        progress_bar.progress(66)

        hub = IntelligenceHub()

        # 최신 데이터 파일 찾기
        import glob
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        json_files = glob.glob(os.path.join(data_dir, f"data_{ticker.replace('.', '_')}*.json"))

        if json_files:
            latest_file = max(json_files, key=os.path.getmtime)
            analysis_result = hub.analyze_with_reliability(latest_file)

            progress_bar.progress(100)
            status.success("[OK] 비판적 분석 완료!")

            time.sleep(0.5)
            progress_bar.empty()
            status.empty()

            return {
                'data': data_result,
                'analysis': analysis_result
            }
        else:
            st.error("[ERROR] 데이터 파일을 찾을 수 없습니다.")
            return None

    except Exception as e:
        status.error(f"[ERROR] 분석 중 오류 발생: {str(e)}")
        st.exception(e)
        return None


def display_analysis_result(result, ticker, company_name):
    """분석 결과 표시"""

    st.markdown("---")
    st.markdown(f"## [CHART] {company_name} ({ticker}) - 비판적 분석 보고서")

    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["[DATA] 주요 지표", "[LIST] AI 분석 보고서", "[FILE] 상세 데이터"])

    with tab1:
        # 주가 데이터
        stock_data = result['data']['stock_data']

        if 'data' in stock_data and stock_data['data']:
            data_list = stock_data['data']

            # 메트릭 카드
            col1, col2, col3, col4 = st.columns(4)

            first_close = data_list[0]['close']
            last_close = data_list[-1]['close']
            change = last_close - first_close
            change_pct = (change / first_close) * 100

            with col1:
                st.metric("현재가", f"{last_close:,.0f}원")

            with col2:
                st.metric("7일 변동", f"{change:+,.0f}원", f"{change_pct:+.2f}%")

            with col3:
                high = max([d['high'] for d in data_list])
                st.metric("7일 최고", f"{high:,.0f}원")

            with col4:
                low = min([d['low'] for d in data_list])
                st.metric("7일 최저", f"{low:,.0f}원")

            # 간단한 차트
            st.markdown("#### [CHART] 주가 추이 (7일)")

            dates = [d['date'] for d in data_list]
            closes = [d['close'] for d in data_list]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=closes,
                mode='lines+markers',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))

            fig.update_layout(
                height=300,
                xaxis_title="날짜",
                yaxis_title="주가 (원)",
                template="plotly_white"
            )

            st.plotly_chart(fig, use_container_width=True)

        # 뉴스
        st.markdown("#### [NEWS] 주요 뉴스")
        news_list = result['data'].get('news', [])

        if news_list and 'error' not in news_list[0]:
            for news in news_list[:3]:
                with st.expander(f"[{news.get('source', 'N/A')}] {news.get('title', 'N/A')}"):
                    st.write(news.get('description', 'N/A'))
                    st.caption(f"[DATE] {news.get('published', 'N/A')}")
        else:
            st.info("뉴스 데이터가 없습니다.")

        # 공시
        st.markdown("#### [LIST] 주요 공시")
        disclosures = result['data'].get('disclosures', [])

        if disclosures and 'error' not in disclosures[0]:
            for disc in disclosures[:3]:
                with st.expander(f"{disc.get('report_name', 'N/A')} - {disc.get('submitted_date', 'N/A')}"):
                    st.write(f"**회사:** {disc.get('company', 'N/A')}")
                    if disc.get('url') != 'N/A':
                        st.markdown(f"[[LINK] 공시 보기]({disc.get('url')})")
        else:
            st.info("공시 데이터가 없습니다.")

    with tab2:
        # AI 분석 보고서
        analysis_text = result['analysis']['analysis']
        st.markdown(analysis_text)

        # 보고서 저장 및 전송 옵션
        st.markdown("---")
        st.markdown("### [EXPORT] 리포트 내보내기")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("[SAVE] 보고서 다운로드 (Markdown)", key="download_report", use_container_width=True):
                hub = IntelligenceHub()
                report_path = hub.save_report(result['analysis'], ticker)
                st.success(f"[OK] 보고서가 저장되었습니다: {report_path}")

        with col2:
            if st.button("[EMAIL] PDF 리포트 메일로 받기", key="email_pdf_simple", use_container_width=True):
                st.info("[TIP] 기본 PDF 리포트가 전송됩니다. 전문가급 리포트는 오른쪽 버튼을 사용하세요.")

        with col3:
            if st.button("[TARGET] 전문가급 PDF 리포트 생성 및 전송", key="expert_pdf", type="primary", use_container_width=True):
                st.markdown("---")
                st.markdown("### [START] 전문가급 리포트 생성 중")

                # 상태 메시지를 위한 placeholder
                status_placeholder = st.empty()
                progress_bar = st.progress(0)

                # 상태 업데이트를 위한 단계
                stages = [
                    "[DOC] PDF 문서 초기화 중...",
                    "[EDIT] 표지 생성 중...",
                    "[DATA] 섹션 1: 데이터 팩트 체크 작성 중...",
                    "[CHART] 차트 이미지 생성 중...",
                    "[AI] 섹션 2: AI 비판적 분석 작성 중...",
                    "[CHART] 섹션 3: 기술적 지표 요약 작성 중...",
                    "[WARN] 섹션 4: AI 자기 비판 작성 중...",
                    "[SAVE] PDF 파일 저장 중...",
                    "[OK] PDF 생성 완료!",
                    "[EMAIL] 이메일 설정 확인 중...",
                    "[EMAIL] 이메일 메시지 작성 중...",
                    "[ATTACH] PDF 파일 첨부 중...",
                    "[EXPORT] 이메일 전송 중...",
                    "[OK] 이메일 전송 완료!"
                ]

                current_stage = [0]  # 리스트로 만들어 내부 함수에서 수정 가능하게

                def status_callback(message: str):
                    """상태 업데이트 콜백"""
                    status_placeholder.info(f"[REFRESH] {message}")

                    # 진행률 계산
                    for i, stage in enumerate(stages):
                        if stage in message or message in stage:
                            progress = (i + 1) / len(stages)
                            progress_bar.progress(progress)
                            current_stage[0] = i
                            break

                try:
                    report_manager = ExpertReportManager()

                    # 주가 차트 생성
                    stock_data_list = result['data']['stock_data'].get('data', [])
                    chart_fig = None

                    if stock_data_list:
                        dates = [d['date'] for d in stock_data_list]
                        closes = [d['close'] for d in stock_data_list]

                        chart_fig = go.Figure()
                        chart_fig.add_trace(go.Scatter(
                            x=dates,
                            y=closes,
                            mode='lines+markers',
                            line=dict(color='#667eea', width=3),
                            marker=dict(size=8),
                            name='주가'
                        ))

                        chart_fig.update_layout(
                            title=f"{company_name} 주가 추이",
                            xaxis_title="날짜",
                            yaxis_title="주가 (원)",
                            template="plotly_white",
                            height=400
                        )

                    # 전문가급 PDF 생성 및 전송
                    success = report_manager.generate_and_send_expert_report(
                        ticker=ticker,
                        company_name=company_name,
                        analysis_text=analysis_text,
                        stock_data=result['data']['stock_data'],
                        chart_fig=chart_fig,
                        status_callback=status_callback
                    )

                    progress_bar.progress(1.0)

                    if success:
                        status_placeholder.success("[OK] 전문가급 PDF 리포트가 이메일로 전송되었습니다!")
                        st.balloons()

                        st.markdown("---")
                        st.markdown("### [LIST] 리포트 구성")
                        st.markdown("""
                        **전송된 PDF에는 다음이 포함되어 있습니다:**

                        1. **[DATA] 섹션 1: 데이터 기반 팩트 체크**
                           - 주가 요약 (기간, 등락률, 최고/최저)
                           - 주가 차트 이미지

                        2. **[AI] 섹션 2: AI 비판적 분석**
                           - 데이터-내러티브 괴리 분석
                           - 공시 진위 판별
                           - 강세론 vs 약세론 (5:5 균형)
                           - 종합 판단

                        3. **[CHART] 섹션 3: 기술적 지표 요약**
                           - 신뢰도 점수 및 해석

                        4. **[WARN] 섹션 4: AI 자기 비판 (Self-Criticism)**
                           - 데이터 불완전성
                           - 시점 차이 문제
                           - AI 할루시네이션 가능성
                           - 맥락 부족
                           - 감정과 편향

                        **이메일에는:**
                        - [TARGET] AI 위험 신호 점수
                        - [LIST] 핵심 요약 3줄
                        - [WARN] 투자 주의사항
                        """)

                    else:
                        status_placeholder.error("[ERROR] 이메일 전송 실패. .env 파일의 이메일 설정을 확인하세요.")
                        st.info("""
                        **Gmail 사용 시 설정 방법:**
                        1. Google 계정 > 보안 > 2단계 인증 활성화
                        2. 앱 비밀번호 생성: https://myaccount.google.com/apppasswords
                        3. .env 파일에 설정:
                           - SENDER_EMAIL=your-email@gmail.com
                           - APP_PASSWORD=16자리-앱-비밀번호 (공백 제거)
                           - RECIPIENT_EMAIL=받을-이메일@gmail.com
                        """)

                except Exception as e:
                    status_placeholder.error(f"[ERROR] 오류 발생: {str(e)}")
                    st.exception(e)

    with tab3:
        # JSON 데이터
        st.json(result['data'])


def main():
    """메인 함수"""

    # 헤더
    st.markdown("""
    <div class="main-header">
        <h1>[TARGET] Global Macro Intelligence Hub</h1>
        <p>실시간 이상 징후 종목 모니터링 + AI 비판적 분석</p>
    </div>
    """, unsafe_allow_html=True)

    # 사이드바
    with st.sidebar:
        st.markdown("### [SETTINGS] 설정")

        # API 키 확인
        api_keys_ok = all([
            os.getenv('DART_API_KEY'),
            os.getenv('NEWS_API_KEY'),
            os.getenv('ANTHROPIC_API_KEY')
        ])

        if api_keys_ok:
            st.success("[OK] API 키 설정 완료")
        else:
            st.error("[ERROR] API 키 확인 필요")
            st.info(".env 파일에서 API 키를 설정하세요.")

        st.markdown("---")

        # 스크리너 설정
        st.markdown("### [SEARCH] 스크리닝 조건")
        st.markdown("""
        - [OK] 거래량 2배 이상 급증
        - [OK] RSI ≤ 30 (과매도)
        - [OK] RSI ≥ 70 (과매수)
        """)

        st.markdown("---")

        # 사용 가이드
        st.markdown("### [GUIDE] 사용 가이드")
        st.markdown("""
        1. "[REFRESH] 스크리닝 실행" 클릭
        2. 이상 징후 종목 확인
        3. 관심 종목 선택
        4. "분석 시작" 클릭
        5. AI 보고서 확인
        """)

        st.markdown("---")

        # 정보
        with st.expander("[INFO] 비용 정보"):
            st.markdown("""
            **무료:**
            - 스크리닝 (수치 계산만)
            - 종목 리스트 확인

            **유료 (Claude API):**
            - 비판적 분석 보고서
            - 버튼 클릭 시에만 호출
            """)

    # 메인 영역
    st.markdown("## [ALERT] 실시간 이상 징후 종목")

    # 스크리닝 버튼
    col1, col2 = st.columns([3, 1])

    with col1:
        st.info("[TIP] 스크리닝을 실행하여 주목할 만한 종목을 찾아보세요. (Claude API 호출 없음, 무료)")

    with col2:
        run_button = st.button("[REFRESH] 스크리닝 실행", type="primary", use_container_width=True)

    # 스크리닝 실행
    if run_button:
        with st.spinner("[SEARCH] 20개 종목 분석 중... (약 30초 소요)"):
            watchlist = run_screener()

            if watchlist:
                st.session_state.watchlist = watchlist
                st.session_state.watchlist_time = datetime.now()
                st.success(f"[OK] 스크리닝 완료! {len(watchlist)}개 종목 발견")
                st.rerun()
            else:
                st.warning("[WARN] 현재 이상 징후를 보이는 종목이 없습니다.")

    # 기존 watchlist 로드
    if 'watchlist' not in st.session_state:
        watchlist_data = load_watchlist()
        if watchlist_data:
            st.session_state.watchlist = watchlist_data.get('stocks', [])
            st.session_state.watchlist_time = datetime.fromisoformat(watchlist_data['generated_at'])

    # watchlist 표시
    if 'watchlist' in st.session_state and st.session_state.watchlist:
        watchlist = st.session_state.watchlist

        # 업데이트 시간
        if 'watchlist_time' in st.session_state:
            update_time = st.session_state.watchlist_time.strftime('%Y-%m-%d %H:%M:%S')
            st.caption(f"[DATE] 마지막 스크리닝: {update_time}")

        st.markdown("")

        # 종목 카드 형식으로 표시
        for stock in watchlist:
            # 컨테이너로 각 종목 묶기
            with st.container():
                col_main, col_chart, col_button = st.columns([2, 2, 1])

                with col_main:
                    # 종목 정보
                    price_color = "metric-positive" if stock['price']['change_pct'] >= 0 else "metric-negative"

                    st.markdown(f"""
                    <div class="anomaly-card">
                        <h3 style='margin: 0; color: #2c3e50;'>
                            {stock['company_name']}
                            <span style='color: #7f8c8d; font-size: 0.8em;'>({stock['ticker']})</span>
                        </h3>
                        <p style='margin: 0.5rem 0; font-size: 1.2em;'>
                            <strong>{stock['price']['current']:,.0f}원</strong>
                            <span class='{price_color}'>
                                {stock['price']['change_pct']:+.2f}%
                            </span>
                        </p>
                        <p style='margin: 0; color: #e74c3c; font-weight: bold;'>
                            [ALERT] {' | '.join(stock['reasons'])}
                        </p>
                        <p style='margin: 0.3rem 0 0 0; color: #7f8c8d; font-size: 0.85em;'>
                            거래량: {stock['volume']['current']:,}
                            (평균 대비 <strong>{stock['volume']['ratio']:.2f}배</strong>)
                            | RSI: <strong>{stock['indicators']['rsi']:.1f}</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                with col_chart:
                    # 미니 차트
                    chart = create_stock_mini_chart(stock['ticker'])
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)

                with col_button:
                    st.markdown("<br>", unsafe_allow_html=True)  # 정렬용 여백
                    if st.button(
                        "[AI] 클로드 비판 분석 시작",
                        key=f"analyze_{stock['ticker']}",
                        use_container_width=True,
                        type="primary"
                    ):
                        st.session_state.selected_stock = stock
                        st.session_state.show_analysis = True
                        st.rerun()

                st.markdown("")  # 종목 간 간격

    else:
        st.info("[LIST] 스크리닝을 실행하여 이상 징후 종목을 확인하세요.")

    # 분석 결과 표시
    if 'show_analysis' in st.session_state and st.session_state.show_analysis:
        stock = st.session_state.selected_stock

        st.markdown("---")
        st.markdown("---")

        # 분석 컨테이너
        st.markdown(f"""
        <div class="analysis-container">
            <h2>[AI] AI 비판적 분석 진행 중</h2>
            <h3>{stock['company_name']} ({stock['ticker']})</h3>
        </div>
        """, unsafe_allow_html=True)

        # 분석 실행
        result = analyze_stock(stock['ticker'], stock['company_name'])

        if result:
            # 분석 완료 - 결과 표시
            st.session_state.analysis_result = result
            st.session_state.show_analysis = False
            st.rerun()

    # 분석 결과가 있으면 표시
    if 'analysis_result' in st.session_state:
        stock = st.session_state.selected_stock
        result = st.session_state.analysis_result

        # 초기화 버튼
        if st.button("[BACK] 목록으로 돌아가기", key="back_to_list"):
            del st.session_state.analysis_result
            del st.session_state.selected_stock
            st.rerun()

        display_analysis_result(result, stock['ticker'], stock['company_name'])

    # 푸터
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><b>Global Macro Intelligence Hub</b></p>
        <p>비용 효율적 AI 분석 시스템 | 스크리닝 무료 + 온디맨드 분석</p>
        <p>[WARN] 본 보고서는 정보 제공 목적이며, 투자 권유가 아닙니다.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
