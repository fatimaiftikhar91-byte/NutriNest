import ast
import json
import os
import re
import random
from datetime import date, datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

try:
    from groq import Groq
except Exception:
    Groq = None


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NutriNest | Family Wellness",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# PREMIUM UI
# =========================================================

st.markdown(
    """
<style>

:root {
    --ink: #25302B;
    --muted: #68756E;
    --cream: #FBF8F3;
    --white: #FFFFFF;
    --sage: #E7F0E7;
    --mint: #EEF7F1;
    --peach: #FBE9DD;
    --lavender: #EEEAF7;
    --butter: #FFF3CF;
    --accent: #587864;
    --accent-dark: #395847;
    --gold: #C98D3D;
    --line: #E2DED5;
}

.stApp {
    background:
        radial-gradient(circle at 5% 0%, rgba(231,240,231,.85), transparent 25rem),
        radial-gradient(circle at 95% 5%, rgba(251,233,221,.75), transparent 27rem),
        linear-gradient(180deg, #FBF8F3 0%, #F8F7F2 100%);
    color: var(--ink);
}

.block-container {
    max-width: 1350px;
    padding-top: 1.4rem;
    padding-bottom: 4rem;
}

h1,h2,h3,h4,h5,h6,p,label,span {
    color: var(--ink);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#EAF2E9,#F7F1E8);
}

.hero {
    border-radius: 30px;
    padding: 2.3rem;
    margin-bottom: 1.4rem;
    background:
        linear-gradient(
            120deg,
            rgba(231,240,231,.95),
            rgba(251,233,221,.92),
            rgba(238,234,247,.95)
        );
    border: 1px solid rgba(88,120,100,.14);
    box-shadow: 0 18px 50px rgba(50,65,55,.08);
}

.hero-kicker {
    display:inline-block;
    padding:.4rem .8rem;
    border-radius:999px;
    background:rgba(255,255,255,.75);
    font-size:.78rem;
    font-weight:800;
    letter-spacing:.08em;
    color:#486454;
}

.hero-title {
    font-size:clamp(2rem,4vw,3.4rem);
    line-height:1.05;
    font-weight:900;
    letter-spacing:-.04em;
    margin:.65rem 0;
}

.hero-sub {
    max-width:800px;
    color:#58665F;
    font-size:1.05rem;
    line-height:1.6;
}

.quote-card {
    border-radius:22px;
    padding:1.4rem 1.6rem;
    margin:1rem 0 1.5rem;
    background:linear-gradient(135deg,#FFFDF8,#EEF7F1);
    border:1px solid #E1E6DE;
    box-shadow:0 10px 28px rgba(50,65,55,.06);
}

.quote-text {
    font-size:1.25rem;
    font-weight:800;
    line-height:1.5;
    color:#35493E;
}

.quote-author {
    color:#738078;
    font-size:.86rem;
    margin-top:.45rem;
}

.feature-card {
    min-height:190px;
    border-radius:23px;
    padding:1.25rem;
    border:1px solid #E2DED5;
    background:rgba(255,255,255,.90);
    box-shadow:0 9px 28px rgba(40,55,47,.055);
    transition:.2s ease;
    margin-bottom:1rem;
}

.feature-card:hover {
    transform:translateY(-4px);
    box-shadow:0 16px 36px rgba(40,55,47,.10);
}

.feature-icon {
    font-size:2.15rem;
}

.feature-title {
    font-size:1.1rem;
    font-weight:850;
    margin:.55rem 0 .25rem;
}

.feature-desc {
    color:#69766F;
    font-size:.88rem;
    line-height:1.45;
}

.member-card,
.soft-card,
.recipe-card,
.stat-card {
    border-radius:20px;
    padding:1.1rem 1.2rem;
    background:rgba(255,255,255,.92);
    border:1px solid #E2DED5;
    box-shadow:0 8px 25px rgba(40,55,47,.055);
    margin-bottom:.9rem;
}

.member-card {
    background:linear-gradient(145deg,#FFFFFF,#F1F7F1);
}

.recipe-card {
    background:linear-gradient(145deg,#FFFFFF,#FFF9EE);
}

.stat-card {
    text-align:center;
}

.big-number {
    font-size:1.9rem;
    font-weight:900;
    color:#486B56;
}

.small-label {
    color:#748078;
    font-size:.82rem;
}

.pill {
    display:inline-block;
    padding:.28rem .65rem;
    border-radius:999px;
    background:#F2EEE5;
    color:#675B49;
    font-size:.76rem;
    font-weight:750;
    margin:.15rem;
}

.macro-chip {
    display:inline-block;
    padding:.3rem .6rem;
    border-radius:999px;
    background:#EEF5EF;
    border:1px solid #DCE8DD;
    color:#456051;
    font-size:.78rem;
    font-weight:750;
    margin:.16rem;
}

.progress-wrap {
    background:#E9E6DE;
    border-radius:999px;
    height:10px;
    overflow:hidden;
    margin:.5rem 0;
}

.progress-fill {
    background:linear-gradient(90deg,#587864,#8AA891);
    height:100%;
    border-radius:999px;
}

.slideshow {
    position:relative;
    height:210px;
    overflow:hidden;
    border-radius:26px;
    margin-bottom:1.5rem;
}

.slide {
    position:absolute;
    inset:0;
    opacity:0;
    padding:2rem;
    display:flex;
    flex-direction:column;
    justify-content:center;
    animation:slideFade 20s infinite;
}

.slide:nth-child(1) {
    background:linear-gradient(120deg,#E7F0E7,#F4F8F2);
    animation-delay:0s;
}

.slide:nth-child(2) {
    background:linear-gradient(120deg,#FBE9DD,#FFF5ED);
    animation-delay:5s;
}

.slide:nth-child(3) {
    background:linear-gradient(120deg,#EEEAF7,#F7F5FC);
    animation-delay:10s;
}

.slide:nth-child(4) {
    background:linear-gradient(120deg,#FFF3CF,#FFF9E7);
    animation-delay:15s;
}

.slide h2 {
    margin:0 0 .4rem;
    font-size:1.75rem;
    font-weight:900;
}

.slide p {
    max-width:650px;
    color:#657169;
}

@keyframes slideFade {
    0% {opacity:0;}
    5% {opacity:1;}
    23% {opacity:1;}
    28% {opacity:0;}
    100% {opacity:0;}
}

.section-heading {
    font-size:1.45rem;
    font-weight:900;
    margin:1.4rem 0 .9rem;
}

.page-header {
    padding:1.3rem 1.5rem;
    border-radius:22px;
    background:linear-gradient(120deg,#EAF2E9,#FFF9F2);
    border:1px solid #E2DED5;
    margin-bottom:1.3rem;
}

.page-header h1 {
    margin:0;
    font-size:2rem;
    font-weight:900;
}

.page-header p {
    margin:.35rem 0 0;
    color:#69766F;
}

.stButton > button {
    border-radius:13px;
    min-height:2.65rem;
    font-weight:800;
    border:1px solid #587864;
    background:#587864;
    color:white !important;
    box-shadow:0 5px 14px rgba(57,88,71,.12);
}

.stButton > button:hover {
    background:#395847;
    border-color:#395847;
}

div[data-testid="stMetric"] {
    border-radius:18px;
    border:1px solid #E2DED5;
    background:rgba(255,255,255,.88);
    padding:.8rem 1rem;
}

[data-testid="stMetricValue"] {
    color:#3D5D4A;
    font-weight:900;
}

div[data-baseweb="select"] > div,
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border-radius:12px !important;
    background:white !important;
    color:#25302B !important;
}

div[data-testid="stExpander"] {
    border-radius:16px;
    border:1px solid #E2DED5;
    background:rgba(255,255,255,.72);
}

[data-testid="stDataFrame"] {
    border-radius:16px;
    overflow:hidden;
}

.back-button {
    margin-bottom:.5rem;
}

hr {
    border-color:#E4E0D7;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# DATA
# =========================================================

DATA_CANDIDATES = [
    "data/nutrinest_recipes_clean.csv",
    "data/recipes.csv",
    "data/nutrinest_recipes.csv",
    "nutrinest_recipes_clean.csv",
    "recipes.csv",
]


def find_recipe_file():
    for path in DATA_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


@st.cache_data(show_spinner=False)
def load_recipes():
    path = find_recipe_file()

    if not path:
        return pd.DataFrame(), None

    try:
        df = pd.read_csv(path)
    except Exception:
        return pd.DataFrame(), path

    df.columns = [str(c).strip().lower() for c in df.columns]

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

    df = df.rename(
        columns={
            old: new
            for old, new in rename_map.items()
            if old in df.columns
        }
    )

    for col in ["calories", "protein_g", "carbs_g", "fat_g"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    defaults = {
        "recipe_name": "Unnamed Recipe",
        "cuisine": "Unspecified",
        "meal_type": "Main",
        "ingredients": "",
        "steps": "",
        "allergens": "",
        "tags": "",
    }

    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = default

    return df, path


recipes_df, recipe_source = load_recipes()


# =========================================================
# AI
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

    if key and Groq:
        try:
            return Groq(api_key=key)
        except Exception:
            return None

    return None


client = get_client()


# =========================================================
# NUTRITION ENGINE
# =========================================================

def calculate_nutrition(age, sex, height_cm, weight_kg, activity, goal):

    if sex.lower() == "male":
        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            + 5
        )
    else:
        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            - 161
        )

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
        "BMI": round(
            weight_kg / ((height_cm / 100) ** 2),
            1
        ),
        "BMR": round(bmr),
        "TDEE": round(tdee),
        "Target": round(target),
        "Protein": round(target * .25 / 4),
        "Carbs": round(target * .50 / 4),
        "Fat": round(target * .25 / 9),
        "Fiber": 30,
    }


# =========================================================
# ALLERGY ENGINE
# =========================================================

ALLERGY_KEYWORDS = {
    "nuts": [
        "nut", "almond", "peanut", "cashew",
        "walnut", "pistachio"
    ],
    "dairy": [
        "milk", "cheese", "yogurt",
        "cream", "butter", "paneer"
    ],
    "gluten": [
        "wheat", "flour", "bread",
        "roti", "chapati", "pasta", "barley"
    ],
    "egg": [
        "egg", "eggs"
    ],
    "seafood": [
        "fish", "prawn", "shrimp",
        "seafood", "tuna", "salmon"
    ],
}


def safe_for_family(df, family):

    if df.empty or not family:
        return df.copy()

    blocked = []

    for member in family:

        for allergy in member.get("allergies", []):

            if allergy != "none":
                blocked.extend(
                    ALLERGY_KEYWORDS.get(
                        allergy,
                        [allergy]
                    )
                )

    if not blocked:
        return df.copy()

    text = (
        df["ingredients"]
        .fillna("")
        .astype(str)
        + " "
        + df["recipe_name"]
        .fillna("")
        .astype(str)
        + " "
        + df["allergens"]
        .fillna("")
        .astype(str)
    ).str.lower()

    mask = ~text.apply(
        lambda x: any(
            word in x for word in blocked
        )
    )

    return df[mask].copy()


# =========================================================
# PARSERS
# =========================================================

def parse_listish(value):

    if value is None:
        return []

    try:
        if pd.isna(value):
            return []
    except Exception:
        pass

    if isinstance(value, list):
        return [
            str(x).strip()
            for x in value
            if str(x).strip()
        ]

    text = str(value).strip()

    if not text:
        return []

    try:
        parsed = ast.literal_eval(text)

        if isinstance(parsed, list):
            return [
                str(x).strip()
                for x in parsed
                if str(x).strip()
            ]
    except Exception:
        pass

    return [
        x.strip()
        for x in re.split(r",|;|\||\n", text)
        if x.strip()
    ]


def normalize_text(value):
    return re.sub(
        r"[^a-z0-9 ]",
        " ",
        str(value).lower()
    )


# =========================================================
# CUISINES
# =========================================================

CUISINE_MAP = {
    "Desi / Pakistani": [
        "pakistani",
        "desi",
        "indian",
        "south asian",
        "home-style",
    ],
    "Chinese": [
        "chinese",
        "asian",
    ],
    "Italian": [
        "italian",
    ],
    "Continental": [
        "continental",
        "european",
        "american",
        "western",
        "international",
    ],
}


def get_cuisine_recipes(
    df,
    selected_cuisines,
    family=None
):

    if df.empty:
        return pd.DataFrame()

    data = safe_for_family(
        df,
        family or []
    )

    if not selected_cuisines:
        return data.reset_index(drop=True)

    if "Mixed" in selected_cuisines:
        return data.reset_index(drop=True)

    keywords = []

    for cuisine in selected_cuisines:
        keywords.extend(
            CUISINE_MAP.get(
                cuisine,
                [cuisine.lower()]
            )
        )

    mask = data["cuisine"].fillna("").astype(str).str.lower().apply(
        lambda x: any(
            keyword in x
            for keyword in keywords
        )
    )

    filtered = data[mask]

    if filtered.empty:
        return data.reset_index(drop=True)

    return filtered.reset_index(drop=True)


# =========================================================
# PANTRY ENGINE
# =========================================================

PANTRY_CATEGORIES = {
    "🥩 Proteins": [
        "Chicken",
        "Beef",
        "Mutton",
        "Fish",
        "Eggs",
        "Lentils",
        "Chickpeas",
        "Beans",
        "Tofu",
    ],
    "🌾 Grains & Staples": [
        "Rice",
        "Brown Rice",
        "Flour",
        "Whole Wheat Flour",
        "Oats",
        "Bread",
        "Pasta",
        "Noodles",
    ],
    "🥬 Vegetables": [
        "Tomato",
        "Onion",
        "Potato",
        "Spinach",
        "Carrot",
        "Cucumber",
        "Capsicum",
        "Cauliflower",
        "Peas",
        "Garlic",
        "Ginger",
    ],
    "🍎 Fruits": [
        "Apple",
        "Banana",
        "Orange",
        "Mango",
        "Guava",
        "Dates",
        "Lemon",
    ],
    "🥛 Dairy": [
        "Milk",
        "Yogurt",
        "Cheese",
        "Paneer",
        "Butter",
    ],
    "🌿 Herbs & Spices": [
        "Coriander",
        "Mint",
        "Cumin",
        "Turmeric",
        "Chilli",
        "Black Pepper",
        "Garam Masala",
    ],
    "🫙 Oils & Sauces": [
        "Cooking Oil",
        "Olive Oil",
        "Soy Sauce",
        "Tomato Sauce",
        "Chilli Sauce",
    ],
}


def pantry_match(recipe, pantry):

    pantry_normalized = [
        normalize_text(x)
        for x in pantry
    ]

    ingredients = parse_listish(
        recipe.get("ingredients", "")
    )

    if not ingredients:
        return 0, [], []

    matched = []
    missing = []

    for ingredient in ingredients:

        ing = normalize_text(
            ingredient
        )

        found = False

        for pantry_item in pantry_normalized:

            if (
                pantry_item in ing
                or ing in pantry_item
            ):
                found = True
                break

        if found:
            matched.append(
                ingredient
            )
        else:
            missing.append(
                ingredient
            )

    percentage = round(
        len(matched) /
        max(len(ingredients), 1)
        * 100
    )

    return percentage, matched, missing


def smart_recipe_matches(
    df,
    pantry,
    family=None,
    limit=12
):

    if df.empty:
        return pd.DataFrame()

    safe_df = safe_for_family(
        df,
        family or []
    )

    rows = []

    for _, row in safe_df.iterrows():

        match, matched, missing = pantry_match(
            row,
            pantry
        )

        item = row.to_dict()

        item["pantry_match"] = match
        item["matched_items"] = matched
        item["missing_items"] = missing

        rows.append(item)

    result = pd.DataFrame(rows)

    if result.empty:
        return result

    return result.sort_values(
        by=["pantry_match"],
        ascending=False
    ).head(limit)


# =========================================================
# AI JSON
# =========================================================

def extract_json(text):

    if not text:
        return None

    cleaned = text.strip()

    if "```" in cleaned:

        parts = cleaned.split("```")

        cleaned = max(
            parts,
            key=len
        )

        cleaned = re.sub(
            r"^json",
            "",
            cleaned,
            flags=re.I
        ).strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}") + 1

    if start < 0 or end <= start:
        return None

    try:
        return json.loads(
            cleaned[start:end]
        )
    except Exception:
        return None


# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "page": "Dashboard",
    "family": [],
    "logs": [],
    "meal_plan": None,
    "workouts": {},
    "pantry": [],
    "shopping_list": [],
    "favorites": [],
    "budget": {
        "period": "Monthly",
        "amount": 30000,
    },
}

for key, value in DEFAULTS.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# NAVIGATION
# =========================================================

def go(page):
    st.session_state.page = page
    st.rerun()


def page_back():
    if st.session_state.page != "Dashboard":
        if st.button(
            "← Back to Dashboard",
            key="back_dashboard"
        ):
            go("Dashboard")


# =========================================================
# QUOTES
# =========================================================

QUOTES = [
    (
        "Small steps every day lead to big changes.",
        "Daily Motivation 🌱"
    ),
    (
        "Consistency beats perfection.",
        "Fitness Mindset 💪"
    ),
    (
        "Your health is an investment, not an expense.",
        "Wellness Reminder ❤️"
    ),
    (
        "Eat well. Move often. Rest deeply.",
        "Healthy Living 🥗"
    ),
    (
        "A healthy family is built one good choice at a time.",
        "Family Wellness 👨‍👩‍👧‍👦"
    ),
    (
        "Progress may be slow, but every healthy choice counts.",
        "Motivation ✨"
    ),
    (
        "Nourish your body with food that makes you feel good.",
        "Nutrition Tip 🍎"
    ),
    (
        "You do not need to be perfect. You just need to keep going.",
        "Fitness Mindset 🔥"
    ),
    (
        "Take care of your body. It is the only place you have to live.",
        "Health Reminder 💚"
    ),
    (
        "Healthy habits create a healthier future.",
        "Wellness 🌿"
    ),
]


def random_quote():

    return random.choice(
        QUOTES
    )


# =========================================================
# DASHBOARD
# =========================================================

def dashboard():

    quote, category = random_quote()

    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">
                SMART FAMILY WELLNESS
            </div>

            <div class="hero-title">
                Welcome to NutriNest 🥗
            </div>

            <p class="hero-sub">
                Your family's friendly nutrition, meal-planning,
                pantry, fitness and progress companion — all in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # SLIDESHOW
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="slideshow">

            <div class="slide">
                <h2>🥗 Personalized Nutrition</h2>
                <p>
                    Understand your family's calorie and macro targets
                    and make healthier everyday choices.
                </p>
            </div>

            <div class="slide">
                <h2>🍛 Smart Family Meals</h2>
                <p>
                    Create practical meals with individual portions,
                    nutrition goals and family preferences in mind.
                </p>
            </div>

            <div class="slide">
                <h2>🧺 Cook What You Have</h2>
                <p>
                    Select ingredients already in your pantry and
                    discover recipes you can make right now.
                </p>
            </div>

            <div class="slide">
                <h2>💪 Move & Track Progress</h2>
                <p>
                    Build weekly workouts and visualize your health
                    and fitness journey over time.
                </p>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # QUOTE
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="quote-card">
            <div class="quote-text">
                “{quote}”
            </div>
            <div class="quote-author">
                {category}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # QUICK STATS
    # -----------------------------------------------------

    total_calories = sum(
        m["nutrition"]["Target"]
        for m in st.session_state.family
    )

    daily_budget = (
        st.session_state.budget["amount"]
        if st.session_state.budget["period"] == "Daily"
        else 0
    )

    if st.session_state.budget["period"] == "Weekly":
        daily_budget = (
            st.session_state.budget["amount"] / 7
        )

    elif st.session_state.budget["period"] == "Monthly":
        daily_budget = (
            st.session_state.budget["amount"] / 30
        )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Family Members",
        len(st.session_state.family)
    )

    c2.metric(
        "Daily Calories",
        f"{total_calories:,}"
    )

    c3.metric(
        "Pantry Items",
        len(st.session_state.pantry)
    )

    c4.metric(
        "Daily Budget",
        f"Rs {daily_budget:,.0f}"
    )

    # -----------------------------------------------------
    # FEATURE CARDS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">Everything your family needs 💚</div>',
        unsafe_allow_html=True,
    )

    features = [
        (
            "👨‍👩‍👧‍👦",
            "Family Profiles",
            "Members, goals, BMI, BMR, TDEE and personalized nutrition targets.",
            "Family Profiles",
        ),
        (
            "🍽️",
            "Smart Meal Planner",
            "Create a complete family-friendly 7-day meal plan.",
            "Meal Planner",
        ),
        (
            "🧺",
            "Smart Pantry",
            "Select what you already have and discover meals you can cook.",
            "Smart Pantry",
        ),
        (
            "🍛",
            "Recipe Explorer",
            "Explore recipes by cuisine, meal type, nutrition and pantry match.",
            "Recipe Explorer",
        ),
        (
            "💰",
            "Budget & Shopping",
            "Manage household or individual budgets and smart shopping lists.",
            "Budget & Shopping",
        ),
        (
            "💪",
            "Workout Planner",
            "Build a personalized 7-day workout routine around goals and equipment.",
            "Workout Planner",
        ),
        (
            "📊",
            "Progress",
            "Track weight, BMI, meals, calories and workout consistency.",
            "Progress",
        ),
        (
            "❤️",
            "Favorites",
            "Keep your favorite recipes together for quick access.",
            "Favorites",
        ),
    ]

    for start in range(0, len(features), 4):

        row = features[start:start + 4]

        cols = st.columns(4)

        for col, feature in zip(cols, row):

            icon, title, desc, destination = feature

            with col:

                st.markdown(
                    f"""
                    <div class="feature-card">
                        <div class="feature-icon">
                            {icon}
                        </div>
                        <div class="feature-title">
                            {title}
                        </div>
                        <div class="feature-desc">
                            {desc}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    f"Open {title} →",
                    key=f"dashboard_{title}",
                    use_container_width=True,
                ):
                    go(destination)

    # -----------------------------------------------------
    # DASHBOARD GRAPHS
    # -----------------------------------------------------

    if st.session_state.family:

        st.markdown(
            '<div class="section-heading">Family nutrition overview 📊</div>',
            unsafe_allow_html=True,
        )

        nutrition_rows = []

        for member in st.session_state.family:

            n = member["nutrition"]

            nutrition_rows.append(
                {
                    "Member": member["name"],
                    "Calories": n["Target"],
                    "Protein": n["Protein"],
                    "Carbs": n["Carbs"],
                    "Fat": n["Fat"],
                }
            )

        nutrition_df = pd.DataFrame(
            nutrition_rows
        )

        c1, c2 = st.columns(2)

        with c1:

            fig = px.bar(
                nutrition_df,
                x="Member",
                y=[
                    "Protein",
                    "Carbs",
                    "Fat"
                ],
                barmode="group",
                title="Daily macro targets",
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=10,
                    r=10,
                    t=50,
                    b=10
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with c2:

            fig = px.bar(
                nutrition_df,
                x="Member",
                y="Calories",
                title="Daily calorie targets",
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=10,
                    r=10,
                    t=50,
                    b=10
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# =========================================================
# FAMILY PROFILES
# =========================================================

def family_profiles():

    page_back()

    st.markdown(
        """
        <div class="page-header">
            <h1>👨‍👩‍👧‍👦 Family Profiles</h1>
            <p>
                Add each family member so NutriNest can personalize
                nutrition, portions, workouts and recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form(
        "family_form",
        clear_on_submit=True
    ):

        st.markdown("### Add / update member")

        c1, c2 = st.columns(2)

        with c1:

            name = st.text_input(
                "Name",
                placeholder="e.g. Father"
            )

            age = st.number_input(
                "Age",
                min_value=10,
                max_value=100,
                value=30
            )

            sex = st.selectbox(
                "Sex",
                ["male", "female"]
            )

            height = st.number_input(
                "Height (cm)",
                min_value=120,
                max_value=230,
                value=170
            )

            weight = st.number_input(
                "Weight (kg)",
                min_value=25,
                max_value=250,
                value=70
            )

        with c2:

            goal = st.selectbox(
                "Main goal",
                [
                    "weight_loss",
                    "maintenance",
                    "weight_gain",
                ],
                format_func=lambda x:
                    x.replace("_", " ").title()
            )

            activity = st.selectbox(
                "Activity level",
                [
                    "sedentary",
                    "light",
                    "moderate",
                    "active",
                    "very_active",
                ],
                index=2,
                format_func=lambda x:
                    x.replace("_", " ").title()
            )

            allergies = st.multiselect(
                "Food allergies",
                [
                    "none",
                    "nuts",
                    "dairy",
                    "gluten",
                    "egg",
                    "seafood",
                ],
                default=["none"]
            )

            medical = st.multiselect(
                "Health considerations",
                [
                    "none",
                    "diabetes",
                    "hypertension",
                    "thyroid",
                    "pcos",
                ],
                default=["none"]
            )

            workout_location = st.selectbox(
                "Workout location",
                ["home", "gym"]
            )

            equipment = st.multiselect(
                "Available equipment",
                [
                    "none",
                    "yoga_mat",
                    "dumbbells",
                    "resistance_bands",
                    "bench",
                    "full_gym",
                ],
                default=["yoga_mat"]
            )

        save = st.form_submit_button(
            "Save family member",
            use_container_width=True
        )

    if save:

        clean_name = (
            name.strip()
            or "Member"
        )

        nutrition = calculate_nutrition(
            age,
            sex,
            height,
            weight,
            activity,
            goal
        )

        member = {
            "name": clean_name,
            "age": int(age),
            "sex": sex,
            "height_cm": float(height),
            "weight_kg": float(weight),
            "goal": goal,
            "activity_level": activity,
            "allergies": allergies,
            "medical": medical,
            "workout_location": workout_location,
            "equipment": equipment,
            "nutrition": nutrition,
        }

        st.session_state.family = [
            m
            for m in st.session_state.family
            if m["name"].casefold()
            != clean_name.casefold()
        ]

        st.session_state.family.append(
            member
        )

        st.success(
            f"{clean_name} saved successfully."
        )

        st.rerun()

    if st.session_state.family:

        st.markdown(
            '<div class="section-heading">Family overview</div>',
            unsafe_allow_html=True
        )

        cols = st.columns(
            min(
                3,
                len(st.session_state.family)
            )
        )

        for i, member in enumerate(
            st.session_state.family
        ):

            n = member["nutrition"]

            with cols[i % len(cols)]:

                st.markdown(
                    f"""
                    <div class="member-card">
                        <span class="pill">
                            {member['goal'].replace('_',' ').title()}
                        </span>

                        <h3>
                            {member['name']}
                        </h3>

                        <p>
                            BMI {n['BMI']} ·
                            {member['activity_level'].replace('_',' ').title()}
                        </p>

                        <div class="big-number">
                            {n['Target']}
                            <span style="font-size:.8rem">
                                kcal/day
                            </span>
                        </div>

                        <span class="macro-chip">
                            Protein {n['Protein']}g
                        </span>

                        <span class="macro-chip">
                            Carbs {n['Carbs']}g
                        </span>

                        <span class="macro-chip">
                            Fat {n['Fat']}g
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    f"Remove {member['name']}",
                    key=f"remove_member_{member['name']}",
                    use_container_width=True
                ):

                    st.session_state.family = [
                        m
                        for m in st.session_state.family
                        if m["name"]
                        != member["name"]
                    ]

                    st.rerun()


# =========================================================
# SMART PANTRY
# =========================================================

def smart_pantry():

    page_back()

    st.markdown(
        """
        <div class="page-header">
            <h1>🧺 Smart Pantry</h1>
            <p>
                Tick the ingredients you already have.
                NutriNest will find recipes that use them.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    selected = []

    for category, items in PANTRY_CATEGORIES.items():

        with st.expander(
            category,
            expanded=True
        ):

            cols = st.columns(4)

            for i, item in enumerate(items):

                with cols[i % 4]:

                    checked = st.checkbox(
                        item,
                        value=item in st.session_state.pantry,
                        key=f"pantry_{item}"
                    )

                    if checked:
                        selected.append(
                            item
                        )

    st.session_state.pantry = selected

    st.markdown(
        '<div class="section-heading">Your pantry</div>',
        unsafe_allow_html=True
    )

    if selected:

        st.write(
            " · ".join(
                f"🌿 {x}"
                for x in selected
            )
        )

    else:

        st.info(
            "Select ingredients above to build your pantry."
        )

    # -----------------------------------------------------
    # SMART MATCHES
    # -----------------------------------------------------

    if selected and not recipes_df.empty:

        st.markdown(
            '<div class="section-heading">✨ What can I cook now?</div>',
            unsafe_allow_html=True
        )

        matches = smart_recipe_matches(
            recipes_df,
            selected,
            st.session_state.family,
            limit=12
        )

        if matches.empty:

            st.info(
                "No suitable recipes found."
            )

        else:

            for idx, row in matches.iterrows():

                name = row.get(
                    "recipe_name",
                    "Recipe"
                )

                match = int(
                    row.get(
                        "pantry_match",
                        0
                    )
                )

                calories = row.get(
                    "calories"
                )

                protein = row.get(
                    "protein_g"
                )

                missing = row.get(
                    "missing_items",
                    []
                )

                matched = row.get(
                    "matched_items",
                    []
                )

                with st.container():

                    st.markdown(
                        f"""
                        <div class="recipe-card">
                            <h3>
                                🍛 {name}
                            </h3>

                            <span class="pill">
                                🟢 {match}% pantry match
                            </span>

                            <span class="pill">
                                🔥 {round(float(calories)) if pd.notna(calories) else '—'} kcal
                            </span>

                            <span class="pill">
                                💪 {float(protein):g}g protein
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    a, b = st.columns(2)

                    with a:

                        st.markdown(
                            "**Available from pantry**"
                        )

                        if matched:
                            st.write(
                                " · ".join(
                                    matched[:12]
                                )
                            )
                        else:
                            st.caption(
                                "No exact pantry match."
                            )

                    with b:

                        st.markdown(
                            "**Still needed**"
                        )

                        if missing:

                            st.write(
                                " · ".join(
                                    missing[:10]
                                )
                            )

                            if st.button(
                                "🛒 Add missing ingredients",
                                key=f"shopping_{idx}"
                            ):

                                for item in missing:

                                    if item not in st.session_state.shopping_list:
                                        st.session_state.shopping_list.append(
                                            item
                                        )

                                st.success(
                                    "Missing ingredients added to shopping list."
                                )

                        else:

                            st.success(
                                "You have everything needed! 🎉"
                            )


# =========================================================
# RECIPE EXPLORER
# =========================================================

def recipe_explorer():

    page_back()

    st.markdown(
        """
        <div class="page-header">
            <h1>🍛 Recipe Explorer</h1>
            <p>
                Discover recipes by cuisine, meal type, nutrition,
                ingredients and pantry availability.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if recipes_df.empty:

        st.error(
            "Recipe CSV could not be found."
        )

        return

    c1, c2, c3 = st.columns(3)

    with c1:

        search = st.text_input(
            "🔎 Search",
            placeholder="Chicken, rice, daal..."
        )

    with c2:

        meal_type = st.selectbox(
            "Meal type",
            [
                "All",
                "Breakfast",
                "Lunch",
                "Dinner",
                "Snack",
                "Main",
            ]
        )

    with c3:

        cuisine_options = [
            "All"
        ] + sorted(
            recipes_df["cuisine"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        cuisine = st.selectbox(
            "Cuisine",
            cuisine_options
        )

    c1, c2, c3 = st.columns(3)

    with c1:

        max_cal = st.slider(
            "Maximum calories",
            100,
            1200,
            800
        )

    with c2:

        min_protein = st.slider(
            "Minimum protein (g)",
            0,
            80,
            0
        )

    with c3:

        pantry_only = st.checkbox(
            "Prioritize pantry matches"
        )

    data = safe_for_family(
        recipes_df,
        st.session_state.family
    ).copy()

    if search.strip():

        haystack = (
            data["recipe_name"].fillna("").astype(str)
            + " "
            + data["ingredients"].fillna("").astype(str)
            + " "
            + data["tags"].fillna("").astype(str)
        ).str.lower()

        data = data[
            haystack.str.contains(
                re.escape(search.lower()),
                na=False
            )
        ]

    if meal_type != "All":

        data = data[
            data["meal_type"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(
                meal_type.lower(),
                na=False
            )
        ]

    if cuisine != "All":

        data = data[
            data["cuisine"]
            .fillna("")
            .astype(str)
            .str.casefold()
            == cuisine.casefold()
        ]

    if "calories" in data.columns:

        data = data[
            data["calories"].isna()
            | (
                data["calories"]
                <= max_cal
            )
        ]

    if "protein_g" in data.columns:

        data = data[
            data["protein_g"].isna()
            | (
                data["protein_g"]
                >= min_protein
            )
        ]

    if pantry_only and st.session_state.pantry:

        scored = smart_recipe_matches(
            data,
            st.session_state.pantry,
            st.session_state.family,
            limit=100
        )

        data = scored

    st.caption(
        f"{len(data)} recipes found"
    )

    for idx, (_, row) in enumerate(
        data.head(40).iterrows()
    ):

        name = row.get(
            "recipe_name",
            "Recipe"
        )

        calories = row.get(
            "calories"
        )

        protein = row.get(
            "protein_g"
        )

        is_favorite = (
            name in
            st.session_state.favorites
        )

        with st.expander(
            f"🍽️ {name}"
            f"  ·  "
            f"{'⭐ Favorite' if is_favorite else '♡'}"
        ):

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Calories",
                "—"
                if pd.isna(calories)
                else f"{float(calories):.0f}"
            )

            c2.metric(
                "Protein",
                "—"
                if pd.isna(protein)
                else f"{float(protein):g}g"
            )

            c3.metric(
                "Carbs",
                "—"
                if pd.isna(row.get("carbs_g"))
                else f"{float(row.get('carbs_g')):g}g"
            )

            c4.metric(
                "Fat",
                "—"
                if pd.isna(row.get("fat_g"))
                else f"{float(row.get('fat_g')):g}g"
            )

            st.write(
                f"**Cuisine:** {row.get('cuisine','Unspecified')}"
            )

            st.write(
                f"**Meal:** {row.get('meal_type','Main')}"
            )

            ingredients = parse_listish(
                row.get(
                    "ingredients",
                    ""
                )
            )

            if ingredients:

                st.markdown(
                    "**Ingredients**"
                )

                st.write(
                    " · ".join(
                        ingredients[:30]
                    )
                )

            steps = row.get(
                "steps",
                ""
            )

            if pd.notna(steps) and str(steps).strip():

                st.markdown(
                    "**Method**"
                )

                st.write(
                    str(steps)
                )

            if st.session_state.pantry:

                match, matched, missing = pantry_match(
                    row,
                    st.session_state.pantry
                )

                st.progress(
                    match / 100,
                    text=f"Pantry match: {match}%"
                )

                if missing:

                    st.caption(
                        "Missing: "
                        + ", ".join(
                            missing[:8]
                        )
                    )

            fav_label = (
                "☆ Remove Favorite"
                if is_favorite
                else "⭐ Add Favorite"
            )

            if st.button(
                fav_label,
                key=f"favorite_{idx}_{name}"
            ):

                if is_favorite:

                    st.session_state.favorites.remove(
                        name
                    )

                else:

                    st.session_state.favorites.append(
                        name
                    )

                st.rerun()


# =========================================================
# BUDGET & SHOPPING
# =========================================================

def budget_shopping():

    page_back()

    st.markdown(
        """
        <div class="page-header">
            <h1>💰 Budget & Shopping</h1>
            <p>
                Plan food spending and keep your shopping list
                connected to your meal and pantry choices.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        period = st.selectbox(
            "Budget period",
            [
                "Daily",
                "Weekly",
                "Monthly",
            ],
            index=[
                "Daily",
                "Weekly",
                "Monthly",
            ].index(
                st.session_state.budget["period"]
            )
        )

    with c2:

        amount = st.number_input(
            f"{period} household budget (PKR)",
            min_value=500,
            max_value=1000000,
            value=int(
                st.session_state.budget["amount"]
            ),
            step=500
        )

    st.session_state.budget = {
        "period": period,
        "amount": amount
    }

    st.markdown(
        '<div class="section-heading">Budget snapshot</div>',
        unsafe_allow_html=True
    )

    daily_equivalent = amount

    if period == "Weekly":
        daily_equivalent = amount / 7

    elif period == "Monthly":
        daily_equivalent = amount / 30

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Household Budget",
        f"Rs {amount:,}"
    )

    c2.metric(
        "Approx. Daily",
        f"Rs {daily_equivalent:,.0f}"
    )

    c3.metric(
        "Pantry Items",
        len(st.session_state.pantry)
    )

    # -----------------------------------------------------
    # INDIVIDUAL ALLOCATION
    # -----------------------------------------------------

    if st.session_state.family:

        st.markdown(
            '<div class="section-heading">Optional individual allocations</div>',
            unsafe_allow_html=True
        )

        allocation_total = 0

        for member in st.session_state.family:

            value = st.number_input(
                f"{member['name']} allocation (PKR)",
                min_value=0,
                max_value=int(amount),
                value=0,
                step=500,
                key=f"budget_{member['name']}"
            )

            allocation_total += value

        if allocation_total > amount:

            st.error(
                "Individual allocations exceed the household budget."
            )

        else:

            st.success(
                f"Allocated: Rs {allocation_total:,} · "
                f"Unallocated: Rs {amount-allocation_total:,}"
            )

    # -----------------------------------------------------
    # SHOPPING
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">🛒 Smart Shopping List</div>',
        unsafe_allow_html=True
    )

    with st.form(
        "manual_shopping"
    ):

        item = st.text_input(
            "Add item",
            placeholder="e.g. yogurt, tomatoes..."
        )

        add = st.form_submit_button(
            "Add item",
            use_container_width=True
        )

    if add and item.strip():

        item = item.strip()

        if item not in st.session_state.shopping_list:

            st.session_state.shopping_list.append(
                item
            )

    if st.session_state.shopping_list:

        for i, item in enumerate(
            st.session_state.shopping_list
        ):

            c1, c2 = st.columns(
                [8, 1]
            )

            with c1:

                st.markdown(
                    f"🛒 **{item}**"
                )

            with c2:

                if st.button(
                    "×",
                    key=f"remove_shop_{i}"
                ):

                    st.session_state.shopping_list.pop(
                        i
                    )

                    st.rerun()

        if st.button(
            "Clear shopping list"
        ):

            st.session_state.shopping_list = []

            st.rerun()

    else:

        st.info(
            "Your shopping list is empty."
        )


# =========================================================
# MEAL PLANNER
# =========================================================

def meal_planner():

    page_back()

    st.markdown(
        """
        <div class="page-header">
            <h1>🍽️ Smart Family Meal Planner</h1>
            <p>
                Build a practical 7-day plan using family goals,
                allergies, pantry ingredients, cuisine and budget preferences.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.family:

        st.warning(
            "Add at least one family member first."
        )

        if st.button(
            "Add Family Member →"
        ):
            go("Family Profiles")

        return

    c1, c2 = st.columns(2)

    with c1:

        cuisines = st.multiselect(
            "Preferred cuisines",
            [
                "Desi / Pakistani",
                "Chinese",
                "Italian",
                "Continental",
                "Mixed",
            ],
            default=["Desi / Pakistani"]
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
                "Pantry first",
            ],
            default=[
                "Less oil",
                "High protein"
            ]
        )

    use_pantry = (
        "Pantry first" in preferences
        and bool(st.session_state.pantry)
    )

    if use_pantry:

        st.success(
            f"🧺 Pantry-first planning enabled — "
            f"{len(st.session_state.pantry)} ingredients available."
        )

    if st.button(
        "✨ Generate 7-Day Family Meal Plan",
        type="primary",
        use_container_width=True
    ):

        safe_df = get_cuisine_recipes(
            recipes_df,
            cuisines,
            st.session_state.family
        )

        if safe_df.empty:

            st.error(
                "No suitable recipes found."
            )

            return

        # -------------------------------------------------
        # PANTRY PRIORITY
        # -------------------------------------------------

        if use_pantry:

            scored = smart_recipe_matches(
                safe_df,
                st.session_state.pantry,
                st.session_state.family,
                limit=100
            )

            if not scored.empty:

                safe_df = scored

        # -------------------------------------------------
        # FALLBACK PLAN
        # -------------------------------------------------

        fallback_meals = [
            (
                "Breakfast",
                "Vegetable Omelette + Whole Wheat Roti",
                380,
                22
            ),
            (
                "Lunch",
                "Chicken Karahi + Brown Rice",
                520,
                38
            ),
            (
                "Evening Snack",
                "Chana Chaat",
                240,
                11
            ),
            (
                "Dinner",
                "Dal + Whole Wheat Roti + Salad",
                470,
                22
            ),
        ]

        fallback = []

        for day in range(1, 8):

            daily = []

            for meal, main, cal, protein in fallback_meals:

                portions = {}

                for member in st.session_state.family:

                    if member["goal"] == "weight_loss":
                        portions[
                            member["name"]
                        ] = "0.85 serving"

                    elif member["goal"] == "weight_gain":
                        portions[
                            member["name"]
                        ] = "1.15 servings"

                    else:
                        portions[
                            member["name"]
                        ] = "1 serving"

                daily.append(
                    {
                        "meal": meal,
                        "main": main,
                        "calories": cal,
                        "protein": protein,
                        "portions": portions,
                    }
                )

            fallback.append(
                {
                    "day": day,
                    "meals": daily
                }
            )

        plan = {
            "days": fallback,
            "notes": (
                "Family plan generated with allergy-aware "
                "and nutrition-aware defaults."
            )
        }

        # -------------------------------------------------
        # GROQ AI
        # -------------------------------------------------

        if client:

            family_info = []

            for member in st.session_state.family:

                family_info.append(
                    {
                        "name": member["name"],
                        "goal": member["goal"],
                        "target_calories": member["nutrition"]["Target"],
                        "protein": member["nutrition"]["Protein"],
                        "allergies": member["allergies"],
                        "medical": member["medical"],
                    }
                )

            recipe_sample = (
                safe_df[
                    [
                        "recipe_name",
                        "meal_type",
                        "calories",
                        "protein_g",
                        "ingredients",
                    ]
                ]
                .head(40)
                .fillna("")
                .to_dict("records")
            )

            prompt = f"""
Create a practical 7-day shared family meal plan.

Family:
{json.dumps(family_info)}

Cuisines:
{json.dumps(cuisines)}

Preferences:
{json.dumps(preferences)}

Pantry:
{json.dumps(st.session_state.pantry)}

Available recipes:
{json.dumps(recipe_sample)}

Requirements:
- Exactly 7 days.
- Each day must have Breakfast, Lunch,
  Evening Snack and Dinner.
- Shared meals should be family-friendly.
- Individual portions can differ.
- Respect allergies.
- Prefer pantry ingredients.
- Prefer reasonable calorie and protein targets.
- Avoid extreme dieting.
- Keep meals realistic for a household.
- Do not provide medical treatment.

Return ONLY valid JSON:

{{
  "days": [
    {{
      "day": 1,
      "meals": [
        {{
          "meal": "Breakfast",
          "main": "Recipe",
          "calories": 400,
          "protein": 25,
          "portions": {{
             "Member": "1 serving"
          }}
        }}
      ]
    }}
  ],
  "notes": "..."
}}
"""

            try:

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": "Return valid JSON only."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        },
                    ],
                    temperature=.35,
                    max_tokens=5000,
                )

                ai_plan = extract_json(
                    response.choices[0].message.content
                )

                if (
                    isinstance(ai_plan, dict)
                    and ai_plan.get("days")
                ):

                    plan = ai_plan

            except Exception:
                pass

        st.session_state.meal_plan = plan

        st.success(
            "Your 7-day family plan is ready! 🎉"
        )

    # -----------------------------------------------------
    # DISPLAY PLAN
    # -----------------------------------------------------

    if st.session_state.meal_plan:

        plan = st.session_state.meal_plan

        st.markdown(
            '<div class="section-heading">Your weekly plan 📅</div>',
            unsafe_allow_html=True
        )

        for day in plan.get(
            "days",
            []
        ):

            day_num = day.get(
                "day",
                "?"
            )

            with st.expander(
                f"Day {day_num}",
                expanded=(day_num == 1)
            ):

                for meal in day.get(
                    "meals",
                    []
                ):

                    name = meal.get(
                        "main",
                        "Meal"
                    )

                    st.markdown(
                        f"""
                        <div class="soft-card">
                            <h3>
                                {meal.get('meal','Meal')}
                                · {name}
                            </h3>

                            <span class="macro-chip">
                                🔥 {meal.get('calories','—')} kcal
                            </span>

                            <span class="macro-chip">
                                💪 {meal.get('protein','—')}g protein
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    portions = meal.get(
                        "portions",
                        {}
                    )

                    if portions:

                        st.markdown(
                            "**Individual portions**"
                        )

                        for member, portion in portions.items():

                            st.write(
                                f"👤 **{member}:** {portion}"
                            )

        notes = plan.get(
            "notes"
        )

        if notes:

            st.info(
                f"💡 {notes}"
            )


# =========================================================
# WORKOUT
# =========================================================

def workout_planner():

    page_back()

    st.markdown(
        """
        <div class="page-header">
            <h1>💪 Workout Planner</h1>
            <p>
                Create a simple weekly fitness routine based on
                your goal, activity level, location and equipment.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.family:

        st.warning(
            "Add a family member first."
        )

        return

    names = [
        m["name"]
        for m in st.session_state.family
    ]

    selected = st.selectbox(
        "Select member",
        names
    )

    member = next(
        m
        for m in st.session_state.family
        if m["name"] == selected
    )

    st.markdown(
        f"""
        <div class="soft-card">
            <span class="pill">
                {member['goal'].replace('_',' ').title()}
            </span>

            <span class="pill">
                {member['workout_location'].title()}
            </span>

            <p>
                <b>Equipment:</b>
                {', '.join(member['equipment']).replace('_',' ')}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🏃 Generate 7-Day Workout",
        type="primary",
        use_container_width=True
    ):

        fallback = {
            "member": selected,
            "week": [
                {
                    "day": 1,
                    "focus": "Full Body",
                    "exercises": [
                        {
                            "name": "Bodyweight Squats",
                            "sets": "3",
                            "reps": "12"
                        },
                        {
                            "name": "Incline Push-ups",
                            "sets": "3",
                            "reps": "10"
                        },
                        {
                            "name": "Brisk Walk",
                            "duration": "20 min"
                        }
                    ]
                },
                {
                    "day": 2,
                    "focus": "Recovery",
                    "exercises": [
                        {
                            "name": "Gentle Stretching",
                            "duration": "15 min"
                        }
                    ]
                },
                {
                    "day": 3,
                    "focus": "Lower Body",
                    "exercises": [
                        {
                            "name": "Lunges",
                            "sets": "3",
                            "reps": "10 each"
                        },
                        {
                            "name": "Glute Bridges",
                            "sets": "3",
                            "reps": "15"
                        }
                    ]
                },
                {
                    "day": 4,
                    "focus": "Rest",
                    "exercises": []
                },
                {
                    "day": 5,
                    "focus": "Upper Body + Core",
                    "exercises": [
                        {
                            "name": "Wall Push-ups",
                            "sets": "3",
                            "reps": "12"
                        },
                        {
                            "name": "Plank",
                            "duration": "30 sec"
                        }
                    ]
                },
                {
                    "day": 6,
                    "focus": "Cardio",
                    "exercises": [
                        {
                            "name": "Brisk Walking",
                            "duration": "30 min"
                        }
                    ]
                },
                {
                    "day": 7,
                    "focus": "Recovery",
                    "exercises": [
                        {
                            "name": "Gentle Stretching",
                            "duration": "15 min"
                        }
                    ]
                }
            ]
        }

        plan = fallback

        if client:

            prompt = f"""
Create a practical beginner-friendly 7-day workout plan.

Person:
{member['name']}

Goal:
{member['goal']}

Activity:
{member['activity_level']}

Location:
{member['workout_location']}

Equipment:
{member['equipment']}

Return ONLY JSON:

{{
  "member": "{member['name']}",
  "week": [
    {{
      "day": 1,
      "focus": "Full Body",
      "exercises": [
        {{
          "name": "Exercise",
          "sets": "3",
          "reps": "10"
        }}
      ]
    }}
  ]
}}

Keep it general and safe.
Do not present it as medical treatment.
"""

            try:

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": "Return valid JSON only."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=.3,
                    max_tokens=2500
                )

                ai_plan = extract_json(
                    response.choices[0].message.content
                )

                if (
                    isinstance(ai_plan, dict)
                    and ai_plan.get("week")
                ):
                    plan = ai_plan

            except Exception:
                pass

        st.session_state.workouts[
            selected
        ] = plan

        st.success(
            "Workout plan created! 💪"
        )

    current = st.session_state.workouts.get(
        selected
    )

    if current:

        for day in current.get(
            "week",
            []
        ):

            day_num = day.get(
                "day",
                "?"
            )

            focus = day.get(
                "focus",
                "Workout"
            )

            exercises = day.get(
                "exercises",
                []
            )

            with st.expander(
                f"Day {day_num} · {focus}",
                expanded=(day_num == 1)
            ):

                if not exercises:

                    st.write(
                        "🌙 Rest / recovery day"
                    )

                for exercise in exercises:

                    if exercise.get(
                        "duration"
                    ):

                        st.write(
                            f"• **{exercise.get('name','Exercise')}** "
                            f"— {exercise['duration']}"
                        )

                    else:

                        st.write(
                            f"• **{exercise.get('name','Exercise')}** "
                            f"— {exercise.get('sets','')} × "
                            f"{exercise.get('reps','')}"
                        )

                completed = st.checkbox(
                    "Mark this day complete",
                    key=f"complete_{selected}_{day_num}"
                )

                if completed:

                    st.session_state.logs.append(
                        {
                            "date": str(date.today()),
                            "member": selected,
                            "type": "workout",
                            "item": focus,
                            "minutes": 30,
                            "status": "completed",
                        }
                    )


# =========================================================
# PROGRESS
# =========================================================

def progress_page():

    page_back()

    st.markdown(
        """
        <div class="page-header">
            <h1>📊 Progress Tracker</h1>
            <p>
                Track your family's nutrition, weight, meals,
                calories and fitness consistency.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.family:

        st.warning(
            "Add a family member first."
        )

        return

    names = [
        m["name"]
        for m in st.session_state.family
    ]

    selected = st.selectbox(
        "Select member",
        names
    )

    member = next(
        m
        for m in st.session_state.family
        if m["name"] == selected
    )

    # -----------------------------------------------------
    # LOG PROGRESS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-heading">📝 Log today's progress</div>',
        unsafe_allow_html=True
    )

    with st.form(
        "progress_form"
    ):

        c1, c2, c3 = st.columns(3)

        with c1:

            weight = st.number_input(
                "Weight (kg)",
                min_value=25.0,
                max_value=250.0,
                value=float(
                    member["weight_kg"]
                ),
                step=.1
            )

        with c2:

            calories = st.number_input(
                "Calories consumed",
                min_value=0,
                max_value=10000,
                value=0,
                step=50
            )

        with c3:

            protein = st.number_input(
                "Protein consumed (g)",
                min_value=0,
                max_value=500,
                value=0,
                step=5
            )

        submit = st.form_submit_button(
            "Save Progress",
            use_container_width=True
        )

    if submit:

        st.session_state.logs.append(
            {
                "date": str(date.today()),
                "member": selected,
                "type": "progress",
                "weight": weight,
                "calories": calories,
                "protein": protein,
            }
        )

        st.success(
            "Progress saved! 🌱"
        )

    # -----------------------------------------------------
    # LOG MEAL
    # -----------------------------------------------------

    with st.expander(
        "🍽️ Log a meal"
    ):

        with st.form(
            "meal_log"
        ):

            meal_name = st.text_input(
                "Meal name",
                "Breakfast"
            )

            status = st.selectbox(
                "Status",
                [
                    "followed",
                    "different",
                    "skipped"
                ]
            )

            submit_meal = st.form_submit_button(
                "Log Meal"
            )

        if submit_meal:

            st.session_state.logs.append(
                {
                    "date": str(date.today()),
                    "member": selected,
                    "type": "meal",
                    "item": meal_name,
                    "status": status,
                }
            )

            st.success(
                "Meal logged."
            )

    # -----------------------------------------------------
    # ANALYTICS
    # -----------------------------------------------------

    progress_logs = [
        x
        for x in st.session_state.logs
        if x.get("member") == selected
        and x.get("type") == "progress"
    ]

    if progress_logs:

        df = pd.DataFrame(
            progress_logs
        )

        df["date"] = pd.to_datetime(
            df["date"]
        )

        df = df.sort_values(
            "date"
        )

        latest_weight = df.iloc[-1]["weight"]

        first_weight = df.iloc[0]["weight"]

        weight_change = (
            latest_weight
            - first_weight
        )

        target = member["nutrition"]["Target"]

        latest_calories = df.iloc[-1].get(
            "calories",
            0
        )

        latest_protein = df.iloc[-1].get(
            "protein",
            0
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Current Weight",
            f"{latest_weight:.1f} kg"
        )

        c2.metric(
            "Weight Change",
            f"{weight_change:+.1f} kg"
        )

        c3.metric(
            "Latest Calories",
            f"{latest_calories:,.0f}"
        )

        c4.metric(
            "Latest Protein",
            f"{latest_protein:,.0f} g"
        )

        st.markdown(
            '<div class="section-heading">📈 Weight trend</div>',
            unsafe_allow_html=True
        )

        fig = px.line(
            df,
            x="date",
            y="weight",
            markers=True,
            title=f"{selected} — Weight Over Time"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        c1, c2 = st.columns(2)

        with c1:

            fig = px.bar(
                df,
                x="date",
                y="calories",
                title="Calories consumed"
            )

            fig.add_hline(
                y=target,
                line_dash="dash",
                annotation_text="Target"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with c2:

            fig = px.line(
                df,
                x="date",
                y="protein",
                markers=True,
                title="Protein intake"
            )

            fig.add_hline(
                y=member["nutrition"]["Protein"],
                line_dash="dash",
                annotation_text="Target"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:

        st.info(
            "Log your first progress entry to unlock your graphs. 📈"
        )

    # -----------------------------------------------------
    # WORKOUT ANALYTICS
    # -----------------------------------------------------

    workout_logs = [
        x
        for x in st.session_state.logs
        if x.get("member") == selected
        and x.get("type") == "workout"
    ]

    if workout_logs:

        workout_df = pd.DataFrame(
            workout_logs
        )

        workout_df["date"] = pd.to_datetime(
            workout_df["date"]
        )

        workout_summary = (
            workout_df
            .groupby("date")
            .size()
            .reset_index(name="Completed Workouts")
        )

        st.markdown(
            '<div class="section-heading">💪 Workout consistency</div>',
            unsafe_allow_html=True
        )

        fig = px.bar(
            workout_summary,
            x="date",
            y="Completed Workouts",
            title="Workout completion"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# FAVORITES
# =========================================================

def favorites_page():

    page_back()

    st.markdown(
        """
        <div class="page-header">
            <h1>❤️ Favorite Recipes</h1>
            <p>
                Your saved recipes in one convenient place.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.favorites:

        st.info(
            "No favorites yet. Open Recipe Explorer and save your favorites ⭐"
        )

        return

    if recipes_df.empty:

        return

    for favorite in st.session_state.favorites:

        matches = recipes_df[
            recipes_df["recipe_name"]
            .astype(str)
            .casefold()
            == favorite.casefold()
        ]

        if matches.empty:
            continue

        row = matches.iloc[0]

        with st.expander(
            f"❤️ {favorite}"
        ):

            st.write(
                f"**Cuisine:** {row.get('cuisine','Unspecified')}"
            )

            st.write(
                f"**Calories:** {row.get('calories','—')}"
            )

            st.write(
                f"**Protein:** {row.get('protein_g','—')}g"
            )

            ingredients = parse_listish(
                row.get("ingredients","")
            )

            if ingredients:

                st.write(
                    "**Ingredients:** "
                    + ", ".join(
                        ingredients[:20]
                    )
                )

            if st.button(
                "Remove Favorite",
                key=f"remove_fav_{favorite}"
            ):

                st.session_state.favorites.remove(
                    favorite
                )

                st.rerun()


# =========================================================
# MAIN ROUTER
# =========================================================

page = st.session_state.page

if page == "Dashboard":

    dashboard()

elif page == "Family Profiles":

    family_profiles()

elif page == "Meal Planner":

    meal_planner()

elif page == "Smart Pantry":

    smart_pantry()

elif page == "Recipe Explorer":

    recipe_explorer()

elif page == "Budget & Shopping":

    budget_shopping()

elif page == "Workout Planner":

    workout_planner()

elif page == "Progress":

    progress_page()

elif page == "Favorites":

    favorites_page()

else:

    st.session_state.page = "Dashboard"

    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<hr>

<div style="
    text-align:center;
    color:#7A847E;
    padding:1rem;
    font-size:.82rem;
">
    🥗 <b>NutriNest</b> · Smart Family Nutrition & Wellness
    <br>
    Eat well · Move well · Live well 💚
</div>
""",
    unsafe_allow_html=True
)
