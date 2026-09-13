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

st.markdown("""
<div style="background: linear-gradient(90deg, #134E3A, #166534); 
            color: white; 
            padding: 12px 20px; 
            border-radius: 12px; 
            font-weight: 600; 
            margin-bottom: 25px;
            text-align: center;">
    ✨ NutriNest — Fresh Professional Design Loaded
</div>
""", unsafe_allow_html=True)
# ===================== FRESH PROFESSIONAL DESIGN =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ===== MAIN BACKGROUND (Soft Cream Pastel) ===== */
.stApp {
    background-color: #F7F3EB !important;
}

/* ===== FORCE DARK TEXT EVERYWHERE ===== */
.stApp p, .stApp span, .stApp div, .stApp label,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
    color: #1F1F1F !important;
}

/* ===== SIDEBAR (Deep Sage) ===== */
section[data-testid="stSidebar"] {
    background-color: #2F5D50 !important;
}
section[data-testid="stSidebar"] * {
    color: #F4F7F5 !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    padding: 5px 0 !important;
}
section[data-testid="stSidebar"] label {
    color: #F4F7F5 !important;
}

/* ===== HEADER ===== */
.big-title {
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    color: #2F5D50 !important;
    letter-spacing: -0.8px !important;
    margin-bottom: 0.2rem !important;
}
.subtitle {
    color: #5C5C5C !important;
    font-size: 1.05rem !important;
    margin-bottom: 2.2rem !important;
    font-weight: 500 !important;
}

/* ===== CARDS (Soft Mint Pastel) ===== */
.card, .meal-card {
    background: #E8F0EB !important;
    border-radius: 18px !important;
    padding: 1.6rem !important;
    border: 1px solid #D1E0D7 !important;
    box-shadow: 0 4px 18px rgba(47, 93, 80, 0.06) !important;
    margin-bottom: 1.3rem !important;
}
.card h3, .meal-card h3 {
    color: #2F5D50 !important;
    font-weight: 700 !important;
    margin: 0 0 0.4rem 0 !important;
}

/* Value text */
.card-value {
    font-size: 1.85rem !important;
    font-weight: 700 !important;
    color: #C48A2A !important;
    margin: 0.6rem 0 !important;
}

/* ===== PILLS ===== */
.pill {
    display: inline-block !important;
    background: #D8EBE0 !important;
    color: #1F4A3C !important;
    padding: 0.32rem 0.85rem !important;
    border-radius: 20px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    margin: 4px 5px 0 0 !important;
    border: 1px solid #B8D6C6 !important;
}

/* ===== BUTTONS (Soft Gold) ===== */
.stButton > button {
    background-color: #C48A2A !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 11px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.4rem !important;
    box-shadow: 0 3px 10px rgba(196, 138, 42, 0.2) !important;
}
.stButton > button:hover {
    background-color: #A87320 !important;
    color: #FFFFFF !important;
}
.stButton > button * {
    color: #FFFFFF !important;
}

/* ===== INPUTS (Clean + Dark Text) ===== */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #1F1F1F !important;
    border: 1.5px solid #D6D0C4 !important;
    border-radius: 9px !important;
}
.stTextInput input::placeholder {
    color: #8A8A8A !important;
}
.stSelectbox [data-baseweb="select"] span {
    color: #1F1F1F !important;
}

