import streamlit as st
import json
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Valentine's Request - Christian Hoy", page_icon="💘", layout="centered")

# --- DATA PERSISTENCE ---
DB_FILE = "stats.json"

def load_stats():
    if not os.path.exists(DB_FILE):
        return {"yes": 0, "no": 0}
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {"yes": 0, "no": 0}

def save_stats(choice):
    stats = load_stats()
    stats[choice] += 1
    with open(DB_FILE, "w") as f:
        json.dump(stats, f)

# --- SESSION STATE ---
if 'clicks' not in st.session_state:
    st.session_state.clicks = 0
if 'exploded' not in st.session_state:
    st.session_state.exploded = False
if 'yes_scale' not in st.session_state:
    st.session_state.yes_scale = 1.0
if 'no_clicks_after' not in st.session_state:
    st.session_state.no_clicks_after = 0
if 'final_choice' not in st.session_state:
    st.session_state.final_choice = None

# --- CUSTOM CSS ---
# Using Raspberry (#880e4f) for text to ensure readability on Beige (#F5F5DC)
# Centering the UI using Flexbox and styling the glossy heart
st.markdown(f"""
<style>
    .stApp {{
        background-color: #F5F5DC;
    }}
    
    /* Center all content */
    .main {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }}

    /* High-Contrast Text */
    h1, h2, h3, p, span {{
        color: #880e4f !important;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
    }}

    /* The Glossy Heart Button */
    .stButton > button {{
        border-radius: 50px !important;
        transition: all 0.2s ease-in-out !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }}

    /* Heart specific styling */
    div[data-testid="stButton"] button:has(div:contains("💗")) {{
        background: transparent !important;
        border: none !important;
        font-size: 150px !important;
        animation: heartBeat {max(0.2, 1.5 - st.session_state.clicks * 0.1)}s infinite;
        transform: scale({1 + st.session_state.clicks * 0.1});
        box-shadow: none !important;
    }}

    @keyframes heartBeat {{
        0% {{ transform: scale({1 + st.session_state.clicks * 0.1}); }}
        50% {{ transform: scale({1.2 + st.session_state.clicks * 0.1}); }}
        100% {{ transform: scale({1 + st.session_state.clicks * 0.1}); }}
    }}

    /* Dynamic YES Button */
    .yes-btn > div > button {{
        background-color: #4CAF50 !important;
        color: white !important;
        transform: scale({st.session_state.yes_scale}) !important;
        z-index: 1000;
        margin: 20px;
    }}

    /* NO Button */
    .no-btn > div > button {{
        background-color: #ff4b4b !important;
        color: white !important;
        margin: 20px;
    }}

    .footer {{
        position: fixed;
        bottom: 20px;
        width: 100%;
        text-align: center;
        color: #ff8da1;
    }}
</style>
""", unsafe_allow_html=True)

# --- APP LAYOUT ---
st.markdown('<div class="main">', unsafe_allow_html=True)

if not st.session_state.exploded:
    st.markdown("<h1>A Special Message for You 🏹</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Click the heart 10 times!</h3>", unsafe_allow_html=True)
    
    # Message Logic
    progress_msgs = ["You can do it!", "I love you", "Keep going!", "Almost there!", "Don't stop!", "So close!", "POPPING!", "Ready?", "Now!", "BOOM!"]
    if st.session_state.clicks > 0:
        msg = progress_msgs[min(st.session_state.clicks-1, 9)]
        st.markdown(f"**{msg}**")

    # The Massive Clickable Heart
    if st.button("💗", key="heart_main"):
        st.session_state.clicks += 1
        if st.session_state.clicks >= 10:
            st.session_state.exploded = True
        st.rerun()

else:
    if st.session_state.final_choice is None:
        st.markdown("<h1>Will you be my Valentine? 🌹</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="yes-btn">', unsafe_allow_html=True)
            if st.button("YES! 💖", key="yes_final"):
                save_stats("yes")
                st.session_state.final_choice = "YES"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            # Hide NO button after enough clicks
            if st.session_state.no_clicks_after < 14:
                st.markdown('<div class="no-btn">', unsafe_allow_html=True)
                if st.button("No 💔", key="no_final"):
                    st.session_state.no_clicks_after += 1
                    st.session_state.yes_scale += 0.8  # Aggressive growth
                    save_stats("no")
                    if st.session_state.no_clicks_after >= 10:
                        st.toast("Will a box of chocolates change your mind? 🍫")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("<p><i>No is no longer an option...</i> 😉</p>", unsafe_allow_html=True)

    else:
        st.balloons()
        st.markdown("<h1>I knew you'd say yes! 🥰</h1>", unsafe_allow_html=True)
        st.markdown("<h3>You've made me the happiest!</h3>", unsafe_allow_html=True)
        
        # Stats Section
        stats = load_stats()
        st.divider()
        st.markdown("### 📊 Live Stats")
        st.write(f"Total 'Yes' Responses: {stats['yes']}")
        st.write(f"Total 'No' Attempts: {stats['no']}")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        🏹 Crafted by Danger Development | For Christian Hoy 💘
    </div>
""", unsafe_allow_html=True)
