import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(
    page_title="NutriNest",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CLEAN PASTEL UI =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Background - Soft Cream */
.stApp {
    background-color: #F8F5F0 !important;
}

/* Force dark text on main area */
.main p, .main span, .main div, .main label,
.main h1, .main h2, .main h3, .main h4 {
    color: #1C1917 !important;
}

/* Sidebar - Deep Green */
section[data-testid="stSidebar"] {
    background-color: #2F5D50 !important;
}
section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-weight: 500 !important;
}

/* Input fields - Dark text force */
input, textarea {
    color: #1C1917 !important;
    background-color: #FFFFFF !important;
}
.stTextInput input, .stNumberInput input {
    color: #1C1917 !important;
    background-color: #FFFFFF !important;
    border: 1.5px solid #D6D3D1 !important;
    border-radius: 8px !important;
}
.stTextInput input::placeholder {
    color: #9CA3AF !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    color: #1C1917 !important;
    background-color: #FFFFFF !important;
}

/* Cards */
.card {
    background: #FFFFFF !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    border: 1px solid #E7E5E4 !important;
    box-shadow: 0 4px 18px rgba(0,0,0,0.04) !important;
    margin-bottom: 1.2rem !important;
}
.card h3 {
    color: #2F5D50 !important;
    margin: 0 0 0.3rem 0 !important;
    font-weight: 700 !important;
}
.card-value {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #C48A2A !important;
    margin: 0.5rem 0 !important;
}

/* Meal cards */
.meal-card {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    padding: 1.4rem 1.6rem !important;
    border-left: 5px solid #C48A2A !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.04) !important;
    margin-bottom: 1.3rem !important;
}
.meal-card h3 {
    color: #2F5D50 !important;
    margin-top: 0 !important;
}

/* Pills */
.pill {
    display: inline-block !important;
    background: #E8F0EB !important;
    color: #1F4A3C !important;
    padding: 0.3rem 0.8rem !important;
    border-radius: 20px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    margin: 3px 4px 0 0 !important;
}

