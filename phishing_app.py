import streamlit as st 
import pandas as pd
import numpy as np
import joblib
import re
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Phishing Website Detector",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========== CSS LOADING =========
def load_css():
    """Load CSS robustly for any device and path."""
    css_path = os.path.join(os.path.dirname(__file__), "ui.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("CSS file not found! UI may look different.")
load_css()

# ==================== HEADER ====================
st.markdown(
    "<h1 style='text-align:center;'>🛡️&nbsp;&nbsp;Phishing Website Detector&nbsp;&nbsp;🛡️</h1>",
    unsafe_allow_html=True
)

# ==================== MODEL LOADING ====================
@st.cache_resource
def load_model():
    try:
        model = joblib.load("my_phishing_detector.pkl")
        return model
    except:
        return None

model = load_model()

if model is None:
    st.error("❌ Model failed to load. Try Again.")
    st.stop()

# ==================== URL INPUT ====================
st.markdown('<div class="section-header">🔍 Website Analysis</div>', unsafe_allow_html=True)

url = st.text_input(
    "**Enter Website URL**", 
    placeholder="https://example.com",
    help="Paste the full URL of the website you want to check"
)

# ==================== AUTO FEATURE DETECTION ====================
auto_features = {}
if url:
    with st.container():
        st.info("**🔍 Analyzing URL Structure**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # IP Address Check
            if re.search(r'\d+\.\d+\.\d+\.\d+', url):
                auto_features['UsingIP'] = 1
                st.error("**IP Address** ❌")
            else:
                auto_features['UsingIP'] = 0
                st.success("**Domain Name** ✅")
        
        with col2:
            # URL Length Check
            if len(url) > 75:
                auto_features['LongURL'] = 1
                st.error("**Long URL** ❌")
            else:
                auto_features['LongURL'] = 0
                st.success("**Normal URL** ✅")
        
        with col3:
            # HTTPS Check
            if url.startswith('https://'):
                auto_features['HTTPS'] = 0
                st.success("**HTTPS Secure** ✅")
            else:
                auto_features['HTTPS'] = 1
                st.error("**No HTTPS** ❌")


# ==================== MANUAL QUESTIONS ====================
st.markdown('<div class="section-header">📝 Quick Questions</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Website Behavior**")
    redirecting = st.radio("Multiple Redirects?", ["No", "Yes"], key="redirects", help="Does the site redirect through multiple URLs frequently?")
    sdomains = st.radio("Suspicious Subdomains?", ["No", "Yes"], key="subdomains",help="Is there many domains like 'login.site.verify.com'?")

with col2:
    st.markdown("**Website Reputation**")
    traffic = st.radio("Popular Website?", ["Yes", "No"], key="traffic",help="Is it well known, popular website?")
    reputation = st.radio("Trusted Source?", ["Yes", "No"], key="reputation", help="Have you heard good things about this site?")




# ==================== FEATURE PREPARATION ====================
features={}
features['UsingIP'] = auto_features.get('UsingIP', 0)
features['LongURL'] = auto_features.get('LongURL', 0)
features['Redirecting//'] = 1 if redirecting == "Yes" else 0
features['HTTPS'] = auto_features.get('HTTPS', 1)  # 1 = insecure
features['SubDomains'] = 1 if sdomains == "Yes" else 0
features['AnchorURL'] = 0
features['WebsiteTraffic'] = 0 if traffic == "Yes" else 1
features['PageRank'] = 0 if reputation == "Yes" else 1
features['GoogleIndex'] = 0


# ==================== ANALYSIS ====================
if st.button("**🚀 ANALYZE WEBSITE**", type="primary", use_container_width=True):
    with st.spinner("Analyzing website features..."):
        # Create DataFrame and predict
        web_df = pd.DataFrame([features])
        prediction = model.predict(web_df)[0]
        probability = model.predict_proba(web_df)[0]
        
        # Calculate feature counts
        suspicious_count = sum(1 for v in features.values() if v == 1)
        good_count = sum(1 for v in features.values() if v == 0)

        # Determine result
        is_phishing = (prediction == 1)
        # --- Calculate confidence ---
        # --- Use model probability directly ---
        if is_phishing:
            confidence = probability[1] * 100   # Model confidence for phishing
        else:
            confidence = probability[0] * 100   # Model confidence for legitimate


    # ==================== RESULTS DISPLAY ====================
    st.markdown("---")
    
    if is_phishing:
        st.markdown("""
        <div class="result-container phishing">
            <div class="result-icon">🚨</div>
            <div class="result-content">
                <h2>PHISHING WEBSITE DETECTED</h2>
                <p><strong>Warning:</strong> This website shows strong characteristics of phishing attacks. 
                Do not enter any personal or financial information.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-container legitimate">
            <div class="result-icon">✅</div>
            <div class="result-content">
                <h2>LEGITIMATE WEBSITE</h2>
                <p>This website appears safe based on our analysis. However, always practice good security habits online.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Confidence and feature summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Confidence (Model Prediction)", f"{confidence:.1f}%")
    
    with col2:
        st.metric("Suspicious Features", f"{suspicious_count}/9")
    
    with col3:
        st.metric("Safe Features", f"{good_count}/9")
    
    # Feature breakdown (optional - can be removed for cleaner look)
    with st.expander("📊 View Detailed Analysis"):
        for feature, value in features.items():
            status = "❌ Suspicious" if value == 1 else "✅ Safe"
            st.write(f"**{feature}:** {status}")
    st.caption("**Note: Confidence is based on the trained model's prediction, not feature count.**")
# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🛡️ Built with Random Forest Algorithm with model accuracy upto 91%</p>
    <p><small>Note: This tool provides only educational insights. Always verify website authenticity through multiple sources.</small></p>
</div>
""", unsafe_allow_html=True)