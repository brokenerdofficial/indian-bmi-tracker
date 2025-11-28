import streamlit as st

# --- 1. Page Configuration (Wide Layout for Desktop, Auto-Stack for Mobile) ---
st.set_page_config(
    page_title="BodyMetrics Professional",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. Professional Design System (CSS) ---
st.markdown("""
<style>
    /* IMPORT CLEAN FONT */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --primary: #2563EB; /* Professional Blue */
        --bg-color: #F8FAFC; /* Light Slate Background */
        --card-bg: #FFFFFF;
        --text-dark: #1E293B;
        --text-gray: #64748B;
        --border: #E2E8F0;
    }

    /* GENERAL APP STYLING */
    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
    }
    
    /* HIDE DEFAULT STREAMLIT ELEMENTS */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* INPUT FIELDS - CLEAN & SHARP */
    .stNumberInput input, .stSelectbox div {
        background-color: white;
        color: var(--text-dark);
        border-radius: 8px;
        border: 1px solid var(--border);
    }

    /* CARD SYSTEM (Used for all results) */
    .pro-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05); /* Subtle professional shadow */
        height: 100%;
        transition: transform 0.2s ease;
    }
    .pro-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* TYPOGRAPHY */
    h1, h2, h3 { color: var(--text-dark); font-weight: 700; letter-spacing: -0.5px; }
    p { color: var(--text-gray); font-size: 15px; line-height: 1.6; }
    
    .metric-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--text-gray);
        font-weight: 600;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: var(--text-dark);
    }
    .metric-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 8px;
    }

    /* RESPONSIVE GRID FOR MEALS */
    .meal-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }
    .meal-item {
        background: #F8FAFC;
        border-left: 4px solid var(--primary);
        padding: 16px;
        border-radius: 8px;
    }

    /* BUTTON STYLING */
    div.stButton > button {
        background-color: var(--primary);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.2s;
    }
    div.stButton > button:hover {
        background-color: #1D4ED8; /* Darker Blue */
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Medical Logic (Backend) ---

def get_clinical_data(bmi):
    # Returns: Category, Hex Color, Text Color (for contrast)
    if bmi < 18.5: return "Underweight", "#DBEAFE", "#1E40AF" # Light Blue bg, Dark Blue text
    elif 18.5 <= bmi <= 22.9: return "Normal Weight", "#DCFCE7", "#166534" # Green
    elif 23.0 <= bmi <= 24.9: return "Overweight", "#FEF3C7", "#92400E" # Yellow/Orange
    else: return "Obese", "#FEE2E2", "#991B1B" # Red

def calculate_metrics(weight, height_cm, age, gender, activity):
    # 1. BMI
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    
    # 2. TDEE (Mifflin-St Jeor)
    bmr = (10 * weight) + (6.25 * height_cm) - (5 * age) + (5 if gender == "Male" else -161)
    act_map = {
        "Sedentary (Office/Desk Job)": 1.2,
        "Lightly Active (1-3 days/week)": 1.375,
        "Moderately Active (3-5 days/week)": 1.55,
        "Very Active (6-7 days/week)": 1.725,
        "Extra Active (Physical Labor)": 1.9
    }
    tdee = int(bmr * act_map.get(activity, 1.2))
    
    return bmi, tdee

def get_diet_protocol(category):
    if category == "Underweight":
        return {
            "Protocol": "Caloric Surplus (+300 kcal)",
            "Focus": "Nutrient Density & Frequency",
            "Meals": [
                ("Breakfast", "2 Paneer Parathas + Curd", "High Protein/Carb"),
                ("Lunch", "Rice, Dal Tadka (Ghee), Mixed Veg", "Calorie Dense"),
                ("Snack", "Banana Shake with Nuts & Dates", "Healthy Fats"),
                ("Dinner", "3 Rotis + Chicken/Paneer Curry", "Sustained Energy")
            ]
        }
    elif category == "Normal Weight":
        return {
            "Protocol": "Maintenance",
            "Focus": "Macronutrient Balance",
            "Meals": [
                ("Breakfast", "Vegetable Poha/Upma or Idli", "Light Start"),
                ("Lunch", "2 Rotis, Dal, Seasonal Sabzi, Salad", "Fiber Rich"),
                ("Snack", "Whole Fruit or Green Tea", "Antioxidants"),
                ("Dinner", "Multigrain Roti + Lauki/Torai", "Easy Digestion")
            ]
        }
    elif category == "Overweight":
        return {
            "Protocol": "Caloric Deficit (-500 kcal)",
            "Focus": "Volume Eating & High Fiber",
            "Meals": [
                ("Breakfast", "Oats Porridge or Moong Dal Chilla", "Complex Carbs"),
                ("Lunch", "1 Roti + Dal + Large Salad Bowl", "Satiety Focus"),
                ("Snack", "Roasted Makhana or Buttermilk", "Low Calorie"),
                ("Dinner", "Grilled Protein Salad or Soup", "Light End")
            ]
        }
    else: # Obese
        return {
            "Protocol": "Aggressive Reduction",
            "Focus": "Low Carb & Anti-Inflammatory",
            "Meals": [
                ("Breakfast", "Veg Juice + Egg Whites", "Protein Kick"),
                ("Lunch", "Jowar Roti + Leafy Greens + Raita", "Low Glycemic"),
                ("Snack", "Green Tea + 5 Almonds", "Metabolism"),
                ("Dinner", "Lentil Soup + Sautéed Veggies", "No Heavy Carbs")
            ]
        }

# --- 4. UI Layout ---

# Header
st.markdown("<h3>🏥 BodyMetrics <span style='color:#2563EB'>Pro</span></h3>", unsafe_allow_html=True)
st.markdown("<p>Professional Health Assessment • Indian Standards</p>", unsafe_allow_html=True)
st.divider()

# --- INPUT SECTION (Responsive Columns) ---
# We use standard text/number inputs for precision
with st.container():
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    
    with c1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age (Years)", 15, 90, 25)
    
    with c2:
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 72.0, format="%.1f")
        activity = st.selectbox("Activity Level", [
            "Sedentary (Office/Desk Job)",
            "Lightly Active (1-3 days/week)",
            "Moderately Active (3-5 days/week)",
            "Very Active (6-7 days/week)",
            "Extra Active (Physical Labor)"
        ])
        
    with c3:
        height_ft = st.number_input("Height (Feet)", 3, 7, 5)
        height_in = st.number_input("Height (Inches)", 0, 11, 7)
        # Internal Calculation
        height_cm = (height_ft * 12 + height_in) * 2.54
        
    with c4:
        st.write("") # Spacer to align button
        st.write("") 
        if st.button("Generate Assessment"):
            calc_trigger = True
        else:
            calc_trigger = False

# --- 5. RESULTS SECTION ---
if calc_trigger:
    # Calculations
    bmi, tdee = calculate_metrics(weight, height_cm, age, gender, activity)
    cat_text, cat_bg, cat_color = get_clinical_data(bmi)
    diet_data = get_diet_protocol(cat_text)
    
    if cat_text in ["Overweight", "Obese"]: target_cals = tdee - 500
    elif cat_text == "Underweight": target_cals = tdee + 300
    else: target_cals = tdee

    st.divider()
    
    # METRICS ROW
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown(f"""
        <div class="pro-card">
            <div class="metric-label">Clinical BMI</div>
            <div class="metric-value">{bmi:.1f}</div>
            <div class="metric-badge" style="background-color: {cat_bg}; color: {cat_color};">
                {cat_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div class="pro-card">
            <div class="metric-label">Maintenance (TDEE)</div>
            <div class="metric-value">{tdee}</div>
            <p style="margin-top:5px; font-size:13px;">Daily calories to maintain weight</p>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""
        <div class="pro-card" style="border-color: #2563EB;">
            <div class="metric-label">Target Goal</div>
            <div class="metric-value" style="color: #2563EB;">{target_cals}</div>
            <p style="margin-top:5px; font-size:13px; color: #2563EB;"><b>{diet_data['Protocol']}</b></p>
        </div>
        """, unsafe_allow_html=True)

    # DIET PLAN ROW
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📋 Recommended Protocol")
    st.markdown(f"<p>Clinical Focus: <b>{diet_data['Focus']}</b></p>", unsafe_allow_html=True)
    
    # Constructing the Grid HTML
    grid_html = '<div class="meal-grid">'
    
    for meal_name, food, note in diet_data['Meals']:
        grid_html += f"""
        <div class="pro-card meal-item">
            <div class="metric-label">{meal_name}</div>
            <div style="font-weight: 600; color: #1E293B; margin-top: 4px;">{food}</div>
            <div style="font-size: 13px; color: #64748B; margin-top: 8px;">• {note}</div>
        </div>
        """
    
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 12px; border-top: 1px solid #E2E8F0; padding-top: 20px;">
    Assessment Tool v2.1 • Neon Fix / Brokenerd • Not for medical diagnosis
</div>
""", unsafe_allow_html=True)