import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import google.generativeai as genai
import requests
import hashlib

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AgriScanner | AI Plant Doctor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  IMMERSIVE DARK NATURE UI CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #0a1f0a, #040d04);
        color: #e0f2f1;
    }
    
    /* Sidebar Redesign */
    [data-testid="stSidebar"] {
        background-color: #061406 !important;
        border-right: 1px solid rgba(76, 175, 80, 0.1);
    }
    
    .sidebar-content {
        padding: 1.5rem;
        background: rgba(46, 125, 50, 0.1);
        border-radius: 15px;
        border: 1px solid rgba(76, 175, 80, 0.2);
        margin-bottom: 1rem;
        color: #a5d6a7;
    }

    /* Glassmorphism Header */
    .main-header {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 2.5rem;
        text-align: center;
    }
    
    .main-title {
        background: linear-gradient(to right, #81c784, #4caf50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -1.5px;
    }
    
    .main-subtitle {
        color: #a5d6a7;
        font-size: 1.1rem;
        font-weight: 400;
        opacity: 0.8;
    }

    /* Dark Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(8px);
        padding: 1.8rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        background: rgba(76, 175, 80, 0.05);
        border-color: rgba(76, 175, 80, 0.3);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #81c784;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }

    /* Result Container Redesign */
    .result-container {
        background: rgba(0, 0, 0, 0.2);
        padding: 2rem;
        border-radius: 24px;
        border: 1px solid rgba(76, 175, 80, 0.2);
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
    }
    
    .prediction-header {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1.2rem;
    }
    
    .confidence-badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 50px;
        background: rgba(76, 175, 80, 0.15);
        color: #a5d6a7;
        font-weight: 600;
        font-size: 0.85rem;
        margin-right: 0.8rem;
        border: 1px solid rgba(76, 175, 80, 0.2);
    }

    /* Section Headers */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Overriding Streamlit elements for Dark Theme */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 10px 10px 0 0;
        color: #a5d6a7;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(76, 175, 80, 0.1) !important;
        color: #ffffff !important;
        border-bottom: 3px solid #4caf50 !important;
    }
    
    .stProgress > div > div > div > div {
        background-color: #4caf50;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background-color: #2e7d32;
        color: white;
        border: none;
        padding: 0.6rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #388e3c;
        box-shadow: 0 0 15px rgba(76, 175, 80, 0.4);
    }

    /* ── Login Page ── */
    .login-hero {
        text-align: center;
        margin-top: 4rem;
        margin-bottom: 2rem;
    }

    .login-logo {
        font-size: 4rem;
        filter: drop-shadow(0 0 20px rgba(76, 175, 80, 0.6));
    }

    .login-title {
        background: linear-gradient(to right, #81c784, #4caf50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        margin: 0.5rem 0 0.2rem 0;
    }

    .login-tagline {
        color: #a5d6a7;
        font-size: 1rem;
        opacity: 0.8;
    }

    .login-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        padding: 2.5rem 2.5rem 1.5rem 2.5rem;
        border-radius: 24px;
        border: 1px solid rgba(76, 175, 80, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        padding: 2rem 2rem 1rem 2rem;
        border-radius: 24px;
        border: 1px solid rgba(76, 175, 80, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  AUTHENTICATION
# ─────────────────────────────────────────────
def _sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def load_users():
    """Load users from .streamlit/secrets.toml; fall back to a demo account."""
    try:
        users = dict(st.secrets["users"])
        if users:
            return users
    except Exception:
        pass
    return {"farmer": "agri@123"}

def authenticate(username, password):
    users = load_users()
    stored = users.get(username)
    if stored is None:
        return False
    # Accept plaintext or sha256-hashed secrets
    return password == stored or _sha256(password) == stored

# Session state defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ── Login screen ──
if not st.session_state.logged_in:
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("""
            <div class="login-hero">
                <div class="login-logo">🌿</div>
                <div class="login-title">AgriScanner</div>
                <div class="login-tagline">Next-Gen AI Plant Disease Intelligence</div>
            </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("#### 🔐 Sign in to continue")
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("🚀 Sign In")

        if submitted:
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid username or password. Please try again.")

        st.markdown(
            "<center style='color:#81c784;opacity:0.6;font-size:0.8rem;'>"
            "Developed with ❤️ for Indian Farmers</center>",
            unsafe_allow_html=True
        )
    st.stop()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # Inline SVG logo — no external request, so the page never hangs on load
    st.markdown("""
        <div style="text-align:center;">
        <svg width="72" height="72" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="leafGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#81c784"/>
                    <stop offset="100%" stop-color="#2e7d32"/>
                </linearGradient>
            </defs>
            <circle cx="32" cy="32" r="30" fill="rgba(76,175,80,0.08)" stroke="rgba(76,175,80,0.35)"/>
            <path d="M32 12 C46 16 52 28 50 44 C34 46 22 40 18 28 C16 20 22 14 32 12 Z"
                  fill="url(#leafGrad)"/>
            <path d="M32 15 L32 44" stroke="#040d04" stroke-width="2" opacity="0.55"/>
            <path d="M32 24 L24 20 M32 30 L22 27 M32 36 L24 34 M32 24 L40 20 M32 30 L42 27 M32 36 L40 34"
                  stroke="#040d04" stroke-width="1.6" opacity="0.45"/>
        </svg>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("# AgriScanner")
    st.markdown("### Your Digital Crop Doctor")
    st.markdown("---")
    
    st.markdown("""
    <div class='sidebar-content'>
    <b>How to use:</b><br>
    1. Check local weather risk<br>
    2. Upload or snap a leaf photo<br>
    3. Get instant AI diagnosis<br>
    4. Follow expert treatment tips
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Pro Tip:** For best results, ensure the leaf is well-lit and centered in the frame.")
    
    st.markdown("---")
    st.markdown(f"👤 Signed in as **{st.session_state.username}**")
    if st.button("🚪 Log Out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    
    st.markdown("---")
    st.caption("Developed with ❤️ for Indian Farmers")
    st.caption("Version 2.0 | Powered by Gemini")

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
    <div class="main-header">
        <div class="main-title">🌿 AgriScanner</div>
        <div class="main-subtitle">Next-Gen AI Plant Disease Intelligence</div>
    </div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  GEMINI API CONFIG
#  Works with ANY valid key — the model is auto-detected.
# ─────────────────────────────────────────────
GEMINI_API_KEY = None
try:
    GEMINI_API_KEY = st.secrets["gemini"]["api_key"]
    genai.configure(api_key=GEMINI_API_KEY)
except Exception:
    st.sidebar.warning("⚠️ Gemini API Key not found in secrets.toml")
    GEMINI_API_KEY = None

# Preferred models, best first. "…-latest" aliases auto-update and are the
# most durable across key types, so they lead. The first usable one wins.
PREFERRED_GEMINI_MODELS = [
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-pro-latest",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-pro",
]

@st.cache_resource(show_spinner=False)
def resolve_gemini_model():
    """Return the first model this key can actually generate with.

    Tries PREFERRED_GEMINI_MODELS in order and ping-tests each one, so it
    works with any key — including keys where a listed model is not yet
    enabled. The result is cached for the session.
    Returns the working model name, or None if none respond.
    """
    if not GEMINI_API_KEY:
        return None

    for name in PREFERRED_GEMINI_MODELS:
        try:
            genai.GenerativeModel(name).generate_content("ping", request_options={"timeout": 8})
            return name
        except Exception:
            continue

    # Nothing preferred worked — try whatever the key lists as available.
    try:
        for m in genai.list_models():
            if "generateContent" in (getattr(m, "supported_generation_methods", []) or []):
                name = m.name.replace("models/", "")
                if name in PREFERRED_GEMINI_MODELS:
                    continue
                try:
                    genai.GenerativeModel(name).generate_content("ping", request_options={"timeout": 8})
                    return name
                except Exception:
                    continue
    except Exception:
        pass

    return None

# ─────────────────────────────────────────────
#  LOAD MODEL
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("agriscanner-model.keras")

try:
    with st.spinner("🧠 Loading AgriScanner AI model (first run may take a few seconds)..."):
        model = load_model()
    with st.sidebar:
        st.success("🤖 Model Ready")
except Exception as e:
    st.sidebar.error(f"Model Error: {e}")
    st.stop()

# Gemini status is best-effort — never let it block or break the page.
try:
    _active_gemini = resolve_gemini_model()
    with st.sidebar:
        if _active_gemini:
            st.success(f"✨ Gemini Ready ({_active_gemini})")
        else:
            st.warning("⚠️ Gemini key missing — AI advice disabled")
except Exception:
    with st.sidebar:
        st.warning("⚠️ Gemini status unavailable")

# ─────────────────────────────────────────────
#  CLASS NAMES  — exact sorted folder names
#  (must match training order exactly)
# ─────────────────────────────────────────────
class_names = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

# Human-readable display names
display_names = [
    "Apple Scab", "Apple Black Rot", "Apple Cedar Apple Rust", "Apple Healthy",
    "Blueberry Healthy", "Cherry Powdery Mildew", "Cherry Healthy",
    "Corn Cercospora Leaf Spot", "Corn Common Rust", "Corn Northern Leaf Blight", "Corn Healthy",
    "Grape Black Rot", "Grape Esca (Black Measles)", "Grape Leaf Blight", "Grape Healthy",
    "Orange Citrus Greening (Haunglongbing)",
    "Peach Bacterial Spot", "Peach Healthy",
    "Pepper Bell Bacterial Spot", "Pepper Bell Healthy",
    "Potato Early Blight", "Potato Late Blight", "Potato Healthy",
    "Raspberry Healthy", "Soybean Healthy", "Squash Powdery Mildew",
    "Strawberry Leaf Scorch", "Strawberry Healthy",
    "Tomato Bacterial Spot", "Tomato Early Blight", "Tomato Late Blight",
    "Tomato Leaf Mold", "Tomato Septoria Leaf Spot", "Tomato Spider Mites",
    "Tomato Target Spot", "Tomato Yellow Leaf Curl Virus",
    "Tomato Mosaic Virus", "Tomato Healthy"
]

# ─────────────────────────────────────────────
#  SEVERITY ESTIMATOR
# ─────────────────────────────────────────────
def estimate_severity(confidence):
    if confidence >= 90:
        return "🔴 SEVERE"
    elif confidence >= 75:
        return "🟡 MODERATE"
    else:
        return "🟢 MILD"

# ─────────────────────────────────────────────
#  GEMINI DISEASE ANALYSIS
# ─────────────────────────────────────────────
def get_gemini_analysis(disease, confidence, severity):
    if not GEMINI_API_KEY:
        return "⚠️ AI Analysis unavailable: No API key configured. Add one under [gemini] in .streamlit/secrets.toml."
    prompt = f"""
A plant disease scanner has detected the following:
Disease   : {disease}
Confidence: {confidence:.1f}%
Severity  : {severity}

Provide a response in this exact format:

🔬 WHAT IS THIS DISEASE:
(2 sentences explaining the disease)

⚡ IMMEDIATE ACTIONS:
• (action 1)
• (action 2)
• (action 3)

💊 RECOMMENDED TREATMENT:
• (pesticide/fungicide name, dosage, Indian brand name)
• (alternative treatment)

🛡️ PREVENTION FOR NEXT SEASON:
• (tip 1)
• (tip 2)

Keep it practical and simple for an Indian farmer. Be concise.
"""
    resolved = resolve_gemini_model()

    # Try the resolved model first, then sweep the preference list as a safety net.
    candidates = [resolved] + [m for m in PREFERRED_GEMINI_MODELS if m != resolved]
    last_error = None
    for name in candidates:
        if not name:
            continue
        try:
            gemini_model = genai.GenerativeModel(name)
            response = gemini_model.generate_content(prompt, request_options={"timeout": 30})
            if response and getattr(response, "text", None):
                return response.text
        except Exception as e:
            last_error = e
            continue

    msg = str(last_error) if last_error else "Unknown error"
    if "404" in msg or "not found" in msg.lower():
        return ("⚠️ AI Analysis unavailable: no usable Gemini model was found for this API key. "
                "Please verify the key is from https://aistudio.google.com/app/apikey.")
    if "API_KEY" in msg or "401" in msg or "403" in msg or "permission" in msg.lower():
        return "⚠️ AI Analysis unavailable: the API key was rejected. Check that it is valid and enabled."
    return f"⚠️ AI Analysis unavailable: {msg}"

# ─────────────────────────────────────────────
#  WEATHER + RISK ALERT
# ─────────────────────────────────────────────
@st.cache_data(ttl=600, show_spinner=False)
def get_weather_risk(disease_key):
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=16.5&longitude=80.6&current=temperature_2m,relative_humidity_2m,rain"
        data     = requests.get(url, timeout=5).json()['current']
        temp     = data['temperature_2m']
        humidity = data['relative_humidity_2m']
        rain     = data['rain']

        high_risk = [
            "Tomato___Late_blight", "Potato___Late_blight",
            "Grape___Black_rot", "Apple___Apple_scab",
            "Tomato___Early_blight", "Corn_(maize)___Northern_Leaf_Blight",
            "Squash___Powdery_mildew", "Cherry_(including_sour)___Powdery_mildew"
        ]

        if humidity > 80 and disease_key in high_risk:
            risk = "🔴 HIGH RISK — Spray immediately, conditions favour spread"
        elif humidity > 60:
            risk = "🟡 MODERATE — Monitor closely"
        else:
            risk = "🟢 LOW RISK — Conditions are okay"

        return temp, humidity, rain, risk
    except:
        return None, None, None, "⚪ Weather data unavailable"

# ─────────────────────────────────────────────
#  PREDICTION FUNCTION
#  !! CRITICAL: raw [0-255] image passed directly
#  !! Model handles preprocessing internally
#  !! NEVER call preprocess_input() before this
# ─────────────────────────────────────────────
def predict(image):
    img_resized  = image.resize((224, 224)).convert("RGB")
    img_array    = np.expand_dims(np.array(img_resized), axis=0).astype('float32')
    # raw [0-255] — model's internal layers handle normalization
    raw_preds    = model.predict(img_array, verbose=0)[0]
    probs        = raw_preds / np.sum(raw_preds)
    top3_idx     = np.argsort(probs)[::-1][:3]
    return top3_idx, probs

# ─────────────────────────────────────────────
#  WEATHER DISPLAY
# ─────────────────────────────────────────────
with st.container():
    st.markdown("### 🌤️ Local Environmental Context")
    with st.spinner("Fetching local weather data..."):
        temp, humidity, rain, _ = get_weather_risk("")
    
    if temp:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Temperature</div>
                    <div class="metric-value">{temp}°C</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Humidity</div>
                    <div class="metric-value">{humidity}%</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Rainfall</div>
                    <div class="metric-value">{rain}mm</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Weather data currently unavailable. Using standard diagnosis mode.")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  IMAGE INPUT
# ─────────────────────────────────────────────
st.subheader("📤 Upload or Capture Leaf Image")
tab1, tab2 = st.tabs(["📁 Upload Image", "📷 Use Camera"])

with tab1:
    uploaded_file = st.file_uploader("Choose a leaf image", type=["jpg", "jpeg", "png"])

with tab2:
    camera_image = st.camera_input("Take a photo of the leaf")

# ─────────────────────────────────────────────
#  PROCESS IMAGE
# ─────────────────────────────────────────────
image = None
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
elif camera_image:
    image = Image.open(camera_image).convert("RGB")

if image is not None:
    st.markdown("---")
    res_col1, res_col2 = st.columns([1, 1.2])
    
    with res_col1:
        st.markdown("#### 📸 Captured Leaf")
        st.image(image, use_column_width=True)
        
        with st.spinner("🔍 Analyzing leaf patterns..."):
            top3_idx, probs = predict(image)
        
        # ── Weather risk alert in image column ──
        _, _, _, risk = get_weather_risk(class_names[top3_idx[0]])
        st.info(f"📍 **Environmental Risk:**\n{risk}")

    with res_col2:
        pred_idx    = top3_idx[0]
        confidence  = float(probs[pred_idx] * 100)
        disease_name = display_names[pred_idx]
        severity    = estimate_severity(confidence)
        is_healthy  = "healthy" in class_names[pred_idx].lower()

        st.markdown(f"""
            <div class="result-container">
                <div class="metric-label">Primary Diagnosis</div>
                <div class="prediction-header">🌱 {disease_name}</div>
                <div>
                    <span class="confidence-badge">Confidence: {confidence:.1f}%</span>
                    <span class="confidence-badge">Severity: {severity}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if is_healthy:
            st.success("✅ **Healthy Leaf Detected.** Your plant looks great! Keep up the good work.")
        elif confidence < 60:
            st.warning("⚠️ **Low Confidence.** The diagnosis might be inaccurate. Try a clearer photo.")
        else:
            st.error("🚨 **Disease Detected.** Immediate action recommended.")

        # ── Top 3 predictions with styled bars ──
        with st.expander("📊 View Detailed Probability Distribution", expanded=True):
            for i, idx in enumerate(top3_idx):
                conf = float(probs[idx] * 100)
                st.write(f"**{display_names[idx]}**")
                st.progress(conf / 100)
                st.caption(f"Match probability: {conf:.1f}%")

    # ── Gemini analysis section ──
    if not is_healthy:
        st.markdown("---")
        st.markdown("### 🤖 AI Doctor's Prescription")
        if GEMINI_API_KEY: 
            with st.spinner("Consulting AI expert for treatment plan..."):
                analysis = get_gemini_analysis(disease_name, confidence, severity)
            
            # Render Gemini analysis in a nice box
            st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.03); padding: 2.5rem; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.05); color: #e0f2f1; line-height: 1.6;">
                    {analysis}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("💡 Add your Gemini API key in the sidebar to get detailed AI treatment advice.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<center style='color: #81c784; opacity: 0.6; font-size: 0.8rem;'>Made with ❤️ by AgriScanner Team | VIT-AP University</center>", unsafe_allow_html=True)
    if st.button("🔄 Start New Scan"):
        st.rerun()
