# Global Macro Intelligence Hub

AI 기반 비판적 주식 분석 시스템

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## Features

- **Smart Screening**: 20개 주요 종목 자동 스크리닝 (거래량, RSI 기반)
- **Critical Analysis**: Claude AI의 비판적 추론 프레임워크
- **Data-Narrative Gap Analysis**: 뉴스와 실제 주가 데이터 괴리 분석
- **Reliability Score**: AI 분석 신뢰도 점수 (0-100)
- **Professional PDF Reports**: 전문가급 PDF 보고서 생성 및 이메일 전송

## Tech Stack

- **Frontend**: Streamlit
- **AI**: Claude Sonnet 4 (Anthropic)
- **Data Sources**: 
  - yfinance (주가 데이터)
  - Google News RSS (뉴스)
  - OpenDART API (한국 공시)

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/global-macro-intelligence-hub.git
cd global-macro-intelligence-hub
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set API Keys

Create a `.env` file:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
DART_API_KEY=your_dart_api_key

# Optional (for email reports)
SENDER_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@gmail.com
```

### 4. Run Application

#### Streamlit Web App (Recommended)
```bash
streamlit run streamlit_app.py
```

#### CLI Mode
```bash
# Stock screening
python screener.py

# Individual stock analysis
python main.py --ticker 005930.KS
```

## API Keys Setup

### 1. Anthropic API (Required)
- Sign up at [console.anthropic.com](https://console.anthropic.com/)
- Get API key from dashboard
- Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

### 2. DART API (Required for Korean stocks)
- Sign up at [opendart.fss.or.kr](https://opendart.fss.or.kr/)
- Request API key
- Add to `.env`: `DART_API_KEY=your_key`

### 3. Email (Optional)
For Gmail:
1. Enable 2-factor authentication
2. Generate app password: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Add to `.env`

## Deployment to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Set secrets in Streamlit Cloud dashboard (same as .env format)
5. Deploy!

## Usage

### Web Interface

1. **Screening**: Click "스크리닝 실행" to find noteworthy stocks
2. **Analysis**: Select a stock and click "분석 시작"
3. **Report**: View analysis and download PDF report
4. **Email**: Send professional PDF report to email

### CLI

```bash
# Screen stocks
python screener.py

# Analyze specific stock
python main.py --ticker 005930.KS

# Full workflow
python example_workflow.py
```

## Project Structure

```
├── streamlit_app.py        # Main web application
├── screener.py             # Stock screening module
├── data_collector.py       # Data collection (stock, news, disclosures)
├── critical_analyzer.py    # AI critical analysis
├── report_manager.py       # PDF report generation
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
└── .env                    # API keys (not in git)
```

## Critical Analysis Framework

Our AI applies three key principles:

1. **Data-Narrative Discrepancy**: Identifies gaps between news narratives and actual stock movements
2. **Disclosure Credibility Check**: Validates corporate disclosures against historical performance
3. **Confirmation Bias Elimination**: Balances bullish and bearish cases (5:5 ratio)

## Reliability Score

Every analysis includes a reliability score (0-100):

- **80-100**: High reliability
- **60-79**: Moderate reliability
- **40-59**: Low reliability - additional data needed
- **0-39**: Very low reliability - significant data gaps

## Disclaimer

This tool provides information for educational purposes only. It is NOT investment advice.

- AI can hallucinate or make errors
- Past performance does not guarantee future results
- Always conduct additional due diligence
- Consult with financial professionals before investing

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Support

For questions or issues, please open a GitHub issue.

---

**Powered by Claude Sonnet 4 | Built with Streamlit**
