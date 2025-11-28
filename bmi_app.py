import streamlit as st
import os

# --- 1. Page Config ---
st.set_page_config(
    page_title="Health Metrics Pro",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. Neumorphism Light Theme CSS ---
st.markdown("""
<style>
    /* Import Professional Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Global Reset & Font definition */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* --- NEUMORPHISM CORE COLORS --- */
    :root {
        --bg-color: #ECF0F3; /* Soft light grey background */
        --text-dark: #333333;
        --text-mid: #555555;
        --text-light: #888888;
        /* The magic shadows for the extruded look */
        --neu-shadow-dark: 9px 9px 16px rgb(163, 177, 198, 0.6);
        --neu-shadow-light: -9px -9px 16px rgba(255, 255, 255, 0.8);
    }

    /* Force App Background Color */
    .stApp {
        background-color: var(--bg-color);
    }
    
    /* --- WIDGET STYLING FOR LIGHT THEME --- */
    /* Ensure widget labels and text are dark */
    .stSlider label, .stSelectbox label, .stRadio label, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p {
        color: var(--text-dark) !important;
    }
    /* Style the slider thumbs and tracks to blend better */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: var(--bg-color) !important;
        box-shadow: var(--neu-shadow-dark);
        border: 2px solid #fff;
    }
    
    /* Selectbox styling */
    div[data-baseweb="select"] > div {
        background-color: var(--bg-color) !important;
        border: none !important;
        box-shadow: inset 4px 4px 8px rgb(163, 177, 198, 0.4), inset -4px -4px 8px rgba(255, 255, 255, 0.8) !important;
        color: var(--text-dark) !important;
        border-radius: 12px !important;
    }

    /* --- NEUMORPHIC CARD CLASSES --- */
    /* The main extruded card style */
    .neu-card {
        background-color: var(--bg-color);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        /* The double shadow creates the pop-out effect */
        box-shadow: var(--neu-shadow-dark), var(--neu-shadow-light);
        transition: all 0.3s ease;
    }
    
    /* Optional: Slight hover effect to lift the card further */
    .neu-card:hover {
        box-shadow: 12px 12px 20px rgb(163, 177, 198, 0.7), -12px -12px 20px rgba(255, 255, 255, 0.9);
    }

    /* A container style for inputs to group them visually */
    .input-container {
         background-color: var(--bg-color);
         border-radius: 20px;
         padding: 20px;
         /* A slightly softer shadow for the input area */
         box-shadow: 5px 5px 10px rgb(163, 177, 198, 0.5), -5px -5px 10px rgba(255, 255, 255, 0.8);
         margin-bottom: 20px;
    }
    
    /* --- TYPOGRAPHY & METRICS --- */
    .metric-label {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: var(--text-mid);
        margin-bottom: 10px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 36px;
        font-weight: 800;
        color: var(--text-dark);
        margin: 0;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 15px;
        color: var(--text-light);
        margin-top: 6px;
        font-weight: 500;
    }

    /* --- BUTTON STYLING --- */
    div.stButton > button {
        background-color: var(--bg-color) !important;
        color: var(--text-dark) !important;
        border: none !important;
        padding: 14px 24px;
        font-weight: 700;
        letter-spacing: 1px;
        border-radius: 50px; /* rounded pill shape common in Neumorphism */
        width: 100%;
        box-shadow: var(--neu-shadow-dark), var(--neu-shadow-light) !important;
        transition: all 0.2s ease-in-out;
    }
    /* Pressed state for the button */
    div.stButton > button:active {
        box-shadow: inset 4px 4px 8px rgb(163, 177, 198, 0.5), inset -4px -4px 8px rgba(255, 255, 255, 0.9) !important;
        transform: scale(0.98);
    }

    /* Hide Streamlit clutter */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Footer */
    .pro-footer {
        text-align: center;
        padding: 40px 0;
        color: var(--text-mid);
        font-size: 13px;
        margin-top: 40px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Logic Functions (Unchanged logic, updated colors for light theme) ---

def get_status(bmi):
    # Colors tweaked to look better on light background (slightly darker)
    if bmi < 18.5: return "Underweight", "#039BE5"  # Darker Blue
    elif 18.5 <= bmi <= 22.9: return "Normal Range", "#43A047"  # Darker Green
    elif 23.0 <= bmi <= 24.9: return "Overweight", "#FB8C00"  # Darker Orange
    else: return "Obese", "#E53935"  # Darker Red

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
    # (Diet plan text remains the same as previous version)
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

# Header Area
col_logo, col_title = st.columns([1, 4])
with col_logo:
    # Using an emoji as a fallback logo that fits the theme
    st.markdown("<h1 style='font-size: 60px; text-align: center;'>🩺</h1>", unsafe_allow_html=True)

with col_title:
    st.markdown("<h1 style='color: #333; margin-bottom: 5px; font-weight: 800;'>Health Metrics Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #777; font-size: 16px; font-weight: 500;'>Indian Standard Protocol</p>", unsafe_allow_html=True)

st.write("") # Spacer

# --- INPUT SECTION (Sliding Widgets) ---
# We wrap inputs in a neumorphic container for visual grouping
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown("### 👤 Patient Details")

c1, c2 = st.columns(2)
with c1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    # CHANGED TO SLIDER
    age = st.slider("Age (Years)", min_value=10, max_value=100, value=25, step=1)

with c2:
    # CHANGED TO SLIDER
    weight = st.slider("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5, format="%d kg")
    activity = st.selectbox("Activity Level", [
        "Sedentary (Office Job)",
        "Lightly Active (1-3 days)",
        "Moderately Active (3-5 days)",
        "Very Active (6-7 days)",
        "Extra Active (Physical Job)"
    ])

st.markdown("---")
st.markdown("### 📏 Height Measurement")
h1, h2 = st.columns(2)
with h1:
    # CHANGED TO SLIDER
    height_ft = st.slider("Feet", min_value=3, max_value=7, value=5, step=1)
with h2:
    # CHANGED TO SLIDER
    height_in = st.slider("Inches", min_value=0, max_value=11, value=7, step=1)

# Calculate CM immediately
height_cm = (height_ft * 12 + height_in) * 2.54
height_m = height_cm / 100

st.markdown('</div>', unsafe_allow_html=True) # End input container

st.markdown("<br>", unsafe_allow_html=True)
# The button styles itself via CSS to look Neumorphic
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

    st.markdown("<br>", unsafe_allow_html=True)
    
    # RESULT CARDS (Using CSS Grid in HTML for responsive layout)
    # The .neu-card class gives them the extruded look
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px;">
        <div class="neu-card">
            <div class="metric-label">BMI Score</div>
            <div class="metric-value" style="color: {color_code}">{bmi:.1f}</div>
            <div class="metric-sub" style="color: {color_code}; font-weight: 700;">{status}</div>
        </div>
        <div class="neu-card">
            <div class="metric-label">Maintenance (TDEE)</div>
            <div class="metric-value">{tdee}</div>
            <div class="metric-sub">kcal / day</div>
        </div>
        <div class="neu-card">
            <div class="metric-label">Recommended Target</div>
            <div class="metric-value" style="color: #333">{target_cals}</div>
            <div class="metric-sub">kcal / day to reach goal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # DIET PLAN SECTION
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 Clinical Recommendations")
    
    # Using Neumorphic card for diet plan
    st.markdown(f"""
    <div class="neu-card">
        <h3 style="color: #333; margin-top:0; font-weight: 800;">{plan['Goal']}</h3>
        <p style="color: #666; font-size: 15px; margin-bottom: 20px; font-weight: 500;">Strategy: <span style="color:{color_code}">{plan['Strategy']}</span></p>
        
        <div style="background-color: #ECF0F3; padding: 20px; border-radius: 15px; box-shadow: inset 5px 5px 10px #d1d9e6, inset -5px -5px 10px #ffffff; border-left: 5px solid {color_code};">
            <p style="color: #444; white-space: pre-line; line-height: 1.8; font-weight: 500; margin:0;">{plan['Diet']}</p>
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