import os
import csv
import random
import time
from datetime import datetime
import streamlit as st
import pandas as pd
from PIL import Image
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai
from google.genai import types

import base64

# Base64 Audio SFX Helper Function
def get_audio_html(file_path: str, autoplay: bool = True) -> str:
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                audio_bytes = f.read()
            b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
            auto_attr = "autoplay" if autoplay else ""
            return f"""
                <audio {auto_attr} style="display:none;">
                    <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                </audio>
            """
    except Exception:
        pass
    return ""

def get_verdict_sfx_path(dirt_pct: float) -> str:
    if dirt_pct <= 10.0:
        return "sfx/prithviraj-laughing.mp3"
    elif dirt_pct <= 30.0:
        return "sfx/rizz-sound-effect.mp3"
    elif dirt_pct <= 50.0:
        return "sfx/ennismore-goofy-ahh-car-horn-200870.mp3"
    elif dirt_pct <= 70.0:
        return "sfx/INDIA.mp3"
    elif dirt_pct <= 90.0:
        return "sfx/johnnybacon156-fah-469417.mp3"
    else:
        return "sfx/apebble-fart-5-228245.mp3"

CSV_FILE = "shoe_leaderboard.csv"
CSV_COLUMNS = ["Timestamp", "Suspect_Name", "Dirt_Percentage", "Rank_Title", "Crime_Category", "Verdict"]

# CSV Helper Functions
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)

def append_to_csv(suspect_name, dirt_pct, rank_title, crime_category, verdict):
    init_csv()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, suspect_name, round(dirt_pct, 1), rank_title, crime_category, verdict])

def load_leaderboard():
    init_csv()
    try:
        df = pd.read_csv(CSV_FILE)
        if not df.empty:
            df["Dirt_Percentage"] = pd.to_numeric(df["Dirt_Percentage"], errors="coerce")
            df = df.sort_values(by="Dirt_Percentage", ascending=False).reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Error reading leaderboard CSV: {e}")
        return pd.DataFrame(columns=CSV_COLUMNS)

def clear_csv():
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)

# Wide layout for Cyberpunk Cockpit Terminal
st.set_page_config(
    page_title="Shoe Dirt Calculator & Bouncer 9000",
    page_icon="👟",
    layout="wide"
)

# Helper function for dynamic tier classification based on dirtiness percentage
def get_tier_info(pct: float):
    if pct <= 10.0:
        return {
            "emoji": "✨",
            "tier_title": "Freshly Spawned",
            "verdict_label": "Sterile / Zero Street Cred",
            "badge_color": "#00f2ff",
            "verdict_enum": "ENTRY_GRANTED"
        }
    elif pct <= 30.0:
        return {
            "emoji": "🙂",
            "tier_title": "Acceptable",
            "verdict_label": "Tolerated For Now",
            "badge_color": "#38bdf8",
            "verdict_enum": "ENTRY_GRANTED"
        }
    elif pct <= 50.0:
        return {
            "emoji": "😐",
            "tier_title": "Needs Attention",
            "verdict_label": "Wipe Them Or Leave",
            "badge_color": "#ffe600",
            "verdict_enum": "CONDITIONAL_ENTRY"
        }
    elif pct <= 70.0:
        return {
            "emoji": "💀",
            "tier_title": "Walking Problem",
            "verdict_label": "Active Contaminant",
            "badge_color": "#f97316",
            "verdict_enum": "HOUSE_ENTRY_DENIED"
        }
    elif pct <= 90.0:
        return {
            "emoji": "☠️",
            "tier_title": "Please Don't Enter The House",
            "verdict_label": "Entry Denied",
            "badge_color": "#ef4444",
            "verdict_enum": "HOUSE_ENTRY_DENIED"
        }
    else:
        return {
            "emoji": "🪦",
            "tier_title": "Archaeological Artifact",
            "verdict_label": "Biological Disaster",
            "badge_color": "#ff007f",
            "verdict_enum": "HOUSE_ENTRY_DENIED"
        }

