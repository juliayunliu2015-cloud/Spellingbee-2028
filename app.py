import streamlit as st
import pandas as pd
import sqlite3
import os
import random
import io
from datetime import date
from gtts import gTTS

# --- CONFIGURATION & PAGE SETUP ---
st.set_page_config(page_title="Spelling Bee 2026", page_icon="🏆", layout="centered")

# --- LIGHT PURPLE THEME CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f5f0ff 0%, #ede9f6 50%, #f5f0ff 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #6b21a8 !important;
        font-weight: 700 !important;
        text-shadow: none;
    }
    
    /* Text */
    p, label, .stMarkdown {
        color: #5b21a8 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(233, 213, 255, 0.6);
        border-radius: 15px;
        padding: 10px;
        border: 2px solid rgba(168, 85, 247, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 10px;
        color: #7c3aed;
        font-weight: 900;
        font-size: 18px;
        border: 1px solid rgba(168, 85, 247, 0.2);
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #a855f7 0%, #d946ef 100%);
        color: white !important;
        border: 1px solid #a855f7;
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);
    }
    
    /* Input Fields */
    .stTextInput input {
        background-color: white !important;
        border: 2px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 12px !important;
        color: #5b21a8 !important;
        font-size: 18px !important;
        padding: 12px !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus {
        border-color: #a855f7 !important;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.2) !important;
    }
    
    /* Buttons */
    .stButton button {
        color: #ffffff !important;
        border: 1px solid #6d28d9 !important;
        border-radius: 12px !important;
        padding: 14px 35px !important;
        font-weight: 900 !important;
        font-size: 17px !important;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        letter-spacing: 0.5px;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.5);
        background: linear-gradient(135deg, #6d28d9 0%, #7c3aed 100%) !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: white !important;
        border: 2px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 12px !important;
        color: #5b21a8 !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #a855f7 0%, #d946ef 50%, #fbbf24 100%);
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(168, 85, 247, 0.2);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background-color: rgba(34, 197, 94, 0.1) !important;
        border: 2px solid #22c55e !important;
        border-radius: 12px !important;
        color: #15803d !important;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1) !important;
        border: 2px solid #ef4444 !important;
        border-radius: 12px !important;
        color: #dc2626 !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        background-color: white !important;
        border-radius: 12px !important;
        border: 2px solid rgba(168, 85, 247, 0.2) !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(168, 85, 247, 0.2) !important;
        margin: 30px 0 !important;
    }
    
    /* Cards/Containers */
    .element-container {
        background-color: rgba(233, 213, 255, 0.2);
        border-radius: 12px;
        padding: 8px;
    }
    
    /* Gold Heading */
    .gold-heading {
        color: #ffffff !important;
        margin: 0;
        font-family: 'Poppins', sans-serif;
        text-align: left;
        font-size: 2.5rem;
        font-weight: 800;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6), 0 0 4px rgba(0, 0, 0, 0.9) !important;
    }
    
    /* Gold Subtitle */
    .gold-subtitle {
        color: #ffffff !important;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 15px 0 0 0;
        text-align: left;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6), 0 0 4px rgba(0, 0, 0, 0.9) !important;
    }
    
    /* Listen Button Text */
    .listen-text {
        color: #ffffff !important;
        font-weight: 900 !important;
    }
    
    /* Remove font-size constraint */
    .st-emotion-cache-15okssx {
        font-size: inherit !important;
    }
    
    /* Reduce spacing */
    .stMetric {
        padding: 5px 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENCOURAGEMENT HEADER ---
st.markdown("""
    <div style="
        background-image: url(https://lh3.googleusercontent.com/aida-public/AB6AXuCr7AYPvVeqUPBshUWTIWJ2iXIQ-8K8woQJVGZzn3gXZOsD91x8eOwU5k1T9eDH0b8uekjykG9rQWN9kNidIOCSsd7p06J8IQ-11QKISWUKktStRsvX6OMpfJvCsTRYpo0Od6Lo3PzYt_R-4ub7Qf8h2gF39R8zVmMyA__pbMkAN2-H2q9T7SHEMfm5ULKJ1bkUS8YXaE2PlMU-5ep8QL2i4x-7ScztKYKjlG8ZguBjXW60PcBOj9SX88vAxsPyEuuZpbcOYlkE3Uc);
        background-size: cover;
        background-position: center 15%;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        border: 3px solid rgba(168, 85, 247, 0.3);
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.15);
    ">
        <h1 class="gold-heading">
            GO FOR THE GOLD, VIVIAN! ✨
        </h1>
        <p class="gold-subtitle">
            "Every word you master today is a step closer to the 2026 Trophy! 🏆✨"
        </p>
    </div>
""", unsafe_allow_html=True)

DB_PATH = "scores.db"
DATA_FILE = "2017-18 Junior Spelling Study Guide.xlsx"
DAILY_EXAM_GOAL = 33

# --- DATABASE FUNCTIONS ---
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            word TEXT NOT NULL,
            correctly_spelled INTEGER NOT NULL,
            attempts INTEGER NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_exam_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            correct_count INTEGER DEFAULT 0,
            total_attempted INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def load_words():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["word", "definition"])
    try:
        df = pd.read_excel(DATA_FILE)
        word_col = df.columns[0]
        def_col = df.columns[1] if len(df.columns) > 1 else None
        
        clean_rows = []
        for _, row in df.iterrows():
            if pd.isna(row[word_col]): continue
            clean_rows.append({
                "word": str(row[word_col]).strip(),
                "definition": str(row[def_col]).strip() if def_col and not pd.isna(row[def_col]) else "No definition available."
            })
        return pd.DataFrame(clean_rows).sort_values("word").reset_index(drop=True)
    except:
        return pd.DataFrame(columns=["word", "definition"])

