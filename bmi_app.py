import streamlit as st
import os

# --- 1. Page Config ---
st.set_page_config(
    page_title="Health Metrics Pro",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. Advanced CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #0E1117; }

    /* ANIMATIONS */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translate3d(0, 20px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }

    /* --- MOBILE GRID FIX --- */
    /* Forces columns to be 50% width on mobile (Side-by-Side inputs) */
    @media (max-width: 640px) {
        div[data-testid="column"] {
            width: 50% !important;
            flex: 1 1 50% !important;
            min-width: 50% !important;
        }
    }
    
    /* INPUT STYLING */
    .stNumberInput input, .stSelectbox div {
        color: #FFFFFF !important;
        background-color: #1E1E1E !important; 
        border: 1px solid #333 !important;
        border-radius: 8px !important;
    }
    /* Hide label on mobile to save space */
    label { color: #888 !important; font-size: 11px !important; }

    /* CARD STYLING */
    .pro-card {
        background-color: #1E1E1E;
        border: 1px solid #333;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(255, 255, 255, 0.05);
        animation: fadeInUp 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }
    
    /* DIET PLAN STACKS */
    .meal-card {
        background-color: #161B22; 
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 15px;
        height: 100%;
        border-left: 4px solid #4FC3F7;
    }

    /* TYPOGRAPHY */
    .metric-val { font-size: 26px; font-weight: 700; color: #FFF; }
    .metric-lbl { font-size: 10px; text-transform: uppercase; color: #888; letter-spacing: 1px; }
    .meal-title { font-size: 11px; font-weight: 700; color: #AAA; text-transform: uppercase; margin-bottom: 6px; }
    .meal-food { 
        font-size: 13px; 
        color: #FFF; 
        font-weight: 500; 
        line-height: 1.4; 
        white-space: pre-line; /* Allows newlines to show */
    }

    /* BUTTON */
    div.stButton > button {
        background-color: #FFF; color: #000; border-radius: 10px;
        padding: 12px; font-weight: 600; border: none; width: 100%;
        box-shadow: 0 0 10px rgba(255,255,255,0.2);
    }
    
    #MainMenu, header, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- 3. Logic & Helpers ---

def get_metrics(weight, height_cm, age, gender, activity):
    bmi = weight / ((height_cm/100) ** 2)
    bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) + (5 if gender == "Male" else -161)
    act_map = {"Sedentary": 1.2, "Light Active": 1.375, "Moderate Active": 1.55, "Very Active": 1.725, "Extra Active": 1.9}
    tdee = int(bmr * act_map.get(activity, 1.2))
    return bmi, tdee

def get_health_status(bmi):
    if bmi < 18.5: return "Underweight", "#4FC3F7"
    elif 18.5 <= bmi <= 22.9: return "Normal", "#66BB6A"
    elif 23.0 <= bmi <= 24.9: return "Overweight", "#FFA726"
    else: return "Obese", "#EF5350"

def get_diet_plan(category):
    if category == "Underweight":
        return {
            "Goal": "Weight Gain", "Strategy": "Surplus (+300 kcal)",
            "Meals": {"Breakfast": "2 Paneer Parathas + Curd\n(or 3 Eggs + Toast)", "Lunch": "Rice Bowl + Dal Tadka\n+ Mixed Sabzi", "Snack": "Banana Shake with Nuts", "Dinner": "3 Rotis + Chicken Curry"}
        }
    elif category == "Normal":
        return {
            "Goal": "Maintenance", "Strategy": "Healthy Balance",
            "Meals": {"Breakfast": "Poha with Veggies\n(or Idli Sambar)", "Lunch": "2 Rotis + Dal + Sabzi\n+ Salad", "Snack": "Seasonal Fruit", "Dinner": "2 Multigrain Rotis\n+ Bottle Gourd Sabzi"}
        }
    elif category == "Overweight":
        return {
            "Goal": "Fat Loss", "Strategy": "Deficit (-500 kcal)",
            "Meals": {"Breakfast": "Oats Porridge\n(or Moong Dal Chilla)", "Lunch": "1 Roti + Dal + Salad\n(Cucumber/Tomato)", "Snack": "Roasted Makhana", "Dinner": "Grilled Paneer Salad\n(or Clear Soup)"}
        }
    else:
        return {
            "Goal": "Aggressive Loss", "Strategy": "Strict Low Carb",
            "Meals": {"Breakfast": "Veg Juice (Spinach)\n+ 2 Egg Whites", "Lunch": "1 Jowar Roti + Saag\n+ Cucumber Raita", "Snack": "Black Coffee + Almonds", "Dinner": "Lentil Soup (No Oil)\n+ Sautéed Veggies"}
        }

# Helper to generate HTML safely (Prevents Syntax Errors)
def make_meal_html(title, food, color, delay):
    return f"""
    <div class="pro-card" style="padding:0; border:none; background:transparent; margin-bottom:10px; animation-delay: {delay}s;">
        <div class="meal-card" style="border-left-color: {color};">
            <div class="meal-title">{title}</div>
            <div class="meal-food">{food}</div>
        </div>
    </div>
    """

# --- 4. Main Layout ---

# HTML Header
st.markdown("""
<div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
    <div style="font-size: 40px;">🧬</div>
    <div>
        <h3 style="color: white; margin: 0;">Health Metrics Pro</h3>
        <span style="color: #888; font-size: 12px;">Indian Standards • Mobile Optimized</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- COMPACT INPUT GRID (2 per row on Mobile) ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    gender = st.selectbox("Gender", ["Male", "Female"])
with c2:
    age = st.number_input("Age", 10, 90, 25)
with c3:
    weight = st.number_input("Wt (kg)", 30.0, 200.0, 70.0, format="%.1f")
with c4:
    h_ft = st.number_input("Ht (Ft)", 3, 7, 5)

# Row 2
c5, c6, c7 = st.columns([1, 2, 1]) 
with c5:
    h_in = st.number_input("Ht (In)", 0, 11, 7)
with c6:
    activity = st.selectbox("Activity Level", ["Sedentary", "Light Active", "Moderate Active", "Very Active"])
with c7:
    st.write("") 
    st.write("") 
    calc = st.button("GO")

# Calculation
height_cm = (h_ft * 12 + h_in) * 2.54

if calc:
    bmi, tdee = get_metrics(weight, height_cm, age, gender, activity)
    cat, color = get_health_status(bmi)
    plan = get_diet_plan(cat)
    target = tdee - 500 if cat in ["Overweight", "Obese"] else (tdee + 300 if cat == "Underweight" else tdee)

    st.markdown("---")
    
    # 1. METRICS ROW
    st.markdown(f"""
    <div style="display: flex; gap: 10px; margin-bottom: 15px;">
        <div class="pro-card" style="flex:1; text-align:center; padding:15px; animation-delay: 0.1s;">
            <div class="metric-lbl">BMI</div>
            <div class="metric-val" style="color: {color}">{bmi:.1f}</div>
            <div style="color:{color}; font-size:11px; font-weight:600">{cat}</div>
        </div>
        <div class="pro-card" style="flex:1; text-align:center; padding:15px; animation-delay: 0.2s;">
            <div class="metric-lbl">TDEE</div>
            <div class="metric-val">{tdee}</div>
            <div style="color:#888; font-size:11px;">kcal/day</div>
        </div>
        <div class="pro-card" style="flex:1; text-align:center; padding:15px; animation-delay: 0.3s;">
            <div class="metric-lbl">TARGET</div>
            <div class="metric-val" style="color:#FFF">{target}</div>
            <div style="color:#888; font-size:11px;">Goal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. MEAL STACKS (Grid Layout)
    st.markdown("#### 📅 Diet Plan")
    m = plan['Meals']
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown(make_meal_html("🍳 Breakfast", m['Breakfast'], "#FFD700", "0.4"), unsafe_allow_html=True)
        st.markdown(make_meal_html("🍎 Snack", m['Snack'], "#FF6B6B", "0.5"), unsafe_allow_html=True)
        
    with col_b:
        st.markdown(make_meal_html("🍛 Lunch", m['Lunch'], "#4FC3F7", "0.4"), unsafe_allow_html=True)
        st.markdown(make_meal_html("🍲 Dinner", m['Dinner'], "#9575CD", "0.5"), unsafe_allow_html=True)

st.markdown("<div style='text-align:center; color:#444; font-size:11px; margin-top:30px;'>NEON FIX / BROKENERD © 2025</div>", unsafe_allow_html=True)
