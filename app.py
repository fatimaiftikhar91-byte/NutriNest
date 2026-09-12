import streamlit as st
import pandas as pd
import json
import os
from datetime import date
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NutriNest",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PROFESSIONAL UI ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp {
        background-color: #F7F4EE !important;
        font-family: 'Inter', sans-serif !important;
        color: #1C1917 !important;
    }

    /* Force dark text */
    .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, 
    .stApp h5, .stApp h6, .stApp label, .stApp span, .stApp div {
        color: #1C1917 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #14532D 0%, #166534 100%) !important;
    }
    [data-testid="stSidebar"] * {
        color: #F0FDF4 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    /* Titles */
    .main-title {
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        color: #14532D !important;
        letter-spacing: -0.8px !important;
        margin-bottom: 0.15rem !important;
    }
    .sub-title {
        color: #57534E !important;
        font-size: 1.05rem !important;
        margin-bottom: 2rem !important;
        font-weight: 500 !important;
    }

    /* Cards */
    .member-card {
        background: #FFFFFF !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        border: 1px solid #E7E5E4 !important;
        box-shadow: 0 4px 18px rgba(0,0,0,0.04) !important;
        margin-bottom: 1.2rem !important;
    }
    .member-card h3 {
        color: #14532D !important;
        margin: 0 0 0.3rem 0 !important;
    }

    .plate-card {
        background: #FFFFFF !important;
        border-radius: 14px !important;
        padding: 1.4rem 1.6rem !important;
        border-left: 5px solid #D97706 !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04) !important;
        margin-bottom: 1.3rem !important;
    }
    .plate-card h3 {
        color: #14532D !important;
        margin-top: 0 !important;
    }

    /* Macro pills */
    .macro-box {
        background: #ECFDF5 !important;
        color: #065F46 !important;
        border-radius: 50px !important;
        padding: 0.35rem 0.8rem !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        display: inline-block !important;
        margin: 4px 5px 0 0 !important;
        border: 1px solid #A7F3D0 !important;
    }

    /* Buttons */
    .stButton > button {
        background: #D97706 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.55rem 1.3rem !important;
    }
    .stButton > button:hover {
        background: #B45309 !important;
        color: white !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #14532D !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #57534E !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD RECIPES ----------------
@st.cache_data
def load_recipes():
    possible_paths = ["data/recipes.csv", "./data/recipes.csv", "recipes.csv"]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                if len(df) > 0:
                    df.columns = [str(c).lower().strip().replace(" ", "_") for c in df.columns]
                    
                    # Standardize column names
                    rename_map = {
                        "name": "recipe_name",
                        "recipe": "recipe_name",
                        "mealtype": "meal_type",
                        "calorie": "calories",
                        "protein": "protein_g",
                        "carbs": "carbs_g",
                        "fat": "fat_g"
                    }
                    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
                    
                    if "recipe_name" not in df.columns and len(df.columns) > 0:
                        df = df.rename(columns={df.columns[0]: "recipe_name"})
                    
                    return df
            except Exception as e:
                st.warning(f"Could not load {path}: {e}")
    
    # Fallback built-in recipes
    data = [
        {"recipe_name": "Chicken Karahi", "meal_type": "lunch", "cuisine": "Pakistani", "calories": 320, "protein_g": 30, "carbs_g": 10, "fat_g": 18, "ingredients": "Chicken, Tomato, Onion, Ginger, Garlic, Spices, Oil"},
        {"recipe_name": "Chicken Biryani", "meal_type": "lunch", "cuisine": "Pakistani", "calories": 480, "protein_g": 27, "carbs_g": 58, "fat_g": 15, "ingredients": "Chicken, Rice, Yogurt, Onion, Spices, Oil"},
        {"recipe_name": "Daal Chawal", "meal_type": "dinner", "cuisine": "Pakistani", "calories": 420, "protein_g": 16, "carbs_g": 70, "fat_g": 9, "ingredients": "Lentils, Rice, Onion, Tomato, Spices, Oil"},
        {"recipe_name": "Vegetable Omelette", "meal_type": "breakfast", "cuisine": "Pakistani", "calories": 220, "protein_g": 14, "carbs_g": 5, "fat_g": 15, "ingredients": "Eggs, Onion, Tomato, Green Chili, Oil"},
        {"recipe_name": "Chana Chaat", "meal_type": "snack", "cuisine": "Pakistani", "calories": 260, "protein_g": 11, "carbs_g": 42, "fat_g": 5, "ingredients": "Chickpeas, Tomato, Onion, Cucumber, Lemon, Chaat Masala"},
        {"recipe_name": "Chicken Tikka", "meal_type": "dinner", "cuisine": "Pakistani", "calories": 290, "protein_g": 36, "carbs_g": 6, "fat_g": 13, "ingredients": "Chicken, Yogurt, Lemon, Ginger, Garlic, Tikka Spices"},
        {"recipe_name": "Aloo Keema", "meal_type": "dinner", "cuisine": "Pakistani", "calories": 350, "protein_g": 25, "carbs_g": 22, "fat_g": 18, "ingredients": "Minced Meat, Potatoes, Onion, Tomato, Spices, Oil"},
        {"recipe_name": "Palak Paneer", "meal_type": "lunch", "cuisine": "Pakistani", "calories": 350, "protein_g": 18, "carbs_g": 15, "fat_g": 25, "ingredients": "Spinach, Paneer, Onion, Tomato, Spices, Oil"},
        {"recipe_name": "Seekh Kabab", "meal_type": "dinner", "cuisine": "Pakistani", "calories": 300, "protein_g": 28, "carbs_g": 5, "fat_g": 18, "ingredients": "Minced Meat, Onion, Ginger, Garlic, Spices"},
        {"recipe_name": "Raita", "meal_type": "side", "cuisine": "Pakistani", "calories": 100, "protein_g": 4, "carbs_g": 8, "fat_g": 5, "ingredients": "Yogurt, Cucumber, Onion, Spices"},
    ]
    return pd.DataFrame(data)

recipes_df = load_recipes()

# ---------------- GROQ CLIENT ----------------
def get_client():
    key = os.environ.get("GROQ_API_KEY")
    if key:
        try:
            from groq import Groq
            return Groq(api_key=key)
        except:
            return None
    return None

client = get_client()

# ---------------- NUTRITION CALCULATOR ----------------
def calculate_nutrition(age, sex, height_cm, weight_kg, activity, goal):
    if sex.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    mult = {
        "sedentary": 1.2, "light": 1.375, "moderate": 1.55,
        "active": 1.725, "very_active": 1.9
    }
    tdee = bmr * mult.get(activity, 1.55)

    if goal == "weight_loss":
        target = tdee - 400
    elif goal == "weight_gain":
        target = tdee + 300
    else:
        target = tdee

    return {
        "BMI": round(weight_kg / ((height_cm / 100) ** 2), 1),
        "BMR": round(bmr),
        "TDEE": round(tdee),
        "Target": round(target),
        "Protein": round(target * 0.25 / 4),
        "Carbs": round(target * 0.50 / 4),
        "Fat": round(target * 0.25 / 9),
        "Fiber": 30
    }

# ---------------- SESSION STATE ----------------
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

# ---------------- SIDEBAR ----------------
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
            allergies = st.multiselect("Allergies", ["none", "nuts", "dairy", "gluten", "egg", "seafood"], default=["none"])
            medical = st.multiselect("Medical Conditions", ["none", "diabetes", "hypertension", "thyroid", "pcos"], default=["none"])
            location = st.radio("Workout Location", ["home", "gym"], horizontal=True)
            equipment = st.multiselect("Available Equipment", ["none", "yoga_mat", "dumbbells", "resistance_bands", "bench", "full_gym"], default=["yoga_mat"])

            if st.form_submit_button("Save Member", use_container_width=True):
                nutri = calculate_nutrition(age, sex, height, weight, activity, goal)
                member = {
                    "name": name, "age": age, "sex": sex,
                    "height_cm": height, "weight_kg": weight,
                    "goal": goal, "activity_level": activity,
                    "allergies": allergies, "medical": medical,
                    "workout_location": location, "equipment": equipment,
                    "nutrition": nutri
                }
                st.session_state.family = [m for m in st.session_state.family if m["name"] != name]
                st.session_state.family.append(member)
                st.success(f"{name} saved successfully!")

    if st.session_state.family:
        for m in st.session_state.family:
            st.write(f"**{m['name']}** — {m['nutrition']['Target']} kcal")

    st.markdown("---")
    st.session_state.budget["daily"] = st.number_input("Daily Budget (PKR)", 300, 5000, st.session_state.budget["daily"], 50)

# ---------------- HEADER ----------------
st.markdown('<p class="main-title">🥗 NutriNest</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Smart Family Nutrition • Shared Meals • Personalized Portions</p>', unsafe_allow_html=True)

# ======================================================
# DASHBOARD
# ======================================================
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
                <div class="member-card">
                    <h3>{m['name']}</h3>
                    <p style="margin:0.3rem 0; color:#57534E;">{m['goal'].replace('_',' ').title()} • BMI {n['BMI']}</p>
                    <h2 style="margin:0.6rem 0; color:#D97706;">{n['Target']} kcal</h2>
                    <div>
                        <span class="macro-box">Protein {n['Protein']}g</span>
                        <span class="macro-box">Carbs {n['Carbs']}g</span>
                        <span class="macro-box">Fat {n['Fat']}g</span>
                        <span class="macro-box">Fiber ~{n['Fiber']}g</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Today's Snapshot")

        if st.session_state.logs:
            df_logs = pd.DataFrame(st.session_state.logs)
            meal_logs = df_logs[df_logs["type"] == "meal"]
            workout_logs = df_logs[df_logs["type"] == "workout"]

            c1, c2 = st.columns(2)
            with c1:
                if len(meal_logs) > 0:
                    fig = px.bar(
                        meal_logs.groupby("member").size().reset_index(name="count"),
                        x="member", y="count", title="Meals Logged",
                        color_discrete_sequence=["#D97706"]
                    )
                    st.plotly_chart(fig, use_container_width=True)
            with c2:
                if len(workout_logs) > 0:
                    fig2 = px.bar(
                        workout_logs.groupby("member")["minutes"].sum().reset_index(),
                        x="member", y="minutes", title="Workout Minutes",
                        color_discrete_sequence=["#166534"]
                    )
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No progress logged yet. Go to the Progress page to start tracking.")

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Recipes in Database", len(recipes_df))
        c2.metric("Pantry Items", len(st.session_state.pantry))
        c3.metric("Daily Budget", f"Rs {st.session_state.budget['daily']}")

# ======================================================
# MEAL PLAN
# ======================================================
elif page == "Meal Plan":
    st.subheader("Shared Family Meal Plan")

    if not st.session_state.family:
        st.warning("Please add family members first.")
    else:
        with st.expander("Plan Preferences", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                cuisines = st.multiselect(
                    "Preferred Cuisines",
                    ["Desi / Pakistani", "Chinese", "Italian", "Continental", "Mixed"],
                    default=["Desi / Pakistani"]
                )
            with col2:
                prefs = st.multiselect(
                    "Meal Preferences",
                    ["Less oil", "High protein", "More fiber", "Vegetarian options", "Quick to cook", "Budget friendly"],
                    default=["Less oil", "High protein"]
                )

        if st.button("Generate Detailed Meal Plan", type="primary", use_container_width=True):
            with st.spinner("Creating plan..."):
                # Simple but good fallback plan
                plan = {
                    "day": "Day 1",
                    "meals": [
                        {
                            "meal": "Breakfast",
                            "main": "Vegetable Omelette + Whole Wheat Roti",
                            "sides": ["Cucumber", "Green tea"],
                            "calories": 380, "protein": 22, "carbs": 28, "fat": 18,
                            "fiber_tip": "Add extra salad or flax seeds",
                            "protein_tip": "Eggs already provide good protein",
                            "portions": {m["name"]: "1 plate" for m in st.session_state.family},
                            "description": "Fluffy vegetable omelette with soft whole wheat roti."
                        },
                        {
                            "meal": "Lunch",
                            "main": "Lean Chicken Karahi + Brown Rice",
                            "sides": ["Mixed salad", "Raita"],
                            "calories": 520, "protein": 38, "carbs": 45, "fat": 18,
                            "fiber_tip": "Brown rice + salad give good fiber",
                            "protein_tip": "Chicken is excellent lean protein",
                            "portions": {m["name"]: "1 serving" for m in st.session_state.family},
                            "description": "Home-style chicken karahi with less oil and fiber-rich brown rice."
                        },
                        {
                            "meal": "Evening Snack",
                            "main": "Chana Chaat",
                            "sides": ["Lemon", "Coriander"],
                            "calories": 240, "protein": 11, "carbs": 38, "fat": 5,
                            "fiber_tip": "Chickpeas are high in fiber",
                            "protein_tip": "Add boiled egg for more protein",
                            "portions": {m["name"]: "1 bowl" for m in st.session_state.family},
                            "description": "Protein and fiber rich chickpea chaat."
                        },
                        {
                            "meal": "Dinner",
                            "main": "Dal Tadka + 2 Rotis",
                            "sides": ["Cucumber raita"],
                            "calories": 480, "protein": 22, "carbs": 62, "fat": 14,
                            "fiber_tip": "Dal is excellent for fiber",
                            "protein_tip": "Add kebab or chicken tikka for more protein",
                            "portions": {m["name"]: "1 serving" for m in st.session_state.family},
                            "description": "Comforting dal with soft rotis and light raita."
                        }
                    ],
                    "notes": f"Plan based on {', '.join(cuisines)}. Budget target ≈ Rs {st.session_state.budget['daily']}."
                }
                st.session_state.meal_plan = plan

        if st.session_state.meal_plan:
            plan = st.session_state.meal_plan
            st.success(f"{plan.get('day', 'Day 1')} Plan is ready")

            for meal in plan.get("meals", []):
                st.markdown(f"""
                <div class="plate-card">
                    <h3>🍽 {meal.get('meal')} — {meal.get('main')}</h3>
                    <p style="color:#44403C; margin-bottom:0.8rem;">{meal.get('description', '')}</p>
                </div>
                """, unsafe_allow_html=True)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Calories", f"{meal.get('calories', '—')} kcal")
                c2.metric("Protein", f"{meal.get('protein', '—')} g")
                c3.metric("Carbs", f"{meal.get('carbs', '—')} g")
                c4.metric("Fat", f"{meal.get('fat', '—')} g")

                st.write("**Sides:** " + ", ".join(meal.get("sides", [])))
                st.write("**Portions:**")
                for person, portion in meal.get("portions", {}).items():
                    st.write(f"• **{person}**: {portion}")

                st.info(f"🌿 **Fiber tip:** {meal.get('fiber_tip', 'Add salad or whole grains')}")
                st.success(f"💪 **Protein tip:** {meal.get('protein_tip', 'Good protein source')}")
                st.markdown("---")

            st.caption(plan.get("notes", ""))

# ======================================================
# RECIPES
# ======================================================
elif page == "Recipes":
    st.subheader("Recipe Browser")

    if len(recipes_df) == 0:
        st.warning("No recipes found.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            search = st.text_input("Search by name")
        with c2:
            cuisine_options = ["All"]
            if "cuisine" in recipes_df.columns:
                cuisine_options += sorted(recipes_df["cuisine"].dropna().astype(str).str.title().unique().tolist()[:20])
            cuisine = st.selectbox("Cuisine", cuisine_options)
        with c3:
            max_cal = st.slider("Max Calories", 100, 900, 650)

        filtered = recipes_df.copy()
        if "calories" in filtered.columns:
            filtered = filtered[filtered["calories"].notna()]
            filtered = filtered[filtered["calories"] <= max_cal]

        if cuisine != "All" and "cuisine" in filtered.columns:
            filtered = filtered[filtered["cuisine"].astype(str).str.lower().str.contains(cuisine.lower(), na=False)]

        if search:
            filtered = filtered[filtered["recipe_name"].astype(str).str.lower().str.contains(search.lower(), na=False)]

        st.write(f"**{len(filtered)} recipes found**")

        for _, row in filtered.head(20).iterrows():
            name = row.get("recipe_name", "Unknown")
            cal = row.get("calories", "—")
            pro = row.get("protein_g", "—")
            with st.expander(f"{name}  •  {cal} kcal  •  Protein {pro}g"):
                if "ingredients" in row and pd.notna(row["ingredients"]):
                    st.write("**Ingredients:**")
                    st.write(str(row["ingredients"])[:600])
                if "cuisine" in row:
                    st.caption(f"Cuisine: {row['cuisine']}")

# ======================================================
# PANTRY
# ======================================================
elif page == "Pantry":
    st.subheader("My Pantry")
    st.caption("Add ingredients you already have at home.")

    new_item = st.text_input("Add item (e.g. chicken, daal, rice, yogurt)")
    if st.button("Add to Pantry") and new_item.strip():
        item = new_item.strip().lower()
        if item not in st.session_state.pantry:
            st.session_state.pantry.append(item)
            st.success(f"Added: {item}")
        else:
            st.info("Already in pantry")

    if st.session_state.pantry:
        st.write("**Current pantry items:**")
        for i, item in enumerate(st.session_state.pantry):
            col1, col2 = st.columns([6, 1])
            col1.write(f"• {item.title()}")
            if col2.button("🗑️", key=f"p{i}"):
                st.session_state.pantry.pop(i)
                st.rerun()
    else:
        st.info("Pantry is empty.")

# ======================================================
# WORKOUT
# ======================================================
elif page == "Workout":
    st.subheader("Equipment-Based Workout")

    if not st.session_state.family:
        st.warning("Please add family members first.")
    else:
        selected = st.selectbox("Select Member", [m["name"] for m in st.session_state.family])
        member = next(m for m in st.session_state.family if m["name"] == selected)

        st.write(f"**Location:** {member['workout_location'].title()}  |  **Equipment:** {', '.join(member['equipment'])}  |  **Goal:** {member['goal'].replace('_', ' ').title()}")

        if st.button("Generate 7-Day Workout", type="primary"):
            with st.spinner("Creating personalized plan..."):
                plan = {
                    "member": member["name"],
                    "week": [
                        {"day": 1, "focus": "Full Body", "exercises": [{"name": "Bodyweight Squats", "sets": "3", "reps": "12"}, {"name": "Push-ups", "sets": "3", "reps": "10"}, {"name": "Walking", "duration": "20 min"}]},
                        {"day": 2, "focus": "Rest", "exercises": []},
                        {"day": 3, "focus": "Lower Body", "exercises": [{"name": "Lunges", "sets": "3", "reps": "10 each"}, {"name": "Glute Bridges", "sets": "3", "reps": "15"}]},
                        {"day": 4, "focus": "Rest", "exercises": []},
                        {"day": 5, "focus": "Upper + Core", "exercises": [{"name": "Wall Push-ups", "sets": "3", "reps": "12"}, {"name": "Plank", "duration": "30 sec"}]},
                        {"day": 6, "focus": "Cardio", "exercises": [{"name": "Brisk Walk", "duration": "30 min"}]},
                        {"day": 7, "focus": "Recovery", "exercises": [{"name": "Stretching", "duration": "15 min"}]}
                    ]
                }
                st.session_state.workouts[member["name"]] = plan

        if selected in st.session_state.workouts:
            for day in st.session_state.workouts[selected].get("week", []):
                with st.expander(f"Day {day['day']}: {day['focus']}", expanded=(day["day"] == 1)):
                    if not day.get("exercises"):
                        st.write("Rest day 💤")
                    else:
                        for ex in day["exercises"]:
                            if "duration" in ex:
                                st.write(f"• {ex['name']} — {ex['duration']}")
                            else:
                                st.write(f"• {ex['name']} — {ex.get('sets', '')} × {ex.get('reps', '')}")

# ======================================================
# PROGRESS
# ======================================================
elif page == "Progress":
    st.subheader("Progress Tracking")

    if not st.session_state.family:
        st.warning("Please add family members first.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Log Meal")
            m_name = st.selectbox("Member", [m["name"] for m in st.session_state.family], key="lm")
            meal_name = st.text_input("Meal name", "Breakfast")
            status = st.selectbox("Status", ["followed", "different", "skipped"])
            if st.button("Log Meal", use_container_width=True):
                st.session_state.logs.append({
                    "date": str(date.today()), "member": m_name,
                    "type": "meal", "item": meal_name, "status": status
                })
                st.success("Meal logged")

        with c2:
            st.markdown("#### Log Workout")
            w_name = st.selectbox("Member ", [m["name"] for m in st.session_state.family], key="lw")
            w_status = st.selectbox("Status ", ["completed", "skipped", "rest"])
            minutes = st.number_input("Minutes", 0, 180, 30)
            if st.button("Log Workout", use_container_width=True):
                st.session_state.logs.append({
                    "date": str(date.today()), "member": w_name,
                    "type": "workout", "status": w_status,
                    "minutes": minutes if w_status == "completed" else 0
                })
                st.success("Workout logged")

        st.markdown("---")
        if st.session_state.logs:
            for m in st.session_state.family:
                logs = [l for l in st.session_state.logs if l["member"] == m["name"]]
                meals = [l for l in logs if l["type"] == "meal"]
                workouts = [l for l in logs if l["type"] == "workout"]
                st.write(f"**{m['name']}**")
                st.write(f"Meals: {len(meals)} | Followed: {sum(1 for x in meals if x['status']=='followed')} | Workouts: {sum(1 for x in workouts if x['status']=='completed')} | Minutes: {sum(x.get('minutes',0) for x in workouts)}")
        else:
            st.info("No logs yet.")
