import streamlit as st

# --- 1. Page Configuration & Custom CSS ---
st.set_page_config(
    page_title="Indian Health & Diet Tracker",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI/UX, Cards, and Footer
st.markdown("""
    <style>
    /* Hide default Streamlit footer */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    
    /* Custom Footer Styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f3f6;
        color: #333;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #ddd;
        z-index: 100;
    }
    
    /* Card Styling for Results */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF4B4B;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Logic Functions ---

def get_indian_bmi_category(bmi):
    if bmi < 18.5: return "Underweight", "#3498db" # Blue
    elif 18.5 <= bmi <= 22.9: return "Normal", "#2ecc71" # Green
    elif 23.0 <= bmi <= 24.9: return "Overweight", "#f1c40f" # Yellow
    else: return "Obese", "#e74c3c" # Red

def calculate_tdee(weight, height_cm, age, gender, activity_level):
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) - 161
    
    multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    return int(bmr * multipliers.get(activity_level, 1.2))

def get_diet_plan(category):
    # (Same Logic as before, organized for Tabs)
    plans = {
        "Underweight": {
            "Goal": "Weight Gain",
            "Cals": "+300-500 surplus",
            "B": "2 Aloo Parathas + Curd OR 3 Eggs + Toast + Full Cream Milk",
            "L": "Jeera Rice, Yellow Dal (Ghee), Mixed Sabzi, Salad",
            "S": "Banana Shake with Nuts / Chana Chaat",
            "D": "3 Rotis + Paneer Butter Masala / Chicken Curry",
            "Tip": "Eat calorie-dense foods like nuts, ghee, and dairy."
        },
        "Normal": {
            "Goal": "Maintenance",
            "Cals": "Maintenance TDEE",
            "B": "Poha/Upma with Veggies OR Idli Sambar",
            "L": "2 Rotis, Seasonal Sabzi, Dal, Curd, Salad",
            "S": "Fruit (Apple/Papaya) or Green Tea",
            "D": "2 Multigrain Rotis, Lauki/Torai Sabzi, Dal",
            "Tip": "Focus on protein and fiber. Stay hydrated."
        },
        "Overweight": {
            "Goal": "Weight Loss",
            "Cals": "-500 deficit",
            "B": "Oats Upma / Daliya with Veggies OR Moong Dal Chilla",
            "L": "1-2 Multigrain Rotis, Boiled Dal, Big Salad",
            "S": "Roasted Makhana or Buttermilk (Chaas)",
            "D": "Grilled Paneer Salad or Papaya + Soup",
            "Tip": "Replace white rice with brown rice/quinoa. Walk 10k steps."
        },
        "Obese": {
            "Goal": "Strict Weight Loss",
            "Cals": "-500 to -700 deficit",
            "B": "Vegetable Juice (Spinach/Cucumber) + 2 Egg Whites",
            "L": "1 Jowar Roti, Leafy Greens (Saag), Cucumber Raita",
            "S": "Green Tea + 5 Almonds",
            "D": "Lentil Soup / Clear Soup + Sautéed Veggies",
            "Tip": "No sugar, no fried food, no maida. Intermittent fasting helps."
        }
    }
    return plans.get(category, plans["Normal"])

# --- 3. Sidebar (Inputs & Logo) ---

with st.sidebar:
    # --- LOGO SECTION ---
    # Replace the URL below with "logo.png" if you have a local file
    try:
        st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=100) 
    except:
        st.write("LOGO HERE")
    
    st.markdown("### ⚙️ User Details")
    
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    age = st.slider("Age", 10, 100, 25)
    
    st.markdown("---")
    
    weight = st.number_input("Weight (kg)", 1.0, 200.0, 70.0)
    
    height_mode = st.radio("Height Unit", ["Feet/Inches", "Centimeters"], horizontal=True)
    if height_mode == "Centimeters":
        height_cm = st.number_input("Height (cm)", 50, 250, 170)
        height_m = height_cm/100
    else:
        c1, c2 = st.columns(2)
        with c1: feet = st.number_input("Feet", 1, 8, 5)
        with c2: inches = st.number_input("Inches", 0, 11, 6)
        height_cm = (feet*12 + inches)*2.54
        height_m = height_cm/100

    st.markdown("---")
    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"])
    
    calculate_btn = st.button("🚀 Calculate Now", use_container_width=True)

# --- 4. Main Dashboard ---

st.title("🇮🇳 Indian Health Dashboard")
st.markdown("Your personalized guide to BMI, TDEE, and Indian Nutrition.")

if calculate_btn:
    # Calculations
    bmi = weight / (height_m ** 2)
    category, color = get_indian_bmi_category(bmi)
    tdee = calculate_tdee(weight, height_cm, age, gender, activity)
    
    if category in ["Overweight", "Obese"]:
        target_calories = tdee - 500
    elif category == "Underweight":
        target_calories = tdee + 300
    else:
        target_calories = tdee

    # --- RESULTS SECTION (Cards) ---
    st.markdown("### 📊 Your Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>BMI</h3>
            <h1 style="color: {color};">{bmi:.1f}</h1>
            <p><b>{category}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>TDEE</h3>
            <h1 style="color: #555;">{tdee}</h1>
            <p>Maintenance Cals</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Target</h3>
            <h1 style="color: #FF4B4B;">{target_calories}</h1>
            <p>Daily Goal</p>
        </div>
        """, unsafe_allow_html=True)

    # Visual Progress Bar for BMI
    st.write("")
    st.caption("BMI Scale (Asian Standard): Underweight < 18.5 | Normal 18.5-22.9 | Overweight > 23")
    st.progress(min(bmi / 40, 1.0)) # Normalized to max BMI of 40

    # --- DIET PLAN SECTION (Tabs) ---
    st.markdown("---")
    st.subheader(f"🥗 {category} Diet Plan")
    plan = get_diet_plan(category)
    
    st.info(f"💡 **Strategy:** {plan['Goal']} ({plan['Cals']}) — {plan['Tip']}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🍳 Breakfast", "🍛 Lunch", "🍎 Snack", "🍲 Dinner"])
    
    with tab1:
        st.success(plan['B'])
        st.image("https://images.unsplash.com/photo-1593560708920-638787c80880?auto=format&fit=crop&q=80&w=300", width=200) # Placeholder Food Image
    with tab2:
        st.warning(plan['L'])
    with tab3:
        st.info(plan['S'])
    with tab4:
        st.error(plan['D'])

else:
    # Default State (Before Calculation)
    st.info("👈 Please enter your details in the sidebar and click **Calculate Now**.")
    st.image("https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&q=80&w=1000", caption="Healthy Lifestyle")

# --- 5. Custom Footer ---
st.markdown("""
    <div class="footer">
        <p>❤️ Developed by <b>Brokenerd</b> | Medical Disclaimer: Consult a doctor before starting any strict diet.</p>
    </div>
    """, unsafe_allow_html=True)