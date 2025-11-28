import streamlit as st

def get_indian_bmi_category(bmi):
    """
    Returns the category based on Asian/Indian BMI Standards.
    Source: Ministry of Health & Family Welfare / WHO Asian guidelines.
    """
    if bmi < 18.5:
        return "Underweight", "blue"
    elif 18.5 <= bmi <= 22.9:
        return "Normal Range", "green"
    elif 23.0 <= bmi <= 24.9:
        return "Overweight", "orange"
    else:
        return "Obese", "red"

def get_diet_plan(category):
    """
    Provides general Indian diet suggestions based on BMI category.
    """
    plans = {
        "Underweight": {
            "Focus": "Calorie Surplus & Protein",
            "Breakfast": "2 Aloo/Paneer Parathas with Curd OR 3 Eggs + Toast + Full Cream Milk.",
            "Lunch": "Jeera Rice, Yellow Dal tadka (with Ghee), Mixed Sabzi, Salad.",
            "Snack": "Banana Shake with nuts / Chana Chaat.",
            "Dinner": "3 Rotis with Paneer Butter Masala or Chicken Curry + Rice.",
            "Tip": "Add healthy fats like Ghee and nuts to your meals."
        },
        "Normal Range": {
            "Focus": "Maintenance & Balance",
            "Breakfast": "Poha/Upma with lots of veggies OR Idli Sambar.",
            "Lunch": "2 Rotis, Seasonal Sabzi, Dal, Curd, Salad.",
            "Snack": "Fruit (Apple/Papaya) or Green Tea.",
            "Dinner": "2 Multigrain Rotis, Lauki/Torai Sabzi, Dal.",
            "Tip": "Maintain hydration and stick to home-cooked meals."
        },
        "Overweight": {
            "Focus": "Calorie Deficit & High Fiber",
            "Breakfast": "Oats Upma / Daliya with veggies OR Moong Dal Chilla.",
            "Lunch": "1-2 Multigrain Rotis, Boiled Dal (less oil), Big bowl of Salad.",
            "Snack": "Roasted Makhana or Buttermilk (Chaas).",
            "Dinner": "Grilled Paneer/Chicken Salad or Papaya + Soup (Avoid heavy carbs at night).",
            "Tip": "Replace white rice with brown rice or quinoa. Reduce sugar intake."
        },
        "Obese": {
            "Focus": "Strict Deficit, Low Carb & Movement",
            "Breakfast": "Vegetable Juice (Spinach/Cucumber) + 2 Boiled Eggs (Whites).",
            "Lunch": "1 Bajra/Jowar Roti, Leafy Greens (Saag), Cucumber Raita.",
            "Snack": "Green Tea + 5 Almonds.",
            "Dinner": "Lentil Soup / Clear Soup + Sautéed Vegetables.",
            "Tip": "Avoid sugar, fried foods, and refined flour (Maida) completely."
        }
    }
    return plans.get(category, {})

# --- App Layout ---
st.set_page_config(page_title="Indian Health & BMI Tracker", page_icon="🥗")

st.title("🇮🇳 Indian BMI Calculator & Diet Planner")
st.write("Calculate your BMI based on **Asian/Indian Standards** and get a localized diet plan.")

# --- Input Section ---
col1, col2 = st.columns(2)

with col1:
    weight = st.number_input("Enter Weight (kg)", min_value=1.0, value=70.0, step=0.1)

with col2:
    height_unit = st.radio("Height Unit", ["Centimeters", "Feet & Inches"])
    
    if height_unit == "Centimeters":
        height_cm = st.number_input("Enter Height (cm)", min_value=50.0, value=170.0)
        height_m = height_cm / 100
    else:
        c1, c2 = st.columns(2)
        with c1:
            feet = st.number_input("Feet", min_value=1, value=5)
        with c2:
            inches = st.number_input("Inches", min_value=0, value=6)
        # Convert feet/inches to meters
        height_m = ((feet * 12) + inches) * 0.0254

# --- Calculation ---
if st.button("Calculate BMI"):
    if height_m > 0:
        bmi = weight / (height_m ** 2)
        category, color = get_indian_bmi_category(bmi)
        
        st.divider()
        
        # Display Results
        st.markdown(f"### Your BMI is: **{bmi:.2f}**")
        st.markdown(f"Category: <span style='color:{color}; font-weight:bold; font-size:20px'>{category}</span>", unsafe_allow_html=True)
        
        # Indian Standards Note
        st.info("ℹ️ **Note:** Indian medical standards define 'Overweight' starting at BMI 23.0, which is stricter than the global standard (25.0) due to higher genetic risks.")
        
        # Diet Plan Section
        st.divider()
        st.subheader(f"🥗 Suggested Diet Plan for: {category}")
        
        plan = get_diet_plan(category)
        
        st.markdown(f"**Goal:** {plan['Focus']}")
        
        c_breakfast, c_lunch = st.columns(2)
        c_snack, c_dinner = st.columns(2)
        
        with c_breakfast:
            st.success(f"**🍳 Breakfast:**\n\n{plan['Breakfast']}")
        with c_lunch:
            st.warning(f"**🍛 Lunch:**\n\n{plan['Lunch']}")
        with c_snack:
            st.info(f"**🍎 Snack:**\n\n{plan['Snack']}")
        with c_dinner:
            st.error(f"**🍲 Dinner:**\n\n{plan['Dinner']}")
            
        st.markdown(f"**💡 Pro Tip:** {plan['Tip']}")
        
    else:
        st.error("Please enter a valid height.")