# --- APP INITIALIZATION ---
init_db()
words_df = load_words()

# Session State Initialization
if "current_word" not in st.session_state:
    st.session_state.current_word = None
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "exam_mode" not in st.session_state:
    st.session_state.exam_mode = "All Words"

# --- UI TABS ---
tab_exam, tab_learn = st.tabs(["🎯 Daily Exam", "📖 Alphabetical Learn"])

# --- TAB 1: DAILY EXAM ---
with tab_exam:
    st.header("Daily Challenge")
    
    modes = ["All Words", "❌ Incorrect Words Only"] + list(range(1, 14))
    
    if st.session_state.exam_mode not in modes:
        st.session_state.exam_mode = "All Words"
        
    exam_group = st.selectbox(
        "Select Exam Group or Practice Mode:",
        options=modes,
        index=modes.index(st.session_state.exam_mode),
        key="exam_mode_selector"
    )

    if "word_queue" not in st.session_state or st.session_state.exam_mode != exam_group:
        st.session_state.exam_mode = exam_group
        st.session_state.word_queue = []

    if exam_group == "All Words":
        pool = words_df
    elif exam_group == "❌ Incorrect Words Only":
        conn = get_db_connection()
        bad_list = [row['word'] for row in conn.execute("SELECT DISTINCT word FROM scores WHERE correctly_spelled = 0").fetchall()]
        conn.close()
        pool = words_df[words_df['word'].isin(bad_list)]
    else:
        words_per_group = 31
        start_idx = (exam_group - 1) * words_per_group
        end_idx = start_idx + words_per_group
        pool = words_df.iloc[start_idx:end_idx]

    if not pool.empty and len(st.session_state.word_queue) == 0:
        indices = pool.index.tolist()
        random.shuffle(indices)
        st.session_state.word_queue = indices
        st.session_state.current_word = pool.loc[st.session_state.word_queue.pop(0)]
        st.session_state.attempts = 0

    if not pool.empty:
        conn = get_db_connection()
        today_date = date.today().isoformat()
        row = conn.execute("SELECT correct_count FROM daily_exam_progress WHERE date = ?", (today_date,)).fetchone()
        score_today = row[0] if row else 0
        conn.close()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Daily Progress", f"{score_today}/{DAILY_EXAM_GOAL}")
        with col2:
            st.metric("Words Left", len(st.session_state.word_queue))
        
        st.progress(min(score_today / DAILY_EXAM_GOAL, 1.0))

        word_to_spell = st.session_state.current_word["word"]
        audio_io = io.BytesIO()
        gTTS(text=str(word_to_spell), lang="en").write_to_fp(audio_io)
        
        col_audio, col_form = st.columns([1, 2])
        
        with col_audio:
            st.audio(audio_io, format="audio/mp3")
        
        with col_form:
            with st.form(key="spell_form", clear_on_submit=True):
                user_input = st.text_input("Type the word:")
                col_check, col_space = st.columns([1, 1])
                with col_check:
                    if st.form_submit_button("Check"):
                        st.session_state.attempts += 1
                        is_correct = user_input.strip().lower() == str(word_to_spell).strip().lower()
                        
                        conn = get_db_connection()
                        conn.execute("INSERT INTO scores (date, word, correctly_spelled, attempts) VALUES (?, ?, ?, ?)",
                                     (today_date, word_to_spell, int(is_correct), st.session_state.attempts))
                        
                        st.session_state.last_result = {
                            "is_correct": is_correct, "word": word_to_spell,
                            "definition": st.session_state.current_word["definition"]
                        }

                        if is_correct:
                            conn.execute("INSERT INTO daily_exam_progress (date, correct_count, total_attempted) VALUES (?, 1, 1) ON CONFLICT(date) DO UPDATE SET correct_count = correct_count + 1, total_attempted = total_attempted + 1", (today_date,))
                            if st.session_state.word_queue:
                                st.session_state.current_word = pool.loc[st.session_state.word_queue.pop(0)]
                            else:
                                st.session_state.current_word = None
                            st.session_state.attempts = 0
                        else:
                            conn.execute("INSERT INTO daily_exam_progress (date, total_attempted) VALUES (?, 1) ON CONFLICT(date) DO UPDATE SET total_attempted = total_attempted + 1", (today_date,))
                        
                        conn.commit()
                        conn.close()
                        st.rerun()

        if st.session_state.last_result:
            res = st.session_state.last_result
            if res["is_correct"]: 
                st.success("✅ Correct!")
            else:
                st.error("❌ Incorrect - Correct Spelling: " + res['word'])
                st.markdown(f"<p style='color: black; font-size: 1em; margin: 0;'>Meaning: {res['definition']}</p>", unsafe_allow_html=True)
       
            if st.button("Next Word"):
                if st.session_state.word_queue:
                    st.session_state.current_word = pool.loc[st.session_state.word_queue.pop(0)]
                    st.session_state.attempts = 0
                else:
                    st.session_state.current_word = None
                st.session_state.last_result = None
                st.rerun()
    else:
        st.info("No words found in this mode.")

# --- TAB 2: ALPHABETICAL LEARN ---
with tab_learn:
    st.header("📖 Alphabetical Study Groups")
    
    group_num = st.selectbox("Select Learning Group (1-13):", range(1, 14), key="learn_group_choice")
    
    words_per_group = 31
    start_idx = (group_num - 1) * words_per_group
    end_idx = start_idx + words_per_group
    
    current_group = words_df.iloc[start_idx:end_idx].reset_index(drop=True)
    
    st.divider()

    for idx, row in current_group.iterrows():
        col_text, col_audio = st.columns([3, 1])
        
        word_to_read = str(row['word']).replace('.0', '').strip()

        with col_text:
            st.markdown(f"### {word_to_read}")
            st.write(f"**Meaning:** {row['definition']}")
        
        with col_audio:
            if st.button(f"🔊 Listen", key=f"study_btn_{idx}"):
                audio_io_learn = io.BytesIO()
                gTTS(text=word_to_read, lang="en").write_to_fp(audio_io_learn)
                st.audio(audio_io_learn, format="audio/mp3", autoplay=True)
        
        st.divider()

