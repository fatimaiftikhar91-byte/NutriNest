import ast
import json
import os
import re
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

try:
    from groq import Groq
except Exception:
    Groq = None


# =========================================================
# PAGE
# =========================================================
st.set_page_config(
    page_title="NutriNest",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# DESIGN SYSTEM — soft pastel, dark readable text
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --ink: #25302B;
        --muted: #66736D;
        --cream: #FBF8F3;
        --sage: #E7F0E7;
        --mint: #EEF7F1;
        --peach: #FBE9DD;
        --lavender: #EEEAF7;
        --butter: #FFF3CF;
        --accent: #587864;
        --accent-dark: #395847;
        --gold: #C98D3D;
        --line: #DEDCD5;
        --white: #FFFFFF;
    }

    .stApp {
        background:
          radial-gradient(circle at 8% 0%, rgba(231,240,231,.70), transparent 26rem),
          radial-gradient(circle at 95% 8%, rgba(251,233,221,.65), transparent 25rem),
          var(--cream);
        color: var(--ink);
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E9F1E8 0%, #F5F1E8 100%);
        border-right: 1px solid #DDE4DC;
    }

    [data-testid="stSidebar"] * {
        color: var(--ink);
    }

    [data-testid="stSidebar"] .stRadio label {
        padding: .42rem .4rem;
        border-radius: 10px;
    }

    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: var(--ink);
    }

    .hero {
        background: linear-gradient(120deg, #E7F0E7 0%, #F9EBDD 50%, #EEEAF7 100%);
        border: 1px solid rgba(88,120,100,.15);
        border-radius: 26px;
        padding: 2rem 2.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 16px 40px rgba(45,62,52,.07);
    }

    .hero-kicker {
        display: inline-block;
        background: rgba(255,255,255,.72);
        border: 1px solid rgba(88,120,100,.18);
        border-radius: 999px;
        padding: .35rem .75rem;
        font-weight: 700;
        color: var(--accent-dark);
        margin-bottom: .65rem;
        font-size: .83rem;
    }

    .hero-title {
        font-size: clamp(2.0rem, 4vw, 3.25rem);
        line-height: 1.05;
        font-weight: 850;
        letter-spacing: -.03em;
        margin: 0 0 .55rem 0;
        color: #26332D;
    }

    .hero-sub {
        color: #56645E;
        font-size: 1.05rem;
        max-width: 760px;
        margin: 0;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: var(--ink);
        margin: .25rem 0 1rem 0;
    }

    .member-card, .soft-card, .plate-card {
        background: rgba(255,255,255,.90);
        border: 1px solid #E3E0D8;
        border-radius: 18px;
        padding: 1.15rem 1.2rem;
        box-shadow: 0 8px 24px rgba(43,55,48,.055);
        margin-bottom: .85rem;
    }

    .member-card {
        min-height: 190px;
        background: linear-gradient(155deg, #FFFFFF 0%, #F2F8F3 100%);
    }

    .plate-card {
        border-left: 5px solid #C98D3D;
        background: linear-gradient(140deg, #FFFFFF 0%, #FFF9ED 100%);
    }

    .macro-chip {
        display: inline-block;
        background: #EFF5EF;
        border: 1px solid #DCE9DE;
        border-radius: 999px;
        padding: .30rem .62rem;
        margin: .18rem .18rem .1rem 0;
        font-size: .82rem;
        font-weight: 700;
        color: #40544A;
    }

    .subtle {
        color: var(--muted);
    }

    .pill {
        display:inline-block;
        padding:.28rem .62rem;
        border-radius:999px;
        background:#F4EEE5;
        color:#695B48;
        font-size:.78rem;
        font-weight:700;
        margin-right:.3rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,.86);
        border: 1px solid #E2E0D8;
        border-radius: 16px;
        padding: .8rem 1rem;
        box-shadow: 0 6px 18px rgba(43,55,48,.04);
    }

    [data-testid="stMetricValue"] {
        color: #33483D;
        font-weight: 800;
    }

    div[data-testid="stExpander"] {
        background: rgba(255,255,255,.72);
        border: 1px solid #E2E0D8;
        border-radius: 14px;
        overflow: hidden;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 12px;
        min-height: 2.7rem;
        font-weight: 750;
        border: 1px solid #587864;
        background: #587864;
        color: white !important;
        box-shadow: 0 5px 14px rgba(57,88,71,.14);
        transition: all .15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: #395847;
        border-color: #395847;
        transform: translateY(-1px);
    }

    div[data-baseweb="select"] > div,
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        border-radius: 12px !important;
        background: #FFFFFF !important;
        border-color: #D8DDD8 !important;
        color: #25302B !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #E2E0D8;
        border-radius: 14px;
        overflow: hidden;
    }

    .footer-note {
        margin-top: 2rem;
        padding: .8rem 1rem;
        border-radius: 14px;
        background: #F4F0E8;
        color: #6E665A;
        font-size: .82rem;
        text-align: center;
    }

    @media (max-width: 800px) {
        .block-container {padding-top: 1rem;}
        .hero {padding: 1.4rem;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATA HELPERS
# =========================================================
DATA_CANDIDATES = [
    "data/nutrinest_recipes_clean.csv",
    "data/recipes.csv",
    "data/nutrinest_recipes.csv",
    "nutrinest_recipes_clean.csv",
    "recipes.csv",
]


def _first_existing_path():
    for candidate in DATA_CANDIDATES:
        if os.path.exists(candidate):
            return candidate
    return None


@st.cache_data(show_spinner=False)
def load_recipes():
    path = _first_existing_path()
    if not path:
        return pd.DataFrame(), None

    df = pd.read_csv(path)
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Accept the column names used across the tested notebook versions.
    rename_map = {
        "recipe name": "recipe_name",
        "dish name": "recipe_name",
        "name": "recipe_name",
        "calories_per_serving": "calories",
        "reported_calories": "calories",
        "protein(g)": "protein_g",
        "protein_g_per_serving": "protein_g",
        "carbs(g)": "carbs_g",
        "carbohydrates (g)": "carbs_g",
        "carbs_g_per_serving": "carbs_g",
        "fat(g)": "fat_g",
        "fats (g)": "fat_g",
        "fat_g_per_serving": "fat_g",
        "meal type": "meal_type",
        "cuisine_type": "cuisine",
        "cuisine type": "cuisine",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    for col in ["calories", "protein_g", "carbs_g", "fat_g"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "recipe_name" not in df.columns:
        df["recipe_name"] = "Unnamed recipe"
    if "cuisine" not in df.columns:
        df["cuisine"] = "Unspecified"
    if "meal_type" not in df.columns:
        df["meal_type"] = "main"
    if "ingredients" not in df.columns:
        df["ingredients"] = ""
    if "steps" not in df.columns:
        df["steps"] = ""

    return df, path


recipes_df, recipe_source = load_recipes()


# =========================================================
# AI CLIENT
# =========================================================
def get_secret(name):
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass
    return os.environ.get(name)


@st.cache_resource(show_spinner=False)
def get_client():
    key = get_secret("GROQ_API_KEY")
    if key and Groq is not None:
        try:
            return Groq(api_key=key)
        except Exception:
            return None
    return None


client = get_client()


# =========================================================
# CORE NUTRITION
# =========================================================
def calculate_nutrition(age, sex, height_cm, weight_kg, activity, goal):
    # Same Mifflin-St Jeor logic as the tested notebook.
    if sex.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    multipliers = {
        "sedentary": 1.20,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.90,
    }
    tdee = bmr * multipliers.get(activity, 1.55)

    if goal == "weight_loss":
        target = tdee - 400
    elif goal == "weight_gain":
        target = tdee + 300
    else:
        target = tdee

    target = max(target, 1200)

    return {
        "BMI": round(weight_kg / ((height_cm / 100) ** 2), 1),
        "BMR": round(bmr),
        "TDEE": round(tdee),
        "Target": round(target),
        "Protein": round(target * 0.25 / 4),
        "Carbs": round(target * 0.50 / 4),
        "Fat": round(target * 0.25 / 9),
        "Fiber": 30,
    }


ALLERGY_KEYWORDS = {
    "nuts": ["nut", "almond", "peanut", "cashew", "walnut", "pistachio"],
    "dairy": ["milk", "cheese", "yogurt", "cream", "butter", "paneer"],
    "gluten": ["wheat", "flour", "bread", "roti", "chapati", "pasta", "barley"],
    "egg": ["egg", "eggs"],
    "seafood": ["fish", "prawn", "shrimp", "seafood", "tuna", "salmon"],
}


def safe_for_family(df, family):
    if df.empty or not family:
        return df.copy()

    blocked = []
    for member in family:
        for allergy in member.get("allergies", []):
            if allergy != "none":
                blocked.extend(ALLERGY_KEYWORDS.get(allergy, [allergy]))

    if not blocked:
        return df.copy()

    text = (
        df.get("ingredients", pd.Series("", index=df.index)).fillna("").astype(str)
        + " "
        + df.get("recipe_name", pd.Series("", index=df.index)).fillna("").astype(str)
    ).str.lower()

    mask = ~text.apply(lambda x: any(word in x for word in blocked))
    return df[mask].copy()


CUISINE_MAP = {
    "Desi / Pakistani": ["pakistani", "desi", "indian", "south asian", "home-style"],
    "Chinese": ["chinese", "asian"],
    "Italian": ["italian"],
    "Continental": ["continental", "european", "american", "western", "international"],
}


def get_cuisine_recipes(df, selected_cuisines, family=None):
    if df is None or df.empty:
        return pd.DataFrame()

    data = df.copy()
    data = safe_for_family(data, family or [])

    if "calories" in data.columns:
        data = data[data["calories"].isna() | data["calories"].between(80, 1000)]

    if not selected_cuisines or "Mixed" in selected_cuisines:
        return data.reset_index(drop=True)

    keywords = []
    for cuisine in selected_cuisines:
        keywords.extend(CUISINE_MAP.get(cuisine, [cuisine.lower()]))

    mask = data["cuisine"].fillna("").astype(str).str.lower().apply(
        lambda value: any(keyword in value for keyword in keywords)
    )
    filtered = data[mask]
    return (filtered if not filtered.empty else data).reset_index(drop=True)


def parse_listish(value):
    if pd.isna(value):
        return []
    if isinstance(value, list):
        return value
    text = str(value).strip()
    if not text:
        return []
    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
    except Exception:
        pass
    return [x.strip() for x in re.split(r",|;", text) if x.strip()]


def recipe_pool(df, max_cal=700, meal_hint=None, n=12):
    if df.empty:
        return []
    temp = df.copy()

    if "calories" in temp.columns:
        temp = temp[temp["calories"].isna() | (temp["calories"] <= max_cal)]

    if meal_hint and "meal_type" in temp.columns:
        hinted = temp[
            temp["meal_type"].fillna("").astype(str).str.lower().str.contains(meal_hint, na=False)
        ]
        if len(hinted) >= 2:
            temp = hinted

    keep = [c for c in ["recipe_name", "cuisine", "calories", "protein_g", "carbs_g", "fat_g"] if c in temp.columns]
    return temp[keep].head(n).fillna("").to_dict("records")


def extract_json(text):
    if not text:
        return None
    cleaned = text.strip()
    if "```" in cleaned:
        chunks = cleaned.split("```")
        cleaned = max(chunks, key=len).replace("json", "", 1).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}") + 1
    if start < 0 or end <= start:
        return None
    try:
        return json.loads(cleaned[start:end])
    except Exception:
        return None


# =========================================================
# SESSION
# =========================================================
defaults = {
    "family": [],
    "logs": [],
    "meal_plan": None,
    "workouts": {},
    "pantry": [],
    "budget": {"daily": 900},
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🥗 NutriNest")
    st.caption("Family Nutrition & Fitness")
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Dashboard", "Meal Plan", "Recipes", "Pantry", "Workout", "Progress"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### Family Members")

    with st.expander("➕ Add / update member"):
        with st.form("member_form"):
            name = st.text_input("Name", "Father")
            c1, c2 = st.columns(2)
            with c1:
                age = st.number_input("Age", 10, 90, 40)
                sex = st.selectbox("Sex", ["male", "female"])
            with c2:
                height = st.number_input("Height (cm)", 120, 220, 170)
                weight = st.number_input("Weight (kg)", 30, 180, 70)

            goal = st.selectbox("Goal", ["weight_loss", "maintenance", "weight_gain"])
            activity = st.selectbox(
                "Activity level",
                ["sedentary", "light", "moderate", "active", "very_active"],
                index=2,
            )
            allergies = st.multiselect(
                "Allergies",
                ["none", "nuts", "dairy", "gluten", "egg", "seafood"],
                default=["none"],
            )
            medical = st.multiselect(
                "Medical conditions",
                ["none", "diabetes", "hypertension", "thyroid", "pcos"],
                default=["none"],
            )
            location = st.radio("Workout location", ["home", "gym"], horizontal=True)
            equipment = st.multiselect(
                "Available equipment",
                ["none", "yoga_mat", "dumbbells", "resistance_bands", "bench", "full_gym"],
                default=["yoga_mat"],
            )

            save = st.form_submit_button("Save member", use_container_width=True)
            if save:
                cleaned_name = name.strip() or "Member"
                member = {
                    "name": cleaned_name,
                    "age": int(age),
                    "sex": sex,
                    "height_cm": float(height),
                    "weight_kg": float(weight),
                    "goal": goal,
                    "activity_level": activity,
                    "allergies": allergies,
                    "medical": medical,
                    "workout_location": location,
                    "equipment": equipment,
                    "nutrition": calculate_nutrition(age, sex, height, weight, activity, goal),
                }
                st.session_state.family = [
                    m for m in st.session_state.family
                    if m["name"].casefold() != cleaned_name.casefold()
                ]
                st.session_state.family.append(member)
                st.success(f"{cleaned_name} saved.")

    if st.session_state.family:
        for member in st.session_state.family:
            c1, c2 = st.columns([5, 1])
            c1.markdown(
                f"**{member['name']}**  \n"
                f"<span style='font-size:.78rem;color:#6a756f'>{member['nutrition']['Target']} kcal/day</span>",
                unsafe_allow_html=True,
            )
            if c2.button("×", key=f"remove_{member['name']}", help="Remove member"):
                st.session_state.family = [
                    m for m in st.session_state.family if m["name"] != member["name"]
                ]
                st.rerun()

    st.markdown("---")
    st.session_state.budget["daily"] = st.number_input(
        "Daily food budget (PKR)",
        min_value=300,
        max_value=5000,
        value=int(st.session_state.budget["daily"]),
        step=50,
    )

    st.markdown("---")
    if recipe_source:
        st.success(f"Dataset connected\n\n`{recipe_source}`")
    else:
        st.warning("Recipe CSV not found in `data/`.")

    st.caption("AI: " + ("Connected" if client else "Fallback mode"))


# =========================================================
# HERO
# =========================================================
st.markdown(
    """
    <div class="hero">
      <div class="hero-kicker">SMART FAMILY WELLNESS</div>
      <div class="hero-title">Nutrition that fits the whole family.</div>
      <p class="hero-sub">
        Shared meals, individual calorie targets, pantry-aware planning,
        recipe discovery, equipment-based workouts and simple progress tracking.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DASHBOARD
# =========================================================
if page == "Dashboard":
    st.markdown('<div class="section-title">Family overview</div>', unsafe_allow_html=True)

    if not st.session_state.family:
        st.info("Add your first family member from the sidebar to start.")
    else:
        columns = st.columns(min(3, len(st.session_state.family)))
        for i, member in enumerate(st.session_state.family):
            n = member["nutrition"]
            with columns[i % len(columns)]:
                st.markdown(
                    f"""
                    <div class="member-card">
                        <span class="pill">{member['goal'].replace('_', ' ').title()}</span>
                        <h3 style="margin:.6rem 0 .15rem">{member['name']}</h3>
                        <p class="subtle" style="margin:.1rem 0">BMI {n['BMI']} · {member['activity_level'].replace('_',' ').title()}</p>
                        <h2 style="margin:.55rem 0;color:#587864">{n['Target']} <span style="font-size:.85rem">kcal/day</span></h2>
                        <span class="macro-chip">Protein {n['Protein']}g</span>
                        <span class="macro-chip">Carbs {n['Carbs']}g</span>
                        <span class="macro-chip">Fat {n['Fat']}g</span>
                        <span class="macro-chip">Fiber ~{n['Fiber']}g</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("### Today's snapshot")
        c1, c2, c3 = st.columns(3)
        c1.metric("Recipes in database", len(recipes_df))
        c2.metric("Pantry items", len(st.session_state.pantry))
        c3.metric("Daily family budget", f"Rs {st.session_state.budget['daily']:,}")

        if st.session_state.logs:
            logs_df = pd.DataFrame(st.session_state.logs)
            a, b = st.columns(2)

            with a:
                meals = logs_df[logs_df["type"] == "meal"]
                if not meals.empty:
                    counts = meals.groupby("member").size().reset_index(name="Meals")
                    fig = px.bar(counts, x="member", y="Meals", title="Meals logged")
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        showlegend=False,
                        margin=dict(l=10, r=10, t=45, b=10),
                    )
                    st.plotly_chart(fig, use_container_width=True)

            with b:
                workouts = logs_df[logs_df["type"] == "workout"]
                if not workouts.empty:
                    mins = workouts.groupby("member")["minutes"].sum().reset_index()
                    fig = px.bar(mins, x="member", y="minutes", title="Workout minutes")
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        showlegend=False,
                        margin=dict(l=10, r=10, t=45, b=10),
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.caption("Progress charts will appear after you log meals or workouts.")


# =========================================================
# MEAL PLAN
# =========================================================
elif page == "Meal Plan":
    st.markdown('<div class="section-title">Shared family meal plan</div>', unsafe_allow_html=True)

    if not st.session_state.family:
        st.warning("Please add at least one family member first.")
    else:
        with st.expander("Plan preferences", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                cuisines = st.multiselect(
                    "Preferred cuisines",
                    ["Desi / Pakistani", "Chinese", "Italian", "Continental", "Mixed"],
                    default=["Desi / Pakistani"],
                )
            with c2:
                preferences = st.multiselect(
                    "Meal preferences",
                    [
                        "Less oil",
                        "High protein",
                        "More fiber",
                        "Vegetarian options",
                        "Quick to cook",
                        "Budget friendly",
                    ],
                    default=["Less oil", "High protein"],
                )

        if st.button("✨ Generate detailed meal plan", type="primary", use_container_width=True):
            with st.spinner("Building your family plan..."):
                safe_recipes = get_cuisine_recipes(
                    recipes_df, cuisines, family=st.session_state.family
                )

                family_info = [
                    {
                        "name": m["name"],
                        "goal": m["goal"],
                        "target_calories": m["nutrition"]["Target"],
                        "protein_g": m["nutrition"]["Protein"],
                        "allergies": m["allergies"],
                        "medical_conditions": m["medical"],
                    }
                    for m in st.session_state.family
                ]

                breakfast_pool = recipe_pool(safe_recipes, 450, "breakfast")
                lunch_pool = recipe_pool(safe_recipes, 700, "lunch")
                snack_pool = recipe_pool(safe_recipes, 350, "snack")
                dinner_pool = recipe_pool(safe_recipes, 650, "dinner")

                # Tested-app fallback, improved only for presentation/portion sanity.
                fallback = {
                    "day": "Day 1",
                    "meals": [
                        {
                            "meal": "Breakfast",
                            "main": "Vegetable Omelette + Whole Wheat Roti",
                            "sides": ["Cucumber", "Green tea"],
                            "calories": 380,
                            "protein": 22,
                            "carbs": 28,
                            "fat": 18,
                            "fiber_tip": "Add extra salad, fruit or seeds for more fiber.",
                            "protein_tip": "Eggs already provide a strong protein base.",
                            "description": "A balanced, familiar breakfast with vegetables and whole grains.",
                        },
                        {
                            "meal": "Lunch",
                            "main": "Lean Chicken Karahi + Brown Rice",
                            "sides": ["Mixed salad", "Raita"],
                            "calories": 520,
                            "protein": 38,
                            "carbs": 45,
                            "fat": 18,
                            "fiber_tip": "Brown rice and salad improve the fiber content.",
                            "protein_tip": "Chicken provides lean protein.",
                            "description": "Home-style chicken karahi prepared with less oil.",
                        },
                        {
                            "meal": "Evening Snack",
                            "main": "Chana Chaat",
                            "sides": ["Lemon", "Coriander"],
                            "calories": 240,
                            "protein": 11,
                            "carbs": 38,
                            "fat": 5,
                            "fiber_tip": "Chickpeas are naturally rich in fiber.",
                            "protein_tip": "Add a boiled egg only if it fits the family's allergy needs.",
                            "description": "A light, filling chickpea snack.",
                        },
                        {
                            "meal": "Dinner",
                            "main": "Dal + Whole Wheat Roti",
                            "sides": ["Cucumber salad"],
                            "calories": 470,
                            "protein": 22,
                            "carbs": 62,
                            "fat": 13,
                            "fiber_tip": "Lentils and whole grains support fiber intake.",
                            "protein_tip": "Lentils provide plant protein.",
                            "description": "A simple, comforting family dinner.",
                        },
                    ],
                    "notes": f"Fallback plan · daily food budget target ≈ Rs {st.session_state.budget['daily']}.",
                }

                for meal in fallback["meals"]:
                    meal["portions"] = {}
                    for member in st.session_state.family:
                        goal = member["goal"]
                        if goal == "weight_loss":
                            portion = "0.85 serving"
                        elif goal == "weight_gain":
                            portion = "1.15 servings"
                        else:
                            portion = "1 serving"
                        meal["portions"][member["name"]] = portion

                plan = fallback

                if client:
                    prompt = f"""
You are helping a family plan everyday meals.

Create ONE shared Day 1 meal plan with exactly four meals:
Breakfast, Lunch, Evening Snack, Dinner.

Selected cuisines: {json.dumps(cuisines)}
Preferences: {json.dumps(preferences)}
Family: {json.dumps(family_info)}
Pantry: {json.dumps(st.session_state.pantry)}
Daily food budget: PKR {st.session_state.budget['daily']}

Use recipe names from these dataset pools whenever suitable:
Breakfast: {json.dumps(breakfast_pool[:8])}
Lunch: {json.dumps(lunch_pool[:8])}
Snack: {json.dumps(snack_pool[:8])}
Dinner: {json.dumps(dinner_pool[:8])}

Rules:
- Respect selected cuisines.
- Respect listed allergies. Never recommend a known allergen.
- Keep one shared dish per meal; customize PORTION SIZE per member.
- Do not claim medical treatment or disease reversal.
- Keep suggestions practical for home cooking and the stated budget.
- If nutrition numbers are unknown in the dataset, estimate modestly and do not imply they are lab-verified.

Return ONLY valid JSON:
{{
  "day": "Day 1",
  "meals": [
    {{
      "meal": "Breakfast",
      "main": "dish name",
      "sides": ["side 1"],
      "calories": 380,
      "protein": 22,
      "carbs": 30,
      "fat": 15,
      "fiber_tip": "short tip",
      "protein_tip": "short tip",
      "portions": {{"Person name": "1 serving"}},
      "description": "short description"
    }}
  ],
  "notes": "short plan note"
}}
"""
                    try:
                        response = client.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[
                                {
                                    "role": "system",
                                    "content": "Return valid JSON only. Follow allergy constraints carefully.",
                                },
                                {"role": "user", "content": prompt},
                            ],
                            temperature=0.25,
                            max_tokens=2200,
                        )
                        ai_plan = extract_json(response.choices[0].message.content)
                        if (
                            isinstance(ai_plan, dict)
                            and isinstance(ai_plan.get("meals"), list)
                            and len(ai_plan["meals"]) >= 4
                        ):
                            plan = ai_plan
                    except Exception as exc:
                        st.warning(f"AI was unavailable, so the built-in fallback plan is shown. ({exc})")

                st.session_state.meal_plan = plan

        plan = st.session_state.meal_plan
        if plan:
            st.success(f"{plan.get('day', 'Day 1')} plan is ready.")
            for meal in plan.get("meals", []):
                st.markdown(
                    f"""
                    <div class="plate-card">
                        <span class="pill">{meal.get('meal', 'Meal')}</span>
                        <h3 style="margin:.55rem 0 .3rem">{meal.get('main', 'Meal')}</h3>
                        <p class="subtle" style="margin:0">{meal.get('description', '')}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Calories", f"{meal.get('calories', '—')} kcal")
                c2.metric("Protein", f"{meal.get('protein', '—')} g")
                c3.metric("Carbs", f"{meal.get('carbs', '—')} g")
                c4.metric("Fat", f"{meal.get('fat', '—')} g")

                sides = meal.get("sides", [])
                if sides:
                    st.markdown("**Sides:** " + ", ".join(map(str, sides)))

                portions = meal.get("portions", {})
                if portions:
                    cols = st.columns(min(4, len(portions)))
                    for i, (person, portion) in enumerate(portions.items()):
                        cols[i % len(cols)].info(f"**{person}**\n\n{portion}")

                a, b = st.columns(2)
                a.info("🌿 " + str(meal.get("fiber_tip", "Add vegetables or whole grains where suitable.")))
                b.success("💪 " + str(meal.get("protein_tip", "Include an appropriate protein source.")))

            st.caption(plan.get("notes", ""))


# =========================================================
# RECIPES
# =========================================================
elif page == "Recipes":
    st.markdown('<div class="section-title">Recipe browser</div>', unsafe_allow_html=True)

    if recipes_df.empty:
        st.warning(
            "No recipe CSV was found. Put your recipe file inside the GitHub `data/` folder "
            "and name it `nutrinest_recipes_clean.csv` or `recipes.csv`."
        )
    else:
        c1, c2, c3 = st.columns([1.5, 1, 1])
        with c1:
            search = st.text_input("Search recipes", placeholder="e.g. chicken, pasta, chana")
        with c2:
            cuisines_available = ["All"] + sorted(
                recipes_df["cuisine"].dropna().astype(str).str.strip().replace("", "Unspecified").unique().tolist()
            )[:60]
            cuisine = st.selectbox("Cuisine", cuisines_available)
        with c3:
            if "calories" in recipes_df.columns and recipes_df["calories"].notna().any():
                max_cal = st.slider("Max calories", 100, 1000, 650, step=25)
            else:
                max_cal = 1000

        family_safe_only = st.toggle(
            "Hide recipes that may contain a selected family allergen",
            value=True,
        )

        filtered = recipes_df.copy()
        if family_safe_only:
            filtered = safe_for_family(filtered, st.session_state.family)

        if "calories" in filtered.columns:
            filtered = filtered[filtered["calories"].isna() | (filtered["calories"] <= max_cal)]

        if cuisine != "All":
            filtered = filtered[
                filtered["cuisine"].fillna("").astype(str).str.casefold() == cuisine.casefold()
            ]

        if search.strip():
            needle = search.strip().casefold()
            haystack = (
                filtered["recipe_name"].fillna("").astype(str)
                + " "
                + filtered["ingredients"].fillna("").astype(str)
            ).str.casefold()
            filtered = filtered[haystack.str.contains(re.escape(needle), na=False)]

        st.caption(f"{len(filtered)} recipes found")

        for idx, row in filtered.head(40).iterrows():
            name = row.get("recipe_name", "Unknown recipe")
            cal = row.get("calories", None)
            protein = row.get("protein_g", None)
            cuisine_name = row.get("cuisine", "Unspecified")

            label_parts = [str(name)]
            if pd.notna(cal):
                label_parts.append(f"{round(float(cal))} kcal")
            if pd.notna(protein):
                label_parts.append(f"{float(protein):g}g protein")

            with st.expander("  •  ".join(label_parts)):
                st.markdown(f"**Cuisine:** {cuisine_name}")
                if pd.notna(row.get("meal_type", None)):
                    st.markdown(f"**Meal type:** {row.get('meal_type')}")

                ingredients = row.get("ingredients", "")
                if pd.notna(ingredients) and str(ingredients).strip():
                    st.markdown("**Ingredients**")
                    parsed = parse_listish(ingredients)
                    if parsed:
                        st.write(" · ".join(parsed[:30]))
                    else:
                        st.write(str(ingredients))

                steps = row.get("steps", "")
                if pd.notna(steps) and str(steps).strip():
                    st.markdown("**Method**")
                    st.write(str(steps))

                metrics = st.columns(4)
                metrics[0].metric("Calories", "—" if pd.isna(cal) else f"{float(cal):.0f}")
                metrics[1].metric("Protein", "—" if pd.isna(protein) else f"{float(protein):g}g")
                carb = row.get("carbs_g", None)
                fat = row.get("fat_g", None)
                metrics[2].metric("Carbs", "—" if pd.isna(carb) else f"{float(carb):g}g")
                metrics[3].metric("Fat", "—" if pd.isna(fat) else f"{float(fat):g}g")


# =========================================================
# PANTRY
# =========================================================
elif page == "Pantry":
    st.markdown('<div class="section-title">My pantry</div>', unsafe_allow_html=True)
    st.caption("Add ingredients you already have. They are sent to the meal planner as preferred ingredients.")

    with st.form("pantry_form", clear_on_submit=True):
        c1, c2 = st.columns([5, 1])
        with c1:
            new_item = st.text_input("Ingredient", placeholder="e.g. chicken, daal, rice, yogurt")
        with c2:
            st.write("")
            st.write("")
            add = st.form_submit_button("Add", use_container_width=True)

    if add and new_item.strip():
        item = new_item.strip().lower()
        if item not in st.session_state.pantry:
            st.session_state.pantry.append(item)
            st.success(f"Added {item.title()}.")
        else:
            st.info("That ingredient is already in your pantry.")

    if st.session_state.pantry:
        st.markdown("### Available ingredients")
        for i, item in enumerate(st.session_state.pantry):
            c1, c2 = st.columns([8, 1])
            c1.markdown(f"<div class='soft-card'>🌿 <b>{item.title()}</b></div>", unsafe_allow_html=True)
            if c2.button("Remove", key=f"pantry_remove_{i}"):
                st.session_state.pantry.pop(i)
                st.rerun()

        if st.button("Clear pantry"):
            st.session_state.pantry = []
            st.rerun()
    else:
        st.info("Your pantry is empty.")


# =========================================================
# WORKOUT
# =========================================================
elif page == "Workout":
    st.markdown('<div class="section-title">Equipment-based workout</div>', unsafe_allow_html=True)

    if not st.session_state.family:
        st.warning("Please add a family member first.")
    else:
        selected = st.selectbox("Select member", [m["name"] for m in st.session_state.family])
        member = next(m for m in st.session_state.family if m["name"] == selected)

        st.markdown(
            f"""
            <div class="soft-card">
                <span class="pill">{member['workout_location'].title()}</span>
                <span class="pill">{member['goal'].replace('_',' ').title()}</span>
                <h3 style="margin:.65rem 0 .2rem">{member['name']}</h3>
                <p class="subtle" style="margin:0">
                    Equipment: {', '.join(member['equipment']).replace('_',' ')}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🏃 Generate 7-day workout", type="primary", use_container_width=True):
            with st.spinner("Creating workout plan..."):
                plan = {
                    "member": member["name"],
                    "week": [
                        {"day": 1, "focus": "Full Body", "exercises": [
                            {"name": "Bodyweight Squats", "sets": "3", "reps": "12"},
                            {"name": "Push-ups", "sets": "3", "reps": "10"},
                            {"name": "Walking", "duration": "20 min"},
                        ]},
                        {"day": 2, "focus": "Rest", "exercises": []},
                        {"day": 3, "focus": "Lower Body", "exercises": [
                            {"name": "Lunges", "sets": "3", "reps": "10 each"},
                            {"name": "Glute Bridges", "sets": "3", "reps": "15"},
                        ]},
                        {"day": 4, "focus": "Rest", "exercises": []},
                        {"day": 5, "focus": "Upper Body + Core", "exercises": [
                            {"name": "Wall / Incline Push-ups", "sets": "3", "reps": "12"},
                            {"name": "Plank", "duration": "30 sec"},
                        ]},
                        {"day": 6, "focus": "Cardio", "exercises": [
                            {"name": "Brisk Walk", "duration": "30 min"}
                        ]},
                        {"day": 7, "focus": "Recovery", "exercises": [
                            {"name": "Gentle Stretching", "duration": "15 min"}
                        ]},
                    ],
                }

                if client:
                    prompt = f"""
Create a practical 7-day workout plan.
Person: {member['name']}
Goal: {member['goal']}
Location: {member['workout_location']}
Equipment: {member['equipment']}
Activity level: {member['activity_level']}

Return ONLY JSON in this shape:
{{
  "member":"name",
  "week":[
    {{
      "day":1,
      "focus":"Full Body",
      "exercises":[
        {{"name":"Exercise","sets":"3","reps":"10"}},
        {{"name":"Walk","duration":"20 min"}}
      ]
    }}
  ]
}}
Keep it general, beginner-friendly, and do not present it as medical treatment.
"""
                    try:
                        response = client.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[
                                {"role": "system", "content": "Return valid JSON only."},
                                {"role": "user", "content": prompt},
                            ],
                            temperature=0.3,
                            max_tokens=1900,
                        )
                        ai_plan = extract_json(response.choices[0].message.content)
                        if isinstance(ai_plan, dict) and ai_plan.get("week"):
                            plan = ai_plan
                    except Exception:
                        pass

                st.session_state.workouts[member["name"]] = plan

        current = st.session_state.workouts.get(selected)
        if current:
            for day_item in current.get("week", []):
                day_num = day_item.get("day", "?")
                focus = day_item.get("focus", "Workout")
                with st.expander(f"Day {day_num} · {focus}", expanded=(day_num == 1)):
                    exercises = day_item.get("exercises", [])
                    if not exercises:
                        st.write("Recovery / rest day 🌙")
                    for ex in exercises:
                        if ex.get("duration"):
                            st.write(f"• **{ex.get('name','Exercise')}** — {ex['duration']}")
                        else:
                            st.write(
                                f"• **{ex.get('name','Exercise')}** — "
                                f"{ex.get('sets','')} × {ex.get('reps','')}"
                            )


# =========================================================
# PROGRESS
# =========================================================
elif page == "Progress":
    st.markdown('<div class="section-title">Progress tracking</div>', unsafe_allow_html=True)

    if not st.session_state.family:
        st.warning("Please add a family member first.")
    else:
        a, b = st.columns(2)

        with a:
            st.markdown("### 🍽 Log meal")
            with st.form("meal_log_form"):
                member_name = st.selectbox(
                    "Member",
                    [m["name"] for m in st.session_state.family],
                    key="meal_member",
                )
                meal_name = st.text_input("Meal", "Breakfast")
                meal_status = st.selectbox("Status", ["followed", "different", "skipped"])
                if st.form_submit_button("Log meal", use_container_width=True):
                    st.session_state.logs.append(
                        {
                            "date": str(date.today()),
                            "member": member_name,
                            "type": "meal",
                            "item": meal_name,
                            "status": meal_status,
                            "minutes": 0,
                        }
                    )
                    st.success("Meal logged.")

        with b:
            st.markdown("### 🏃 Log workout")
            with st.form("workout_log_form"):
                workout_member = st.selectbox(
                    "Member",
                    [m["name"] for m in st.session_state.family],
                    key="workout_member",
                )
                workout_status = st.selectbox("Status", ["completed", "skipped", "rest"])
                minutes = st.number_input("Minutes", 0, 180, 30)
                if st.form_submit_button("Log workout", use_container_width=True):
                    st.session_state.logs.append(
                        {
                            "date": str(date.today()),
                            "member": workout_member,
                            "type": "workout",
                            "status": workout_status,
                            "minutes": int(minutes) if workout_status == "completed" else 0,
                        }
                    )
                    st.success("Workout logged.")

        if st.session_state.logs:
            st.markdown("### Summary")
            summary_cols = st.columns(min(3, len(st.session_state.family)))
            for i, member in enumerate(st.session_state.family):
                logs = [x for x in st.session_state.logs if x["member"] == member["name"]]
                meals = [x for x in logs if x["type"] == "meal"]
                workouts = [x for x in logs if x["type"] == "workout"]
                followed = sum(x.get("status") == "followed" for x in meals)
                completed = sum(x.get("status") == "completed" for x in workouts)
                total_minutes = sum(x.get("minutes", 0) for x in workouts)

                with summary_cols[i % len(summary_cols)]:
                    st.markdown(
                        f"""
                        <div class="member-card">
                            <h3>{member['name']}</h3>
                            <p>Meals followed: <b>{followed}</b> / {len(meals)}</p>
                            <p>Workouts completed: <b>{completed}</b></p>
                            <p>Workout minutes: <b>{total_minutes}</b></p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            logs_df = pd.DataFrame(st.session_state.logs)
            st.dataframe(logs_df, use_container_width=True, hide_index=True)

            csv = logs_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download progress CSV",
                data=csv,
                file_name="nutrinest_progress.csv",
                mime="text/csv",
            )

            if st.button("Clear progress logs"):
                st.session_state.logs = []
                st.rerun()
        else:
            st.info("No progress entries yet.")


st.markdown(
    """
    <div class="footer-note">
      NutriNest provides general wellness planning, not medical diagnosis or individualized clinical treatment.
    </div>
    """,
    unsafe_allow_html=True,
)
