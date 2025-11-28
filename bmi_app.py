import streamlit as st
import os

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Health Connect",
    page_icon="🍎",
    layout="centered", # 'Centered' looks more like a mobile app on desktop
    initial_sidebar_state="expanded"
)

# --- 2. THE IPHONE UI SYSTEM (CSS) ---
st.markdown("""
<style>
    /* IMPORT APPLE SYSTEM FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* GLOBAL APP BACKGROUND */
    .stApp {
        background-color: #F2F2F7; /* iOS System Gray 6 */
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* HIDE DEFAULT STREAMLIT ELEMENTS */
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    
    /* CUSTOM CARD COMPONENT (iOS Style) */
    .ios-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.06); /* Soft Apple Shadow */
        transition: transform 0.2s ease;
    }
    .ios-card:hover {
        transform: translateY(-2px);
    }

    /* METRIC GRID (RESPONSIVE) */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-bottom: 20px;
    }
    
    /* MOBILE ADJUSTMENT: Stack columns on small screens */
    @media (max-width: 600px) {
        .metric-container {
            grid-template-columns: 1fr;
        }
    }

    /* INDIVIDUAL METRIC BOXES */
    .metric-box {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.02);
    }
    .metric-label {
        font-size: 13px;
        color: #8E8E93; /* iOS Label Gray */
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #1C1C1E;
    }
    .metric-sub {
        font-size: 14px;
        font-weight: 600;
        margin-top: 5px;
    }

    /* TABS STYLING (Segmented Control Look) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #E5E5EA; /* iOS Segmented Control BG */
        padding: 4px;
        border-radius: 12px;
        gap: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 9px;
        background-color: transparent;
        border: none;
        color: #000;
        flex: 1; /* Distribute space evenly */
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    /* FOOTER */
    .ios-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-top: 1px solid #C6C6C8;
        padding: 15px;
        text-align: center;
        font-size: 12px;
        color: #8E8E93;
        z-index: 999;
    }
    
    /* INPUT FIELDS ROUNDING */
    .stNumberInput input, .stSelectbox div, .stRadio {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Logic ---
def get_details(bmi):
    # Colors: Green(Success), Blue(Info), Yellow(Warning), Red(Danger)
    if bmi < 18.5: return "Underweight", "#007AFF" # iOS Blue
    elif 18.5 <= bmi <= 22.9: return "Normal", "#34C759" # iOS Green
    elif 23.0 <= bmi <= 24.9: return "Overweight", "#FF9500" # iOS Orange
    else: return "Obese", "#FF3B30" # iOS Red

def calc_tdee(weight, height_cm, age, gender, activity):
    bmr = (10*weight) + (6.25*height_cm) - (5*age) + (5 if gender=="Male" else -161)
    act_map = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725, "Extra Active": 1.9}
    return int(bmr * act_map.get(activity, 1.2))

def get_meals(cat):
    # Returns (Emoji, Breakfast, Lunch, Snack, Dinner, Tip)
    if cat == "Underweight":
        return ("🥑", "2 Paneer Parathas + Curd", "Rice, Dal Tadka (Ghee), Sabzi", "Banana Shake + Nuts", "3 Rotis + Chicken/Paneer Curry", "Focus on calorie-dense foods like nuts and ghee.")
    elif cat == "Normal":
        return ("🥗", "Poha/Upma + Veggies", "2 Rotis, Dal, Sabzi, Curd", "Apple or Green Tea", "2 Multigrain Rotis + Lauki Sabzi", "Maintain protein intake and hydration.")
    elif cat == "Overweight":
        return ("🏃", "Oats/Daliya or Moong Chilla", "1 Multigrain Roti + Dal + Salad", "Roasted Makhana / Chaas", "Grilled Paneer Salad or Soup", "Cut sugar. Walk 10,000 steps daily.")
    else: # Obese
        return ("🔥", "Veg Juice + 2 Egg Whites", "1 Jowar Roti + Saag + Raita", "Green Tea + 5 Almonds", "Lentil Soup + Sautéed Veggies", "Strictly no fried food/sugar. Intermittent Fasting.")

# --- 4. Sidebar ---
with st.sidebar:
    # LOGO HANDLING
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    else:
        st.warning("⚠️ 'logo.png' not found. Ensure it's in the same folder.")
        st.markdown("### Neon Fix / Brokenerd") # Text fallback

    st.markdown("#### Personal Details")
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True, label_visibility="collapsed")
    age = st.number_input("Age", 10, 100, 25)
    
    st.markdown("#### Body Stats")
    weight = st.number_input("Weight (kg)", 1.0, 200.0, 72.0)
    
    # Height Tabs inside sidebar for cleaner UI
    h_tab1, h_tab2 = st.tabs(["Ft/In", "CM"])
    with h_tab1:
        c1, c2 = st.columns(2)
        with c1: feet = st.number_input("Ft", 1, 8, 5)
        with c2: inches = st.number_input("In", 0, 11, 6)
        height_cm = (feet*12 + inches)*2.54
    with h_tab2:
        h_cm_input = st.number_input("Cm", 50, 250, 170)
        # Overwrite if this tab is active (Basic logic)
        # Note: In a complex app we'd use session state, but this works for display
        if h_cm_input != 170: 
            height_cm = h_cm_input

    height_m = height_cm/100
    
    st.markdown("#### Lifestyle")
    activity = st.selectbox("Activity", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"], label_visibility="collapsed")
    
    st.write("") # Spacer
    calc = st.button("Calculate Health Plan", type="primary", use_container_width=True)

# --- 5. Main UI ---

# Header
st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>Health Mate 🇮🇳</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8E8E93; margin-bottom: 30px;'>Advanced Indian BMI & Diet Calculator</p>", unsafe_allow_html=True)

if calc:
    # Math
    bmi = weight / (height_m ** 2)
    tdee = calc_tdee(weight, height_cm, age, gender, activity)
    category, color = get_details(bmi)
    emoji, b, l, s, d, tip = get_meals(category)
    
    if category in ["Overweight", "Obese"]: target = tdee - 500
    elif category == "Underweight": target = tdee + 300
    else: target = tdee

    # --- IOS CARDS (HTML Injection) ---
    
    # 1. The Summary Grid
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-box">
            <div class="metric-label">BMI Score</div>
            <div class="metric-value" style="color: {color}">{bmi:.1f}</div>
            <div class="metric-sub" style="color: {color}">{category}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Daily Needs</div>
            <div class="metric-value">{tdee}</div>
            <div class="metric-sub" style="color: #8E8E93">kcal/day</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Target Goal</div>
            <div class="metric-value" style="color: #007AFF">{target}</div>
            <div class="metric-sub" style="color: #007AFF">kcal/day</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. The Progress Bar
    st.caption("BMI Scale (Asian Standard)")
    st.progress(min(bmi/40, 1.0))
    
    # 3. The Diet Card
    st.markdown(f"""
    <div class="ios-card">
        <h3 style="margin-top:0"> {emoji} Recommended Diet Plan</h3>
        <p style="color:#666; font-size:14px; margin-bottom:20px;">
            Strategy: <b>{tip}</b>
        </p>
    """, unsafe_allow_html=True)

    # Close HTML div temporarily to insert Streamlit Tabs (Native widgets work better for interactivity)
    
    d_tab1, d_tab2, d_tab3, d_tab4 = st.tabs(["🍳 Breakfast", "🍛 Lunch", "🍎 Snack", "🍲 Dinner"])
    
    with d_tab1: st.info(b)
    with d_tab2: st.warning(l)
    with d_tab3: st.success(s)
    with d_tab4: st.error(d)
    
    st.markdown("</div>", unsafe_allow_html=True) # Close ios-card

else:
    # Empty State
    st.markdown("""
    <div class="ios-card" style="text-align: center; padding: 40px;">
        <h2 style="color: #C7C7CC;">👋</h2>
        <h3 style="color: #333;">Welcome!</h3>
        <p style="color: #8E8E93;">Enter your details in the sidebar to generate your personalized Indian health report.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. Sticky Footer ---
st.markdown("""
    <div class="ios-footer">
        <b>Neon Fix / Brokenerd</b> &nbsp;|&nbsp; Designed for Indian Health Standards
    </div>
""", unsafe_allow_html=True)