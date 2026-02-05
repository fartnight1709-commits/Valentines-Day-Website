import streamlit as st
import json
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Valentine Invitation", page_icon="💝", layout="centered")

# --- DATA PERSISTENCE (THE TRACKER) ---
DB_FILE = "response_stats.json"

def get_stats():
    if not os.path.exists(DB_FILE):
        return {"yes": 0, "no": 0}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def update_stats(choice):
    stats = get_stats()
    stats[choice] += 1
    with open(DB_FILE, "w") as f:
        json.dump(stats, f)

# --- SESSION STATE ---
if 'clicks' not in st.session_state:
    st.session_state.clicks = 0
if 'no_count' not in st.session_state:
    st.session_state.no_count = 0
if 'yes_size' not in st.session_state:
    st.session_state.yes_size = 30 # Initial font size in pixels

# --- DANGER DEVELOPMENT CUSTOM CSS ---
# Centering logic, glossy UI, and the beating heart animation
beat_speed = max(0.2, 1.2 - (st.session_state.clicks * 0.1))
heart_scale = 1 + (st.session_state.clicks * 0.15)

st.markdown(f"""
<style>
    /* Absolute Centering */
    .stApp {{
        background-color: #F5F5DC;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    
    .centered-container {{
        text-align: center;
        max-width: 600px;
        margin: auto;
    }}

    /* Readability: High-contrast Raspberry Maroon text */
    h1, h2, h3, p, div {{
        color: #800020 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }}

    /* Glossy Pink UI for Buttons */
    .stButton > button {{
        background: linear-gradient(145deg, #ffc0cb, #ff8da1) !important;
        color: white !important;
        border-radius: 25px !important;
        border: 2px solid #ff8da1 !important;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.1), inset -2px -2px 5px rgba(255,255,255,0.4) !important;
        font-weight: bold !important;
        transition: transform 0.2s ease;
    }}

    /* Massive Clickable Heart Styling */
    button[kind="secondary"]:has(div:contains("💗")) {{
        font-size: 150px !important;
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        animation: heartbeat {beat_speed}s infinite;
        transform: scale({heart_scale});
    }}

    @keyframes heartbeat {{
        0% {{ transform: scale({heart_scale}); }}
        50% {{ transform: scale({heart_scale + 0.1}); }}
        100% {{ transform: scale({heart_scale}); }}
    }}

    /* Dynamic YES button scaling */
    .yes-btn button {{
        font-size: {st.session_state.yes_size}px !important;
        padding: 20px 40px !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- APP UI ---
st.markdown('<div class="centered-container">', unsafe_allow_html=True)

# STAGE 1: THE HEART CLICKS
if st.session_state.clicks < 10:
    st.markdown("<h1>🏹 A Special Message 🏹</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Click the heart 10 times!</h3>", unsafe_allow_html=True)
    
    # Progress Messages
    msgs = ["You can do it!", "I love you", "Keep going!", "Harder!", "Almost!", "So close!", "BEATING FAST!", "Ready?", "Now!", "BOOM!"]
    if st.session_state.clicks > 0:
        st.markdown(f"**{msgs[st.session_state.clicks-1]}**")

    # The Clickable Heart
    if st.button("💗", key="heart_btn"):
        st.session_state.clicks += 1
        st.rerun()

# STAGE 2: THE PROPOSAL
else:
    if "answered" not in st.session_state:
        st.markdown("<h1>Will you be my Valentine? 🌹</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="yes-btn">', unsafe_allow_html=True)
            if st.button("YES! 💖", key="yes_btn"):
                update_stats("yes")
                st.session_state.answered = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            if st.session_state.no_count < 14:
                if st.button("No 💔", key="no_btn"):
                    st.session_state.no_count += 1
                    st.session_state.yes_size += 15 # Increase size of YES
                    update_stats("no")
                    if st.session_state.no_count >= 10:
                        st.toast("Will a box of chocolates change your mind? 🍫")
                    st.rerun()
            else:
                st.markdown("<p><i>No is no longer an option...</i> 😉</p>", unsafe_allow_html=True)

    else:
        # THE SUCCESS SCREEN
        st.balloons()
        st.markdown("<h1>I knew you'd say yes! 🥰</h1>", unsafe_allow_html=True)
        
        # Display Stats System
        stats = get_stats()
        st.markdown("---")
        st.markdown("### 📊 Danger Production Analytics")
        st.write(f"Total 'Yes' Responses: {stats['yes']}")
        st.write(f"Total 'No' Attempts: {stats['no']}")

st.markdown('</div>', unsafe_allow_html=True)

# Footer Styling
st.markdown("""
    <div style="margin-top: 50px; opacity: 0.7;">
        <p>💘 Crafted by Danger Development made by Christian Hoy 🏹</p>
    </div>
""", unsafe_allow_html=True)
