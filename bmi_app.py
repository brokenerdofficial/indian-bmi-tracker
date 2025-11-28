import streamlit as st

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="NeuHealth Pro",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. Neumorphic Design System (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    :root {
        --bg-color: #E0E5EC;
        --text-main: #4A5568;
        --highlight: #ffffff;
        --shadow: #a3b1c6;
        --accent: #4D7CFE;
    }

    /* GLOBAL RESET */
    html, body, .stApp {
        background-color: var(--bg-color);
        font-family: 'Poppins', sans-serif;
        color: var(--text-main);
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* NEUMORPHIC CARD (OUTSET) */
    .neu-card {
        background-color: var(--bg-color);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 9px 9px 16px var(--shadow), 
                   -9px -9px 16px var(--highlight);
        margin-bottom: 25px;
        transition: transform 0.2s;
    }
    
    /* MEAL CARD SPECIFIC */
    .meal-card {
        background-color: var(--bg-color);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 6px 6px 10px var(--shadow), 
                   -6px -6px 10px var(--highlight);
        height: 100%; /* For grid alignment */
        border-left: 5px solid var(--accent);
    }

    /* INPUT CONTAINER (INSET) */
    .inset-container {
        border-radius: 15px;
        background: var(--bg-color);
        box-shadow: inset 6px 6px 10px var(--shadow), 
                    inset -6px -6px 10px var(--highlight);
        padding: 20px;
        margin-bottom: 20px;
    }

    /* TYPOGRAPHY */
    h1, h2, h3 { color: #2D3748; font-weight: 700; }
    p { line-height: 1.6; font-size: 14px; }
    .label-text { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #718096; }
    .big-number { font-size: 32px; font-weight: 800; color: #2D3748; }

    /* WIDGET OVERRIDES */
    .stSlider > div > div > div { background-color: var(--accent) !important; }
    .stSelectbox > div > div { 
        background-color: var(--bg-color); 
        border: none; 
        box-shadow: 5px 5px 10px var(--shadow), -5px -5px 10px var(--highlight);
        border-radius: 10px;
    }
    
    /* GRID LAYOUTS */
    .results-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    .meals-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* Stack on mobile, side-by-side on desktop */
        gap: 20px;
    }

    /* BUTTON */
    div.stButton > button {
        width: 100%;
        background-color: var(--bg-color);
        color: var(--accent);
        font-weight: 700;
        border: none;
        padding: 15px;
        border-radius: 50px;
        box-shadow: 6px 6px 10px var(--shadow), -6px -6px 10px var(--highlight);
        transition: all 0.2s;
    }
    div.stButton > button:active {
        box-shadow: inset 4px 4px 8px var(--shadow), inset -4px -4px 8px var(--highlight);
        transform: scale(0.98);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Logic & Data ---

def get_health_data(bmi):
    if bmi < 18.5: return "Underweight", "#3182CE" # Blue
    elif 18.5 <= bmi <= 22.9: return "Normal", "#38A169" # Green
    elif 23.0 <= bmi <= 24.9: return "Overweight", "#DD6B20" # Orange
    else: return "Obese", "#E53E3E" # Red

def calculate_tdee(weight, height_cm, age, gender, activity):
    # Mifflin-St Jeor
    bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) + (5 if gender == "Male" else -161)
    multipliers = {
        "Sedentary (Desk Job)": 1.2,
        "Light Active (1-3 days)": 1.375,
        "Moderate Active (3-5 days)": 1.55,
        "Very Active (6-7 days)": 1.725,
        "Extra Active (Physical Job)": 1.9
    }
    return int(bmr * multipliers.get(activity, 1.2))

def get_diet_stack(category):
    # Returns structured dictionary for the stacks
    if category == "Underweight":
        return {
            "Strategy": "Calorie Surplus (+300kcal)",
            "Tip": "Focus on liquid calories and healthy fats.",
            "Meals": {
                "Breakfast": "2 Paneer Parathas + Curd OR 4 Eggs + Toast.",
                "Lunch": "Rice bowl with Dal Tadka (Ghee), Mixed Veg, Salad.",
                "Snack": "Banana Shake with Dates & Nuts.",
                "Dinner": "3 Rotis with Chicken Curry or Paneer Butter Masala."
            }
        }
    elif category == "Normal":
        return {
            "Strategy": "Maintenance & Balance",
            "Tip": "Ensure sufficient protein intake (1g per kg bodyweight).",
            "Meals": {
                "Breakfast": "Poha/Upma with lots of veggies OR Idli Sambar.",
                "Lunch": "2 Phulkas, Seasonal Sabzi, Dal, Curd.",
                "Snack": "Fruit Platter (Papaya/Apple) or Green Tea.",
                "Dinner": "2 Multigrain Rotis, Bottle Gourd (Lauki) Sabzi."
            }
        }
    elif category == "Overweight":
        return {
            "Strategy": "Calorie Deficit (-500kcal)",
            "Tip": "Volume eating: Fill half your plate with vegetables.",
            "Meals": {
                "Breakfast": "Oats Porridge (No sugar) OR Moong Dal Chilla.",
                "Lunch": "1 Multigrain Roti, Boiled Dal, Big Bowl of Cucumber Salad.",
                "Snack": "Roasted Makhana or Buttermilk (Chaas).",
                "Dinner": "Grilled Paneer/Tofu Salad or Clear Soup."
            }
        }
    else: # Obese
        return {
            "Strategy": "Aggressive Deficit",
            "Tip": "Eliminate sugar, fried foods, and refined flour completely.",
            "Meals": {
                "Breakfast": "Spinach & Cucumber Juice + 2 Egg Whites.",
                "Lunch": "1 Jowar Roti, Leafy Greens (Saag), Raita.",
                "Snack": "Black Coffee or Green Tea + 5 Almonds.",
                "Dinner": "Lentil Soup with sautéed vegetables (No Rice/Roti)."
            }
        }

# --- 4. Main UI Layout ---

# Header
c1, c2 = st.columns([1, 6])
with c1:
    st.markdown("<h1 style='font-size: 50px;'>🧬</h1>", unsafe_allow_html=True)
with c2:
    st.markdown("<h1>NeuHealth <span style='color:#4D7CFE'>Pro</span></h1>", unsafe_allow_html=True)
    st.caption("Indian Metric Standard • Neumorphic Design")

st.write("")

# Inputs Container
st.markdown('<div class="neu-card">', unsafe_allow_html=True)
st.markdown("### 👤 User Profile")

col_a, col_b = st.columns(2)
with col_a:
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.slider("Age", 10, 90, 25)
with col_b:
    activity = st.selectbox("Activity", [
        "Sedentary (Desk Job)",
        "Light Active (1-3 days)",
        "Moderate Active (3-5 days)",
        "Very Active (6-7 days)",
        "Extra Active (Physical Job)"
    ])
    weight = st.slider("Weight (kg)", 30, 200, 72)

st.markdown("---")
st.markdown("### 📏 Height")
h1, h2 = st.columns(2)
with h1:
    ft = st.slider("Feet", 3, 7, 5)
with h2:
    inc = st.slider("Inches", 0, 11, 7)

# Calculation
height_cm = (ft * 12 + inc) * 2.54
height_m = height_cm / 100
st.markdown('</div>', unsafe_allow_html=True)

# Button
if st.button("CALCULATE PLAN"):
    
    # Process
    bmi = weight / (height_m ** 2)
    tdee = calculate_tdee(weight, height_cm, age, gender, activity)
    cat, color = get_health_data(bmi)
    data = get_diet_stack(cat)
    
    if cat in ["Overweight", "Obese"]: target = tdee - 500
    elif cat == "Underweight": target = tdee + 300
    else: target = tdee

    # --- RESULTS SECTION ---
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. Metrics Grid
    st.markdown(f"""
    <div class="results-grid">
        <div class="neu-card" style="text-align:center; border-bottom: 5px solid {color}">
            <div class="label-text">Your BMI</div>
            <div class="big-number" style="color: {color}">{bmi:.1f}</div>
            <div style="color: {color}; font-weight:600">{cat}</div>
        </div>
        <div class="neu-card" style="text-align:center;">
            <div class="label-text">TDEE</div>
            <div class="big-number">{tdee}</div>
            <div style="font-size:12px">Maintenance Cals</div>
        </div>
        <div class="neu-card" style="text-align:center;">
            <div class="label-text">Target Goal</div>
            <div class="big-number" style="color: #4D7CFE">{target}</div>
            <div style="font-size:12px">Daily Limit</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Strategy Banner (Inset Style)
    st.markdown(f"""
    <div class="inset-container">
        <h3 style="margin:0; color: {color}">Strategy: {data['Strategy']}</h3>
        <p style="margin-top: 5px; color: #666;">💡 {data['Tip']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 3. Meals Grid (The Stacks)
    st.markdown("### 🥗 Recommended Meal Plan")
    
    meals = data['Meals']
    
    # We use f-strings carefully to inject meal data into HTML
    st.markdown(f"""
    <div class="meals-grid">
        <div class="meal-card">
            <div class="label-text">🍳 BREAKFAST</div>
            <p style="font-weight: 500; margin-top: 10px;">{meals['Breakfast']}</p>
        </div>
        <div class="meal-card">
            <div class="label-text">🍛 LUNCH</div>
            <p style="font-weight: 500; margin-top: 10px;">{meals['Lunch']}</p>
        </div>
        <div class="meal-card">
            <div class="label-text">🍎 SNACK</div>
            <p style="font-weight: 500; margin-top: 10px;">{meals['Snack']}</p>
        </div>
        <div class="meal-card">
            <div class="label-text">🍲 DINNER</div>
            <p style="font-weight: 500; margin-top: 10px;">{meals['Dinner']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br><div style='text-align:center; color:#A0AEC0; font-size:12px;'>Neon Fix / Brokenerd © 2025</div>", unsafe_allow_html=True)