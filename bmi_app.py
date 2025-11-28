import streamlit as st
import os

# --- 1. Page Config ---
st.set_page_config(
    page_title="Health Metrics Pro",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. Professional Dark Theme CSS with Animations & Shadows ---
st.markdown("""
<style>
    /* Import Professional Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Reset */
    * {
        font-family: 'Inter', sans-serif !important;
    }

    /* Force Dark Theme Backgrounds */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Input Fields Styling */
    .stNumberInput input, .stSelectbox div, .stRadio label {
        color: #FFFFFF !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #262730 !important;
        border-color: #41444C !important;
        transition: border-color 0.3s ease;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #FFFFFF !important;
    }

    /* --- ANIMATIONS DEFINITION --- */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translate3d(0, 20px, 0);
        }
        to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
        }
    }

    /* --- PROFESSIONAL CARD STYLING (With White Shadows) --- */
    .pro-card {
        background-color: #1E1E1E;
        border: 1px solid #333333;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        
        /* The White Box Shadow (Subtle Glow) */
        box-shadow: 0 4px 6px rgba(255, 255, 255, 0.05);
        
        /* Animation properties */
        animation: fadeInUp 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        transition: all 0.3s ease;
    }
    
    /* Hover Effect: Lift & Intensify Glow */
    .pro-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Metrics Styling */
    .metric-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #A0A0A0;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
    }
    .metric-sub {
        font-size: 14px;
        color: #888;
        margin-top: 4px;
    }

    /* Button Styling */
    div.stButton > button {
        background-color: #FFFFFF;
        color: #000000;
        border: none;
        padding: 14px 24px;
        font-weight: 600;
        border-radius: 12px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(255, 255, 255, 0.1);
    }
    div.stButton > button:hover {
        background-color: #F0F0F0;
        color: #000000;
        transform: scale(1.02);
        box-shadow: 0 6px 15px rgba(255, 255, 255, 0.2);
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }

    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Footer */
    .pro-footer {
        text-align: center;
        padding: 40px 0;
        color: #555;
        font-size: 12px;
        border-top: 1px solid #333;
        margin-top: 40px;
        animation: fadeInUp 1s ease forwards;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Logic Functions ---

def get_status(bmi):
    # Returns: Status, Color Hex code
    if bmi < 18.5: return "Underweight", "#4FC3F7"  # Light Blue
    elif 18.5 <= bmi <= 22.9: return "Normal Range", "#66BB6A"  # Green
    elif 23.0 <= bmi <= 24.9: return "Overweight", "#FFA726"  # Orange
    else: return "Obese", "#EF5350"  # Red

def calculate_tdee(weight, height_cm, age, gender, activity):
    # Mifflin-St Jeor Equation
    bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) + (5 if gender == "Male" else -161)
    
    multipliers = {
        "Sedentary (Office Job)": 1.2,
        "Lightly Active (1-3 days)": 1.375,
        "Moderately Active (3-5 days)": 1.55,
        "Very Active (6-7 days)": 1.725,
        "Extra Active (Physical Job)": 1.9
    }
    return int(bmr * multipliers.get(activity, 1.2))

def get_plan_text(category):
    if category == "Underweight":
        return {
            "Goal": "Hypertrophy / Weight Gain",
            "Strategy": "Caloric Surplus (+300 kcal)",
            "Diet": "Focus on calorie-dense whole foods. \n• Breakfast: Parathas with curd or Eggs with whole grain toast. \n• Lunch: Rice, Dal Tadka with Ghee, dense vegetables. \n• Dinner: Protein-rich curry (Chicken/Paneer) with Rotis."
        }
    elif category == "Normal Range":
        return {
            "Goal": "Maintenance & General Health",
            "Strategy": "Maintenance Calories",
            "Diet": "Balanced Macronutrients. \n• Breakfast: Poha/Upma with vegetables or Idli. \n• Lunch: Roti, Dal, Sabzi, Salad. \n• Dinner: Multigrain Roti with light vegetable curry."
        }
    elif category == "Overweight":
        return {
            "Goal": "Fat Loss",
            "Strategy": "Caloric Deficit (-500 kcal)",
            "Diet": "High Volume, Low Calorie. \n• Breakfast: Oats or Daliya (Porridge). \n• Lunch: 1-2 Rotis, boiled Dal, large portion of salad. \n• Dinner: Grilled protein salad or clear soup."
        }
    else: # Obese
        return {
            "Goal": "Aggressive Fat Loss",
            "Strategy": "Strict Deficit & Medical Management",
            "Diet": "Low Carbohydrate / High Fiber. \n• Breakfast: Vegetable juice or Egg whites. \n• Lunch: Jowar Roti with leafy greens. \n• Dinner: Lentil soup. Avoid sugar and refined flour entirely."
        }

# --- 4. Main Layout ---

# Logo & Header
col_logo, col_title = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        # Fallback text if no logo
        st.markdown("<h2 style='color:#FFF;'>NF</h2>", unsafe_allow_html=True)

with col_title:
    st.markdown("<h2 style='color: white; margin-bottom: 0px;'>Health Metrics Pro</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 14px;'>Indian Standard Protocol</p>", unsafe_allow_html=True)

st.markdown("---")

# INPUT SECTION (Grid Layout - Mobile Friendly)
st.markdown("#### Patient Details")

c1, c2 = st.columns(2)
with c1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", 10, 100, 25)

with c2:
    weight = st.number_input("Weight (kg)", 1.0, 300.0, 72.0)
    # Height Logic (Simplified)
    height_ft = st.number_input("Height (Feet)", 3, 8, 5)
    
c3, c4 = st.columns(2)
with c3:
    height_in = st.number_input("Height (Inches)", 0, 11, 7)
    # Convert to CM immediately for logic
    height_cm = (height_ft * 12 + height_in) * 2.54
    height_m = height_cm / 100

with c4:
    activity = st.selectbox("Activity Level", [
        "Sedentary (Office Job)",
        "Lightly Active (1-3 days)",
        "Moderately Active (3-5 days)",
        "Very Active (6-7 days)",
        "Extra Active (Physical Job)"
    ])

st.markdown("<br>", unsafe_allow_html=True)
calc = st.button("CALCULATE METRICS")

# --- 5. Results Section ---
if calc:
    # Calculations
    bmi = weight / (height_m ** 2)
    tdee = calculate_tdee(weight, height_cm, age, gender, activity)
    status, color_code = get_status(bmi)
    plan = get_plan_text(status)
    
    if status in ["Overweight", "Obese"]: target_cals = tdee - 500
    elif status == "Underweight": target_cals = tdee + 300
    else: target_cals = tdee

    st.markdown("---")
    
    # RESULT CARDS (Using CSS Grid for Pro Look)
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
        <div class="pro-card" style="animation-delay: 0.1s;">
            <div class="metric-label">BMI Score</div>
            <div class="metric-value" style="color: {color_code}">{bmi:.1f}</div>
            <div class="metric-sub">{status}</div>
        </div>
        <div class="pro-card" style="animation-delay: 0.2s;">
            <div class="metric-label">Maintenance (TDEE)</div>
            <div class="metric-value">{tdee}</div>
            <div class="metric-sub">kcal / day</div>
        </div>
    </div>
    <div class="pro-card" style="margin-top: 0px; animation-delay: 0.3s;">
        <div class="metric-label">Recommended Target</div>
        <div class="metric-value" style="color: #FFFFFF">{target_cals}</div>
        <div class="metric-sub">kcal / day to reach goal</div>
    </div>
    """, unsafe_allow_html=True)

    # DIET PLAN SECTION
    st.markdown("#### Clinical Recommendations")
    
    st.markdown(f"""
    <div class="pro-card" style="animation-delay: 0.4s;">
        <h4 style="color: white; margin-top:0;">{plan['Goal']}</h4>
        <p style="color: #AAA; font-size: 14px; margin-bottom: 20px;">Strategy: {plan['Strategy']}</p>
        <div style="background-color: #262730; padding: 15px; border-radius: 8px; border-left: 4px solid {color_code};">
            <p style="color: #DDD; white-space: pre-line; line-height: 1.6;">{plan['Diet']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 6. Footer ---
st.markdown("""
    <div class="pro-footer">
        NEON FIX / BROKENERD &copy; 2024<br>
        Developed for Indian Demographics
    </div>

""", unsafe_allow_html=True)


