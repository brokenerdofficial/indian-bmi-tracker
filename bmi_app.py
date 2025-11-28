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
        height: 100%; /* Ensure equal height in grids */
        
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
        line-height: 1.5;
    }
    
    /* Meal Card Specific Text */
    .meal-text {
        color: #E0E0E0;
        font-size: 15px;
        font-weight: 500;
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
            "Meals": {
                "Breakfast": "Parathas with curd or \nEggs with whole grain toast.",
                "Lunch": "Rice, Dal Tadka with Ghee, \ndense vegetables.",
                "Snacks": "Banana shake with nuts \nor Peanut Butter Toast.",
                "Dinner": "Protein-rich curry (Chicken/Paneer) \nwith Rotis."
            }
        }
    elif category == "Normal Range":
        return {
            "Goal": "Maintenance & General Health",
            "Strategy": "Maintenance Calories",
            "Meals": {
                "Breakfast": "Poha/Upma with vegetables \nor Idli Sambar.",
                "Lunch": "Roti, Dal, Sabzi, \nSmall portion of Rice.",
                "Snacks": "Fruit (Apple/Papaya) \nor Roasted Chana.",
                "Dinner": "Multigrain Roti with \nlight vegetable curry."
            }
        }
    elif category == "Overweight":
        return {
            "Goal": "Fat Loss",
            "Strategy": "Caloric Deficit (-500 kcal)",
            "Meals": {
                "Breakfast": "Oats porridge (water/skim milk) \nor Daliya.",
                "Lunch": "1-2 Rotis, boiled Dal, \nLarge portion of salad.",
                "Snacks": "Green Tea and \nCucumber/Carrot sticks.",
                "Dinner": "Grilled protein salad \nor Clear soup with veggies."
            }
        }
    else: # Obese
        return {
            "Goal": "Aggressive Fat Loss",
            "Strategy": "Strict Deficit & Medical Management",
            "Meals": {
                "Breakfast": "Vegetable juice \nor Egg whites (No Yolk).",
                "Lunch": "Jowar Roti with \nLeafy greens (Palak/Methi).",
                "Snacks": "Black Coffee / Green Tea \n(No sugar).",
                "Dinner": "Lentil soup (Moong Dal water). \nAvoid solid carbs at night."
            }
        }

# --- 4. Main Layout ---

# Logo & Header
col_logo, col_title = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)
    else:
        st.markdown("<h2 style='color:#FFF;'>NF</h2>", unsafe_allow_html=True)

with col_title:
    st.markdown("<h2 style='color: white; margin-bottom: 0px;'>Health Metrics Pro</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 14px;'>Indian Standard Protocol</p>", unsafe_allow_html=True)

st.markdown("---")

# INPUT SECTION (Stacked Rows for Mobile/Compact View)
st.markdown("#### Patient Details")

# Row 1: Gender, Age, Weight
r1_c1, r1_c2, r1_c3 = st.columns([1, 1, 1])
with r1_c1:
    gender = st.selectbox("Gender", ["Male", "Female"])
with r1_c2:
    age = st.number_input("Age", 10, 100, 25)
with r1_c3:
    weight = st.number_input("Weight (kg)", 1.0, 300.0, 72.0)

# Row 2: Height Ft, Height In, Activity
# Activity gets slightly more space (flex 2)
r2_c1, r2_c2, r2_c3 = st.columns([1, 1, 2])
with r2_c1:
    height_ft = st.number_input("Height (Ft)", 3, 8, 5)
with r2_c2:
    height_in = st.number_input("Height (In)", 0, 11, 7)
with r2_c3:
    activity = st.selectbox("Activity Level", [
        "Sedentary (Office Job)",
        "Lightly Active (1-3 days)",
        "Moderately Active (3-5 days)",
        "Very Active (6-7 days)",
        "Extra Active (Physical Job)"
    ])

# Logic for Height Calculation
height_cm = (height_ft * 12 + height_in) * 2.54
height_m = height_cm / 100

st.markdown("<br>", unsafe_allow_html=True)
calc = st.button("CALCULATE METRICS")

# --- 5. Results Section ---
if calc:
    # Calculations
    bmi = weight / (height_m ** 2)
    tdee = calculate_tdee(weight, height_cm, age, gender, activity)
    status, color_code = get_status(bmi)
    plan = get_plan_text(status)
    meals = plan['Meals']
    
    if status in ["Overweight", "Obese"]: target_cals = tdee - 500
    elif status == "Underweight": target_cals = tdee + 300
    else: target_cals = tdee

    st.markdown("---")
    
    # RESULT CARDS (2 Top Cards)
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
        <div class="pro-card" style="animation-delay: 0.1s;">
            <div class="metric-label">BMI Score</div>
            <div class="metric-value" style="color: {color_code}">{bmi:.1f}</div>
            <div class="metric-sub">{status}</div>
        </div>
        <div class="pro-card" style="animation-delay: 0.2s;">
            <div class="metric-label">Maintenance</div>
            <div class="metric-value">{tdee}</div>
            <div class="metric-sub">kcal / day</div>
        </div>
    </div>
    
    <div class="pro-card" style="margin-top: 16px; animation-delay: 0.3s;">
        <div class="metric-label">Recommended Target</div>
        <div class="metric-value" style="color: #FFFFFF">{target_cals}</div>
        <div class="metric-sub">kcal / day to reach goal ({plan['Goal']})</div>
    </div>
    """, unsafe_allow_html=True)

    # DIET PLAN SECTION
    st.markdown("#### Clinical Diet Recommendations")
    
    # MEAL CARDS (Grid Layout for Meal Cards)
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 10px;">
        <div class="pro-card" style="animation-delay: 0.4s;">
            <div class="metric-label" style="color: #4FC3F7;">Breakfast</div>
            <div class="meal-text">{meals['Breakfast']}</div>
        </div>
        
        <div class="pro-card" style="animation-delay: 0.5s;">
            <div class="metric-label" style="color: #FFA726;">Lunch</div>
            <div class="meal-text">{meals['Lunch']}</div>
        </div>
        
        <div class="pro-card" style="animation-delay: 0.6s;">
            <div class="metric-label" style="color: #AB47BC;">Snacks</div>
            <div class="meal-text">{meals['Snacks']}</div>
        </div>
        
        <div class="pro-card" style="animation-delay: 0.7s;">
            <div class="metric-label" style="color: #66BB6A;">Dinner</div>
            <div class="meal-text">{meals['Dinner']}</div>
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
