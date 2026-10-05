import streamlit as st
from PIL import Image
from engine.odds_api import OddsAPIService
from engine.ocr_scanner import ScreenshotScanner
from engine.predictor import BasketballPredictor

st.set_page_config(page_title="Basketball Prediction & Odds Machine", layout="wide", page_icon="🏀")
st.title("🏀 Basketball Odds Engine & Slip Generator (>70% Confidence)")

# --- Sidebar API Keys ---
st.sidebar.header("🔑 API Credentials")
odds_api_key = st.sidebar.text_input("The Odds API Key", value=st.secrets.get("ODDS_API_KEY", ""), type="password")
qwen_api_key = st.sidebar.text_input("Qwen API Key (for Screenshots)", value=st.secrets.get("QWEN_API_KEY", ""), type="password")
qwen_base_url = st.sidebar.text_input("Qwen Base URL (Optional)", value=st.secrets.get("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"))

tabs = st.tabs(["📊 Live Odds & Predictions", "📸 Screenshot Scanner", "🎫 Slip Accumulator"])

# ============ TAB 0: Live Odds (Simple List) ============
with tabs[0]:
    st.header("Fetch Match Odds & Generate Boundaries")
    
    if odds_api_key:
        api = OddsAPIService(odds_api_key)
        try:
            with st.spinner("Loading basketball leagues..."):
                leagues = api.get_basketball_leagues()

            if leagues:
                # Create a simple dictionary of all leagues
                league_names = {l['title']: l['key'] for l in leagues}
                selected_league = st.selectbox("Select Basketball League", list(league_names.keys()))

                if st.button("Fetch Matches & Predict", type="primary"):
                    with st.spinner(f"Fetching odds for {selected_league}..."):
                        odds_data = api.get_odds(league_names[selected_league])

                    if odds_data:
                        st.success(f"✅ Found {len(odds_data)} matches")
                        st.write("---")

                        for match in odds_data:
                            home = match['home_team']
                            away = match['away_team']

                            # Dynamic score estimation from odds
                            bookmakers = match.get('bookmakers', [])
                            home_score = 82.0
                            away_score = 78.0

                            if bookmakers:
                                first_bookmaker = bookmakers[0]
                                markets = first_bookmaker.get('markets', [])
                                for market in markets:
                                    if market.get('key') == 'h2h':
                                        outcomes = market.get('outcomes', [])
                                        for outcome in outcomes:
                                            name = outcome.get('name', '')
                                            price = outcome.get('price', 2.0)
                                            if home.lower() in name.lower():
                                                home_score = 80 + (2.5 - price) * 15
                                            elif away.lower() in name.lower():
                                                away_score = 80 + (2.5 - price) * 15

                            preds = BasketballPredictor.calculate_bounds(home_score, away_score)

                            with st.expander(f"🏀 {home} vs {away}"):
                                col1, col2, col3 = st.columns(3)
                                col1.metric("Home Team", home)
                                col1.caption(f"Est. Score: {home_score:.1f}")
                                col2.metric("Away Team", away)
                                col2.caption(f"Est. Score: {away_score:.1f}")
                                col3.metric("Expected Total", preds['expected_fulltime'])
                                st.write("**70% Confidence Bounds:**")
                                st.json(preds)
                    else:
                        st.warning("No matches found for this league.")
            else:
                st.warning("No active basketball leagues found or invalid API key.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("👉 Enter your Odds API key in the sidebar.")

# ============ TAB 1: Screenshot Scanner ============
with tabs[1]:
    st.header("📸 Upload Screenshot (.png, .jpg)")
    uploaded_file = st.file_uploader("Upload Betting App Screenshot", type=["png", "jpg", "jpeg"])

    if uploaded_file and qwen_api_key:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Screenshot", use_container_width=True)

        if st.button("Scan Screenshot with Qwen"):
            with st.spinner("Extracting match odds using Qwen Vision..."):
                scanner = ScreenshotScanner(qwen_api_key, qwen_base_url)
                result = scanner.scan_image(img)
                st.markdown("### Processed Analysis")
                st.markdown(result)
    elif uploaded_file and not qwen_api_key:
        st.warning("Please enter your Qwen API Key in the sidebar to process images.")

# ============ TAB 2: Slip Accumulator ============
with tabs[2]:
    st.header("🎫 Daily / Weekly Accumulator Generator")
    target_confidence = st.slider("Target Confidence", min_value=70, max_value=95, value=75)
    num_legs = st.number_input("Number of Legs", min_value=2, max_value=25, value=10)
    
    if st.button("Generate (>70%) Accumulator"):
        st.success(f"Generated Multi-Leg High-Probability Slip! (Confidence: {target_confidence}%, Legs: {int(num_legs)})")
        st.info("⚠️ Accumulator logic pending — integrate odds_data from Tab 0 to auto-select legs.")