/* Buttons */
.stButton > button {
    background-color: #C48A2A !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
.stButton > button:hover {
    background-color: #A87320 !important;
    color: white !important;
}
.stButton > button * {
    color: white !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #2F5D50 !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    color: #57534E !important;
}

/* Titles */
.big-title {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    color: #2F5D50 !important;
    margin-bottom: 0.2rem !important;
}
.subtitle {
    color: #57534E !important;
    font-size: 1.05rem !important;
    margin-bottom: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ===================== LOAD RECIPES =====================
@st.cache_data
def load_recipes():
    for path in ["data/recipes.csv", "./data/recipes.csv", "recipes.csv"]:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                if len(df) > 0:
                    df.columns = [str(c).lower().strip().replace(" ", "_") for c in df.columns]
                    return df
            except:
                pass
    # Fallback
    return pd.DataFrame([
        {"recipe_name": "Chicken Karahi", "meal_type": "lunch", "cuisine": "Pakistani", "calories": 320, "protein_g": 30, "ingredients": "Chicken, Tomato, Onion, Spices"},
        {"recipe_name": "Chicken Biryani", "meal_type": "lunch", "cuisine": "Pakistani", "calories": 480, "protein_g": 27, "ingredients": "Chicken, Rice, Yogurt, Spices"},
        {"recipe_name": "Daal Chawal", "meal_type": "dinner", "cuisine": "Pakistani", "calories": 420, "protein_g": 16, "ingredients": "Lentils, Rice, Onion, Spices"},
        {"recipe_name": "Vegetable Omelette", "meal_type": "breakfast", "cuisine": "Pakistani", "calories": 220, "protein_g": 14, "ingredients": "Eggs, Onion, Tomato"},
        {"recipe_name": "Chana Chaat", "meal_type": "snack", "cuisine": "Pakistani", "calories": 260, "protein_g": 11, "ingredients": "Chickpeas, Onion, Tomato, Lemon"},
        {"recipe_name": "Chicken Tikka", "meal_type": "dinner", "cuisine": "Pakistani", "calories": 290, "protein_g": 36, "ingredients": "Chicken, Yogurt, Spices"},
        {"recipe_name": "Palak Paneer", "meal_type": "lunch", "cuisine": "Pakistani", "calories": 350, "protein_g": 18, "ingredients": "Spinach, Paneer, Spices"},
        {"recipe_name": "Aloo Keema", "meal_type": "dinner", "cuisine": "Pakistani", "calories": 350, "protein_g": 25, "ingredients": "Minced Meat, Potato, Spices"},
    ])

recipes_df = load_recipes()

# ===================== NUTRITION =====================
def calculate_nutrition(age, sex, height_cm, weight_kg, activity, goal):
    if sex.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    mult = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725, "very_active": 1.9}
    tdee = bmr * mult.get(activity, 1.55)
    if goal == "weight_loss":
        target = tdee - 400
    elif goal == "weight_gain":
        target = tdee + 300
    else:
        target = tdee
    return {
        "BMI": round(weight_kg / ((height_cm / 100) ** 2), 1),
        "Target": round(target),
        "Protein": round(target * 0.25 / 4),
        "Carbs": round(target * 0.50 / 4),
        "Fat": round(target * 0.25 / 9),
        "Fiber": 30
    }

# ===================== SESSION STATE =====================
if "family" not in st.session_state:
    st.session_state.family = []
if "logs" not in st.session_state:
    st.session_state.logs = []
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = None
if "workouts" not in st.session_state:
    st.session_state.workouts = {}
if "pantry" not in st.session_state:
    st.session_state.pantry = []
if "budget" not in st.session_state:
    st.session_state.budget = {"daily": 900}

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("### 🥗 NutriNest")
    st.caption("Family Nutrition & Fitness")
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Dashboard", "Meal Plan", "Recipes", "Pantry", "Workout", "Progress"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("#### Family Members")

    with st.expander("➕ Add / Update Member", expanded=False):
        with st.form("add_member"):
            name = st.text_input("Name", "Father")
            c1, c2 = st.columns(2)
            with c1:
                age = st.number_input("Age", 10, 90, 40)
                sex = st.selectbox("Sex", ["male", "female"])
            with c2:
                height = st.number_input("Height (cm)", 120, 220, 170)
                weight = st.number_input("Weight (kg)", 30, 180, 70)
            goal = st.selectbox("Goal", ["weight_loss", "maintenance", "weight_gain"])
            activity = st.selectbox("Activity Level", ["sedentary", "light", "moderate", "active", "very_active"])
            location = st.radio("Workout Location", ["home", "gym"], horizontal=True)
            equipment = st.multiselect("Equipment", ["none", "yoga_mat", "dumbbells", "resistance_bands", "full_gym"], default=["yoga_mat"])
            if st.form_submit_button("Save Member", use_container_width=True):
                nutri = calculate_nutrition(age, sex, height, weight, activity, goal)
                member = {
                    "name": name, "age": age, "sex": sex,
                    "height_cm": height, "weight_kg": weight,
                    "goal": goal, "activity_level": activity,
                    "workout_location": location, "equipment": equipment,
                    "nutrition": nutri, "allergies": ["none"], "medical": ["none"]
                }
                st.session_state.family = [m for m in st.session_state.family if m["name"] != name]
                st.session_state.family.append(member)
                st.success(f"{name} saved!")

    if st.session_state.family:
        for m in st.session_state.family:
            st.write(f"**{m['name']}** — {m['nutrition']['Target']} kcal")

    st.markdown("---")
    st.session_state.budget["daily"] = st.number_input("Daily Budget (PKR)", 300, 5000, st.session_state.budget["daily"], 50)

# ===================== HEADER =====================
st.markdown('<div class="big-title">🥗 NutriNest</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart Family Nutrition • Shared Meals • Personalized Portions</div>', unsafe_allow_html=True)

# ===================== DASHBOARD =====================
if page == "Dashboard":
    if not st.session_state.family:
        st.info("Please add family members from the sidebar first.")
    else:
        st.subheader("Family Overview")
        cols = st.columns(min(len(st.session_state.family), 3))
        for i, m in enumerate(st.session_state.family):
            with cols[i % len(cols)]:
                n = m["nutrition"]
                st.markdown(f"""
                <div class="card">
                    <h3>{m['name']}</h3>
                    <p style="color:#57534E; margin:0;">{m['goal'].replace('_',' ').title()} • BMI {n['BMI']}</p>
                    <div class="card-value">{n['Target']} kcal</div>
                    <div>
                        <span class="pill">Protein {n['Protein']}g</span>
                        <span class="pill">Carbs {n['Carbs']}g</span>
                        <span class="pill">Fat {n['Fat']}g</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Recipes", len(recipes_df))
        c2.metric("Pantry Items", len(st.session_state.pantry))
        c3.metric("Daily Budget", f"Rs {st.session_state.budget['daily']}")

# ===================== MEAL PLAN =====================
elif page == "Meal Plan":
    st.subheader("Shared Family Meal Plan")
    if not st.session_state.family:
        st.warning("Please add family members first.")
    else:
        if st.button("Generate Meal Plan", type="primary", use_container_width=True):
            plan = {
                "day": "Day 1",
                "meals": [
                    {"meal": "Breakfast", "main": "Vegetable Omelette + Roti", "sides": ["Cucumber", "Tea"], "calories": 380, "protein": 22, "carbs": 28, "fat": 18, "description": "Light high-protein breakfast."},
                    {"meal": "Lunch", "main": "Chicken Karahi + Brown Rice", "sides": ["Salad", "Raita"], "calories": 520, "protein": 38, "carbs": 45, "fat": 18, "description": "Home-style karahi with less oil."},
                    {"meal": "Snack", "main": "Chana Chaat", "sides": ["Lemon"], "calories": 240, "protein": 11, "carbs": 38, "fat": 5, "description": "Fiber-rich healthy snack."},
                    {"meal": "Dinner", "main": "Dal + 2 Rotis", "sides": ["Raita"], "calories": 480, "protein": 22, "carbs": 62, "fat": 14, "description": "Comforting balanced dinner."},
                ]
            }
            st.session_state.meal_plan = plan

        if st.session_state.meal_plan:
            for meal in st.session_state.meal_plan["meals"]:
                st.markdown(f"""
                <div class="meal-card">
                    <h3>{meal['meal']} — {meal['main']}</h3>
                    <p style="color:#44403C;">{meal['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Calories", f"{meal['calories']} kcal")
                c2.metric("Protein", f"{meal['protein']} g")
                c3.metric("Carbs", f"{meal['carbs']} g")
                c4.metric("Fat", f"{meal['fat']} g")
                st.write("**Sides:** " + ", ".join(meal["sides"]))
                st.markdown("---")

# ===================== RECIPES =====================
elif page == "Recipes":
    st.subheader("Recipe Browser")
    search = st.text_input("Search recipes")
    filtered = recipes_df.copy()
    if search:
        filtered = filtered[filtered["recipe_name"].astype(str).str.lower().str.contains(search.lower(), na=False)]
    st.write(f"**{len(filtered)} recipes found**")
    for _, row in filtered.head(15).iterrows():
        with st.expander(f"{row.get('recipe_name', 'Unknown')}  •  {row.get('calories', '—')} kcal"):
            if "ingredients" in row:
                st.write(str(row["ingredients"])[:500])

# ===================== PANTRY =====================
elif page == "Pantry":
    st.subheader("My Pantry")
    item = st.text_input("Add item (chicken, daal, rice...)")
    if st.button("Add to Pantry") and item.strip():
        if item.lower() not in st.session_state.pantry:
            st.session_state.pantry.append(item.lower())
            st.success("Added")
    for i, p in enumerate(st.session_state.pantry):
        col1, col2 = st.columns([6, 1])
        col1.write(f"• {p.title()}")
        if col2.button("🗑️", key=f"del{i}"):
            st.session_state.pantry.pop(i)
            st.rerun()

# ===================== WORKOUT =====================
elif page == "Workout":
    st.subheader("Workout Plan")
    if not st.session_state.family:
        st.warning("Add family members first.")
    else:
        selected = st.selectbox("Member", [m["name"] for m in st.session_state.family])
        if st.button("Generate 7-Day Workout", type="primary"):
            st.session_state.workouts[selected] = [
                {"day": 1, "focus": "Full Body", "exercises": ["Squats 3×12", "Push-ups 3×10", "Walk 20 min"]},
                {"day": 2, "focus": "Rest", "exercises": []},
                {"day": 3, "focus": "Lower Body", "exercises": ["Lunges 3×10", "Glute Bridge 3×15"]},
                {"day": 4, "focus": "Rest", "exercises": []},
                {"day": 5, "focus": "Upper + Core", "exercises": ["Wall Push-ups 3×12", "Plank 30s"]},
                {"day": 6, "focus": "Cardio", "exercises": ["Brisk Walk 30 min"]},
                {"day": 7, "focus": "Recovery", "exercises": ["Stretching 15 min"]},
            ]
        if selected in st.session_state.workouts:
            for d in st.session_state.workouts[selected]:
                with st.expander(f"Day {d['day']}: {d['focus']}"):
                    if not d["exercises"]:
                        st.write("Rest day 💤")
                    else:
                        for e in d["exercises"]:
                            st.write(f"• {e}")

# ===================== PROGRESS =====================
elif page == "Progress":
    st.subheader("Progress Tracking")
    if not st.session_state.family:
        st.warning("Add family members first.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            m = st.selectbox("Member", [x["name"] for x in st.session_state.family], key="m1")
            meal = st.text_input("Meal", "Breakfast")
            status = st.selectbox("Status", ["followed", "different", "skipped"])
            if st.button("Log Meal"):
                st.session_state.logs.append({"member": m, "type": "meal", "item": meal, "status": status, "date": str(date.today())})
                st.success("Logged")
        with c2:
            m2 = st.selectbox("Member ", [x["name"] for x in st.session_state.family], key="m2")
            st2 = st.selectbox("Status ", ["completed", "skipped", "rest"])
            mins = st.number_input("Minutes", 0, 180, 30)
            if st.button("Log Workout"):
                st.session_state.logs.append({"member": m2, "type": "workout", "status": st2, "minutes": mins if st2 == "completed" else 0, "date": str(date.today())})
                st.success("Logged")
