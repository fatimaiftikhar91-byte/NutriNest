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


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NutriNest",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# DESIGN SYSTEM
# IMPORTANT:
# Every HTML block is passed through st.markdown(...,
# unsafe_allow_html=True), so HTML renders correctly.
# ============================================================

st.markdown(
    """
    <style>

    :root {
        --ink: #26342d;
        --muted: #68756e;
        --cream: #fbf8f3;
        --white: #ffffff;
        --sage: #e7f1e7;
        --mint: #edf7f0;
        --peach: #fbe9dd;
        --lavender: #eeeaf7;
        --butter: #fff4cf;
        --accent: #587864;
        --accent-dark: #3f5d4a;
        --line: #e2ded5;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 5% 0%,
                rgba(231,241,231,.85),
                transparent 28rem
            ),
            radial-gradient(
                circle at 95% 4%,
                rgba(251,233,221,.80),
                transparent 28rem
            ),
            var(--cream);

        color: var(--ink);
    }

    .block-container {
        max-width: 1380px;
        padding-top: 1.35rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--ink) !important;
    }

    [data-testid="stMetric"] {
        background: rgba(255,255,255,.94);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: .85rem;
        box-shadow: 0 6px 20px rgba(40,60,48,.05);
    }

    [data-testid="stMetricValue"] {
        color: var(--accent) !important;
        font-weight: 900;
    }

    .stButton > button {
        border-radius: 13px;
        font-weight: 800;
        min-height: 2.55rem;
    }

    .stButton > button[kind="primary"] {
        background: var(--accent);
        border-color: var(--accent);
        color: #ffffff;
    }

    .stButton > button:hover {
        border-color: var(--accent-dark);
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
    }

    /* HERO */

    .hero {
        padding: 2.15rem 2.3rem;
        border-radius: 30px;

        background:
            linear-gradient(
                120deg,
                #e6f0e6,
                #fbe9dd,
                #eeeaf7
            );

        border: 1px solid #dfe5dd;

        box-shadow:
            0 16px 42px rgba(45,65,53,.08);

        margin-bottom: 1rem;
    }

    .hero-badge {
        display: inline-block;

        padding: .4rem .8rem;

        border-radius: 999px;

        background:
            rgba(255,255,255,.80);

        color: #4c6957 !important;

        font-size: .76rem;

        font-weight: 900;

        letter-spacing: .08em;
    }

    .hero-title {
        font-size: 3rem;

        line-height: 1.05;

        font-weight: 950;

        letter-spacing: -.045em;

        margin-top: .7rem;
    }

    .hero-subtitle {
        max-width: 900px;

        color: #5f6d65 !important;

        font-size: 1.03rem;

        line-height: 1.6;

        margin-top: .55rem;
    }

    /* QUOTE */

    .quote-card {
        padding: 1.15rem 1.45rem;

        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                #fffdf7,
                #eef7f0
            );

        border: 1px solid #dfe6de;

        box-shadow:
            0 8px 24px rgba(40,60,48,.06);

        margin:
            1rem
            0
            1.3rem;
    }

    .quote {
        font-size: 1.18rem;

        font-weight: 850;

        color: #3d5948 !important;
    }

    .quote-category {
        margin-top: .35rem;

        color: #78847d !important;

        font-size: .8rem;
    }

    /* SLIDESHOW */

    .slideshow {
        position: relative;

        height: 205px;

        overflow: hidden;

        border-radius: 26px;

        margin:
            1rem
            0
            1.3rem;
    }

    .slide {
        position: absolute;

        inset: 0;

        padding: 2rem;

        display: flex;

        flex-direction: column;

        justify-content: center;

        opacity: 0;

        animation:
            slideFade
            20s
            infinite;
    }

    .slide:nth-child(1) {
        background:
            linear-gradient(
                120deg,
                #e6f0e6,
                #f5f9f4
            );
    }

    .slide:nth-child(2) {
        background:
            linear-gradient(
                120deg,
                #fbe8dc,
                #fff5ed
            );

        animation-delay: 5s;
    }

    .slide:nth-child(3) {
        background:
            linear-gradient(
                120deg,
                #eeeaf7,
                #f8f6fc
            );

        animation-delay: 10s;
    }

    .slide:nth-child(4) {
        background:
            linear-gradient(
                120deg,
                #fff1c9,
                #fff9e8
            );

        animation-delay: 15s;
    }

    .slide h2 {
        font-size: 1.8rem;

        margin:
            0
            0
            .35rem;

        font-weight: 950;
    }

    .slide p {
        max-width: 780px;

        color: #68756e !important;

        margin: 0;
    }

    @keyframes slideFade {

        0% {
            opacity: 0;
        }

        5% {
            opacity: 1;
        }

        23% {
            opacity: 1;
        }

        28% {
            opacity: 0;
        }

        100% {
            opacity: 0;
        }
    }

    /* SECTION */

    .section-title {
        font-size: 1.45rem;

        font-weight: 950;

        margin:
            1.25rem
            0
            .8rem;
    }

    /* FEATURE CARDS */

    .feature-card {
        min-height: 175px;

        padding: 1.2rem;

        border-radius: 22px;

        background:
            rgba(255,255,255,.94);

        border:
            1px solid
            var(--line);

        box-shadow:
            0 8px 26px
            rgba(45,60,50,.06);

        margin-bottom: .65rem;
    }

    .feature-icon {
        font-size: 2.2rem;
    }

    .feature-title {
        font-size: 1.06rem;

        font-weight: 900;

        margin-top: .4rem;
    }

    .feature-description {
        color: #6b7770 !important;

        font-size: .84rem;

        line-height: 1.45;

        margin-top: .25rem;
    }

    /* PAGE HEADER */

    .page-header {
        padding: 1.25rem 1.45rem;

        border-radius: 22px;

        background:
            linear-gradient(
                120deg,
                #eaf2e9,
                #fff9f2
            );

        border:
            1px solid
            var(--line);

        margin-bottom: 1.2rem;
    }

    .page-header h1 {
        margin: 0;

        font-size: 2rem;

        font-weight: 950;
    }

    .page-header p {
        margin: .35rem 0 0;

        color: #6b7770 !important;
    }

    /* CARDS */

    .soft-card,
    .recipe-card,
    .member-card,
    .plate-card {

        padding: 1.05rem 1.15rem;

        border-radius: 20px;

        background:
            rgba(255,255,255,.94);

        border:
            1px solid
            var(--line);

        box-shadow:
            0 7px 22px
            rgba(45,60,50,.05);

        margin-bottom: .8rem;
    }

    .recipe-card {
        background:
            linear-gradient(
                145deg,
                #ffffff,
                #fff9ef
            );
    }

    .member-card {
        background:
            linear-gradient(
                145deg,
                #ffffff,
                #f0f7f0
            );
    }

    .plate-card {
        background:
            linear-gradient(
                145deg,
                #ffffff,
                #f4f8f3
            );
    }

    /* BADGES */

    .pill,
    .macro-chip {

        display: inline-block;

        padding:
            .27rem
            .62rem;

        margin: .13rem;

        border-radius: 999px;

        font-size: .74rem;

        font-weight: 800;
    }

    .pill {
        background: #f1eee6;

        color: #655d4d !important;
    }

    .macro-chip {
        background: #edf5ef;

        color: #496352 !important;
    }

    /* FOOTER */

    .footer-note {
        text-align: center;

        color: #7a857f !important;

        font-size: .8rem;

        padding:
            1.5rem
            0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATASET
# ============================================================

DATA_PATHS = [
    "data/nutrinest_recipes_clean.csv",
    "data/recipes.csv",
    "data/nutrinest_recipes.csv",
    "nutrinest_recipes_clean.csv",
    "recipes.csv",
]


def find_dataset():

    for path in DATA_PATHS:

        if os.path.exists(path):

            return path

    return None


@st.cache_data
def load_recipes():

    path = find_dataset()

    if not path:

        return pd.DataFrame(), None

    try:

        df = pd.read_csv(path)

    except Exception:

        return pd.DataFrame(), path

    df.columns = [
        str(column).strip().lower()
        for column in df.columns
    ]

    aliases = {

        "name":
            "recipe_name",

        "recipe name":
            "recipe_name",

        "dish name":
            "recipe_name",

        "calories_per_serving":
            "calories",

        "calories per serving":
            "calories",

        "protein":
            "protein_g",

        "protein(g)":
            "protein_g",

        "protein per serving":
            "protein_g",

        "carbs":
            "carbs_g",

        "carbohydrates":
            "carbs_g",

        "carbs(g)":
            "carbs_g",

        "fat":
            "fat_g",

        "fat(g)":
            "fat_g",

        "cuisine_type":
            "cuisine",

        "cuisine type":
            "cuisine",

        "meal type":
            "meal_type",
    }

    for old, new in aliases.items():

        if (
            old in df.columns
            and new not in df.columns
        ):

            df = df.rename(
                columns={
                    old: new
                }
            )

    defaults = {

        "recipe_name":
            "Recipe",

        "meal_type":
            "Main",

        "cuisine":
            "Mixed",

        "ingredients":
            "",

        "steps":
            "",

        "allergens":
            "",

        "tags":
            "",

        "calories":
            0,

        "protein_g":
            0,

        "carbs_g":
            0,

        "fat_g":
            0,

        "fiber_g":
            0,

        "servings":
            1,

        "serving_size":
            "1 serving",
    }

    for column, default in defaults.items():

        if column not in df.columns:

            df[column] = default

    numeric_columns = [
        "calories",
        "protein_g",
        "carbs_g",
        "fat_g",
        "fiber_g",
        "servings",
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)

    return df, path


recipes_df, recipe_source = load_recipes()


# ============================================================
# SESSION STATE
# ============================================================

def initialize_state():

    defaults = {

        "page":
            "Dashboard",

        "family":
            [],

        "pantry":
            [],

        "favorites":
            [],

        "shopping_list":
            [],

        "meal_plan":
            None,

        "workouts":
            {},

        "logs":
            [],

        "budget_period":
            "Monthly",

        "budget_amount":
            30000,

        "budget_spent":
            0.0,

        "allocations":
            {},
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


initialize_state()


def go(page_name):

    st.session_state.page = page_name

    st.rerun()


# ============================================================
# HELPERS
# ============================================================

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
        for x in re.split(
            r"[,;|\n]",
            text
        )
        if x.strip()
    ]


def normalize_text(text):

    return re.sub(
        r"[^a-z0-9 ]",
        " ",
        str(text).lower()
    ).strip()


# ============================================================
# ALLERGY FILTER
# ============================================================

ALLERGY_TERMS = {

    "nuts": [
        "nut",
        "almond",
        "peanut",
        "cashew",
        "walnut",
        "pistachio",
    ],

    "dairy": [
        "milk",
        "cheese",
        "yogurt",
        "yoghurt",
        "cream",
        "butter",
        "paneer",
    ],

    "gluten": [
        "wheat",
        "flour",
        "bread",
        "roti",
        "chapati",
        "pasta",
        "barley",
    ],

    "egg": [
        "egg",
        "eggs",
    ],

    "seafood": [
        "fish",
        "prawn",
        "shrimp",
        "seafood",
        "tuna",
        "salmon",
    ],
}


def safe_for_family(row):

    allergies = []

    for member in st.session_state.family:

        allergies.extend(
            [
                str(a).lower()
                for a in member.get(
                    "allergies",
                    []
                )
                if str(a).lower()
                not in (
                    "none",
                    "",
                )
            ]
        )

    if not allergies:

        return True

    text = " ".join(
        [
            str(
                row.get(
                    "recipe_name",
                    ""
                )
            ),
            str(
                row.get(
                    "ingredients",
                    ""
                )
            ),
            str(
                row.get(
                    "allergens",
                    ""
                )
            ),
            str(
                row.get(
                    "tags",
                    ""
                )
            ),
        ]
    ).lower()

    for allergy in allergies:

        terms = ALLERGY_TERMS.get(
            allergy,
            [allergy]
        )

        for term in terms:

            if term in text:

                return False

    return True


# ============================================================
# PANTRY MATCH
# ============================================================

def pantry_match(row):

    ingredients = parse_listish(
        row.get(
            "ingredients",
            ""
        )
    )

    if not ingredients:

        return 0, [], []

    pantry = [
        normalize_text(item)
        for item
        in st.session_state.pantry
    ]

    matched = []
    missing = []

    for ingredient in ingredients:

        normalized_ingredient = normalize_text(
            ingredient
        )

        found = any(
            pantry_item in normalized_ingredient
            or normalized_ingredient in pantry_item
            for pantry_item in pantry
            if pantry_item
        )

        if found:

            matched.append(
                ingredient
            )

        else:

            missing.append(
                ingredient
            )

    percentage = round(
        100
        * len(matched)
        / max(
            1,
            len(ingredients)
        )
    )

    return (
        percentage,
        matched,
        missing,
    )


# ============================================================
# NUTRITION CALCULATOR
# ============================================================

def calculate_nutrition(
    age,
    sex,
    height_cm,
    weight_kg,
    activity,
    goal,
):

    bmr = (
        10 * weight_kg
        + 6.25 * height_cm
        - 5 * age
        + (
            5
            if sex == "Male"
            else -161
        )
    )

    activity_factors = {

        "Sedentary":
            1.20,

        "Light":
            1.375,

        "Moderate":
            1.55,

        "Active":
            1.725,

        "Very Active":
            1.90,
    }

    tdee = (
        bmr
        * activity_factors.get(
            activity,
            1.55
        )
    )

    if goal == "Weight Loss":

        target = tdee - 400

    elif goal == "Weight Gain":

        target = tdee + 300

    else:

        target = tdee

    target = max(
        1200,
        round(target)
    )

    bmi = weight_kg / (
        (height_cm / 100)
        ** 2
    )

    protein = target * 0.25 / 4
    carbs = target * 0.50 / 4
    fat = target * 0.25 / 9

    return {

        "BMI":
            round(
                bmi,
                1
            ),

        "BMR":
            round(bmr),

        "TDEE":
            round(tdee),

        "Target":
            target,

        "Protein":
            round(protein),

        "Carbs":
            round(carbs),

        "Fat":
            round(fat),

        "Fiber":
            30,
    }


# ============================================================
# GROQ
# ============================================================

def get_secret(name):

    try:

        value = st.secrets.get(
            name
        )

        if value:

            return value

    except Exception:

        pass

    return os.getenv(
        name
    )


def get_groq_client():

    if Groq is None:

        return None

    api_key = get_secret(
        "GROQ_API_KEY"
    )

    if not api_key:

        return None

    try:

        return Groq(
            api_key=api_key
        )

    except Exception:

        return None


groq_client = get_groq_client()


def extract_json(text):

    if not text:

        return None

    text = str(
        text
    ).strip()

    if "```" in text:

        parts = text.split(
            "```"
        )

        text = max(
            parts,
            key=len
        ).strip()

        if text.lower().startswith(
            "json"
        ):

            text = text[4:].strip()

    start = text.find(
        "{"
    )

    end = text.rfind(
        "}"
    )

    if (
        start < 0
        or end < 0
    ):

        return None

    try:

        return json.loads(
            text[
                start:
                end + 1
            ]
        )

    except Exception:

        return None


# ============================================================
# QUOTES
# ============================================================

QUOTES = [

    (
        "Healthy habits become easier when the whole family joins in.",
        "Family Health 🏡",
    ),

    (
        "Small healthy choices today create a stronger tomorrow.",
        "Healthy Living 🌱",
    ),

    (
        "Consistency is more powerful than perfection.",
        "Motivation 💚",
    ),

    (
        "Eat well, move often, rest deeply.",
        "Wellness 🌿",
    ),

    (
        "Your health is one of your greatest investments.",
        "Health ❤️",
    ),

    (
        "Every workout is a vote for the person you want to become.",
        "Fitness 💪",
    ),

    (
        "Nourish your body with food that helps you thrive.",
        "Nutrition 🥗",
    ),

    (
        "Progress may be slow, but it is still progress.",
        "Motivation 🔥",
    ),

    (
        "A healthy family grows through healthy habits together.",
        "Family Wellness 👨‍👩‍👧‍👦",
    ),

    (
        "You do not need to be perfect. Just keep moving forward.",
        "Mindset ✨",
    ),
]


def show_quote():

    index = (
        date.today().toordinal()
        % len(QUOTES)
    )

    text, category = QUOTES[
        index
    ]

    st.markdown(
        f"""
        <div class="quote-card">

            <div class="quote">
                “{text}”
            </div>

            <div class="quote-category">
                {category}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PANTRY OPTIONS
# ============================================================

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


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    # HERO

    st.markdown(
        """
        <div class="hero">

            <span class="hero-badge">
                SMART FAMILY WELLNESS
            </span>

            <div class="hero-title">
                Welcome to NutriNest 🥗
            </div>

            <div class="hero-subtitle">
                Your family's nutrition, meal planning,
                pantry, fitness and progress companion —
                beautifully organized in one place.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # SLIDESHOW

    st.markdown(
        """
        <div class="slideshow">

            <div class="slide">

                <h2>
                    🥗 Personalized Nutrition
                </h2>

                <p>
                    Understand calories, protein,
                    carbohydrates, fats and personal
                    nutrition targets.
                </p>

            </div>

            <div class="slide">

                <h2>
                    🍛 Smart Family Meal Planning
                </h2>

                <p>
                    Create practical shared meals while
                    keeping individual portions and
                    nutrition targets in mind.
                </p>

            </div>

            <div class="slide">

                <h2>
                    🧺 Cook From Your Pantry
                </h2>

                <p>
                    Select what you already have and
                    discover recipes you can make now.
                </p>

            </div>

            <div class="slide">

                <h2>
                    💪 Fitness Made Simple
                </h2>

                <p>
                    Build a 7-day routine, mark completed
                    workouts and follow your progress.
                </p>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    show_quote()

    # TOP STATS

    total_calories = sum(
        member["nutrition"]["Target"]
        for member
        in st.session_state.family
    )

    period = (
        st.session_state.budget_period
    )

    amount = (
        st.session_state.budget_amount
    )

    if period == "Daily":

        daily_budget = amount

    elif period == "Weekly":

        daily_budget = amount / 7

    else:

        daily_budget = amount / 30

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Family Members",
        len(
            st.session_state.family
        ),
    )

    c2.metric(
        "Daily Calories",
        f"{total_calories:,}",
    )

    c3.metric(
        "Pantry Items",
        len(
            st.session_state.pantry
        ),
    )

    c4.metric(
        "Daily Budget",
        f"Rs {daily_budget:,.0f}",
    )

    # MODULES

    st.markdown(
        '<div class="section-title">'
        "Your NutriNest modules 💚"
        "</div>",
        unsafe_allow_html=True,
    )

    modules = [

        (
            "👨‍👩‍👧‍👦",
            "Family Profiles",
            "Members, goals, allergies and nutrition targets.",
            "Family Profiles",
        ),

        (
            "🍽️",
            "Meal Planner",
            "Shared 7-day family meals with individual portions.",
            "Meal Planner",
        ),

        (
            "🧺",
            "Smart Pantry",
            "Checkbox pantry and cook-now recommendations.",
            "Smart Pantry",
        ),

        (
            "🍛",
            "Recipe Explorer",
            "Search, filter, nutrition and pantry matching.",
            "Recipe Explorer",
        ),

        (
            "💰",
            "Budget & Shopping",
            "Daily, weekly and monthly household budgeting.",
            "Budget & Shopping",
        ),

        (
            "💪",
            "Workout Planner",
            "Goal-based 7-day fitness schedule.",
            "Workout Planner",
        ),

        (
            "📊",
            "Progress Tracker",
            "Weight, BMI, calories, protein and workout trends.",
            "Progress",
        ),

        (
            "❤️",
            "Favorites",
            "Save and revisit favorite recipes.",
            "Favorites",
        ),
    ]

    for start in range(
        0,
        len(modules),
        4,
    ):

        columns = st.columns(4)

        for column, module in zip(
            columns,
            modules[
                start:
                start + 4
            ],
        ):

            icon, title, description, page = module

            with column:

                st.markdown(
                    f"""
                    <div class="feature-card">

                        <div class="feature-icon">
                            {icon}
                        </div>

                        <div class="feature-title">
                            {title}
                        </div>

                        <div class="feature-description">
                            {description}
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

                    go(page)

    # QUICK ACTIONS

    st.markdown(
        '<div class="section-title">'
        "Quick actions ⚡"
        "</div>",
        unsafe_allow_html=True,
    )

    quick_columns = st.columns(4)

    quick_actions = [

        (
            "➕ Add Family Member",
            "Family Profiles",
        ),

        (
            "🍽️ Create Meal Plan",
            "Meal Planner",
        ),

        (
            "🧺 Update Pantry",
            "Smart Pantry",
        ),

        (
            "📝 Log Progress",
            "Progress",
        ),
    ]

    for column, (
        label,
        page,
    ) in zip(
        quick_columns,
        quick_actions,
    ):

        with column:

            if st.button(
                label,
                key=f"quick_{page}",
                use_container_width=True,
            ):

                go(page)

    # FAMILY NUTRITION GRAPH

    if st.session_state.family:

        st.markdown(
            '<div class="section-title">'
            "Family nutrition overview 📊"
            "</div>",
            unsafe_allow_html=True,
        )

        rows = []

        for member in (
            st.session_state.family
        ):

            n = member[
                "nutrition"
            ]

            rows.append(
                {
                    "Member":
                        member["name"],

                    "Calories":
                        n["Target"],

                    "Protein":
                        n["Protein"],

                    "Carbs":
                        n["Carbs"],

                    "Fat":
                        n["Fat"],
                }
            )

        nutrition_df = pd.DataFrame(
            rows
        )

        a, b = st.columns(2)

        with a:

            figure = px.bar(
                nutrition_df,
                x="Member",
                y=[
                    "Protein",
                    "Carbs",
                    "Fat",
                ],
                barmode="group",
                title="Daily Macronutrient Targets",
            )

            figure.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            st.plotly_chart(
                figure,
                use_container_width=True,
            )

        with b:

            figure = px.bar(
                nutrition_df,
                x="Member",
                y="Calories",
                title="Daily Calorie Targets",
            )

            figure.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            st.plotly_chart(
                figure,
                use_container_width=True,
            )

    # ACTIVITY GRAPH

    if st.session_state.logs:

        logs_df = pd.DataFrame(
            st.session_state.logs
        )

        st.markdown(
            '<div class="section-title">'
            "Activity overview 📈"
            "</div>",
            unsafe_allow_html=True,
        )

        a, b = st.columns(2)

        with a:

            workouts = logs_df[
                logs_df["type"]
                == "workout"
            ]

            if not workouts.empty:

                grouped = (
                    workouts
                    .groupby(
                        "member",
                        as_index=False,
                    )["minutes"]
                    .sum()
                )

                figure = px.bar(
                    grouped,
                    x="member",
                    y="minutes",
                    title="Workout Minutes",
                )

                st.plotly_chart(
                    figure,
                    use_container_width=True,
                )

            else:

                st.info(
                    "Workout graph will appear "
                    "after logging workouts."
                )

        with b:

            meals = logs_df[
                logs_df["type"]
                == "meal"
            ]

            if not meals.empty:

                grouped = (
                    meals
                    .groupby(
                        [
                            "member",
                            "status",
                        ],
                        as_index=False,
                    )
                    .size()
                    .rename(
                        columns={
                            "size":
                                "count"
                        }
                    )
                )

                figure = px.bar(
                    grouped,
                    x="member",
                    y="count",
                    color="status",
                    title="Meal Tracking",
                )

                st.plotly_chart(
                    figure,
                    use_container_width=True,
                )

            else:

                st.info(
                    "Meal graph will appear "
                    "after logging meals."
                )


# ============================================================
# FAMILY PAGE
# ============================================================

def family_page():

    st.markdown(
        """
        <div class="page-header">

            <h1>
                👨‍👩‍👧‍👦 Family Profiles
            </h1>

            <p>
                Personalize nutrition, allergies,
                goals, portions and workouts for
                each family member.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form(
        "family_form",
        clear_on_submit=True,
    ):

        left, right = st.columns(2)

        with left:

            name = st.text_input(
                "Name",
                placeholder="Father",
            )

            age = st.number_input(
                "Age",
                min_value=10,
                max_value=100,
                value=35,
            )

            sex = st.selectbox(
                "Sex",
                [
                    "Male",
                    "Female",
                ],
            )

            height = st.number_input(
                "Height (cm)",
                min_value=120,
                max_value=230,
                value=170,
            )

            weight = st.number_input(
                "Weight (kg)",
                min_value=25.0,
                max_value=250.0,
                value=70.0,
                step=0.5,
            )

        with right:

            goal = st.selectbox(
                "Goal",
                [
                    "Weight Loss",
                    "Maintenance",
                    "Weight Gain",
                ],
            )

            activity = st.selectbox(
                "Activity Level",
                [
                    "Sedentary",
                    "Light",
                    "Moderate",
                    "Active",
                    "Very Active",
                ],
                index=2,
            )

            allergies = st.multiselect(
                "Food Allergies",
                [
                    "None",
                    "Nuts",
                    "Dairy",
                    "Gluten",
                    "Egg",
                    "Seafood",
                ],
                default=["None"],
            )

            conditions = st.multiselect(
                "Health Considerations",
                [
                    "None",
                    "Diabetes",
                    "Hypertension",
                    "Thyroid",
                    "PCOS",
                ],
                default=["None"],
            )

            location = st.selectbox(
                "Workout Location",
                [
                    "Home",
                    "Gym",
                ],
            )

            equipment = st.multiselect(
                "Available Equipment",
                [
                    "None",
                    "Yoga Mat",
                    "Dumbbells",
                    "Resistance Bands",
                    "Bench",
                    "Full Gym",
                ],
                default=[
                    "Yoga Mat"
                ],
            )

        save = st.form_submit_button(
            "Save Family Member",
            use_container_width=True,
        )

    if save:

        if not name.strip():

            st.error(
                "Please enter a name."
            )

        else:

            member_name = name.strip()

            member = {

                "name":
                    member_name,

                "age":
                    int(age),

                "sex":
                    sex,

                "height_cm":
                    float(height),

                "weight_kg":
                    float(weight),

                "goal":
                    goal,

                "activity_level":
                    activity,

                "allergies":
                    allergies,

                "medical":
                    conditions,

                "workout_location":
                    location,

                "equipment":
                    equipment,

                "nutrition":
                    calculate_nutrition(
                        age,
                        sex,
                        height,
                        weight,
                        activity,
                        goal,
                    ),
            }

            st.session_state.family = [

                existing

                for existing
                in st.session_state.family

                if existing["name"].casefold()
                != member_name.casefold()
            ]

            st.session_state.family.append(
                member
            )

            st.success(
                f"{member_name} saved successfully."
            )

            st.rerun()

    if st.session_state.family:

        st.markdown(
            '<div class="section-title">'
            "Family overview"
            "</div>",
            unsafe_allow_html=True,
        )

        columns = st.columns(
            min(
                3,
                len(
                    st.session_state.family
                ),
            )
        )

        for index, member in enumerate(
            st.session_state.family
        ):

            n = member[
                "nutrition"
            ]

            with columns[
                index
                % len(columns)
            ]:

                st.markdown(
                    f"""
                    <div class="member-card">

                        <span class="pill">
                            {member['goal']}
                        </span>

                        <h3>
                            👤 {member['name']}
                        </h3>

                        <p>
                            BMI {n['BMI']}
                            ·
                            {member['activity_level']}
                        </p>

                        <div style="
                            font-size:1.65rem;
                            font-weight:900;
                            color:#587864;
                        ">
                            {n['Target']}
                            kcal/day
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

                        <span class="macro-chip">
                            Fiber {n['Fiber']}g
                        </span>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    f"Remove {member['name']}",
                    key=f"remove_family_{index}",
                    use_container_width=True,
                ):

                    st.session_state.family.pop(
                        index
                    )

                    st.rerun()


# ============================================================
# PANTRY PAGE
# ============================================================

def pantry_page():

    st.markdown(
        """
        <div class="page-header">

            <h1>
                🧺 Smart Pantry
            </h1>

            <p>
                Select ingredients you already have.
                NutriNest will find recipes with the
                highest pantry match.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    selected = []

    for category, items in (
        PANTRY_CATEGORIES.items()
    ):

        with st.expander(
            category,
            expanded=True,
        ):

            columns = st.columns(4)

            for index, item in enumerate(
                items
            ):

                with columns[
                    index % 4
                ]:

                    checked = st.checkbox(
                        item,
                        value=(
                            item
                            in st.session_state.pantry
                        ),
                        key=(
                            f"pantry_"
                            f"{category}_"
                            f"{item}"
                        ),
                    )

                    if checked:

                        selected.append(
                            item
                        )

    st.session_state.pantry = selected

    if selected:

        st.success(
            "Pantry: "
            + " · ".join(
                selected
            )
        )

    else:

        st.info(
            "Select ingredients above "
            "to build your pantry."
        )

    if (
        recipes_df.empty
        or not selected
    ):

        return

    st.markdown(
        '<div class="section-title">'
        "✨ What can I cook now?"
        "</div>",
        unsafe_allow_html=True,
    )

    safe_recipes = recipes_df[
        recipes_df.apply(
            safe_for_family,
            axis=1,
        )
    ].copy()

    results = []

    for _, row in (
        safe_recipes.iterrows()
    ):

        percentage, matched, missing = (
            pantry_match(row)
        )

        results.append(
            (
                percentage,
                matched,
                missing,
                row,
            )
        )

    results.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    for index, (
        percentage,
        matched,
        missing,
        row,
    ) in enumerate(
        results[:20]
    ):

        st.markdown(
            f"""
            <div class="recipe-card">

                <h3>
                    🍛 {row['recipe_name']}
                </h3>

                <span class="pill">
                    🟢 {percentage}%
                    pantry match
                </span>

                <span class="pill">
                    🔥
                    {float(row['calories']):.0f}
                    kcal
                </span>

                <span class="pill">
                    💪
                    {float(row['protein_g']):.0f}g
                    protein
                </span>

            </div>
            """,
            unsafe_allow_html=True,
        )

        left, right = st.columns(2)

        with left:

            st.write(
                "**Available:** "
                + (
                    ", ".join(
                        matched[:12]
                    )
                    if matched
                    else "None"
                )
            )

        with right:

            st.write(
                "**Missing:** "
                + (
                    ", ".join(
                        missing[:12]
                    )
                    if missing
                    else "Nothing 🎉"
                )
            )

            if missing:

                if st.button(
                    "🛒 Add missing",
                    key=f"add_missing_{index}",
                ):

                    for item in missing:

                        if (
                            item
                            not in
                            st.session_state.shopping_list
                        ):

                            st.session_state.shopping_list.append(
                                item
                            )

                    st.success(
                        "Missing ingredients "
                        "added to shopping list."
                    )


# ============================================================
# RECIPE PAGE
# ============================================================

def recipes_page():

    st.markdown(
        """
        <div class="page-header">

            <h1>
                🍛 Recipe Explorer
            </h1>

            <p>
                Search by recipe, meal type,
                cuisine, nutrition and pantry match.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if recipes_df.empty:

        st.error(
            "Recipe dataset not found."
        )

        st.code(
            "data/nutrinest_recipes_clean.csv"
        )

        return

    a, b, c = st.columns(3)

    with a:

        search = st.text_input(
            "🔎 Search",
            placeholder=(
                "Chicken, rice, chana..."
            ),
        )

    with b:

        meal_options = [
            "All"
        ] + sorted(
            recipes_df[
                "meal_type"
            ]
            .astype(str)
            .dropna()
            .unique()
            .tolist()
        )

        meal_type = st.selectbox(
            "Meal Type",
            meal_options,
        )

    with c:

        cuisine_options = [
            "All"
        ] + sorted(
            recipes_df[
                "cuisine"
            ]
            .astype(str)
            .dropna()
            .unique()
            .tolist()
        )

        cuisine = st.selectbox(
            "Cuisine",
            cuisine_options,
        )

    a, b, c, d = st.columns(4)

    with a:

        max_calories = st.slider(
            "Max calories",
            100,
            1500,
            800,
            25,
        )

    with b:

        min_protein = st.slider(
            "Min protein (g)",
            0,
            100,
            0,
        )

    with c:

        filters = st.multiselect(
            "Nutrition filters",
            [
                "High Protein",
                "High Fiber",
                "Vegetarian",
                "Budget Friendly",
            ],
        )

    with d:

        pantry_first = st.checkbox(
            "Prioritize pantry match",
            value=True,
        )

    data = recipes_df[
        recipes_df.apply(
            safe_for_family,
            axis=1,
        )
    ].copy()

    if search.strip():

        searchable = (

            data["recipe_name"]
            .fillna("")
            .astype(str)

            + " "

            + data["ingredients"]
            .fillna("")
            .astype(str)

            + " "

            + data["tags"]
            .fillna("")
            .astype(str)
        ).str.lower()

        data = data[
            searchable.str.contains(
                re.escape(
                    search.lower()
                ),
                na=False,
            )
        ]

    if meal_type != "All":

        data = data[
            data["meal_type"]
            .astype(str)
            .str.casefold()
            .str.contains(
                meal_type.casefold(),
                na=False,
            )
        ]

    if cuisine != "All":

        data = data[
            data["cuisine"]
            .astype(str)
            .str.casefold()
            == cuisine.casefold()
        ]

    data = data[
        data["calories"]
        <= max_calories
    ]

    data = data[
        data["protein_g"]
        >= min_protein
    ]

    if filters:

        tag_text = (

            data["tags"]
            .fillna("")
            .astype(str)
            .str.lower()

            + " "

            + data["ingredients"]
            .fillna("")
            .astype(str)
            .str.lower()
        )

        if "High Protein" in filters:

            data = data[
                data["protein_g"]
                >= 25
            ]

        if "High Fiber" in filters:

            data = data[
                data["fiber_g"]
                >= 6
            ]

        if "Vegetarian" in filters:

            data = data[
                ~tag_text.str.contains(
                    "chicken|beef|mutton|fish|prawn|shrimp|meat",
                    na=False,
                )
            ]

        if "Budget Friendly" in filters:

            data = data[
                data["calories"]
                <= 600
            ]

    if (
        pantry_first
        and st.session_state.pantry
    ):

        data["pantry_match"] = data.apply(
            lambda row:
                pantry_match(row)[0],
            axis=1,
        )

        data = data.sort_values(
            "pantry_match",
            ascending=False,
        )

    st.caption(
        f"{len(data)} recipes found."
    )

    for index, (
        _,
        row,
    ) in enumerate(
        data.head(50).iterrows()
    ):

        name = str(
            row["recipe_name"]
        )

        pantry_percentage = (

            pantry_match(row)[0]

            if st.session_state.pantry

            else None
        )

        with st.expander(
            f"{'❤️' if name in st.session_state.favorites else '🍽️'} {name}"
        ):

            a, b, c, d = st.columns(4)

            a.metric(
                "Calories",
                f"{row['calories']:.0f}",
            )

            b.metric(
                "Protein",
                f"{row['protein_g']:.0f}g",
            )

            c.metric(
                "Carbs",
                f"{row['carbs_g']:.0f}g",
            )

            d.metric(
                "Fat",
                f"{row['fat_g']:.0f}g",
            )

            st.write(
                f"**Cuisine:** "
                f"{row['cuisine']}"
                f" · "
                f"**Meal:** "
                f"{row['meal_type']}"
            )

            if pantry_percentage is not None:

                st.progress(
                    pantry_percentage / 100,
                    text=(
                        "Pantry Match: "
                        f"{pantry_percentage}%"
                    ),
                )

            ingredients = parse_listish(
                row["ingredients"]
            )

            if ingredients:

                st.write(
                    "**Ingredients:** "
                    + " · ".join(
                        ingredients
                    )
                )

            steps = str(
                row.get(
                    "steps",
                    ""
                )
            )

            if steps.strip():

                st.write(
                    "**Method:** "
                    + steps
                )

            if (
                name
                not in st.session_state.favorites
            ):

                if st.button(
                    "⭐ Add Favorite",
                    key=f"favorite_{index}",
                ):

                    st.session_state.favorites.append(
                        name
                    )

                    st.rerun()

            else:

                if st.button(
                    "☆ Remove Favorite",
                    key=f"unfavorite_{index}",
                ):

                    st.session_state.favorites.remove(
                        name
                    )

                    st.rerun()


# ============================================================
# BUDGET
# ============================================================

def budget_page():

    st.markdown(
        """
        <div class="page-header">

            <h1>
                💰 Budget & Shopping
            </h1>

            <p>
                Manage daily, weekly or monthly household
                spending, individual allocations and shopping.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    a, b = st.columns(2)

    with a:

        period_options = [
            "Daily",
            "Weekly",
            "Monthly",
        ]

        period = st.selectbox(
            "Budget Period",
            period_options,
            index=period_options.index(
                st.session_state.budget_period
            ),
        )

    with b:

        amount = st.number_input(
            "Household Budget (PKR)",
            min_value=500,
            max_value=1_000_000,
            value=int(
                st.session_state.budget_amount
            ),
            step=500,
        )

    st.session_state.budget_period = (
        period
    )

    st.session_state.budget_amount = (
        float(amount)
    )

    if period == "Daily":

        daily = amount

    elif period == "Weekly":

        daily = amount / 7

    else:

        daily = amount / 30

    weekly = daily * 7

    monthly = daily * 30

    a, b, c = st.columns(3)

    a.metric(
        "Daily",
        f"Rs {daily:,.0f}",
    )

    b.metric(
        "Weekly",
        f"Rs {weekly:,.0f}",
    )

    c.metric(
        "Monthly",
        f"Rs {monthly:,.0f}",
    )

    st.markdown(
        '<div class="section-title">'
        "Household spending"
        "</div>",
        unsafe_allow_html=True,
    )

    spent = st.number_input(
        "Amount spent in this budget period (PKR)",
        min_value=0.0,
        max_value=float(amount),
        value=min(
            float(
                st.session_state.budget_spent
            ),
            float(amount),
        ),
        step=500.0,
    )

    st.session_state.budget_spent = (
        spent
    )

    remaining = max(
        0,
        amount - spent,
    )

    st.progress(
        min(
            1,
            spent / max(
                1,
                amount,
            ),
        ),
        text=(
            f"Used Rs {spent:,.0f}"
            f" · "
            f"Remaining Rs {remaining:,.0f}"
        ),
    )

    if st.session_state.family:

        st.markdown(
            '<div class="section-title">'
            "Individual allocations"
            "</div>",
            unsafe_allow_html=True,
        )

        total_allocated = 0

        for member in (
            st.session_state.family
        ):

            name = member[
                "name"
            ]

            current = float(
                st.session_state.allocations.get(
                    name,
                    0,
                )
            )

            allocation = st.number_input(
                f"{name} allocation",
                min_value=0.0,
                max_value=float(amount),
                value=min(
                    current,
                    float(amount),
                ),
                step=500.0,
                key=f"allocation_{name}",
            )

            st.session_state.allocations[
                name
            ] = allocation

            total_allocated += allocation

        if total_allocated > amount:

            st.error(
                "Individual allocations "
                "exceed the household budget."
            )

        else:

            st.success(
                f"Allocated Rs {total_allocated:,.0f}"
                f" · "
                f"Unallocated Rs "
                f"{amount-total_allocated:,.0f}"
            )

    st.markdown(
        '<div class="section-title">'
        "🛒 Shopping list"
        "</div>",
        unsafe_allow_html=True,
    )

    a, b = st.columns(
        [5, 1]
    )

    with a:

        item = st.text_input(
            "Add shopping item",
            placeholder=(
                "Tomatoes, chicken, oats..."
            ),
        )

    with b:

        st.write("")

        add_item = st.button(
            "Add",
            use_container_width=True,
        )

    if (
        add_item
        and item.strip()
    ):

        clean_item = item.strip()

        if (
            clean_item
            not in
            st.session_state.shopping_list
        ):

            st.session_state.shopping_list.append(
                clean_item
            )

        st.rerun()

    if st.session_state.shopping_list:

        for index, item in enumerate(
            st.session_state.shopping_list
        ):

            a, b = st.columns(
                [8, 1]
            )

            with a:

                st.markdown(
                    f"""
                    <div class="soft-card">
                        🛒 <b>{item}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with b:

                if st.button(
                    "×",
                    key=f"remove_shop_{index}",
                ):

                    st.session_state.shopping_list.pop(
                        index
                    )

                    st.rerun()

        if st.button(
            "Clear Shopping List"
        ):

            st.session_state.shopping_list = []

            st.rerun()

    else:

        st.info(
            "Shopping list is empty."
        )


# ============================================================
# MEAL PLANNER FALLBACK
# ============================================================

def fallback_meal_plan():

    base_meals = [

        (
            "Breakfast",
            "Vegetable Omelette + Whole Wheat Roti",
            380,
            22,
            28,
            18,
        ),

        (
            "Lunch",
            "Chicken Rice Bowl",
            520,
            35,
            48,
            15,
        ),

        (
            "Snack",
            "Chana Chaat",
            230,
            10,
            35,
            5,
        ),

        (
            "Dinner",
            "Daal + Roti + Salad",
            470,
            22,
            62,
            13,
        ),
    ]

    days = []

    for day_number in range(
        1,
        8,
    ):

        meals = []

        for (
            meal_name,
            recipe_name,
            calories,
            protein,
            carbs,
            fat,
        ) in base_meals:

            portions = {}

            for member in (
                st.session_state.family
            ):

                if (
                    member["goal"]
                    == "Weight Loss"
                ):

                    portion = (
                        "0.85 serving"
                    )

                elif (
                    member["goal"]
                    == "Weight Gain"
                ):

                    portion = (
                        "1.15 servings"
                    )

                else:

                    portion = (
                        "1 serving"
                    )

                portions[
                    member["name"]
                ] = portion

            meals.append(
                {

                    "meal":
                        meal_name,

                    "main":
                        recipe_name,

                    "calories":
                        calories,

                    "protein":
                        protein,

                    "carbs":
                        carbs,

                    "fat":
                        fat,

                    "portions":
                        portions,

                    "sides":
                        [],

                    "description":
                        "A practical "
                        "family-friendly meal.",
                }
            )

        days.append(
            {
                "day":
                    day_number,

                "meals":
                    meals,
            }
        )

    return days


# ============================================================
# AI MEAL PLAN
# ============================================================

def generate_ai_meal_plan(
    cuisines,
    preferences,
):

    if groq_client is None:

        return None

    family_data = [

        {
            "name":
                member["name"],

            "goal":
                member["goal"],

            "target_calories":
                member[
                    "nutrition"
                ]["Target"],

            "protein":
                member[
                    "nutrition"
                ]["Protein"],

            "allergies":
                member["allergies"],
        }

        for member
        in st.session_state.family
    ]

    recipe_pool = []

    if not recipes_df.empty:

        safe = recipes_df[
            recipes_df.apply(
                safe_for_family,
                axis=1,
            )
        ]

        for _, row in safe.head(
            60
        ).iterrows():

            recipe_pool.append(
                {

                    "name":
                        row["recipe_name"],

                    "meal_type":
                        row["meal_type"],

                    "calories":
                        row["calories"],

                    "protein":
                        row["protein_g"],

                    "ingredients":
                        row["ingredients"],
                }
            )

    prompt = f"""
Create a realistic 7-day shared family meal plan.

Family:
{json.dumps(family_data)}

Preferred cuisines:
{json.dumps(cuisines)}

Preferences:
{json.dumps(preferences)}

Pantry:
{json.dumps(st.session_state.pantry)}

Budget:
PKR {st.session_state.budget_amount}
per {st.session_state.budget_period.lower()}

Available recipes:
{json.dumps(recipe_pool)}

Rules:
- Respect all listed allergies.
- Prefer pantry ingredients.
- Use shared dishes where practical.
- Individual portions may differ.
- Include Breakfast, Lunch, Snack and Dinner every day.
- Keep meals realistic for a home kitchen.
- Do not give medical treatment advice.
- Do not claim disease treatment.

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
          "protein": 20,
          "carbs": 40,
          "fat": 15,
          "portions": {{
            "Member": "1 serving"
          }},
          "description": "Short description"
        }}
      ]
    }}
  ]
}}
"""

    try:

        response = (
            groq_client
            .chat
            .completions
            .create(

                model="openai/gpt-oss-120b",

                messages=[

                    {
                        "role":
                            "system",

                        "content":
                            "Return valid JSON only.",
                    },

                    {
                        "role":
                            "user",

                        "content":
                            prompt,
                    },
                ],

                temperature=0.25,

                max_tokens=6000,
            )
        )

        result = extract_json(
            response
            .choices[0]
            .message
            .content
        )

        if (
            isinstance(
                result,
                dict,
            )
            and isinstance(
                result.get(
                    "days"
                ),
                list,
            )
            and len(
                result["days"]
            ) >= 7
        ):

            return result[
                "days"
            ][:7]

    except Exception:

        return None

    return None


# ============================================================
# MEAL PLANNER PAGE
# ============================================================

def meal_page():

    st.markdown(
        """
        <div class="page-header">

            <h1>
                🍽️ Smart Family Meal Planner
            </h1>

            <p>
                Plan shared meals around goals,
                allergies, pantry ingredients,
                cuisine, preferences and budget.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.family:

        st.warning(
            "Add at least one family member first."
        )

        if st.button(
            "Add Family Member →"
        ):

            go(
                "Family Profiles"
            )

        return

    a, b = st.columns(2)

    with a:

        cuisines = st.multiselect(
            "Preferred cuisines",
            [
                "Desi / Pakistani",
                "Indian",
                "Chinese",
                "Italian",
                "Continental",
                "Mixed",
            ],
            default=[
                "Desi / Pakistani"
            ],
        )

    with b:

        preferences = st.multiselect(
            "Preferences",
            [
                "High Protein",
                "High Fiber",
                "Less Oil",
                "Budget Friendly",
                "Quick Meals",
                "Vegetarian",
                "Pantry First",
            ],
            default=[
                "High Protein",
                "Less Oil",
            ],
        )

    if st.session_state.pantry:

        st.success(
            f"🧺 Pantry-aware planning enabled "
            f"with {len(st.session_state.pantry)} "
            "selected ingredients."
        )

    if st.button(
        "✨ Generate 7-Day Family Meal Plan",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner(
            "Creating your family plan..."
        ):

            plan = generate_ai_meal_plan(
                cuisines,
                preferences,
            )

            if plan is None:

                plan = fallback_meal_plan()

                st.info(
                    "AI is unavailable, so "
                    "NutriNest is using its "
                    "built-in meal planning fallback."
                )

            st.session_state.meal_plan = (
                plan
            )

    plan = (
        st.session_state.meal_plan
    )

    if not plan:

        return

    st.success(
        "7-day meal plan ready 🎉"
    )

    for day in plan:

        with st.expander(
            f"Day {day.get('day', '')}",
            expanded=(
                day.get("day")
                == 1
            ),
        ):

            for meal in day.get(
                "meals",
                [],
            ):

                st.markdown(
                    f"""
                    <div class="plate-card">

                        <span class="pill">
                            {meal.get(
                                'meal',
                                'Meal'
                            )}
                        </span>

                        <h3>
                            {meal.get(
                                'main',
                                'Meal'
                            )}
                        </h3>

                        <p>
                            {meal.get(
                                'description',
                                ''
                            )}
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                a, b, c, d = st.columns(4)

                a.metric(
                    "Calories",
                    f"{meal.get('calories', '—')} kcal",
                )

                b.metric(
                    "Protein",
                    f"{meal.get('protein', '—')} g",
                )

                c.metric(
                    "Carbs",
                    f"{meal.get('carbs', '—')} g",
                )

                d.metric(
                    "Fat",
                    f"{meal.get('fat', '—')} g",
                )

                portions = meal.get(
                    "portions",
                    {},
                )

                if portions:

                    columns = st.columns(
                        min(
                            4,
                            len(portions),
                        )
                    )

                    for index, (
                        person,
                        portion,
                    ) in enumerate(
                        portions.items()
                    ):

                        columns[
                            index
                            % len(columns)
                        ].info(
                            f"**{person}**\n\n"
                            f"{portion}"
                        )


# ============================================================
# WORKOUT FALLBACK
# ============================================================

def fallback_workout(
    member
):

    home = (
        member["workout_location"]
        == "Home"
    )

    push_exercise = (
        "Wall / Incline Push-ups"
        if home
        else "Push-ups"
    )

    return {

        "member":
            member["name"],

        "week": [

            {
                "day":
                    1,

                "focus":
                    "Full Body",

                "exercises": [

                    {
                        "name":
                            "Bodyweight Squats",

                        "sets":
                            "3",

                        "reps":
                            "12",
                    },

                    {
                        "name":
                            push_exercise,

                        "sets":
                            "3",

                        "reps":
                            "10",
                    },

                    {
                        "name":
                            "Brisk Walk",

                        "duration":
                            "20 min",
                    },
                ],
            },

            {
                "day":
                    2,

                "focus":
                    "Recovery",

                "exercises": [

                    {
                        "name":
                            "Gentle Stretching",

                        "duration":
                            "15 min",
                    }
                ],
            },

            {
                "day":
                    3,

                "focus":
                    "Lower Body",

                "exercises": [

                    {
                        "name":
                            "Lunges",

                        "sets":
                            "3",

                        "reps":
                            "10 each",
                    },

                    {
                        "name":
                            "Glute Bridges",

                        "sets":
                            "3",

                        "reps":
                            "15",
                    },
                ],
            },

            {
                "day":
                    4,

                "focus":
                    "Rest",

                "exercises":
                    [],
            },

            {
                "day":
                    5,

                "focus":
                    "Upper Body + Core",

                "exercises": [

                    {
                        "name":
                            push_exercise,

                        "sets":
                            "3",

                        "reps":
                            "12",
                    },

                    {
                        "name":
                            "Plank",

                        "duration":
                            "30 sec",
                    },
                ],
            },

            {
                "day":
                    6,

                "focus":
                    "Cardio",

                "exercises": [

                    {
                        "name":
                            "Brisk Walk",

                        "duration":
                            "30 min",
                    }
                ],
            },

            {
                "day":
                    7,

                "focus":
                    "Recovery",

                "exercises": [

                    {
                        "name":
                            "Gentle Stretching",

                        "duration":
                            "15 min",
                    }
                ],
            },
        ],
    }


# ============================================================
# AI WORKOUT
# ============================================================

def generate_ai_workout(
    member
):

    if groq_client is None:

        return None

    prompt = f"""
Create a safe, general 7-day workout plan.

Person:
{member["name"]}

Goal:
{member["goal"]}

Activity:
{member["activity_level"]}

Location:
{member["workout_location"]}

Equipment:
{member["equipment"]}

Include rest/recovery days.

Return ONLY JSON:

{{
  "member": "name",
  "week": [
    {{
      "day": 1,
      "focus": "Full Body",
      "exercises": [
        {{
          "name": "Exercise",
          "sets": "3",
          "reps": "10"
        }},
        {{
          "name": "Walking",
          "duration": "20 min"
        }}
      ]
    }}
  ]
}}

Do not provide medical treatment advice.
"""

    try:

        response = (
            groq_client
            .chat
            .completions
            .create(

                model="openai/gpt-oss-120b",

                messages=[

                    {
                        "role":
                            "system",

                        "content":
                            "Return valid JSON only.",
                    },

                    {
                        "role":
                            "user",

                        "content":
                            prompt,
                    },
                ],

                temperature=0.3,

                max_tokens=3000,
            )
        )

        result = extract_json(
            response
            .choices[0]
            .message
            .content
        )

        if (
            isinstance(
                result,
                dict,
            )
            and isinstance(
                result.get(
                    "week"
                ),
                list,
            )
            and len(
                result["week"]
            ) >= 7
        ):

            return result

    except Exception:

        return None

    return None


# ============================================================
# WORKOUT PAGE
# ============================================================

def workout_page():

    st.markdown(
        """
        <div class="page-header">

            <h1>
                💪 Workout Planner
            </h1>

            <p>
                Personalized 7-day routines based
                on goals, activity, location and equipment.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.family:

        st.warning(
            "Add a family member first."
        )

        return

    names = [
        member["name"]
        for member
        in st.session_state.family
    ]

    selected = st.selectbox(
        "Select Member",
        names,
    )

    member = next(
        member
        for member
        in st.session_state.family
        if member["name"]
        == selected
    )

    st.markdown(
        f"""
        <div class="soft-card">

            <span class="pill">
                {member['goal']}
            </span>

            <span class="pill">
                {member['workout_location']}
            </span>

            <p>
                <b>Equipment:</b>
                {", ".join(member["equipment"])}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "🏃 Generate 7-Day Workout",
        type="primary",
        use_container_width=True,
    ):

        plan = (
            generate_ai_workout(
                member
            )
            or
            fallback_workout(
                member
            )
        )

        st.session_state.workouts[
            selected
        ] = plan

        st.success(
            "Workout plan generated."
        )

    plan = st.session_state.workouts.get(
        selected
    )

    if not plan:

        return

    completed = 0

    for day in plan.get(
        "week",
        [],
    ):

        day_number = day.get(
            "day"
        )

        with st.expander(
            f"Day {day_number} · "
            f"{day.get('focus', 'Workout')}",
            expanded=(
                day_number
                == 1
            ),
        ):

            exercises = day.get(
                "exercises",
                [],
            )

            if not exercises:

                st.write(
                    "🌙 Rest / recovery day"
                )

            for exercise in exercises:

                if exercise.get(
                    "duration"
                ):

                    st.write(
                        f"• **{exercise.get('name', 'Exercise')}** "
                        f"— {exercise['duration']}"
                    )

                else:

                    st.write(
                        f"• **{exercise.get('name', 'Exercise')}** "
                        f"— {exercise.get('sets', '')} "
                        f"× {exercise.get('reps', '')}"
                    )

            completed_today = st.checkbox(
                "Mark day complete",
                key=(
                    f"workout_done_"
                    f"{selected}_"
                    f"{day_number}"
                ),
            )

            if completed_today:

                completed += 1

    st.progress(
        completed / 7,
        text=(
            f"Weekly completion: "
            f"{completed}/7 days"
        ),
    )


# ============================================================
# PROGRESS PAGE
# ============================================================

def progress_page():

    st.markdown(
        """
        <div class="page-header">

            <h1>
                📊 Progress Tracker
            </h1>

            <p>
                Track weight, BMI, calories,
                protein, meals and workout completion.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.family:

        st.warning(
            "Add a family member first."
        )

        return

    names = [
        member["name"]
        for member
        in st.session_state.family
    ]

    selected = st.selectbox(
        "Select Member",
        names,
    )

    member = next(
        member
        for member in st.session_state.family
        if member["name"]
        == selected
    )

    # HEALTH LOG

    left, right = st.columns(2)

    with left:

        st.markdown(
            "### ⚖️ Daily health log"
        )

        with st.form(
            "health_log"
        ):

            weight = st.number_input(
                "Weight (kg)",
                min_value=25.0,
                max_value=250.0,
                value=float(
                    member["weight_kg"]
                ),
                step=0.1,
            )

            calories = st.number_input(
                "Calories consumed",
                min_value=0,
                max_value=10000,
                value=0,
                step=50,
            )

            protein = st.number_input(
                "Protein consumed (g)",
                min_value=0,
                max_value=500,
                value=0,
                step=5,
            )

            save_health = (
                st.form_submit_button(
                    "Save health log",
                    use_container_width=True,
                )
            )

        if save_health:

            bmi = (
                weight
                /
                (
                    (
                        member[
                            "height_cm"
                        ]
                        / 100
                    )
                    ** 2
                )
            )

            st.session_state.logs.append(
                {

                    "date":
                        str(
                            date.today()
                        ),

                    "member":
                        selected,

                    "type":
                        "health",

                    "weight":
                        weight,

                    "bmi":
                        round(
                            bmi,
                            1,
                        ),

                    "calories":
                        calories,

                    "protein":
                        protein,

                    "status":
                        "logged",

                    "minutes":
                        0,
                }
            )

            st.success(
                "Health progress saved."
            )

    # WORKOUT LOG

    with right:

        st.markdown(
            "### 🏃 Workout log"
        )

        with st.form(
            "workout_log"
        ):

            status = st.selectbox(
                "Status",
                [
                    "completed",
                    "skipped",
                    "rest",
                ],
            )

            minutes = st.number_input(
                "Minutes",
                min_value=0,
                max_value=300,
                value=30,
                step=5,
            )

            save_workout = (
                st.form_submit_button(
                    "Save workout",
                    use_container_width=True,
                )
            )

        if save_workout:

            st.session_state.logs.append(
                {

                    "date":
                        str(
                            date.today()
                        ),

                    "member":
                        selected,

                    "type":
                        "workout",

                    "status":
                        status,

                    "minutes":
                        (
                            int(minutes)
                            if status
                            == "completed"
                            else 0
                        ),

                    "weight":
                        None,

                    "bmi":
                        None,

                    "calories":
                        None,

                    "protein":
                        None,
                }
            )

            st.success(
                "Workout saved."
            )

    # MEAL LOG

    st.markdown(
        "### 🍽 Meal log"
    )

    with st.form(
        "meal_log"
    ):

        meal_name = st.text_input(
            "Meal name",
            "Breakfast",
        )

        meal_status = st.selectbox(
            "Meal status",
            [
                "followed",
                "different",
                "skipped",
            ],
        )

        save_meal = (
            st.form_submit_button(
                "Log meal",
                use_container_width=True,
            )
        )

    if save_meal:

        st.session_state.logs.append(
            {

                "date":
                    str(
                        date.today()
                    ),

                "member":
                    selected,

                "type":
                    "meal",

                "item":
                    meal_name,

                "status":
                    meal_status,

                "minutes":
                    0,

                "weight":
                    None,

                "bmi":
                    None,

                "calories":
                    None,

                "protein":
                    None,
            }
        )

        st.success(
            "Meal logged."
        )

    # FILTER LOGS

    rows = [

        row

        for row
        in st.session_state.logs

        if row.get(
            "member"
        )
        == selected
    ]

    if not rows:

        st.info(
            "Add progress entries "
            "to unlock graphs."
        )

        return

    df = pd.DataFrame(
        rows
    )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df = df.sort_values(
        "date"
    )

    health = df[
        df["type"]
        == "health"
    ]

    workouts = df[
        df["type"]
        == "workout"
    ]

    meals = df[
        df["type"]
        == "meal"
    ]

    # HEALTH GRAPHS

    if not health.empty:

        latest = health.iloc[
            -1
        ]

        first_weight = float(
            health.iloc[
                0
            ]["weight"]
        )

        weight_change = (
            float(
                latest["weight"]
            )
            - first_weight
        )

        a, b, c, d = st.columns(4)

        a.metric(
            "Current Weight",
            f"{latest['weight']:.1f} kg",
        )

        b.metric(
            "BMI",
            f"{latest['bmi']:.1f}",
        )

        c.metric(
            "Weight Change",
            f"{weight_change:+.1f} kg",
        )

        d.metric(
            "Calories",
            f"{latest['calories']:,.0f}",
        )

        a, b = st.columns(2)

        with a:

            figure = px.line(
                health,
                x="date",
                y="weight",
                markers=True,
                title="Weight Trend",
            )

            st.plotly_chart(
                figure,
                use_container_width=True,
            )

        with b:

            figure = px.line(
                health,
                x="date",
                y="bmi",
                markers=True,
                title="BMI Trend",
            )

            st.plotly_chart(
                figure,
                use_container_width=True,
            )

        a, b = st.columns(2)

        with a:

            figure = px.bar(
                health,
                x="date",
                y="calories",
                title="Calories vs Target",
            )

            figure.add_hline(
                y=member[
                    "nutrition"
                ]["Target"],
                line_dash="dash",
                annotation_text="Target",
            )

            st.plotly_chart(
                figure,
                use_container_width=True,
            )

        with b:

            figure = px.line(
                health,
                x="date",
                y="protein",
                markers=True,
                title="Protein vs Target",
            )

            figure.add_hline(
                y=member[
                    "nutrition"
                ]["Protein"],
                line_dash="dash",
                annotation_text="Target",
            )

            st.plotly_chart(
                figure,
                use_container_width=True,
            )

    # WORKOUT GRAPH

    if not workouts.empty:

        grouped = (
            workouts
            .groupby(
                "date",
                as_index=False,
            )["minutes"]
            .sum()
        )

        figure = px.bar(
            grouped,
            x="date",
            y="minutes",
            title="Workout Minutes",
        )

        st.plotly_chart(
            figure,
            use_container_width=True,
        )

    # MEAL ADHERENCE

    if not meals.empty:

        followed = int(
            (
                meals["status"]
                == "followed"
            ).sum()
        )

        total_meals = len(
            meals
        )

        adherence = (
            100
            * followed
            / max(
                1,
                total_meals,
            )
        )

        st.metric(
            "Meal Adherence",
            f"{adherence:.0f}%",
            f"{followed}/{total_meals} followed",
        )

    # WEEKLY / MONTHLY

    st.markdown(
        "### 📅 Weekly / monthly summary"
    )

    today = pd.Timestamp(
        date.today()
    )

    weekly = df[
        df["date"]
        >=
        today
        - pd.Timedelta(
            days=6
        )
    ]

    monthly = df[
        df["date"]
        >=
        today
        - pd.Timedelta(
            days=29
        )
    ]

    a, b = st.columns(2)

    a.metric(
        "Last 7 Days Logs",
        len(weekly),
    )

    b.metric(
        "Last 30 Days Logs",
        len(monthly),
    )

    # TABLE

    st.markdown(
        "### 📋 Progress history"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download Progress CSV",
        df.to_csv(
            index=False
        ).encode(
            "utf-8"
        ),
        "nutrinest_progress.csv",
        "text/csv",
    )

    if st.button(
        "Clear all progress logs for this member"
    ):

        st.session_state.logs = [

            row

            for row
            in st.session_state.logs

            if row.get(
                "member"
            )
            != selected
        ]

        st.rerun()


# ============================================================
# FAVORITES
# ============================================================

def favorites_page():

    st.markdown(
        """
        <div class="page-header">

            <h1>
                ❤️ Favorites
            </h1>

            <p>
                Your saved recipes in one place.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.favorites:

        st.info(
            "No favorites yet. "
            "Save recipes from Recipe Explorer."
        )

        return

    if recipes_df.empty:

        return

    for index, name in enumerate(
        st.session_state.favorites
    ):

        matches = recipes_df[
            recipes_df[
                "recipe_name"
            ]
            .astype(str)
            .str.casefold()
            == name.casefold()
        ]

        if matches.empty:

            continue

        row = matches.iloc[
            0
        ]

        with st.expander(
            f"❤️ {name}"
        ):

            a, b, c, d = st.columns(4)

            a.metric(
                "Calories",
                f"{row['calories']:.0f}",
            )

            b.metric(
                "Protein",
                f"{row['protein_g']:.0f}g",
            )

            c.metric(
                "Carbs",
                f"{row['carbs_g']:.0f}g",
            )

            d.metric(
                "Fat",
                f"{row['fat_g']:.0f}g",
            )

            ingredients = parse_listish(
                row["ingredients"]
            )

            st.write(
                "**Ingredients:** "
                + ", ".join(
                    ingredients
                )
            )

            if st.button(
                "Remove Favorite",
                key=f"favorite_remove_{index}",
            ):

                st.session_state.favorites.remove(
                    name
                )

                st.rerun()


# ============================================================
# SIDEBAR
# Sidebar is only a utility area.
# Main feature navigation happens through dashboard cards.
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🥗 NutriNest"
    )

    st.caption(
        "Family Nutrition & Wellness"
    )

    st.divider()

    if st.button(
        "🏠 Dashboard",
        use_container_width=True,
    ):

        go(
            "Dashboard"
        )

    st.divider()

    st.caption(
        "System Status"
    )

    st.write(
        "AI: "
        + (
            "Connected"
            if groq_client
            else
            "Fallback mode"
        )
    )

    st.write(
        "Recipes: "
        + (
            "Connected"
            if not recipes_df.empty
            else
            "Not found"
        )
    )

    if recipe_source:

        st.caption(
            f"Dataset: {recipe_source}"
        )

    st.divider()

    st.caption(
        "Use Streamlit Secrets for "
        "GROQ_API_KEY."
    )

    st.caption(
        "Never upload .streamlit/secrets.toml "
        "to GitHub."
    )


# ============================================================
# MAIN ROUTER
# ============================================================

current_page = (
    st.session_state.page
)

if current_page == "Dashboard":

    dashboard()

elif current_page == "Family Profiles":

    family_page()

elif current_page == "Smart Pantry":

    pantry_page()

elif current_page == "Recipe Explorer":

    recipes_page()

elif current_page == "Budget & Shopping":

    budget_page()

elif current_page == "Meal Planner":

    meal_page()

elif current_page == "Workout Planner":

    workout_page()

elif current_page == "Progress":

    progress_page()

elif current_page == "Favorites":

    favorites_page()

else:

    st.session_state.page = (
        "Dashboard"
    )

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-note">

        🥗 <b>NutriNest</b>
        · Smart Family Nutrition & Wellness

        <br>

        Eat well · Move well · Live well 💚

        <br><br>

        NutriNest provides general wellness
        planning and is not a substitute for
        medical diagnosis or clinical treatment.

    </div>
    """,
    unsafe_allow_html=True,
)
