import streamlit as st
import os

# --- 1. Page Config ---
st.set_page_config(
    page_title="Health Metrics Pro",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. Professional Dark Theme CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #0E1117; }
    
    /* Input Styling */
    .stNumberInput input, .stSelectbox div, .stRadio label { color: #FFFFFF !important; }
    div[data-baseweb="select"] > div {
        background-color: #262730 !important;
        border-color: #41444C !important;
    }
    
    /* --- MOBILE COLUMN FIX (For Inputs) --- */
    /* Forces st.columns to stay side-by-side (50% width) on small screens */
    @media (max-width: 768px) {
        div[data-testid="column"] {
            width: 50% !important;
            flex: 1 1 auto !important;
            min-width: 0px !important;
        }
        /* Fix overlapping text in small inputs */
        .stNumberInput input {
            padding-right: 0px !important; 
            min-width: 0px !important;
        }
    }

    /* Card Animation */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translate3d(0, 20px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }

    /* Professional Card Class */
    .pro-card {
        background-color: #1E1E1E;
        border: 1px solid #333333;
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        box-shadow: 0 4px 6px rgba(255, 255, 255, 0.05);
        animation: fadeInUp 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
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
    
    /* Meal Text Styling */
    .meal-text {
        color: #E0E0E0;
        font-size: 14px;
        font-weight: 500;
        line-height: 1.5;
        white-space: pre-line;
    }
    
    /* Grid Container for Mobile Cards */
    .grid-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 16px;
    }

    /* Button */
    div.stButton > button {
        background-color: #FFFFFF;
        color: #000000;
        border: none;
        padding: 14px 24px;
        font-weight: 600;
        border-radius: 12px;
        width: 100%;
        box-shadow: 0 4px 10px rgba(255, 255, 255, 0.1);
    }
    div.stButton > button:hover {
        background-color: #F0F0F0;
        transform: scale(1.02);
    }
    
    /* Hide Default Elements */
    #MainMenu, header, footer {visibility: hidden;}
    
    .pro-footer {
        text-align: center;
        padding: 40px 0;
        color: #555;
        font-size: 12px;
        border-top: 1px solid #333;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Logic Functions ---

def get_status(bmi):
    if bmi < 18.5: return "Underweight", "#4FC3F7"
    elif 18.5 <= bmi <= 22.9: return "Normal Range", "#66BB6A"
    elif 23.0 <= bmi <= 24.9: return "Overweight", "#FFA726"
    else: return "Obese", "#EF5350"

def calculate_tdee(weight, height_cm, age, gender, activity):
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
            "Meals": {
                "Breakfast": "Vegetable juice \nor Egg whites (No Yolk).",
                "Lunch": "Jowar Roti with \nLeafy greens (Palak/Methi).",
                "Snacks": "Black Coffee / Green Tea \n(No sugar).",
                "Dinner": "Lentil soup (Moong Dal water). \nAvoid solid carbs at night."
            }
        }

# --- 4. Main Layout ---

col_logo, col_title = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo.png"): st.image("logo.png", width=150)
    else: st.markdown("<h2 style='color:#FFF;'>NF</h2>", unsafe_allow_html=True)

with col_title:
    st.markdown("<h2 style='color: white; margin-bottom: 0px;'>Health Metrics Pro</h2>", unsafe_allow_html=True)

st.markdown("---")

# INPUT SECTION
st.markdown("#### Patient Details")

# 1. Gender (Full Row)
gender = st.selectbox("Gender", ["Male", "Female"])

# 2. Age & Weight (Side-by-Side)
c1, c2 = st.columns(2)
with c1: age = st.number_input("Age", 10, 100, 25)
with c2: weight = st.number_input("Weight (kg)", 1.0, 300.0, 72.0)

# 3. Height Fields (Side-by-Side)
c3, c4 = st.columns(2)
with c3: height_ft = st.number_input("Height (Ft)", 3, 8, 5)
with c4: height_in = st.number_input("Height (In)", 0, 11, 7)

# 4. Activity (Full Row)
activity = st.selectbox("Activity Level", [
    "Sedentary (Office Job)", "Lightly Active (1-3 days)", 
    "Moderately Active (3-5 days)", "Very Active (6-7 days)", 
    "Extra Active (Physical Job)"
])

height_cm = (height_ft * 12 + height_in) * 2.54
height_m = height_cm / 100

st.markdown("<br>", unsafe_allow_html=True)
calc = st.button("CALCULATE METRICS")

# --- 5. Results Section ---
if calc:
    bmi = weight / (height_m ** 2)
    tdee = calculate_tdee(weight, height_cm, age, gender, activity)
    status, color_code = get_status(bmi)
    plan = get_plan_text(status)
    meals = plan['Meals']
    
    if status in ["Overweight", "Obese"]: target_cals = tdee - 500
    elif status == "Underweight": target_cals = tdee + 300
    else: target_cals = tdee

    st.markdown("---")
    
    # --- 1. BMI & TDEE (HTML Grid - Side by Side guaranteed) ---
    st.markdown(f"""
    <div class="grid-container">
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
    
    <div class="pro-card" style="margin-top: 0px; animation-delay: 0.3s;">
        <div class="metric-label">Recommended Target</div>
        <div class="metric-value" style="color: #FFFFFF">{target_cals}</div>
        <div class="metric-sub">kcal / day to reach goal ({plan['Goal']})</div>
    </div>
    """, unsafe_allow_html=True)

    # --- 2. Diet Plan (HTML Grid for Meals) ---
    st.markdown("#### Clinical Diet Recommendations")
    
    # We replace newlines with <br> for HTML rendering in the f-string
    bf_text = meals['Breakfast'].replace('\n', '<br>')
    ln_text = meals['Lunch'].replace('\n', '<br>')
    sn_text = meals['Snacks'].replace('\n', '<br>')
    dn_text = meals['Dinner'].replace('\n', '<br>')

    st.markdown(f"""
    <div class="grid-container">
        <div class="pro-card" style="animation-delay: 0.4s;">
            <div class="metric-label" style="color: #4FC3F7;">Breakfast</div>
            <div class="meal-text">{bf_text}</div>
        </div>
        <div class="pro-card" style="animation-delay: 0.5s;">
            <div class="metric-label" style="color: #FFA726;">Lunch</div>
            <div class="meal-text">{ln_text}</div>
        </div>
    </div>

    <div class="grid-container">
        <div class="pro-card" style="animation-delay: 0.6s;">
            <div class="metric-label" style="color: #AB47BC;">Snacks</div>
            <div class="meal-text">{sn_text}</div>
        </div>
        <div class="pro-card" style="animation-delay: 0.7s;">
            <div class="metric-label" style="color: #66BB6A;">Dinner</div>
            <div class="meal-text">{dn_text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 6. Footer ---
st.markdown("""
    <div class="pro-footer">
        BROKENERD &copy; 2025<br>
        Developed for Indian Demographics
    </div>
""", unsafe_allow_html=True)





