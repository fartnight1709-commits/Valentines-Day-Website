import streamlit as st
import json
import os

# --- PAGE CONFIG & THEME ---
st.set_page_config(page_title="Valentine's Invitation", page_icon="💘", layout="centered")

# CSS for Glossy Pink UI, Round Buttons, and Beating Heart
CUSTOM_STYLE = """
<style>
    /* Background and Container */
    .stApp {
        background-color: #F5F5DC; /* Beige/White */
    }
    
    .main-container {
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Glossy Pink Heart Styling */
    .heart {
        background-color: #FFB6C1;
        display: inline-block;
        height: 100px;
        margin: 0 10px;
        position: relative;
        top: 0;
        transform: rotate(-45deg);
        width: 100px;
        transition: all 0.3s ease-in-out;
        box-shadow: inset -5px -5px 15px rgba(255, 255, 255, 0.4), 10px 10px 20px rgba(0,0,0,0.1);
        border-radius: 5px; /* Slight round for glossy effect */
    }
    .heart:before, .heart:after {
        content: "";
        background-color: #FFB6C1;
        border-radius: 50%;
        height: 100px;
        position: absolute;
        width: 100px;
        box-shadow: inset 5px 5px 15px rgba(255, 255, 255, 0.4);
    }
    .heart:before { top: -50px; left: 0; }
    .heart:after { left: 50px; top: 0; }

    /* Animation Logic */
    @keyframes beat {
        0% { transform: scale(1) rotate(-45deg); }
        50% { transform: scale(var(--heart-scale)) rotate(-45deg); }
        100% { transform: scale(1) rotate(-45deg); }
    }

    .beating {
        animation: beat var(--beat-speed) infinite;
    }

    /* Glossy Pink Buttons */
    .stButton>button {
        background: linear-gradient(145deg, #ffc0cb, #ff8da1);
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 10px 25px !important;
        box-shadow: 4px 4px 10px #d1d1b8, -4px -4px 10px #ffffff, inset 2px 2px 5px rgba(255,255,255,0.5);
        font-weight: bold;
    }

    .yes-button>button { background: #28a745 !important; }
    .no-button>button { background: #dc3545 !important; }
</style>
"""

# --- DATA PERSISTENCE ---
DB_FILE = "stats.json"

def load_stats():
    if not os.path.exists(DB_FILE):
        return {"yes": 0, "no": 0}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_stats(choice):
    stats = load_stats()
    stats[choice] += 1
    with open(DB_FILE, "w") as f:
        json.dump(stats, f)
    return stats

# --- SESSION STATE INITIALIZATION ---
if 'clicks' not in st.session_state:
    st.session_state.clicks = 0
if 'exploded' not in st.session_state:
    st.session_state.exploded = False
if 'no_size' not in st.session_state:
    st.session_state.no_size = 1.0
if 'yes_size' not in st.session_state:
    st.session_state.yes_size = 1.0
if 'answered' not in st.session_state:
    st.session_state.answered = False

# --- LOGIC ---
messages = [
    "Keep going!", "You can do it!", "Almost there...", 
    "I love you", "So close!", "Don't stop!", 
    "It's about to pop!", "Harder!", "Nearly!", "BOOM!"
]

# Calculate dynamic animation speeds based on clicks
beat_speed = max(0.2, 1.5 - (st.session_state.clicks * 0.13))
heart_scale = 1.0 + (st.session_state.clicks * 0.15)

st.markdown(CUSTOM_STYLE.replace("--beat-speed", f"{beat_speed}s").replace("--heart-scale", f"{heart_scale}"), unsafe_allow_html=True)

# --- UI LAYOUT ---
st.title("💘 A Special Message for You 💘")

if not st.session_state.exploded:
    st.write("### Click me 10 times!")
    
    # Render Heart
    st.markdown(f'<div style="text-align:center; padding: 100px 0;"><div class="heart beating"></div></div>', unsafe_allow_html=True)
    
    # Progress Message
    if st.session_state.clicks > 0:
        idx = min(st.session_state.clicks - 1, len(messages)-1)
        st.write(f"**{messages[idx]}**")

    if st.button("CLICK HEART 💓"):
        st.session_state.clicks += 1
        if st.session_state.clicks >= 10:
            st.session_state.exploded = True
        st.rerun()

else:
    if not st.session_state.answered:
        st.header("Will you be my Valentine? 🌹")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Yes Button gets bigger if No is clicked > 14 times
            yes_label = "YES! 💖"
            st.markdown(f'<div class="yes-button">', unsafe_allow_html=True)
            if st.button(yes_label, key="yes_btn"):
                save_stats("yes")
                st.session_state.answered = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # Logic for the No button
            if st.session_state.clicks < 24: # 10 (initial) + 14 (extra)
                no_label = "No 💔"
                if st.button(no_label, key="no_btn"):
                    st.session_state.clicks += 1
                    st.session_state.yes_size += 0.5
                    save_stats("no")
                    if st.session_state.clicks >= 24:
                        st.toast("Will a box of chocolates change your mind? 🍫")
                    st.rerun()
            else:
                st.write("No isn't an option anymore... 😉")

    else:
        st.balloons()
        st.success("Yay! I knew you'd say yes! 🥰")
        
        stats = load_stats()
        st.divider()
        st.write("### 📊 Global Responses")
        st.write(f"Total 'Yes' clicks: {stats['yes']}")
        st.write(f"Total 'No' clicks: {stats['no']}")

# --- CUPID DESIGN FOOTER ---
st.markdown("""
    <div style="text-align: center; color: #FF8DA1; margin-top: 50px;">
        <p>🏹 Crafted by Danger Development made by Christian Hoy 💘</p>
    </div>
""", unsafe_allow_html=True)
