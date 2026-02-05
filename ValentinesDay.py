import streamlit as st
import json
import os

# --- ARCHITECTURAL SETUP ---
st.set_page_config(page_title="ValRequest | Christian Hoy", page_icon="💘", layout="centered")

# Data persistence for the "Yes/No" tracker
DB_FILE = "analytics.json"

def load_analytics():
    if not os.path.exists(DB_FILE):
        return {"yes_total": 0, "no_total": 0}
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {"yes_total": 0, "no_total": 0}

def track_click(type):
    stats = load_analytics()
    if type == "yes":
        stats["yes_total"] += 1
    else:
        stats["no_total"] += 1
    with open(DB_FILE, "w") as f:
        json.dump(stats, f)

# --- SESSION STATE MANAGEMENT ---
if 'clicks' not in st.session_state:
    st.session_state.clicks = 0
if 'stage' not in st.session_state:
    st.session_state.stage = "HEART" # HEART -> PROPOSAL -> SUCCESS
if 'no_count' not in st.session_state:
    st.session_state.no_count = 0
if 'yes_scale' not in st.session_state:
    st.session_state.yes_scale = 1.0

# --- CUSTOM CSS (GLOSSY UI & CENTERING) ---
# We use a custom font-family and linear gradients to match the reference images.
beat_speed = max(0.1, 1.0 - (st.session_state.clicks * 0.1))
heart_size = 100 + (st.session_state.clicks * 20)

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Inter:wght@400;700&display=swap');

    .stApp {{
        background-color: #F5F5DC;
    }}

    /* Full screen centering */
    .main-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        min-height: 80vh;
    }}

    /* Typography */
    .title-text {{
        font-family: 'Dancing Script', cursive;
        color: #800020;
        font-size: 3.5rem;
        margin-bottom: 10px;
    }}
    
    .instruction-text {{
        font-family: 'Inter', sans-serif;
        color: #800020;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }}

    /* The Massive Clickable Heart */
    .heart-btn button {{
        background: none !important;
        border: none !important;
        font-size: {heart_size}px !important;
        padding: 0 !important;
        cursor: pointer;
        animation: heart-beat {beat_speed}s infinite;
        transition: all 0.2s ease-in-out;
    }}

    @keyframes heart-beat {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.1); }}
        100% {{ transform: scale(1); }}
    }}

    /* Glossy Pink Buttons */
    .stButton > button {{
        border-radius: 50px !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 20px rgba(255, 105, 180, 0.3), inset 0 -4px 8px rgba(0,0,0,0.1) !important;
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }}

    .yes-container button {{
        background: linear-gradient(135deg, #FF69B4, #FF1493) !important;
        color: white !important;
        transform: scale({st.session_state.yes_scale}) !important;
    }}

    .no-container button {{
        background: #FFB6C1 !important;
        color: #800020 !important;
    }}

    .footer {{
        margin-top: 50px;
        color: #FF69B4;
        font-size: 0.9rem;
    }}
</style>
""", unsafe_allow_html=True)

# --- APPLICATION CORE ---
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

if st.session_state.stage == "HEART":
    st.markdown('<h1 class="title-text">A Special Message 🏹</h1>', unsafe_allow_html=True)
    st.markdown('<p class="instruction-text">Click the heart 10 times!</p>', unsafe_allow_html=True)
    
    # Message Logic
    prompts = ["You can do it!", "I love you!", "Almost there!", "Don't stop!", "Keep going!", "Beating faster!", "POPPING!", "Ready?", "Now!", "BOOM!"]
    if st.session_state.clicks > 0:
        current_msg = prompts[min(st.session_state.clicks-1, 9)]
        st.markdown(f'<p style="color: #FF1493; font-weight: bold;">{current_msg}</p>', unsafe_allow_html=True)

    # Clickable Heart
    st.markdown('<div class="heart-btn">', unsafe_allow_html=True)
    if st.button("💗", key="heart_click"):
        st.session_state.clicks += 1
        if st.session_state.clicks >= 10:
            st.session_state.stage = "PROPOSAL"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.stage == "PROPOSAL":
    st.markdown('<h1 class="title-text">Will you be my Valentine? 🌹</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="yes-container">', unsafe_allow_html=True)
        if st.button("YES! 💖", key="final_yes", use_container_width=True):
            track_click("yes")
            st.session_state.stage = "SUCCESS"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if st.session_state.no_count < 14:
            st.markdown('<div class="no-container">', unsafe_allow_html=True)
            if st.button("No 💔", key="final_no", use_container_width=True):
                st.session_state.no_count += 1
                st.session_state.yes_scale += 0.7  # Aggressive growth
                track_click("no")
                if st.session_state.no_count >= 10:
                    st.toast("Will a box of chocolates change your mind? 🍫")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="font-style: italic; color: #800020;">No is no longer an option... 😉</p>', unsafe_allow_html=True)

elif st.session_state.stage == "SUCCESS":
    st.balloons()
    st.markdown('<h1 class="title-text">I knew you\'d say yes! 🥰</h1>', unsafe_allow_html=True)
    st.markdown('<p class="instruction-text">You have made my Valentine\'s Day unforgettable.</p>', unsafe_allow_html=True)
    
    # Analytics View
    stats = load_analytics()
    st.markdown("---")
    st.markdown(f"**💖 Global 'Yes' Count:** {stats['yes_total']}")
    st.markdown(f"**💔 Global 'No' Attempts:** {stats['no_total']}")

st.markdown('<div class="footer">🏹 Crafted by Danger Development for Christian Hoy 💘</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
