# 🏀 Basketball Odds Engine & Slip Generator

Streamlit app that fetches live basketball odds, scans betting slips via Gemini Vision, and generates >70% confidence accumulator slips.

## Features
- Live odds from The Odds API (NBA, EuroLeague, ACB, BBL, etc.)
- Betting slip OCR via Gemini 2.5 Flash Vision
- Poisson/Pace statistical boundary engine (70%+ confidence)
- Daily/Weekly accumulator slip generator

## Deployment
1. Deploy on Streamlit Cloud from this GitHub repo
2. Add secrets: `ODDS_API_KEY` and `GEMINI_API_KEY`