/* ===== METRICS ===== */
[data-testid="stMetricValue"] {
    color: #2F5D50 !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    color: #5C5C5C !important;
}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader {
    background-color: #E8F0EB !important;
    color: #1F1F1F !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    border: 1px solid #D1E0D7 !important;
}
</style>
""", unsafe_allow_html=True)

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("### 🥗 NutriNest")
    st.caption("Family Nutrition & Fitness")
    st.markdown("---")
    page = st.radio("Navigation", ["Dashboard", "Meal Plan", "Recipes", "Pantry", "Workout", "Progress"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("#### Family Members")

    with st.expander("➕ Add / Update Member"):
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
            activity = st.selectbox("Activity", ["sedentary", "light", "moderate", "active", "very_active"])
            location = st.radio("Workout Location", ["home", "gym"], horizontal=True)
            equipment = st.multiselect("Equipment", ["none", "yoga_mat", "dumbbells", "resistance_bands", "full_gym"], default=["yoga_mat"])
            if st.form_submit_button("Save Member", use_container_width=True):
                nutri = calculate_nutrition(age, sex, height, weight, activity, goal)
                member = {"name": name, "age": age, "sex": sex, "height_cm": height, "weight_kg": weight,
                          "goal": goal, "activity_level": activity, "workout_location": location,
                          "equipment": equipment, "nutrition": nutri, "allergies": ["none"], "medical": ["none"]}
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

# ===================== PAGES =====================
if page == "Dashboard":
    if not st.session_state.family:
        st.info("Please add family members from the sidebar.")
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

elif page == "Meal Plan":
    st.subheader("Shared Family Meal Plan")
    if not st.session_state.family:
        st.warning("Add family members first.")
    else:
        if st.button("Generate Meal Plan", type="primary", use_container_width=True):
            plan = {
                "day": "Day 1",
                "meals": [
                    {"meal": "Breakfast", "main": "Vegetable Omelette + Roti", "sides": ["Cucumber", "Tea"], "calories": 380, "protein": 22, "carbs": 28, "fat": 18, "description": "Light and high-protein start to the day."},
                    {"meal": "Lunch", "main": "Chicken Karahi + Brown Rice", "sides": ["Salad", "Raita"], "calories": 520, "protein": 38, "carbs": 45, "fat": 18, "description": "Home-style karahi with less oil."},
                    {"meal": "Snack", "main": "Chana Chaat", "sides": ["Lemon"], "calories": 240, "protein": 11, "carbs": 38, "fat": 5, "description": "Fiber-rich and filling snack."},
                    {"meal": "Dinner", "main": "Dal + 2 Rotis", "sides": ["Raita"], "calories": 480, "protein": 22, "carbs": 62, "fat": 14, "description": "Comforting and balanced dinner."},
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
                c1,c2,c3,c4 = st.columns(4)
                c1.metric("Calories", f"{meal['calories']} kcal")
                c2.metric("Protein", f"{meal['protein']} g")
                c3.metric("Carbs", f"{meal['carbs']} g")
                c4.metric("Fat", f"{meal['fat']} g")
                st.write("**Sides:** " + ", ".join(meal["sides"]))
                st.markdown("---")

elif page == "Recipes":
    st.subheader("Recipe Browser")
    search = st.text_input("Search recipes")
    filtered = recipes_df.copy()
    if search:
        filtered = filtered[filtered["recipe_name"].astype(str).str.lower().str.contains(search.lower(), na=False)]
    st.write(f"**{len(filtered)} recipes**")
    for _, row in filtered.head(15).iterrows():
        with st.expander(f"{row.get('recipe_name','Unknown')}  •  {row.get('calories','—')} kcal"):
            if "ingredients" in row:
                st.write(str(row["ingredients"])[:500])

elif page == "Pantry":
    st.subheader("My Pantry")
    item = st.text_input("Add item")
    if st.button("Add") and item.strip():
        if item.lower() not in st.session_state.pantry:
            st.session_state.pantry.append(item.lower())
            st.success("Added")
    for i, p in enumerate(st.session_state.pantry):
        col1, col2 = st.columns([6,1])
        col1.write(f"• {p.title()}")
        if col2.button("🗑️", key=f"del{i}"):
            st.session_state.pantry.pop(i)
            st.rerun()

elif page == "Workout":
    st.subheader("Workout Plan")
    if not st.session_state.family:
        st.warning("Add family members first.")
    else:
        selected = st.selectbox("Member", [m["name"] for m in st.session_state.family])
        if st.button("Generate 7-Day Workout", type="primary"):
            st.session_state.workouts[selected] = [
                {"day":1, "focus":"Full Body", "exercises":["Squats 3×12", "Push-ups 3×10", "Walk 20 min"]},
                {"day":2, "focus":"Rest", "exercises":[]},
                {"day":3, "focus":"Lower Body", "exercises":["Lunges 3×10", "Glute Bridge 3×15"]},
                {"day":4, "focus":"Rest", "exercises":[]},
                {"day":5, "focus":"Upper + Core", "exercises":["Wall Push-ups 3×12", "Plank 30s"]},
                {"day":6, "focus":"Cardio", "exercises":["Brisk Walk 30 min"]},
                {"day":7, "focus":"Recovery", "exercises":["Stretching 15 min"]},
            ]
        if selected in st.session_state.workouts:
            for d in st.session_state.workouts[selected]:
                with st.expander(f"Day {d['day']}: {d['focus']}"):
                    if not d["exercises"]:
                        st.write("Rest day 💤")
                    else:
                        for e in d["exercises"]:
                            st.write(f"• {e}")

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
                st.session_state.logs.append({"member": m2, "type": "workout", "status": st2, "minutes": mins if st2=="completed" else 0, "date": str(date.today())})
                st.success("Logged")
