import streamlit as st
import os

# --- 1. Page Config ---
st.set_page_config(
    page_title="Health Metrics Pro",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. Advanced CSS (Mobile Grid + Animations) ---
st.markdown("""
<style>
    /* IMPORT FONT */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #0E1117; }

    /* --- ANIMATIONS --- */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translate3d(0, 20px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }

    /* --- MOBILE GRID SYSTEM (The Magic Fix) --- */
    /* This forces columns to stay side-by-side on mobile */
    @media (max-width: 640px) {
        div[data-testid="column"] {
            width: 50% !important;
            flex: 1 1 50% !important;
            min-width: 50% !important;
        }
    }
    
    /* INPUT STYLING */
    .stNumberInput input, .stSelectbox div, .stRadio label {
        color: #FFFFFF !important;
        background-color: #1E1E1E !important; 
        border: 1px solid #333 !important;
        border-radius: 8px !important;
    }
    .stSelectbox div:hover, .stNumberInput input:hover {
        border-color: #555 !important;
    }
    /* Hide label on mobile to save space if needed, or keep small */
    label { color: #888 !important; font-size: 12px !important; }

    /* --- CARD STYLING --- */
    .pro-card {
        background-color: #1E1E1E;
        border: 1px solid #333;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(255, 255, 255, 0.05);
        animation: fadeInUp 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }
    
    /* MEAL STACK CARD */
    .meal-card {
        background-color: #161B22; /* Slightly darker inner card */
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 15px;
        height: 100%;
        transition: transform 0.2s;
        border-left: 4px solid #4FC3F7; /* Default Accent */
    }
    .meal-card:hover {
        transform: translateY(-3px);
        border-color: #8B949E;
    }

    /* TEXT UTILS */
    .metric-val { font-size: 28px; font-weight: 700; color: #FFF; }
    .metric-lbl { font-size: 11px; text-transform: uppercase; color: #888; letter-spacing: 1px; }
    .meal-title { font-size: 12px; font-weight: 700; color: #888; text-transform: uppercase; margin-bottom: 5px; }
    .meal-food { font-size: 14px; color: #FFF; font-weight: 500; line-height: 1.4; }

    /* BUTTON */
    div.stButton > button {
        background-color: #FFF; color: #000; border-radius: 10px;
        padding: 12px; font-weight: 600; border: none; width: 100%;
        transition: all 0.2s;
        box-shadow: 0 0 10px rgba(255,255,255,0.2);
    }
    div.stButton > button:hover { transform: scale(1.02); background-color: #F0F0F0; }

    #MainMenu, header, footer { visibility: hidden; }
    
    .footer { text-align: center; color: #444; font-size: 11px; padding: 30px 0; margin-top: 20px; border-top: 1px solid #222; }
</style>
""", unsafe_allow_html=True)

# --- 3. Logic & Data ---

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
    # Returns structured data for the stacks
    if category == "Underweight":
        return {
            "Goal": "Weight Gain",
            "Strategy": "Surplus (+300 kcal)",
            "Meals": {
                "Breakfast": "2 Paneer Parathas + Curd\n(or 3 Eggs + Toast)",
                "Lunch": "Rice Bowl + Dal Tadka (Ghee)\n+ Mixed Sabzi",
                "Snack": "Banana Shake with Nuts\n(Almonds/Walnuts)",
                "Dinner": "3 Rotis + Chicken Curry\n(or Paneer Masala)"
            }
        }
    elif category == "Normal":
        return {
            "Goal": "Maintenance",
            "Strategy": "Healthy Balance",
            "Meals": {
                "Breakfast": "Poha with Veggies\n(or Idli Sambar)",
                "Lunch": "2 Rotis + Dal + Sabzi\n+ Bowl of Salad",
                "Snack": "Seasonal Fruit\n(or Green Tea)",
                "Dinner": "2 Multigrain Rotis\n+ Bottle Gourd Sabzi"
            }
        }
    elif category == "Overweight":
        return {
            "Goal": "Fat Loss",
            "Strategy": "Deficit (-500 kcal)",
            "Meals": {
                "Breakfast": "Oats Porridge (Water/Skim Milk)\n(or Moong Dal Chilla)",
                "Lunch": "1 Roti + Dal + Big Salad\n(Cucumber/Tomato)",
                "Snack": "Roasted Makhana\n(or Buttermilk)",
                "Dinner": "Grilled Paneer Salad\n(or Clear Soup)"
            }
        }
    else: # Obese
        return {
            "Goal": "Aggressive Loss",
            "Strategy": "Strict Low Carb",
            "Meals": {
                "Breakfast": "Vegetable Juice (Spinach)\n+ 2 Egg Whites",
                "Lunch": "1 Jowar Roti + Saag\n+ Cucumber Raita",
                "Snack": "Black Coffee\n+ 5 Soaked Almonds",
                "Dinner": "Lentil Soup (No Oil)\n+ Sautéed Veggies"
            }
        }

# --- 4. UI Layout ---

# Header
c_logo, c_title = st.columns([1,5])
with c_logo:
    if os.path.exists("logo.png"): st.image("logo.png", width=60)
    else: st.markdown("## 🧬")
with c_title:
    st.markdown("<h3 style='color:white; margin:0;'>Health Metrics Pro</h3>", unsafe_allow_html=True)
    st.caption("Indian Standards • Mobile Optimized")

st.markdown("---")

# --- MOBILE OPTIMIZED INPUT GRID ---
# Using 4 columns in one row -> On mobile CSS will wrap them to 2 per row (50% width)
st.markdown("#### 📝 Your Details")

# Row 1: Gender, Age, Weight, Height(Ft)
c1, c2, c3, c4 = st.columns(4)
with c1:
    gender = st.selectbox("Gender", ["Male", "Female"])
with c2:
    age = st.number_input("Age", 10, 90, 25)
with c3:
    weight = st.number_input("Wt (kg)", 30.0, 200.0, 70.0, format="%.1f")
with c4:
    h_ft = st.number_input("Ht (Ft)", 3, 7, 5)

# Row 2: Height(In), Activity (Activity takes 3 cols width on desktop to look good)
c5, c6 = st.columns([1, 3])
with c5:
    h_in = st.number_input("Ht (In)", 0, 11, 7)
with c6:
    activity = st.selectbox("Activity Level", ["Sedentary", "Light Active", "Moderate Active", "Very Active"])

# Calculation
height_cm = (h_ft * 12 + h_in) * 2.54

st.write("")
if st.button("CALCULATE PLAN"):
    
    bmi, tdee = get_metrics(weight, height_cm, age, gender, activity)
    cat, color = get_health_status(bmi)
    plan = get_diet_plan(cat)
    
    if cat in ["Overweight", "Obese"]: target = tdee - 500
    elif cat == "Underweight": target = tdee + 300
    else: target = tdee

    st.markdown("---")
    
    # 1. METRICS ROW
    st.markdown(f"""
    <div style="display: flex; gap: 10px; margin-bottom: 20px;">
        <div class="pro-card" style="flex:1; text-align:center; padding:15px; animation-delay: 0.1s;">
            <div class="metric-lbl">BMI SCORE</div>
            <div class="metric-val" style="color: {color}">{bmi:.1f}</div>
            <div style="color:{color}; font-size:12px; font-weight:600">{cat}</div>
        </div>
        <div class="pro-card" style="flex:1; text-align:center; padding:15px; animation-delay: 0.2s;">
            <div class="metric-lbl">TDEE</div>
            <div class="metric-val">{tdee}</div>
            <div style="color:#888; font-size:12px;">Maintenance</div>
        </div>
        <div class="pro-card" style="flex:1; text-align:center; padding:15px; animation-delay: 0.3s;">
            <div class="metric-lbl">TARGET</div>
            <div class="metric-val" style="color:#FFF">{target}</div>
            <div style="color:#888; font-size:12px;">kcal/day</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. DIET STRATEGY
    st.markdown(f"""
    <div class="pro-card" style="padding: 15px; display:flex; justify-content:space-between; align-items:center; animation-delay: 0.4s;">
        <div>
            <div class="metric-lbl">GOAL STRATEGY</div>
            <div style="color:#FFF; font-weight:600;">{plan['Goal']} ({plan['Strategy']})</div>
        </div>
        <div style="font-size:24px;">🥗</div>
    </div>
    """, unsafe_allow_html=True)

    # 3. MEAL STACKS (Grid Layout)
    st.markdown("#### 📅 Daily Meal Stack")
    
    m = plan['Meals']
    
    # Create 2 Columns for the 4 meals
    mc1, mc2 = st.columns(2)
    
    with mc1:
        # Breakfast
        st.markdown(f"""
        <div class="pro-card" style="padding:0; border:none; background:transparent; animation-delay: 0.5s;">
            <div class="meal-card" style="border-left-color: #FFD700;">
                <div class="meal-title">🍳 Breakfast</div>
                <div class="meal-food">{m['Breakfast']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Snack
        st.markdown(f"""
        <div class="pro-card" style="padding:0; border:none; background:transparent; margin-top:15px; animation-delay: 0.6s;">
            <div class="meal-card" style="border-left-color: #FF6B6B;">
                <div class="meal-title">🍎 Snack</div>
                <div class="meal-food">{m['Snack']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with mc2:
        # Lunch
        st.markdown(f"""
        <div class="pro-card" style="padding:0; border:none; background:transparent; animation-delay: 0.5s;">
            <div class="meal-card" style="border-left-color: #4FC3F7;">
                <div class="meal-title">🍛 Lunch</div>
                <div class="meal-food">{m['Lunch']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Dinner
        st.markdown(f"""
        <div class="pro-card" style="padding:0; border:none; background:transparent; margin-top:15px; animation-delay: 0.6s;">
            <div class="meal-card" style="border-left-color: #9575CD;">
                <div class="meal-title">🍲 Dinner</div>
                <div class="meal-food">{m['Dinner']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>NEON FIX / BROKENERD © 2025<br>Made for India 🇮🇳</div>", unsafe_allow_html=True)
