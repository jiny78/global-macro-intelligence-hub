#!/bin/bash

echo "========================================"
echo "Global Macro Intelligence Hub"
echo "Web Dashboard Starting..."
echo "========================================"
echo

cd "$(dirname "$0")"
source venv/Scripts/activate
streamlit run streamlit_app.py
