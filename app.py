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

# ---------------- YOUR EXACT THEME ----------------
st.markdown("""
<style>
    /* ========== GLOBAL ========== */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #F7F4EE 0%, #F2EFE8 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Hide default Streamlit branding a bit */
    #MainMenu, footer {visibility: hidden;}

    /* ========== SIDEBAR ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B4332 0%, #2D6A4F 100%) !important;
        border-right: none;
    }
    [data-testid="stSidebar"] * {
        color: #F8F9FA !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #F8F9FA !important;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 0.3rem 0;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        color: #D8F3DC !important;
    }

    /* ========== HEADER ========== */
    .main-title {
        font-size: 2.7rem;
        font-weight: 800;
        color: #1B4332;
        margin-bottom: 0.1rem;
        letter-spacing: -1px;
    }
    .sub-title {
        color: #52796F;
        font-size: 1.1rem;
        margin-bottom: 2.2rem;
        font-weight: 500;
    }

    /* ========== CARDS ========== */
    .member-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 1.6rem;
        border: 1px solid #E9ECEF;
        box-shadow: 0 10px 30px rgba(27, 67, 50, 0.06);
        margin-bottom: 1.3rem;
        transition: all 0.25s ease;
    }
    .member-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 40px rgba(27, 67, 50, 0.1);
    }

    .plate-card {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 1.5rem 1.7rem;
        border-left: 6px solid #D9971C;
        box-shadow: 0 8px 25px rgba(0,0,0,0.04);
        margin-bottom: 1.5rem;
        color: #212529;
    }

    /* ========== MACRO PILLS ========== */
    .macro-box {
        background: #E9F5EF;
        color: #1B4332;
        border-radius: 50px;
        padding: 0.4rem 0.9rem;
        font-size: 0.84rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 7px;
        margin-top: 6px;
        border: 1px solid #D8F3DC;
    }

    /* ========== BUTTONS ========== */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        background: linear-gradient(135deg, #D9971C 0%, #C48412 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.65rem 1.4rem !important;
        box-shadow: 0 4px 15px rgba(217, 151, 28, 0.25);
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(217, 151, 28, 0.35);
        color: white !important;
    }

    /* ========== METRICS ========== */
    [data-testid="stMetricValue"] {
        color: #1B4332 !important;
        font-weight: 700 !important;
        font-size: 1.55rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #52796F !important;
        font-weight: 500 !important;
    }

    /* ========== INPUTS ========== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 10px !important;
        border: 1.5px solid #DEE2E6 !important;
        padding: 0.6rem 0.9rem !important;
    }
    .stSelectbox > div > div {
        border-radius: 10px !important;
    }

    /* ========== GENERAL ========== */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stSuccess {
        background-color: #D8F3DC;
        border-radius: 12px;
    }
    .stInfo {
        background-color: #E9F5EF;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_recipes():
    # Pehle local file try karo (GitHub pe jo humne daali hai)
    local_paths = [
        "data/recipes.csv",
        "./data/recipes.csv",
        "recipes.csv"
    ]
    
    for path in local_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                df.columns = [c.lower().strip() for c in df.columns]
                return df
            except Exception as e:
                st.warning(f"Error loading {path}: {e}")
    
    # Agar local file na mile to empty DataFrame return karo
        # Debug ke liye
    if df.empty:
        st.warning("Recipes file empty hai ya load nahi hui. Check data/recipes.csv")
    else:
        st.success(f"{len(df)} recipes loaded successfully")
    
    return df
    return pd.DataFrame()

# ---------------- GROQ CLIENT ----------------
def get_client():
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        try:
            from google.colab import userdata
            key = userdata.get("GROQ_API_KEY")
        except:
            key = None
    if key:
        try:
            from groq import Groq
            return Groq(api_key=key)
        except:
            return None
    return None

client = get_client()

# ---------------- NUTRITION ----------------
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

# ---------------- HELPER: Filter by cuisine ----------------
def get_cuisine_recipes(df, selected_cuisines):
    if df is None or len(df) == 0:
        return pd.DataFrame()

    data = df.copy()
    if "calories" in data.columns:
        data = data[data["calories"].notna()]
        data = data[(data["calories"] >= 80) & (data["calories"] <= 900)]

    if not selected_cuisines or "Mixed" in selected_cuisines:
        return data.reset_index(drop=True)

    # Map user selection to possible dataset values
    mapping = {
        "Desi / Pakistani": ["pakistani", "indian", "desi", "south asian"],
        "Chinese": ["chinese", "asian"],
        "Italian": ["italian", "european"],
        "Continental": ["continental", "european", "american", "western"]
    }

    keywords = []
    for c in selected_cuisines:
        keywords.extend(mapping.get(c, [c.lower()]))

    if "cuisine" in data.columns:
        mask = data["cuisine"].astype(str).str.lower().apply(
            lambda x: any(k in x for k in keywords)
        )
        filtered = data[mask]
        if len(filtered) >= 5:
            return filtered.reset_index(drop=True)

    return data.reset_index(drop=True)

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
                    <h3 style="margin:0; color:#2B2B26;">{m['name']}</h3>
                    <p style="margin:0.3rem 0; color:#5a5a52;">{m['goal'].replace('_',' ').title()} • BMI {n['BMI']}</p>
                    <h2 style="margin:0.6rem 0; color:#D9971C;">{n['Target']} kcal</h2>
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
                        color="member", color_discrete_sequence=["#D9971C", "#c48412", "#b3740f"]
                    )
                    st.plotly_chart(fig, use_container_width=True)
            with c2:
                if len(workout_logs) > 0:
                    fig2 = px.bar(
                        workout_logs.groupby("member")["minutes"].sum().reset_index(),
                        x="member", y="minutes", title="Workout Minutes",
                        color="member", color_discrete_sequence=["#D9971C", "#c48412"]
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
            with st.spinner("Creating plan according to selected cuisines + dataset..."):

                # Filter recipes by selected cuisine
                safe_recipes = get_cuisine_recipes(recipes_df, cuisines)

                family_info = []
                for m in st.session_state.family:
                    family_info.append({
                        "name": m["name"],
                        "goal": m["goal"],
                        "target_calories": m["nutrition"]["Target"],
                        "protein": m["nutrition"]["Protein"],
                        "allergies": m["allergies"]
                    })

                # Build dish pools from dataset
                def get_pool(df, max_cal=500, n=8):
                    if len(df) == 0:
                        return []
                    temp = df[df["calories"] <= max_cal] if "calories" in df.columns else df
                    return temp.head(n)[["recipe_name", "cuisine", "calories"]].fillna(0).to_dict("records") if len(temp) > 0 else []

                breakfast_pool = get_pool(safe_recipes, 420)
                lunch_pool = get_pool(safe_recipes, 650)
                snack_pool = get_pool(safe_recipes, 300)
                dinner_pool = get_pool(safe_recipes, 600)

                # Fallback based on cuisine
                if "Chinese" in cuisines and "Desi / Pakistani" not in cuisines:
                    fallback = {
                        "day": "Day 1",
                        "meals": [
                            {"meal": "Breakfast", "main": "Vegetable Fried Rice + Egg", "sides": ["Cucumber", "Green tea"], "calories": 390, "protein": 18, "carbs": 48, "fat": 14,
                             "fiber_tip": "Add extra vegetables for fiber", "protein_tip": "Egg adds good protein",
                             "portions": {m["name"]: "1 plate" for m in st.session_state.family},
                             "description": "Light vegetable fried rice with scrambled egg."},
                            {"meal": "Lunch", "main": "Chicken Stir Fry + Steamed Rice", "sides": ["Stir-fried vegetables"], "calories": 510, "protein": 35, "carbs": 52, "fat": 16,
                             "fiber_tip": "Lots of vegetables = good fiber", "protein_tip": "Chicken is high protein",
                             "portions": {m["name"]: "1 serving" for m in st.session_state.family},
                             "description": "Quick chicken stir fry with colorful vegetables and steamed rice."},
                            {"meal": "Evening Snack", "main": "Boiled Corn + Nuts", "sides": ["Lemon"], "calories": 220, "protein": 7, "carbs": 32, "fat": 8,
                             "fiber_tip": "Corn provides fiber", "protein_tip": "Add a handful of peanuts if needed",
                             "portions": {m["name"]: "1 bowl" for m in st.session_state.family},
                             "description": "Simple and light evening snack."},
                            {"meal": "Dinner", "main": "Clear Chicken Soup + Vegetables", "sides": ["Side salad"], "calories": 380, "protein": 28, "carbs": 25, "fat": 12,
                             "fiber_tip": "Vegetables add fiber", "protein_tip": "Chicken soup is light but protein-rich",
                             "portions": {m["name"]: "1 bowl" for m in st.session_state.family},
                             "description": "Light and comforting clear soup with vegetables."}
                        ],
                        "notes": f"Chinese-style plan. Budget target ≈ Rs {st.session_state.budget['daily']}."
                    }
                elif "Italian" in cuisines and "Desi / Pakistani" not in cuisines:
                    fallback = {
                        "day": "Day 1",
                        "meals": [
                            {"meal": "Breakfast", "main": "Eggs + Whole Grain Toast", "sides": ["Tomato slices"], "calories": 360, "protein": 20, "carbs": 28, "fat": 16,
                             "fiber_tip": "Whole grain toast for fiber", "protein_tip": "Eggs provide high quality protein",
                             "portions": {m["name"]: "1 plate" for m in st.session_state.family},
                             "description": "Simple Italian-inspired breakfast."},
                            {"meal": "Lunch", "main": "Grilled Chicken Pasta (light sauce)", "sides": ["Side salad"], "calories": 530, "protein": 36, "carbs": 55, "fat": 16,
                             "fiber_tip": "Salad adds fiber", "protein_tip": "Chicken is the main protein",
                             "portions": {m["name"]: "1 serving" for m in st.session_state.family},
                             "description": "Light pasta with grilled chicken and minimal oil."},
                            {"meal": "Evening Snack", "main": "Greek Yogurt + Berries", "sides": [], "calories": 200, "protein": 14, "carbs": 22, "fat": 5,
                             "fiber_tip": "Berries add fiber", "protein_tip": "Yogurt is high in protein",
                             "portions": {m["name"]: "1 bowl" for m in st.session_state.family},
                             "description": "Light and protein-rich snack."},
                            {"meal": "Dinner", "main": "Grilled Fish + Roasted Vegetables", "sides": ["Lemon"], "calories": 420, "protein": 34, "carbs": 20, "fat": 18,
                             "fiber_tip": "Roasted vegetables for fiber", "protein_tip": "Fish is excellent lean protein",
                             "portions": {m["name"]: "1 plate" for m in st.session_state.family},
                             "description": "Clean and light Italian-style dinner."}
                        ],
                        "notes": f"Italian-inspired plan. Budget target ≈ Rs {st.session_state.budget['daily']}."
                    }
                else:
                    # Default Desi / Mixed fallback
                    fallback = {
                        "day": "Day 1",
                        "meals": [
                            {"meal": "Breakfast", "main": "Vegetable Omelette + 1 Whole Wheat Roti", "sides": ["Cucumber", "Green tea"], "calories": 380, "protein": 22, "carbs": 28, "fat": 18,
                             "fiber_tip": "Add extra salad or flax seeds", "protein_tip": "Eggs already give good protein",
                             "portions": {m["name"]: "1 plate" for m in st.session_state.family},
                             "description": "Fluffy vegetable omelette with soft whole wheat roti."},
                            {"meal": "Lunch", "main": "Lean Chicken Karahi + Brown Rice", "sides": ["Mixed salad", "Raita"], "calories": 520, "protein": 38, "carbs": 45, "fat": 18,
                             "fiber_tip": "Brown rice + salad = good fiber", "protein_tip": "Chicken is excellent protein",
                             "portions": {m["name"]: ("1.2 servings" if m["goal"]=="weight_loss" else "1 serving") for m in st.session_state.family},
                             "description": "Home-style chicken karahi with less oil and fiber-rich brown rice."},
                            {"meal": "Evening Snack", "main": "Chana Chaat", "sides": ["Lemon", "Coriander"], "calories": 240, "protein": 11, "carbs": 38, "fat": 5,
                             "fiber_tip": "Chickpeas are high in fiber", "protein_tip": "Add boiled egg for more protein",
                             "portions": {m["name"]: "1 bowl" for m in st.session_state.family},
                             "description": "Protein and fiber rich chickpea chaat."},
                            {"meal": "Dinner", "main": "Dal Tadka + 2 Rotis", "sides": ["Cucumber raita", "Optional Kebab"], "calories": 480, "protein": 22, "carbs": 62, "fat": 14,
                             "fiber_tip": "Dal is excellent for fiber", "protein_tip": "Add kebab or chicken tikka for more protein",
                             "portions": {m["name"]: ("1.1 servings" if i==0 else "0.9 servings") for i, m in enumerate(st.session_state.family)},
                             "description": "Comforting dal with soft rotis and light raita."}
                        ],
                        "notes": f"Plan based on {', '.join(cuisines)}. Budget target ≈ Rs {st.session_state.budget['daily']}."
                    }

                plan = fallback

                # AI enhancement with strong cuisine instruction + dataset dishes
                if client:
                    try:
                        prompt = f"""
You are a professional nutritionist creating a SHARED family meal plan.

IMPORTANT: Strictly follow the selected cuisines: {cuisines}
Do NOT default to only Pakistani food if other cuisines are selected.

Family: {json.dumps(family_info)}
Preferences: {prefs}
Pantry: {st.session_state.pantry}
Budget: Rs {st.session_state.budget['daily']}

Available dishes from dataset (use these names when possible):
Breakfast options: {json.dumps(breakfast_pool[:6])}
Lunch options: {json.dumps(lunch_pool[:6])}
Snack options: {json.dumps(snack_pool[:6])}
Dinner options: {json.dumps(dinner_pool[:6])}

Return ONLY valid JSON in this exact format:
{{
  "day": "Day 1",
  "meals": [
    {{
      "meal": "Breakfast",
      "main": "dish name",
      "sides": ["side1", "side2"],
      "calories": 380,
      "protein": 22,
      "carbs": 30,
      "fat": 15,
      "fiber_tip": "short tip",
      "protein_tip": "short tip",
      "portions": {{"Father": "1.2 servings", "Mother": "1 serving"}},
      "description": "short description"
    }}
  ],
  "notes": "short note mentioning the cuisines used"
}}
"""
                        resp = client.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[
                                {"role": "system", "content": "Return only valid JSON. No markdown. Respect the cuisine selection strictly."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.25,
                            max_tokens=2000
                        )
                        raw = resp.choices[0].message.content.strip()
                        if "```" in raw:
                            raw = raw.split("```")[1].replace("json", "").strip()
                        s, e = raw.find("{"), raw.rfind("}") + 1
                        if s >= 0:
                            ai_plan = json.loads(raw[s:e])
                            if "meals" in ai_plan and len(ai_plan["meals"]) >= 3:
                                plan = ai_plan
                    except Exception as e:
                        st.warning(f"AI fallback used: {e}")

                st.session_state.meal_plan = plan

        # Display plan
        if st.session_state.meal_plan:
            plan = st.session_state.meal_plan
            st.success(f"{plan.get('day', 'Day 1')} Plan is ready")

            for meal in plan.get("meals", []):
                st.markdown(f"""
                <div class="plate-card">
                    <h3 style="margin-top:0; color:#2B2B26;">🍽 {meal.get('meal')} — {meal.get('main')}</h3>
                    <p style="color:#3d3d38; margin-bottom:0.8rem;">{meal.get('description', '')}</p>
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
# RECIPES / PANTRY / WORKOUT / PROGRESS (same as before)
# ======================================================
elif page == "Recipes":
    st.subheader("Recipe Browser")
    if len(recipes_df) == 0:
        st.warning("Recipe database could not be loaded.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            search = st.text_input("Search by name")
        with c2:
            cuisine_options = ["All"]
            if "cuisine" in recipes_df.columns:
                cuisine_options += sorted(recipes_df["cuisine"].dropna().astype(str).str.title().unique().tolist()[:25])
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

elif page == "Pantry":
    st.subheader("My Pantry")
    st.caption("Add ingredients you already have. Meal plan will prefer them.")
    new_item = st.text_input("Add item (chicken, daal, rice, yogurt...)")
    if st.button("Add to Pantry") and new_item.strip():
        item = new_item.strip().lower()
        if item not in st.session_state.pantry:
            st.session_state.pantry.append(item)
            st.success(f"Added: {item}")
        else:
            st.info("Already in pantry")
    if st.session_state.pantry:
        for i, item in enumerate(st.session_state.pantry):
            col1, col2 = st.columns([6,1])
            col1.write(f"• {item.title()}")
            if col2.button("🗑️", key=f"p{i}"):
                st.session_state.pantry.pop(i)
                st.rerun()
    else:
        st.info("Pantry is empty.")

elif page == "Workout":
    st.subheader("Equipment-Based Workout")
    if not st.session_state.family:
        st.warning("Please add family members first.")
    else:
        selected = st.selectbox("Select Member", [m["name"] for m in st.session_state.family])
        member = next(m for m in st.session_state.family if m["name"] == selected)
        st.write(f"**Location:** {member['workout_location'].title()} | **Equipment:** {', '.join(member['equipment'])} | **Goal:** {member['goal'].replace('_',' ').title()}")
        if st.button("Generate 7-Day Workout", type="primary"):
            with st.spinner("Creating plan..."):
                plan = {
                    "member": member["name"],
                    "week": [
                        {"day":1,"focus":"Full Body","exercises":[{"name":"Bodyweight Squats","sets":"3","reps":"12"},{"name":"Push-ups","sets":"3","reps":"10"},{"name":"Walking","duration":"20 min"}]},
                        {"day":2,"focus":"Rest","exercises":[]},
                        {"day":3,"focus":"Lower Body","exercises":[{"name":"Lunges","sets":"3","reps":"10 each"},{"name":"Glute Bridges","sets":"3","reps":"15"}]},
                        {"day":4,"focus":"Rest","exercises":[]},
                        {"day":5,"focus":"Upper + Core","exercises":[{"name":"Wall Push-ups","sets":"3","reps":"12"},{"name":"Plank","duration":"30 sec"}]},
                        {"day":6,"focus":"Cardio","exercises":[{"name":"Brisk Walk","duration":"30 min"}]},
                        {"day":7,"focus":"Recovery","exercises":[{"name":"Stretching","duration":"15 min"}]}
                    ]
                }
                if client:
                    try:
                        prompt = f"""Create practical 7-day workout. Name:{member['name']} Goal:{member['goal']} Location:{member['workout_location']} Equipment:{member['equipment']}. Return ONLY JSON."""
                        resp = client.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"system","content":"Return only JSON"},{"role":"user","content":prompt}],
                            temperature=0.3, max_tokens=1800
                        )
                        raw = resp.choices[0].message.content.strip()
                        if "```" in raw: raw = raw.split("```")[1].replace("json","").strip()
                        s, e = raw.find("{"), raw.rfind("}")+1
                        if s >= 0: plan = json.loads(raw[s:e])
                    except: pass
                st.session_state.workouts[member["name"]] = plan
        if selected in st.session_state.workouts:
            for day in st.session_state.workouts[selected].get("week", []):
                with st.expander(f"Day {day['day']}: {day['focus']}", expanded=(day["day"]==1)):
                    if not day.get("exercises"):
                        st.write("Rest day 💤")
                    else:
                        for ex in day["exercises"]:
                            if "duration" in ex:
                                st.write(f"• {ex['name']} — {ex['duration']}")
                            else:
                                st.write(f"• {ex['name']} — {ex.get('sets','')} × {ex.get('reps','')}")

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
                st.session_state.logs.append({"date": str(date.today()), "member": m_name, "type": "meal", "item": meal_name, "status": status})
                st.success("Meal logged")
        with c2:
            st.markdown("#### Log Workout")
            w_name = st.selectbox("Member ", [m["name"] for m in st.session_state.family], key="lw")
            w_status = st.selectbox("Status ", ["completed", "skipped", "rest"])
            minutes = st.number_input("Minutes", 0, 180, 30)
            if st.button("Log Workout", use_container_width=True):
                st.session_state.logs.append({"date": str(date.today()), "member": w_name, "type": "workout", "status": w_status, "minutes": minutes if w_status=="completed" else 0})
                st.success("Workout logged")
        st.markdown("---")
        if st.session_state.logs:
            for m in st.session_state.family:
                logs = [l for l in st.session_state.logs if l["member"] == m["name"]]
                meals = [l for l in logs if l["type"]=="meal"]
                workouts = [l for l in logs if l["type"]=="workout"]
                st.write(f"**{m['name']}** — Meals: {len(meals)} | Followed: {sum(1 for x in meals if x['status']=='followed')} | Workouts: {sum(1 for x in workouts if x['status']=='completed')} | Minutes: {sum(x.get('minutes',0) for x in workouts)}")
        else:
            st.info("No logs yet.")