# Custom Cyberpunk Bouncer Cockpit CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@600;800;900&family=Rajdhani:wght@600;700;800&display=swap');

    /* Cyber Background & Grid */
    .stApp {
        background: linear-gradient(rgba(7, 11, 25, 0.88), rgba(7, 11, 25, 0.94)), url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #00f2ff;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Top Banner Frame */
    .banner-frame {
        border: 2px solid #00f2ff;
        outline: 1px solid #ff007f;
        background: rgba(10, 15, 35, 0.9);
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.3), inset 0 0 20px rgba(0, 242, 255, 0.15);
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        margin-bottom: 25px;
        position: relative;
    }

    .banner-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.6rem;
        font-weight: 900;
        color: #ffffff;
        text-transform: uppercase;
        text-shadow: 0 0 12px #00f2ff, 0 0 25px #ff007f;
        letter-spacing: 2px;
        margin: 0;
    }

    .banner-subtitle {
        font-family: 'Share Tech Mono', monospace;
        color: #ff007f;
        font-size: 1.1rem;
        letter-spacing: 1px;
        margin-top: 5px;
        margin-bottom: 12px;
        text-transform: uppercase;
    }

    .chips-wrapper {
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
    }

    .status-chip {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        padding: 4px 12px;
        border-radius: 4px;
        font-weight: bold;
        border: 1px solid currentColor;
        box-shadow: 0 0 10px currentColor;
    }
    .chip-cyan { color: #00f2ff; background: rgba(0, 242, 255, 0.1); }
    .chip-magenta { color: #ff007f; background: rgba(255, 0, 127, 0.1); }
    .chip-yellow { color: #ffe600; background: rgba(255, 230, 0, 0.1); }

    /* HUD Panel Frames */
    .hud-panel {
        background: rgba(10, 15, 30, 0.85);
        backdrop-filter: blur(12px);
        border: 2px solid #00f2ff;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.25);
        margin-bottom: 20px;
        position: relative;
    }

    .hud-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        font-weight: 800;
        color: #00f2ff;
        text-transform: uppercase;
        border-bottom: 1px solid rgba(0, 242, 255, 0.3);
        padding-bottom: 8px;
        margin-bottom: 15px;
        letter-spacing: 1px;
    }

    /* Bouncer Verdict Box */
    .verdict-box {
        border: 2px solid #ff007f;
        background: rgba(20, 5, 25, 0.9);
        box-shadow: 0 0 30px rgba(255, 0, 127, 0.4);
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }

    .verdict-denied-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: #ff007f;
        text-shadow: 0 0 15px #ff007f;
        letter-spacing: 2px;
    }

    .verdict-granted-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: #39ff14;
        text-shadow: 0 0 15px #39ff14;
        letter-spacing: 2px;
    }

    .verdict-conditional-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: #ffe600;
        text-shadow: 0 0 15px #ffe600;
        letter-spacing: 2px;
    }

    /* Hazard Reasoning Box */
    .hazard-reason-box {
        border: 2px solid #ffe600;
        background: repeating-linear-gradient(
            45deg,
            rgba(255, 230, 0, 0.08),
            rgba(255, 230, 0, 0.08) 10px,
            rgba(10, 15, 30, 0.9) 10px,
            rgba(10, 15, 30, 0.9) 20px
        );
        border-radius: 8px;
        padding: 16px;
        margin-top: 15px;
    }

    .hazard-title {
        font-family: 'Orbitron', sans-serif;
        color: #ffe600;
        font-size: 0.95rem;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    /* Telemetry Stats */
    .telemetry-item {
        background: rgba(5, 10, 20, 0.8);
        border: 1px solid rgba(0, 242, 255, 0.2);
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 10px;
        font-family: 'Share Tech Mono', monospace;
    }

    /* Scrolling Hazard Ticker */
    .ticker-wrap {
        width: 100%;
        background: rgba(255, 0, 127, 0.15);
        border-top: 1px solid #ff007f;
        border-bottom: 1px solid #ff007f;
        overflow: hidden;
        white-space: nowrap;
        padding: 8px 0;
        margin-top: 30px;
    }
    
    .ticker-text {
        display: inline-block;
        font-family: 'Share Tech Mono', monospace;
        color: #ffe600;
        font-size: 0.95rem;
        font-weight: bold;
        letter-spacing: 1px;
        animation: ticker 25s linear infinite;
    }

    @keyframes ticker {
        0% { transform: translate3d(100%, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }

    /* Streamlit Button Styling */
    .stButton > button {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        border-radius: 6px !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #ff007f 0%, #7928ca 100%) !important;
        border: 1px solid #ff007f !important;
        color: #fff !important;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.6) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Top Cyber Banner
st.markdown("""
    <div class="banner-frame">
        <h1 class="banner-title">👟 Shoe Dirt Calculator</h1>
        <div class="banner-subtitle">Automated Forensic Footwear Contamination Analysis</div>
        <div class="chips-wrapper">
            <span class="status-chip chip-cyan">SYSTEM: FORENSIC ANALYZER ONLINE</span>
            <span class="status-chip chip-magenta">SPECTROSCOPY: ARMED</span>
            <span class="status-chip chip-yellow">CONTAMINATION THRESHOLD: HIGH</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Define Pydantic Schema for Structured Output
class ShoeInspectionResult(BaseModel):
    shoe_detected: bool = Field(
        True,
        description="Set to False if the image does NOT contain a shoe or footwear (e.g. face, animal, food, random object, bare feet). Set to True if a shoe/footwear is present."
    )
    dirtiness_percentage: float = Field(
        ..., 
        description="Dirtiness percentage scale from 0.0 (spotless, pristine) to 100.0 (utterly biohazardous, filthy trash)."
    )
    rank_title: str = Field(
        ..., 
        description="A blunt, sarcastic, disrespectful title given to the shoe owner based on how bad their footwear looks."
    )
    crime_category: str = Field(
        ...,
        description="A simple, brutal offense label (e.g., 'Sewer Dragging', 'Pure Laziness', 'Footwear Neglect', 'Biohazard Threat', 'Dumpster Fire')."
    )
    verdict: str = Field(
        ..., 
        description="Must be one of: 'ENTRY_GRANTED', 'CONDITIONAL_ENTRY', or 'HOUSE_ENTRY_DENIED'."
    )
    roast_reason: str = Field(
        ..., 
        description="A raw, brutal, aggressive, and dark roast in simple conversational English. Zero corporate jargon, zero academic fluff."
    )
    detected_brand: str = Field(
        ...,
        description="Visible brand logo or silhouette (e.g., 'Nike', 'Adidas', 'Crocs', 'Puma', 'Converse', or 'Suspect Knockoff / Unknown Market Copy')."
    )
    stockx_valuation: str = Field(
        ...,
        description="A satirical, absurd estimated resale value. If pristine, a tiny valuation; if dirty/beat-up, negative values or hilarious penalties (e.g. '-$14.50 (Seller pays buyer for toxic waste disposal)', '2 rupees and half a tea', 'Immediate ban from StockX')."
    )

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY is missing! Please make sure it's set in your `.env` file.")
else:
    client = genai.Client(api_key=api_key)

    # Initialize session state keys
    if "reset_counter" not in st.session_state:
        st.session_state.reset_counter = 0
    if "input_mode" not in st.session_state:
        st.session_state.input_mode = "📸 Webcam Capture"
    if "prev_mode" not in st.session_state:
        st.session_state.prev_mode = st.session_state.input_mode
    if "camera_active" not in st.session_state:
        st.session_state.camera_active = False
    if "snapped_webcam_img" not in st.session_state:
        st.session_state.snapped_webcam_img = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    def on_mode_change():
        if st.session_state.input_mode != st.session_state.prev_mode:
            st.session_state.reset_counter += 1
            st.session_state.prev_mode = st.session_state.input_mode
            st.session_state.camera_active = False
            st.session_state.snapped_webcam_img = None

    # 3-COLUMN COCKPIT LAYOUT
    col_left, col_center, col_right = st.columns([0.32, 0.44, 0.24])

    items_to_process = []
    widget_key = f"{st.session_state.input_mode}_{st.session_state.reset_counter}"

    # ---------------------------------------------------------
    # LEFT COLUMN: INPUT CONTROLS
    # ---------------------------------------------------------
    with col_left:
        st.markdown("""
            <div class="hud-panel">
                <div class="hud-header">📥 STEP 1: CAPTURE OR UPLOAD FOOTWEAR</div>
            </div>
        """, unsafe_allow_html=True)

        mode = st.radio(
            "Input Mode Selector",
            ["📸 Webcam Capture", "📂 File Upload (Batch Support)"],
            key="input_mode",
            on_change=on_mode_change
        )

        if mode == "📸 Webcam Capture":
            suspect_name_webcam = st.text_input(
                "Subject / Owner Label", 
                value="Anonymous Subject",
                key=f"webcam_name_{st.session_state.reset_counter}"
            )
            
            cam_toggle = st.toggle("Enable Live Sensor Camera", value=st.session_state.camera_active, key=f"cam_toggle_{st.session_state.reset_counter}")
            st.session_state.camera_active = cam_toggle

            if st.session_state.camera_active:
                st.caption("🔴 Live Sensor Stream Active")
                camera_file = st.camera_input("Snap footwear photo", key=widget_key)
                if camera_file:
                    st.session_state.snapped_webcam_img = Image.open(camera_file)
            else:
                st.info("📷 Camera is powered down. Toggle the switch above to activate live sensor.")

            if st.session_state.snapped_webcam_img:
                items_to_process.append({
                    "file": "webcam", 
                    "label": suspect_name_webcam or "Anonymous Subject", 
                    "image": st.session_state.snapped_webcam_img
                })
        else:
            uploaded_files = st.file_uploader(
                "Upload shoe images", 
                type=["jpg", "jpeg", "png", "webp"], 
                accept_multiple_files=True,
                key=widget_key
            )
            if uploaded_files:
                st.markdown("##### 🏷️ Label Owner(s)")
                for idx, uf in enumerate(uploaded_files):
                    img = Image.open(uf)
                    st.image(img, width=80)
                    label = st.text_input(
                        f"Label #{idx + 1}", 
                        value=f"Subject #{idx + 1}", 
                        key=f"label_{idx}_{st.session_state.reset_counter}"
                    )
                    items_to_process.append({"file": uf, "label": label or f"Subject #{idx + 1}", "image": img})

        if items_to_process:
            st.markdown("---")
            if st.button("🗑️ Clear / Flush Inputs", use_container_width=True):
                st.session_state.reset_counter += 1
                st.session_state.camera_active = False
                st.session_state.snapped_webcam_img = None
                st.session_state.last_result = None
                st.rerun()

            scan_btn_label = "🔥 CALCULATE DIRT INDEX (BATCH)" if len(items_to_process) > 1 else "🔥 CALCULATE DIRT INDEX"
            scan_clicked = st.button(scan_btn_label, type="primary", use_container_width=True)

    # ---------------------------------------------------------
    # CENTER COLUMN: FORENSIC DIAGNOSTIC CONSOLE
    # ---------------------------------------------------------
    with col_center:
        st.markdown("""
            <div class="hud-panel">
                <div class="hud-header">🧪 FORENSIC DIAGNOSTIC CONSOLE</div>
            </div>
        """, unsafe_allow_html=True)

        # Audio SFX Toggle Switch
        audio_enabled = st.toggle("🔊 Audio SFX", value=True, key=f"audio_sfx_toggle_{st.session_state.reset_counter}")

        if items_to_process and 'scan_clicked' in locals() and scan_clicked:
            results = []
            progress_bar = st.progress(0.0)

            # Play scan track once during analysis if audio enabled
            audio_placeholder = st.empty()
            if audio_enabled:
                audio_placeholder.markdown(get_audio_html("sfx/manedanezoha.mp3", autoplay=True), unsafe_allow_html=True)

            prompt = (
                "FIRST STEP: Determine if this image actually contains a shoe or footwear. "
                "If it contains a face, animal, food, bare feet, or random non-footwear object, set 'shoe_detected' to False.\n"
                "If shoe_detected is False, write an exasperated, aggressive roast in simple Malayalam/Manglish or blunt English mocking them for scanning random nonsense instead of a shoe (e.g. asking what they expect the shoe calculator to do with this non-shoe object).\n\n"
                "If a shoe IS present, set 'shoe_detected' to True, evaluate the dirtiness percentage from 0.0 (pristine) to 100.0 (utter biohazard trash).\n"
                "BRAND & RESALE VALUATION:\n"
                "- Identify the brand logo or design silhouette (e.g., 'Nike', 'Adidas', 'Crocs', 'Puma', 'Converse', or 'Suspect Knockoff / Unknown Market Copy'). If unbranded or fake-looking, call it out.\n"
                "- Generate a satirical, absurd StockX resale valuation based on condition and filth (e.g. '-$14.50 (Seller pays buyer for toxic waste disposal)', '2 rupees and half a tea', 'Immediate platform ban').\n\n"
                "ROAST INSTRUCTIONS FOR SHOES (SIMPLE, BLUNT, CONVERSATIONAL ENGLISH):\n"
                "- DO NOT use corporate, academic, or forensic jargon like 'unmitigated assault of topsoil' or 'organic grime'.\n"
                "- Write in plain, direct, aggressive, and disrespectful English.\n"
                "- If 0–10%: Sarcastic roast for being a nerd whose shoes look untouched by the outside world.\n"
                "- If 10–50%: Call out laziness, scuffs, neglected soles, and lack of self-respect.\n"
                "- If 50–100%: Completely destroy them. Be angry, dark, and blunt.\n\n"
                "Provide a short sarcastic owner title, a simple brutal crime category, and a verdict ('ENTRY_GRANTED', 'CONDITIONAL_ENTRY', or 'HOUSE_ENTRY_DENIED')."
            )

            FORENSIC_PHRASES = [
                "🧬 Running molecular mud spectroscopy...",
                "💔 Calculating contamination index...",
                "🕵️ Cross-referencing forensic grime database...",
                "☣️ Analyzing bio-degradation parameters...",
                "⚖️ Evaluating indoor clearance status..."
            ]

            for i, item in enumerate(items_to_process):
                status_container = st.status(f"🚨 Analyzing **{item['label']}** ({i+1}/{len(items_to_process)})...", expanded=True)
                selected_phrases = random.sample(FORENSIC_PHRASES, k=2)
                for phrase in selected_phrases:
                    status_container.write(phrase)
                    time.sleep(0.3)

                # Force reload client with fresh key from environment
                current_api_key = os.environ.get("GEMINI_API_KEY")
                active_client = genai.Client(api_key=current_api_key) if current_api_key else client

                models_to_try = [
                    "gemini-2.5-flash",
                    "gemini-3.5-flash",
                    "gemini-2.5-flash-lite",
                    "gemini-3.1-flash-lite"
                ]

                response = None
                last_error = None

                for model_id in models_to_try:
                    try:
                        status_container.write(f"📡 Requesting analysis from `{model_id}`...")
                        response = active_client.models.generate_content(
                            model=model_id,
                            contents=[item['image'], prompt],
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                response_schema=ShoeInspectionResult,
                                temperature=0.7,
                            ),
                        )
                        if response:
                            break
                    except Exception as err:
                        last_error = err
                        status_container.write(f"⚠️ `{model_id}` quota/rate limit error, trying fallback model...")

                try:
                    if not response:
                        raise last_error or Exception("All Gemini models failed or hit quota limits.")

                    parsed_result = ShoeInspectionResult.model_validate_json(response.text)
                    results.append({
                        "item": item,
                        "res": parsed_result
                    })
                    
                    append_to_csv(
                        suspect_name=item["label"],
                        dirt_pct=parsed_result.dirtiness_percentage,
                        rank_title=parsed_result.rank_title,
                        crime_category=parsed_result.crime_category,
                        verdict=parsed_result.verdict
                    )
                    status_container.update(label=f"🎯 Inspection Complete: **{item['label']}**", state="complete", expanded=False)

                except Exception as e:
                    status_container.update(label=f"❌ Failed: {item['label']}", state="error", expanded=True)
                    st.error(f"Error inspecting {item['label']}: {str(e)}")
                
                progress_bar.progress((i + 1) / len(items_to_process))

            # Hard stop analyzing audio and unmount audio slot
            audio_placeholder.empty()
            if audio_enabled:
                import streamlit.components.v1 as components
                components.html("""
                    <script>
                        const audios = window.parent.document.querySelectorAll('audio');
                        audios.forEach(a => { a.pause(); a.currentTime = 0; a.remove(); });
                    </script>
                """, height=0, width=0)

            if results:
                st.session_state.last_result = results

        # Render Active or Previous Scan Results in Center Column
        if st.session_state.last_result:
            results = st.session_state.last_result
            if len(results) == 1:
                item = results[0]["item"]
                res = results[0]["res"]

                # Play single-shot verdict audio SFX via components.html if audio enabled
                if audio_enabled:
                    import streamlit.components.v1 as components
                    sfx_file = "sfx/apebble-fart-5-228245.mp3" if not getattr(res, "shoe_detected", True) else get_verdict_sfx_path(res.dirtiness_percentage)
                    if os.path.exists(sfx_file):
                        with open(sfx_file, "rb") as f:
                            sfx_b64 = base64.b64encode(f.read()).decode("utf-8")
                        components.html(f"""
                            <audio autoplay style="display:none;">
                                <source src="data:audio/mp3;base64,{sfx_b64}" type="audio/mp3">
                            </audio>
                        """, height=0, width=0)

                # NON-SHOE OVERRIDE HANDLING
                if not getattr(res, "shoe_detected", True):
                    st.markdown("""
                        <div class="verdict-box" style="border-color: #ef4444; background: rgba(30, 0, 0, 0.95); box-shadow: 0 0 35px #ef4444;">
                            <div style="font-family: 'Share Tech Mono', monospace; color: #ff8888; font-size: 0.85rem; letter-spacing: 1px;">SYSTEM ALERT // NON-SHOES DETECTED</div>
                            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.4rem; font-weight: 900; color: #ef4444; margin-top: 4px;">
                                AARE KETTIKKANA, AARE KETTIKKANAN ITH ENIKK
                            </div>
                            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.6rem; font-weight: 900; color: #ffffff; text-shadow: 0 0 12px #ef4444; margin-top: 4px;">
                                ⛔ INVALID TARGET // NOT A SHOE
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        st.markdown("""
                            <div class="telemetry-item" style="text-align: center; border-color: #ef4444;">
                                <span style="color: #94a3b8; font-size: 0.8rem;">DIRT INDEX</span>
                                <h2 style="color: #ef4444; margin: 0; font-family: 'Orbitron', sans-serif;">N/A</h2>
                            </div>
                        """, unsafe_allow_html=True)
                    with col_m2:
                        st.markdown(f"""
                            <div class="telemetry-item" style="text-align: center; border-color: #ef4444;">
                                <span style="color: #94a3b8; font-size: 0.8rem;">OFFENSE CATEGORY</span>
                                <h4 style="color: #ef4444; margin: 0; font-family: 'Orbitron', sans-serif;">🚨 INVALID SCAN</h4>
                            </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                        <div class="hazard-reason-box" style="border-color: #ef4444; background: rgba(40, 5, 5, 0.9);">
                            <div class="hazard-title" style="color: #ef4444;">⚠️ SYSTEM EXASPIRATION // NON-SHOE TARGET</div>
                            <p style="color: #fca5a5; font-size: 1.1rem; font-weight: bold; line-height: 1.5; margin: 0;">
                                "{res.roast_reason}"
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

                else:
                    tier_info = get_tier_info(res.dirtiness_percentage)

                    st.markdown(f"""
                        <div class="verdict-box" style="border-color: {tier_info['badge_color']}; box-shadow: 0 0 25px {tier_info['badge_color']};">
                            <div style="font-family: 'Share Tech Mono', monospace; color: #94a3b8; font-size: 0.85rem; letter-spacing: 1px;">CONTAMINATION TIER & VERDICT</div>
                            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; font-weight: 800; color: {tier_info['badge_color']}; margin-top: 4px;">
                                {tier_info['emoji']} {tier_info['tier_title']}
                            </div>
                            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.8rem; font-weight: 900; color: #ffffff; text-shadow: 0 0 12px {tier_info['badge_color']}; margin-top: 2px;">
                                {tier_info['verdict_label']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        st.markdown(f"""
                            <div class="telemetry-item" style="text-align: center; border-color: {tier_info['badge_color']};">
                                <span style="color: #94a3b8; font-size: 0.8rem;">DIRT INDEX</span>
                                <h2 style="color: {tier_info['badge_color']}; margin: 0; font-family: 'Orbitron', sans-serif;">{tier_info['emoji']} {res.dirtiness_percentage:.1f}%</h2>
                            </div>
                        """, unsafe_allow_html=True)
                    with col_m2:
                        st.markdown(f"""
                            <div class="telemetry-item" style="text-align: center;">
                                <span style="color: #94a3b8; font-size: 0.8rem;">OFFENSE CATEGORY</span>
                                <h4 style="color: #00f2ff; margin: 0; font-family: 'Orbitron', sans-serif;">🚨 {res.crime_category}</h4>
                            </div>
                        """, unsafe_allow_html=True)

                    val_str = getattr(res, "stockx_valuation", "N/A")
                    val_color = "#ef4444" if ("-" in val_str or "ban" in val_str.lower() or "disposal" in val_str.lower()) else "#39ff14"
                    brand_str = getattr(res, "detected_brand", "Unbranded / Unknown")

                    st.markdown(f"""
                        <div class="hazard-reason-box" style="border-color: {tier_info['badge_color']};">
                            <div class="hazard-title" style="color: {tier_info['badge_color']};">⚠️ {tier_info['emoji']} {tier_info['tier_title'].upper()} | {tier_info['verdict_label'].upper()}</div>
                            <p style="color: #a855f7; font-weight: bold; margin-top: 4px; margin-bottom: 8px;">Tag: {res.rank_title}</p>
                            
                            <div style="display: flex; gap: 10px; margin-bottom: 12px; flex-wrap: wrap;">
                                <div style="background: rgba(0, 242, 255, 0.1); border: 1px solid #00f2ff; padding: 5px 12px; border-radius: 4px; font-family: 'Share Tech Mono', monospace; font-size: 0.85rem; color: #00f2ff;">
                                    🏷️ BRAND IDENTIFIED: <b>{brand_str}</b>
                                </div>
                                <div style="background: rgba(10, 10, 25, 0.9); border: 1px solid {val_color}; padding: 5px 12px; border-radius: 4px; font-family: 'Share Tech Mono', monospace; font-size: 0.85rem; color: {val_color}; box-shadow: 0 0 10px {val_color};">
                                    📉 ESTIMATED DRIP VALUE: <b>{val_str}</b>
                                </div>
                            </div>

                            <p style="color: #e2e8f0; font-size: 1.05rem; font-style: italic; line-height: 1.5; margin: 0;">
                                "{res.roast_reason}"
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                # Tournament Display inside Center
                st.markdown("<h3 style='color: #ff007f; text-align: center;'>👑 CONTAMINATION CHAMPIONSHIP RANKINGS</h3>", unsafe_allow_html=True)
                sorted_results = sorted(results, key=lambda x: x["res"].dirtiness_percentage, reverse=True)
                for rank_idx, entry in enumerate(sorted_results):
                    res = entry["res"]
                    item = entry["item"]
                    if not getattr(res, "shoe_detected", True):
                        st.markdown(f"""
                            <div class="hud-panel" style="margin-bottom: 10px; border-color: #ef4444; background: rgba(30, 0, 0, 0.8);">
                                <span style="color: #ef4444; font-weight: bold;">INVALID SCAN: {item['label']}</span>
                                <h3 style="color: #ef4444; margin: 4px 0;">AARE KETTIKKANA, AARE KETTIKKANAN ITH ENIKK</h3>
                                <p style="color: #fca5a5; font-style: italic;">"{res.roast_reason}"</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        tier_info = get_tier_info(res.dirtiness_percentage)
                        val_str = getattr(res, "stockx_valuation", "N/A")
                        val_color = "#ef4444" if ("-" in val_str or "ban" in val_str.lower() or "disposal" in val_str.lower()) else "#39ff14"
                        brand_str = getattr(res, "detected_brand", "Unbranded")
                        st.markdown(f"""
                            <div class="hud-panel" style="margin-bottom: 10px; border-color: {tier_info['badge_color']};">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span style="color: #ff007f; font-weight: bold; font-size: 1.1rem;">RANK #{rank_idx + 1}: {item['label']}</span>
                                    <span style="color: {tier_info['badge_color']}; font-weight: bold;">{tier_info['emoji']} {tier_info['tier_title']}</span>
                                </div>
                                <h2 style="color: {tier_info['badge_color']}; margin: 5px 0;">{res.dirtiness_percentage:.1f}% Dirt ({tier_info['verdict_label']})</h2>
                                <p style="color: #00f2ff; margin: 0;"><b>Brand:</b> {brand_str} | <b>StockX Value:</b> <span style="color: {val_color}; font-weight: bold;">{val_str}</span></p>
                                <p style="color: #cbd5e1; font-style: italic; margin-top: 6px;">"{res.roast_reason}"</p>
                            </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("👈 Load footwear images on the left panel and execute the scan to calculate dirt index.")

    # ---------------------------------------------------------
    # RIGHT COLUMN: DIAGNOSTIC TELEMETRY PANEL
    # ---------------------------------------------------------
    with col_right:
        st.markdown("""
            <div class="hud-panel">
                <div class="hud-header">📡 DIAGNOSTIC TELEMETRY</div>
            </div>
        """, unsafe_allow_html=True)

        # 3D Rotating Hologram Shoe Chamber Component
        import streamlit.components.v1 as components
        components.html("""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    background: transparent;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    font-family: 'Courier New', monospace;
                    overflow: hidden;
                }
                .holo-container {
                    perspective: 800px;
                    width: 140px;
                    height: 140px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                }
                .holo-pod {
                    width: 120px;
                    height: 120px;
                    border: 2px solid #00f2ff;
                    border-radius: 50%;
                    box-shadow: 0 0 20px #00f2ff, inset 0 0 15px rgba(0, 242, 255, 0.4);
                    position: absolute;
                    animation: pulseGlow 3s ease-in-out infinite alternate;
                }
                .holo-beam {
                    position: absolute;
                    width: 100px;
                    height: 100px;
                    background: radial-gradient(circle, rgba(0, 242, 255, 0.25) 0%, transparent 70%);
                    border-radius: 50%;
                }
                .sneaker-3d {
                    font-size: 4.2rem;
                    transform-style: preserve-3d;
                    animation: spin3d 6s linear infinite;
                    filter: drop-shadow(0 0 12px #ff007f);
                    cursor: default;
                    user-select: none;
                }
                @keyframes spin3d {
                    0% { transform: rotateY(0deg) rotateX(10deg); }
                    50% { transform: rotateY(180deg) rotateX(-10deg) scale(1.08); }
                    100% { transform: rotateY(360deg) rotateX(10deg); }
                }
                @keyframes pulseGlow {
                    0% { border-color: #00f2ff; box-shadow: 0 0 15px #00f2ff; }
                    100% { border-color: #ff007f; box-shadow: 0 0 25px #ff007f; }
                }
                .sub-text {
                    color: #00f2ff;
                    font-size: 0.72rem;
                    font-weight: bold;
                    letter-spacing: 1px;
                    margin-top: 8px;
                    text-align: center;
                    text-shadow: 0 0 6px #00f2ff;
                }
            </style>
            </head>
            <body>
                <div class="holo-container">
                    <div class="holo-pod"></div>
                    <div class="holo-beam"></div>
                    <div class="sneaker-3d">👟</div>
                </div>
                <div class="sub-text">HOLOGRAPHIC SCAN CHAMBER<br>// ACTIVE ROTATION</div>
            </body>
            </html>
        """, height=185)

        st.markdown("""
            <div class="hud-panel" style="margin-top: 10px;">
                <div class="telemetry-item">
                    <span style="color: #94a3b8;">MODEL:</span> <span style="color: #39ff14;">gemini-3.6-flash</span>
                </div>
                <div class="telemetry-item">
                    <span style="color: #94a3b8;">API LATENCY:</span> <span style="color: #00f2ff;">142ms (OPTIMAL)</span>
                </div>
                <div class="telemetry-item">
                    <span style="color: #94a3b8;">SENSORS:</span> <span style="color: #ffe600;">SPECTROSCOPY ARMED</span>
                </div>
                <div class="telemetry-item">
                    <span style="color: #94a3b8;">CARPET SHIELD:</span> <span style="color: #ff007f;">100% MAXIMUM POWER</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # BOTTOM SECTION: PERSISTENT CLEARANCE LEADERBOARD
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #ff007f; font-family: Orbitron;'>🏆 ALL-TIME SLUDGE HALL OF FAME & SHAME</h2>", unsafe_allow_html=True)

    df_lb = load_leaderboard()

    if not df_lb.empty:
        dirtiest_champ = df_lb.iloc[0]
        cleanest_loser = df_lb.iloc[-1]

        col_champ, col_shame = st.columns(2)
        with col_champ:
            st.markdown(f"""
                <div class="hud-panel" style="border-color: #ff007f; box-shadow: 0 0 25px rgba(255, 0, 127, 0.4);">
                    <span class="status-chip chip-magenta">👑 #1 ALL-TIME SLUDGE OVERLORD</span>
                    <h3 style="margin-top:10px; margin-bottom: 2px; color: #ffffff;">🔥 {dirtiest_champ['Suspect_Name']}</h3>
                    <h2 style="color: #ff007f; margin: 0; font-family: 'Orbitron';">{dirtiest_champ['Dirt_Percentage']:.1f}% DIRT</h2>
                    <p style="margin: 4px 0 0 0; color: #ffe600;"><b>Title:</b> {dirtiest_champ['Rank_Title']}</p>
                </div>
            """, unsafe_allow_html=True)

        with col_shame:
            st.markdown(f"""
                <div class="hud-panel" style="border-color: #94a3b8;">
                    <span class="status-chip chip-cyan">🧼 DISQUALIFIED FOR HYGIENE</span>
                    <h3 style="margin-top:10px; margin-bottom: 2px; color: #94a3b8;">🤡 {cleanest_loser['Suspect_Name']}</h3>
                    <h2 style="color: #64748b; margin: 0; font-family: 'Orbitron';">{cleanest_loser['Dirt_Percentage']:.1f}% DIRT</h2>
                    <p style="margin: 4px 0 0 0; color: #00f2ff;"><b>Title:</b> {cleanest_loser['Rank_Title']}</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("### 🏆 Full Clearance Records")
        for idx, row in df_lb.iterrows():
            rank_num = idx + 1
            st.markdown(f"""
                <div style="background: rgba(10, 15, 30, 0.8); padding: 12px 18px; border-radius: 6px; margin-bottom: 8px; border-left: 4px solid #00f2ff; font-family: 'Share Tech Mono', monospace;">
                    <span style="color: #ff007f; font-weight: bold;">#{rank_num}</span> | 
                    <span style="color: #ffffff; font-weight: bold;">{row['Suspect_Name']}</span> — 
                    <span style="color: #ffe600;">{row['Rank_Title']}</span> | 
                    <span style="color: #00f2ff;">Crime: {row['Crime_Category']}</span> 
                    <span style="float: right; color: #ff007f; font-weight: bold; font-size: 1.2rem;">{row['Dirt_Percentage']:.1f}%</span>
                </div>
            """, unsafe_allow_html=True)

    col_ref, col_del = st.columns([2, 2])
    with col_ref:
        if st.button("🔄 Refresh Clearance Records", use_container_width=True):
            st.rerun()

    with col_del:
        with st.popover("⚠️ Wipe Records"):
            st.warning("Permanently delete CSV records?")
            confirm_clear = st.checkbox("Confirm wipe")
            if st.button("🚨 Clear CSV", type="primary", disabled=not confirm_clear):
                clear_csv()
                st.success("Wiped!")
                st.rerun()

    # Animated Bottom Hazard Ticker Bar
    st.markdown("""
        <div class="ticker-wrap">
            <div class="ticker-text">
                🚨 FORENSIC CONTAMINATION ALERT: FOOTWEAR SPECTROSCOPY ACTIVE... HIGH DENSITY PARTICULATES DETECTED... ALL SUBJECTS SUBJECT TO MANDATORY DIRT INDEX EVALUATION... SEVERE BIO-DEGRADATION PROTOCOLS ENFORCED...
            </div>
        </div>
    """, unsafe_allow_html=True)
