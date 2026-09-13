import ast
import json
import os
import random
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
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NutriNest",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 5% 0%,
            rgba(225, 239, 226, 0.9),
            transparent 28rem
        ),
        radial-gradient(
            circle at 95% 0%,
            rgba(250, 231, 218, 0.8),
            transparent 30rem
        ),
        #FBF8F3;
    color: #25302B;
}

.block-container {
    max-width: 1350px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4, h5, h6 {
    color: #25302B !important;
}

p, label, span {
    color: #35433C;
}

.hero {
    padding: 2.3rem;
    border-radius: 30px;
    background:
        linear-gradient(
            120deg,
            #E7F0E7,
            #FBE9DD,
            #EEEAF7
        );
    border: 1px solid #DDE5DC;
    box-shadow: 0 15px 40px rgba(45, 65, 53, 0.08);
    margin-bottom: 1.3rem;
}

.hero-badge {
    display: inline-block;
    padding: 0.4rem 0.85rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.8);
    color: #486454 !important;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 900;
    line-height: 1.05;
    margin-top: 0.7rem;
    letter-spacing: -0.04em;
}

.hero-subtitle {
    max-width: 850px;
    color: #5F6D65 !important;
    font-size: 1.05rem;
    line-height: 1.65;
}

.quote-card {
    margin: 1rem 0 1.5rem;
    padding: 1.35rem 1.6rem;
    border-radius: 22px;
    background: linear-gradient(
        135deg,
        #FFFDF7,
        #EEF7F0
    );
    border: 1px solid #DFE6DE;
    box-shadow: 0 8px 25px rgba(40, 60, 48, 0.06);
}

.quote {
    font-size: 1.22rem;
    font-weight: 800;
    color: #385044 !important;
}

.quote-category {
    color: #748078 !important;
    font-size: 0.83rem;
    margin-top: 0.4rem;
}

.slideshow {
    height: 205px;
    position: relative;
    overflow: hidden;
    border-radius: 26px;
    margin-bottom: 1.5rem;
}

.slide {
    position: absolute;
    inset: 0;
    padding: 2rem;
    opacity: 0;
    animation: fadeSlide 20s infinite;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.slide:nth-child(1) {
    background: linear-gradient(120deg, #E6F0E7, #F4F8F3);
}

.slide:nth-child(2) {
    background: linear-gradient(120deg, #FBE8DC, #FFF5ED);
    animation-delay: 5s;
}

.slide:nth-child(3) {
    background: linear-gradient(120deg, #EEEAF7, #F8F6FC);
    animation-delay: 10s;
}

.slide:nth-child(4) {
    background: linear-gradient(120deg, #FFF1C9, #FFF9E8);
    animation-delay: 15s;
}

.slide h2 {
    font-size: 1.8rem;
    margin: 0 0 0.35rem;
    font-weight: 900;
}

.slide p {
    max-width: 720px;
    color: #65736B !important;
}

@keyframes fadeSlide {
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

.section-title {
    font-size: 1.45rem;
    font-weight: 900;
    margin: 1.5rem 0 0.9rem;
}

.feature-card {
    min-height: 180px;
    padding: 1.25rem;
    border-radius: 22px;
    background: rgba(255,255,255,0.92);
    border: 1px solid #E3DED5;
    box-shadow: 0 8px 26px rgba(45,60,50,0.06);
    margin-bottom: 0.8rem;
}

.feature-icon {
    font-size: 2.2rem;
}

.feature-title {
    font-size: 1.08rem;
    font-weight: 900;
    margin-top: 0.45rem;
}

.feature-description {
    color: #6C7771 !important;
    font-size: 0.86rem;
    line-height: 1.45;
    margin-top: 0.25rem;
}

.page-header {
    padding: 1.35rem 1.5rem;
    border-radius: 22px;
    background: linear-gradient(
        120deg,
        #EAF2E9,
        #FFF9F2
    );
    border: 1px solid #E1DED6;
    margin-bottom: 1.3rem;
}

.page-header h1 {
    margin: 0;
    font-size: 2rem;
    font-weight: 900;
}

.page-header p {
    margin: 0.4rem 0 0;
    color: #6C7771 !important;
}

.soft-card {
    padding: 1.15rem;
    border-radius: 20px;
    background: rgba(255,255,255,0.92);
    border: 1px solid #E3DED5;
    box-shadow: 0 7px 22px rgba(45,60,50,0.05);
    margin-bottom: 0.9rem;
}

.recipe-card {
    padding: 1.15rem;
    border-radius: 20px;
    background: linear-gradient(
        145deg,
        #FFFFFF,
        #FFF9EF
    );
    border: 1px solid #E5DED1;
    margin-bottom: 0.8rem;
}

.pill {
    display: inline-block;
    padding: 0.28rem 0.65rem;
    margin: 0.15rem;
    border-radius: 999px;
    background: #F1EEE6;
    color: #655D4D !important;
    font-size: 0.75rem;
    font-weight: 750;
}

.macro {
    display: inline-block;
    padding: 0.3rem 0.65rem;
    margin: 0.15rem;
    border-radius: 999px;
    background: #EDF5EF;
    color: #476151 !important;
    font-size: 0.76rem;
    font-weight: 750;
}

.member-card {
    padding: 1.2rem;
    border-radius: 21px;
    background: linear-gradient(
        145deg,
        #FFFFFF,
        #F0F7F0
    );
    border: 1px solid #DDE7DD;
    box-shadow: 0 8px 24px rgba(45,60,50,0.05);
    margin-bottom: 1rem;
}

.big-number {
    font-size: 1.8rem;
    font-weight: 900;
    color: #466853 !important;
}

.stat-card {
    text-align: center;
    padding: 1rem;
    border-radius: 18px;
    background: #FFFFFF;
    border: 1px solid #E1DED6;
}

[data-testid="stMetric"] {
    border-radius: 18px;
    background: rgba(255,255,255,0.9);
    border: 1px solid #E2DED5;
    padding: 0.8rem;
}

[data-testid="stMetricValue"] {
    color: #41614D !important;
    font-weight: 900;
}

.stButton > button {
    border-radius: 13px;
    min-height: 2.6rem;
    font-weight: 800;
    background: #587864;
    border: 1px solid #587864;
    color: white !important;
}

.stButton > button:hover {
    background: #395847;
    border-color: #395847;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border-radius: 12px !important;
    background: white !important;
    color: #25302B !important;
}

div[data-baseweb="select"] > div {
    border-radius: 12px !important;
}

hr {
    border-color: #E2DED5;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# RECIPE DATASET
# =========================================================

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

    if path is None:
        return pd.DataFrame(), None

    try:
        df = pd.read_csv(path)
    except Exception:
        return pd.DataFrame(), path

    df.columns = [
        str(column).strip().lower()
        for column in df.columns
    ]

    rename = {
        "name": "recipe_name",
        "recipe name": "recipe_name",
        "dish name": "recipe_name",
        "calories_per_serving": "calories",
        "calories per serving": "calories",
        "protein(g)": "protein_g",
        "protein": "protein_g",
        "carbs(g)": "carbs_g",
        "carbohydrates": "carbs_g",
        "fat(g)": "fat_g",
        "fat": "fat_g",
        "cuisine type": "cuisine",
        "cuisine_type": "cuisine",
        "meal type": "meal_type",
    }

    for old, new in rename.items():
        if old in df.columns:
            df = df.rename(columns={old: new})

    defaults = {
        "recipe_name": "Recipe",
        "meal_type": "Main",
        "cuisine": "Mixed",
        "ingredients": "",
        "steps": "",
        "allergens": "",
        "tags": "",
        "calories": 0,
        "protein_g": 0,
        "carbs_g": 0,
        "fat_g": 0,
    }

    for column, default in defaults.items():
        if column not in df.columns:
            df[column] = default

    for column in [
        "calories",
        "protein_g",
        "carbs_g",
        "fat_g",
    ]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)

    return df, path


recipes, dataset_path = load_recipes()


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "family" not in st.session_state:
    st.session_state.family = []

if "pantry" not in st.session_state:
    st.session_state.pantry = []

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "shopping_list" not in st.session_state:
    st.session_state.shopping_list = []

if "progress_logs" not in st.session_state:
    st.session_state.progress_logs = []

if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = None

if "workout_plan" not in st.session_state:
    st.session_state.workout_plan = {}

if "budget_period" not in st.session_state:
    st.session_state.budget_period = "Monthly"

if "budget_amount" not in st.session_state:
    st.session_state.budget_amount = 30000


# =========================================================
# NAVIGATION
# =========================================================

def navigate(page_name):
    st.session_state.page = page_name
    st.rerun()


def back_button():

    if st.session_state.page != "Dashboard":

        if st.button(
            "← Back to Dashboard",
            key="back_to_dashboard"
        ):
            navigate("Dashboard")


# =========================================================
# NUTRITION CALCULATOR
# =========================================================

def calculate_nutrition(
    age,
    sex,
    height_cm,
    weight_kg,
    activity,
    goal
):

    if sex == "Male":

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

    activity_factor = {
        "Sedentary": 1.20,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.90,
    }

    tdee = (
        bmr
        * activity_factor.get(
            activity,
            1.55
        )
    )

    if goal == "Weight Loss":
        calories = tdee - 400

    elif goal == "Weight Gain":
        calories = tdee + 300

    else:
        calories = tdee

    calories = max(
        calories,
        1200
    )

    bmi = weight_kg / (
        (height_cm / 100) ** 2
    )

    protein = calories * 0.25 / 4
    carbs = calories * 0.50 / 4
    fat = calories * 0.25 / 9

    return {
        "BMI": round(bmi, 1),
        "BMR": round(bmr),
        "TDEE": round(tdee),
        "Calories": round(calories),
        "Protein": round(protein),
        "Carbs": round(carbs),
        "Fat": round(fat),
        "Fiber": 30,
    }


# =========================================================
# ALLERGY FILTER
# =========================================================

ALLERGY_WORDS = {
    "Nuts": [
        "nut",
        "almond",
        "peanut",
        "cashew",
        "walnut",
        "pistachio",
    ],
    "Dairy": [
        "milk",
        "cheese",
        "yogurt",
        "cream",
        "butter",
        "paneer",
    ],
    "Gluten": [
        "wheat",
        "flour",
        "bread",
        "roti",
        "chapati",
        "pasta",
        "barley",
    ],
    "Egg": [
        "egg",
        "eggs",
    ],
    "Seafood": [
        "fish",
        "prawn",
        "shrimp",
        "seafood",
        "tuna",
        "salmon",
    ],
}


def family_allergies():

    allergies = []

    for member in st.session_state.family:

        for allergy in member.get(
            "allergies",
            []
        ):

            if allergy != "None":
                allergies.append(
                    allergy
                )

    return list(
        set(allergies)
    )


def allergy_safe(row):

    allergies = family_allergies()

    if not allergies:
        return True

    text = (
        str(row.get("recipe_name", ""))
        + " "
        + str(row.get("ingredients", ""))
        + " "
        + str(row.get("allergens", ""))
    ).lower()

    for allergy in allergies:

        words = ALLERGY_WORDS.get(
            allergy,
            [allergy.lower()]
        )

        for word in words:

            if word in text:
                return False

    return True


# =========================================================
# LIST PARSER
# =========================================================

def parse_list(value):

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


def normalize(text):

    return re.sub(
        r"[^a-z0-9 ]",
        " ",
        str(text).lower()
    ).strip()


# =========================================================
# PANTRY MATCH
# =========================================================

def pantry_match(row):

    ingredients = parse_list(
        row.get("ingredients", "")
    )

    if not ingredients:
        return 0, [], []

    pantry = [
        normalize(item)
        for item in st.session_state.pantry
    ]

    matched = []
    missing = []

    for ingredient in ingredients:

        ingredient_normalized = normalize(
            ingredient
        )

        found = False

        for pantry_item in pantry:

            if (
                pantry_item in ingredient_normalized
                or ingredient_normalized in pantry_item
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
        (
            len(matched)
            / max(len(ingredients), 1)
        ) * 100
    )

    return (
        percentage,
        matched,
        missing
    )


# =========================================================
# GROQ
# =========================================================

def get_groq_client():

    if Groq is None:
        return None

    try:

        api_key = st.secrets.get(
            "GROQ_API_KEY"
        )

    except Exception:

        api_key = os.environ.get(
            "GROQ_API_KEY"
        )

    if not api_key:
        api_key = os.environ.get(
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

    text = str(text).strip()

    if "```" in text:

        parts = text.split("```")

        text = max(
            parts,
            key=len
        )

        text = re.sub(
            r"^json",
            "",
            text.strip(),
            flags=re.IGNORECASE
        )

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    try:

        return json.loads(
            text[start:end + 1]
        )

    except Exception:

        return None


# =========================================================
# QUOTES
# =========================================================

QUOTES = [
    (
        "Small healthy choices today create a stronger tomorrow.",
        "Healthy Living 🌱"
    ),
    (
        "Consistency is more powerful than perfection.",
        "Motivation 💚"
    ),
    (
        "Eat well, move often, rest deeply.",
        "Wellness 🌿"
    ),
    (
        "Your health is one of your greatest investments.",
        "Health ❤️"
    ),
    (
        "Every workout is a vote for the person you want to become.",
        "Fitness 💪"
    ),
    (
        "A healthy family grows through healthy habits together.",
        "Family Wellness 👨‍👩‍👧‍👦"
    ),
    (
        "Nourish your body with food that helps you thrive.",
        "Nutrition 🥗"
    ),
    (
        "You do not need to be perfect. Keep moving forward.",
        "Mindset ✨"
    ),
    (
        "Progress may be slow, but it is still progress.",
        "Motivation 🔥"
    ),
    (
        "Healthy habits become easier when the whole family joins in.",
        "Family Health 🏡"
    ),
]


def show_quote():

    text, category = random.choice(
        QUOTES
    )

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
        unsafe_allow_html=True
    )


# =========================================================
# PANTRY ITEMS
# =========================================================

PANTRY = {
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


# =========================================================
# DASHBOARD
# =========================================================

def dashboard():

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
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="slideshow">

            <div class="slide">
                <h2>🥗 Personalized Nutrition</h2>
                <p>
                    Understand calories, protein, carbohydrates,
                    fats and personal nutrition targets.
                </p>
            </div>

            <div class="slide">
                <h2>🍛 Smart Family Meal Planning</h2>
                <p>
                    Create practical meals for the whole family
                    while keeping individual portions in mind.
                </p>
            </div>

            <div class="slide">
                <h2>🧺 Cook From Your Pantry</h2>
                <p>
                    Select what you already have and discover
                    recipes you can make right now.
                </p>
            </div>

            <div class="slide">
                <h2>💪 Fitness & Progress</h2>
                <p>
                    Build weekly workouts and visualize your
                    health journey through meaningful graphs.
                </p>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    show_quote()

    total_calories = sum(
        member["nutrition"]["Calories"]
        for member in st.session_state.family
    )

    budget = st.session_state.budget_amount

    if st.session_state.budget_period == "Weekly":
        daily_budget = budget / 7

    elif st.session_state.budget_period == "Monthly":
        daily_budget = budget / 30

    else:
        daily_budget = budget

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

    st.markdown(
        '<div class="section-title">Your NutriNest modules 💚</div>',
        unsafe_allow_html=True
    )

    modules = [
        (
            "👨‍👩‍👧‍👦",
            "Family Profiles",
            "Manage members, goals and personalized nutrition.",
            "Family Profiles",
        ),
        (
            "🍽️",
            "Meal Planner",
            "Build a smart 7-day family meal plan.",
            "Meal Planner",
        ),
        (
            "🧺",
            "Smart Pantry",
            "Choose ingredients and find meals you can cook.",
            "Smart Pantry",
        ),
        (
            "🍛",
            "Recipe Explorer",
            "Search recipes by cuisine, nutrition and pantry match.",
            "Recipe Explorer",
        ),
        (
            "💰",
            "Budget & Shopping",
            "Manage household budgets and shopping lists.",
            "Budget & Shopping",
        ),
        (
            "💪",
            "Workout Planner",
            "Create personalized weekly workouts.",
            "Workout Planner",
        ),
        (
            "📊",
            "Progress Tracker",
            "Track weight, calories, protein and workouts.",
            "Progress",
        ),
        (
            "❤️",
            "Favorites",
            "Keep your favorite recipes together.",
            "Favorites",
        ),
    ]

    for start in range(
        0,
        len(modules),
        4
    ):

        row = modules[
            start:start + 4
        ]

        columns = st.columns(4)

        for column, module in zip(
            columns,
            row
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
                    unsafe_allow_html=True
                )

                if st.button(
                    f"Open {title} →",
                    key=f"dashboard_{title}",
                    use_container_width=True
                ):
                    navigate(page)

    # -----------------------------------------------------
    # FAMILY DASHBOARD GRAPH
    # -----------------------------------------------------

    if st.session_state.family:

        st.markdown(
            '<div class="section-title">Family nutrition overview 📊</div>',
            unsafe_allow_html=True
        )

        rows = []

        for member in st.session_state.family:

            nutrition = member["nutrition"]

            rows.append(
                {
                    "Member": member["name"],
                    "Calories": nutrition["Calories"],
                    "Protein": nutrition["Protein"],
                    "Carbs": nutrition["Carbs"],
                    "Fat": nutrition["Fat"],
                }
            )

        nutrition_df = pd.DataFrame(
            rows
        )

        c1, c2 = st.columns(2)

        with c1:

            figure = px.bar(
                nutrition_df,
                x="Member",
                y=[
                    "Protein",
                    "Carbs",
                    "Fat"
                ],
                barmode="group",
                title="Daily Macronutrient Targets"
            )

            figure.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )

        with c2:

            figure = px.bar(
                nutrition_df,
                x="Member",
                y="Calories",
                title="Daily Calorie Targets"
            )

            figure.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )


# =========================================================
# FAMILY PROFILES
# =========================================================

def family_profiles():

    back_button()

    st.markdown(
        """
        <div class="page-header">

            <h1>👨‍👩‍👧‍👦 Family Profiles</h1>

            <p>
                Add your family members to personalize nutrition,
                meals, portions and fitness.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form(
        "family_form",
        clear_on_submit=True
    ):

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
                [
                    "Male",
                    "Female"
                ]
            )

            height = st.number_input(
                "Height (cm)",
                min_value=120,
                max_value=230,
                value=170
            )

            weight = st.number_input(
                "Weight (kg)",
                min_value=25.0,
                max_value=250.0,
                value=70.0,
                step=0.5
            )

        with c2:

            goal = st.selectbox(
                "Goal",
                [
                    "Weight Loss",
                    "Maintenance",
                    "Weight Gain",
                ]
            )

            activity = st.selectbox(
                "Activity Level",
                [
                    "Sedentary",
                    "Light",
                    "Moderate",
                    "Active",
                    "Very Active",
                ]
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
                default=["None"]
            )

            medical = st.multiselect(
                "Health Considerations",
                [
                    "None",
                    "Diabetes",
                    "Hypertension",
                    "Thyroid",
                    "PCOS",
                ],
                default=["None"]
            )

            workout_location = st.selectbox(
                "Workout Location",
                [
                    "Home",
                    "Gym"
                ]
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
                default=["Yoga Mat"]
            )

        submit = st.form_submit_button(
            "Save Family Member",
            use_container_width=True
        )

    if submit:

        member_name = name.strip()

        if not member_name:

            st.error(
                "Please enter a name."
            )

        else:

            nutrition = calculate_nutrition(
                age,
                sex,
                height,
                weight,
                activity,
                goal
            )

            member = {
                "name": member_name,
                "age": int(age),
                "sex": sex,
                "height": float(height),
                "weight": float(weight),
                "goal": goal,
                "activity": activity,
                "allergies": allergies,
                "medical": medical,
                "workout_location": workout_location,
                "equipment": equipment,
                "nutrition": nutrition,
            }

            st.session_state.family = [
                old_member
                for old_member in st.session_state.family
                if old_member["name"].lower()
                != member_name.lower()
            ]

            st.session_state.family.append(
                member
            )

            st.success(
                f"{member_name} has been saved successfully."
            )

            st.rerun()

    if st.session_state.family:

        st.markdown(
            '<div class="section-title">Family Overview</div>',
            unsafe_allow_html=True
        )

        columns = st.columns(
            min(
                3,
                len(st.session_state.family)
            )
        )

        for index, member in enumerate(
            st.session_state.family
        ):

            nutrition = member["nutrition"]

            with columns[
                index % len(columns)
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
                            BMI: {nutrition['BMI']}
                        </p>

                        <div class="big-number">
                            {nutrition['Calories']}
                            <span style="font-size:.8rem;">
                                kcal/day
                            </span>
                        </div>

                        <span class="macro">
                            Protein {nutrition['Protein']}g
                        </span>

                        <span class="macro">
                            Carbs {nutrition['Carbs']}g
                        </span>

                        <span class="macro">
                            Fat {nutrition['Fat']}g
                        </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    f"Remove {member['name']}",
                    key=f"remove_{index}",
                    use_container_width=True
                ):

                    st.session_state.family.pop(
                        index
                    )

                    st.rerun()


# =========================================================
# SMART PANTRY
# =========================================================

def smart_pantry():

    back_button()

    st.markdown(
        """
        <div class="page-header">

            <h1>🧺 Smart Pantry</h1>

            <p>
                Select ingredients you already have.
                NutriNest will show recipes you can make now.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    selected = []

    for category, items in PANTRY.items():

        with st.expander(
            category,
            expanded=True
        ):

            columns = st.columns(4)

            for index, item in enumerate(items):

                with columns[
                    index % 4
                ]:

                    checked = st.checkbox(
                        item,
                        value=(
                            item
                            in st.session_state.pantry
                        ),
                        key=f"pantry_{category}_{item}"
                    )

                    if checked:
                        selected.append(
                            item
                        )

    st.session_state.pantry = selected

    st.markdown(
        '<div class="section-title">Current Pantry</div>',
        unsafe_allow_html=True
    )

    if selected:

        st.success(
            " · ".join(
                selected
            )
        )

    else:

        st.info(
            "Select some ingredients above."
        )

    if (
        selected
        and not recipes.empty
    ):

        st.markdown(
            '<div class="section-title">✨ What Can I Cook Now?</div>',
            unsafe_allow_html=True
        )

        safe_recipes = recipes[
            recipes.apply(
                allergy_safe,
                axis=1
            )
        ]

        results = []

        for _, row in safe_recipes.iterrows():

            match, matched, missing = pantry_match(
                row
            )

            results.append(
                {
                    "row": row,
                    "match": match,
                    "matched": matched,
                    "missing": missing,
                }
            )

        results.sort(
            key=lambda item: item["match"],
            reverse=True
        )

        for index, result in enumerate(
            results[:15]
        ):

            row = result["row"]

            name = row["recipe_name"]

            st.markdown(
                f"""
                <div class="recipe-card">

                    <h3>
                        🍛 {name}
                    </h3>

                    <span class="pill">
                        🟢 {result['match']}% Pantry Match
                    </span>

                    <span class="pill">
                        🔥 {row['calories']:.0f} kcal
                    </span>

                    <span class="pill">
                        💪 {row['protein_g']:.0f}g Protein
                    </span>

                </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2 = st.columns(2)

            with c1:

                st.markdown(
                    "**Already available:**"
                )

                if result["matched"]:

                    st.write(
                        ", ".join(
                            result["matched"][:10]
                        )
                    )

                else:

                    st.caption(
                        "No direct matches."
                    )

            with c2:

                st.markdown(
                    "**Missing:**"
                )

                if result["missing"]:

                    st.write(
                        ", ".join(
                            result["missing"][:10]
                        )
                    )

                    if st.button(
                        "🛒 Add Missing Items",
                        key=f"pantry_shop_{index}"
                    ):

                        for item in result["missing"]:

                            if item not in st.session_state.shopping_list:

                                st.session_state.shopping_list.append(
                                    item
                                )

                        st.success(
                            "Items added to shopping list."
                        )

                else:

                    st.success(
                        "You have everything needed! 🎉"
                    )


# =========================================================
# RECIPE EXPLORER
# =========================================================

def recipe_explorer():

    back_button()

    st.markdown(
        """
        <div class="page-header">

            <h1>🍛 Recipe Explorer</h1>

            <p>
                Search recipes by name, meal type, cuisine,
                calories, protein and pantry availability.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if recipes.empty:

        st.error(
            "Recipe dataset was not found."
        )

        st.code(
            "data/nutrinest_recipes_clean.csv"
        )

        return

    c1, c2, c3 = st.columns(3)

    with c1:

        search = st.text_input(
            "🔎 Search Recipe",
            placeholder="Chicken, rice, pasta..."
        )

    with c2:

        meal_type = st.selectbox(
            "Meal Type",
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

        cuisine = st.selectbox(
            "Cuisine",
            [
                "All"
            ]
            + sorted(
                recipes["cuisine"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

    c1, c2, c3 = st.columns(3)

    with c1:

        max_calories = st.slider(
            "Maximum Calories",
            100,
            1500,
            800
        )

    with c2:

        min_protein = st.slider(
            "Minimum Protein",
            0,
            100,
            0
        )

    with c3:

        pantry_priority = st.checkbox(
            "Prioritize Pantry Matches"
        )

    data = recipes[
        recipes.apply(
            allergy_safe,
            axis=1
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
                na=False
            )
        ]

    if meal_type != "All":

        data = data[
            data["meal_type"]
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
            .astype(str)
            .str.lower()
            == cuisine.lower()
        ]

    data = data[
        data["calories"]
        <= max_calories
    ]

    data = data[
        data["protein_g"]
        >= min_protein
    ]

    if (
        pantry_priority
        and st.session_state.pantry
    ):

        data["_pantry_match"] = data.apply(
            lambda row: pantry_match(row)[0],
            axis=1
        )

        data = data.sort_values(
            "_pantry_match",
            ascending=False
        )

    st.caption(
        f"{len(data)} recipes found."
    )

    for index, (_, row) in enumerate(
        data.head(50).iterrows()
    ):

        recipe_name = row["recipe_name"]

        favorite = (
            recipe_name
            in st.session_state.favorites
        )

        with st.expander(
            f"{'❤️' if favorite else '🍽️'} {recipe_name}"
        ):

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Calories",
                f"{row['calories']:.0f}"
            )

            c2.metric(
                "Protein",
                f"{row['protein_g']:.0f}g"
            )

            c3.metric(
                "Carbs",
                f"{row['carbs_g']:.0f}g"
            )

            c4.metric(
                "Fat",
                f"{row['fat_g']:.0f}g"
            )

            st.write(
                f"**Cuisine:** {row['cuisine']}"
            )

            st.write(
                f"**Meal:** {row['meal_type']}"
            )

            ingredients = parse_list(
                row["ingredients"]
            )

            if ingredients:

                st.markdown(
                    "**Ingredients**"
                )

                st.write(
                    " · ".join(
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

                st.markdown(
                    "**Preparation**"
                )

                st.write(
                    steps
                )

            if st.session_state.pantry:

                match, matched, missing = pantry_match(
                    row
                )

                st.progress(
                    match / 100,
                    text=f"Pantry Match: {match}%"
                )

                if missing:

                    st.caption(
                        "Missing: "
                        + ", ".join(
                            missing[:8]
                        )
                    )

            button_text = (
                "☆ Remove Favorite"
                if favorite
                else "⭐ Add Favorite"
            )

            if st.button(
                button_text,
                key=f"favorite_{index}"
            ):

                if favorite:

                    st.session_state.favorites.remove(
                        recipe_name
                    )

                else:

                    st.session_state.favorites.append(
                        recipe_name
                    )

                st.rerun()


# =========================================================
# BUDGET & SHOPPING
# =========================================================

def budget_page():

    back_button()

    st.markdown(
        """
        <div class="page-header">

            <h1>💰 Budget & Smart Shopping</h1>

            <p>
                Manage daily, weekly or monthly household food
                spending and keep your shopping list organized.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        period = st.selectbox(
            "Budget Period",
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
                st.session_state.budget_period
            )
        )

    with c2:

        amount = st.number_input(
            "Household Budget (PKR)",
            min_value=500,
            max_value=1000000,
            value=int(
                st.session_state.budget_amount
            ),
            step=500
        )

    st.session_state.budget_period = period
    st.session_state.budget_amount = amount

    if period == "Daily":

        daily = amount
        weekly = amount * 7
        monthly = amount * 30

    elif period == "Weekly":

        daily = amount / 7
        weekly = amount
        monthly = amount * 4.33

    else:

        daily = amount / 30
        weekly = amount / 4.33
        monthly = amount

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Daily",
        f"Rs {daily:,.0f}"
    )

    c2.metric(
        "Weekly",
        f"Rs {weekly:,.0f}"
    )

    c3.metric(
        "Monthly",
        f"Rs {monthly:,.0f}"
    )

    if st.session_state.family:

        st.markdown(
            '<div class="section-title">Individual Allocations</div>',
            unsafe_allow_html=True
        )

        allocation_total = 0

        for member in st.session_state.family:

            allocation = st.number_input(
                f"{member['name']} Allocation",
                min_value=0,
                max_value=int(amount),
                value=0,
                step=500,
                key=f"allocation_{member['name']}"
            )

            allocation_total += allocation

        if allocation_total > amount:

            st.error(
                "Individual allocations exceed the household budget."
            )

        else:

            remaining = (
                amount
                - allocation_total
            )

            st.success(
                f"Allocated: Rs {allocation_total:,} | "
                f"Remaining: Rs {remaining:,}"
            )

    st.markdown(
        '<div class="section-title">🛒 Smart Shopping List</div>',
        unsafe_allow_html=True
    )

    with st.form(
        "shopping_form"
    ):

        item = st.text_input(
            "Add an item",
            placeholder="e.g. Tomatoes"
        )

        add = st.form_submit_button(
            "Add to Shopping List",
            use_container_width=True
        )

    if add and item.strip():

        item = item.strip()

        if item not in st.session_state.shopping_list:

            st.session_state.shopping_list.append(
                item
            )

        st.rerun()

    if st.session_state.shopping_list:

        for index, item in enumerate(
            st.session_state.shopping_list
        ):

            c1, c2 = st.columns(
                [8, 1]
            )

            with c1:

                st.write(
                    f"🛒 {item}"
                )

            with c2:

                if st.button(
                    "×",
                    key=f"delete_shop_{index}"
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
            "Your shopping list is empty."
        )


# =========================================================
# MEAL PLANNER
# =========================================================

def meal_planner():

    back_button()

    st.markdown(
        """
        <div class="page-header">

            <h1>🍽️ Smart Family Meal Planner</h1>

            <p>
                Create a 7-day family plan using goals, allergies,
                pantry ingredients, cuisine preferences and nutrition targets.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.family:

        st.warning(
            "Please add at least one family member first."
        )

        if st.button(
            "Add Family Member →"
        ):
            navigate(
                "Family Profiles"
            )

        return

    c1, c2 = st.columns(2)

    with c1:

        cuisines = st.multiselect(
            "Preferred Cuisine",
            [
                "Pakistani / Desi",
                "Indian",
                "Chinese",
                "Italian",
                "Continental",
                "Mixed",
            ],
            default=[
                "Pakistani / Desi"
            ]
        )

    with c2:

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
                "Less Oil"
            ]
        )

    if (
        "Pantry First" in preferences
        and st.session_state.pantry
    ):

        st.success(
            "🧺 Pantry-first planning is enabled."
        )

    if st.button(
        "✨ Generate 7-Day Meal Plan",
        use_container_width=True
    ):

        plan = generate_meal_plan(
            cuisines,
            preferences
        )

        st.session_state.meal_plan = plan

        st.success(
            "Your family meal plan is ready! 🎉"
        )

    if st.session_state.meal_plan:

        st.markdown(
            '<div class="section-title">📅 Weekly Family Plan</div>',
            unsafe_allow_html=True
        )

        for day in st.session_state.meal_plan:

            with st.expander(
                f"Day {day['day']}",
                expanded=(
                    day["day"] == 1
                )
            ):

                for meal in day["meals"]:

                    st.markdown(
                        f"""
                        <div class="soft-card">

                            <h3>
                                {meal['meal']} · {meal['name']}
                            </h3>

                            <span class="macro">
                                🔥 {meal['calories']} kcal
                            </span>

                            <span class="macro">
                                💪 {meal['protein']}g protein
                            </span>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    for member, portion in meal[
                        "portions"
                    ].items():

                        st.write(
                            f"👤 **{member}:** {portion}"
                        )


def generate_meal_plan(
    cuisines,
    preferences
):

    # -----------------------------------------------------
    # AI PLAN
    # -----------------------------------------------------

    if groq_client is not None:

        family_data = []

        for member in st.session_state.family:

            family_data.append(
                {
                    "name": member["name"],
                    "goal": member["goal"],
                    "calories": member[
                        "nutrition"
                    ]["Calories"],
                    "protein": member[
                        "nutrition"
                    ]["Protein"],
                    "allergies": member[
                        "allergies"
                    ],
                }
            )

        recipe_data = []

        if not recipes.empty:

            safe = recipes[
                recipes.apply(
                    allergy_safe,
                    axis=1
                )
            ]

            for _, row in safe.head(
                40
            ).iterrows():

                recipe_data.append(
                    {
                        "name": row[
                            "recipe_name"
                        ],
                        "meal_type": row[
                            "meal_type"
                        ],
                        "calories": row[
                            "calories"
                        ],
                        "protein": row[
                            "protein_g"
                        ],
                        "ingredients": row[
                            "ingredients"
                        ],
                    }
                )

        prompt = f"""
Create a realistic 7-day family meal plan.

Family:
{json.dumps(family_data)}

Cuisine:
{json.dumps(cuisines)}

Preferences:
{json.dumps(preferences)}

Pantry:
{json.dumps(st.session_state.pantry)}

Recipes:
{json.dumps(recipe_data)}

Requirements:
- 7 days
- Breakfast
- Lunch
- Snack
- Dinner
- Respect allergies
- Use pantry items where possible
- Individual portions may differ
- Keep meals practical
- Do not give medical treatment advice

Return ONLY JSON in this format:

{{
    "days": [
        {{
            "day": 1,
            "meals": [
                {{
                    "meal": "Breakfast",
                    "name": "Recipe name",
                    "calories": 400,
                    "protein": 20,
                    "portions": {{
                        "Member": "1 serving"
                    }}
                }}
            ]
        }}
    ]
}}
"""

        try:

            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a nutrition meal planning "
                            "assistant. Return valid JSON only."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.3,
                max_tokens=5000,
            )

            result = extract_json(
                response.choices[0].message.content
            )

            if (
                isinstance(result, dict)
                and "days" in result
            ):

                return result["days"]

        except Exception:
            pass

    # -----------------------------------------------------
    # FALLBACK PLAN
    # -----------------------------------------------------

    base_meals = [
        (
            "Breakfast",
            "Egg & Vegetable Breakfast",
            380,
            22,
        ),
        (
            "Lunch",
            "Chicken Rice Bowl",
            520,
            35,
        ),
        (
            "Snack",
            "Chana Chaat",
            230,
            10,
        ),
        (
            "Dinner",
            "Daal, Roti & Salad",
            460,
            22,
        ),
    ]

    weekly_plan = []

    for day_number in range(1, 8):

        meals = []

        for meal_name, meal_title, calories, protein in base_meals:

            portions = {}

            for member in st.session_state.family:

                goal = member["goal"]

                if goal == "Weight Loss":
                    portion = "0.8 serving"

                elif goal == "Weight Gain":
                    portion = "1.2 servings"

                else:
                    portion = "1 serving"

                portions[
                    member["name"]
                ] = portion

            meals.append(
                {
                    "meal": meal_name,
                    "name": meal_title,
                    "calories": calories,
                    "protein": protein,
                    "portions": portions,
                }
            )

        weekly_plan.append(
            {
                "day": day_number,
                "meals": meals,
            }
        )

    return weekly_plan


# =========================================================
# WORKOUT PLANNER
# =========================================================

def workout_planner():

    back_button()

    st.markdown(
        """
        <div class="page-header">

            <h1>💪 Workout Planner</h1>

            <p>
                Create a simple personalized 7-day routine
                based on your fitness goal and available equipment.
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
        member["name"]
        for member in st.session_state.family
    ]

    selected_name = st.selectbox(
        "Select Member",
        names
    )

    member = next(
        member
        for member in st.session_state.family
        if member["name"] == selected_name
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
                Equipment:
                {", ".join(member["equipment"])}
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🏃 Generate 7-Day Workout",
        use_container_width=True
    ):

        plan = generate_workout(
            member
        )

        st.session_state.workout_plan[
            selected_name
        ] = plan

        st.success(
            "Workout plan generated."
        )

    plan = st.session_state.workout_plan.get(
        selected_name
    )

    if plan:

        completed_count = 0

        for day in plan:

            with st.expander(
                f"Day {day['day']} · {day['focus']}",
                expanded=(
                    day["day"] == 1
                )
            ):

                exercises = day[
                    "exercises"
                ]

                if not exercises:

                    st.write(
                        "🌙 Rest and recovery"
                    )

                for exercise in exercises:

                    st.write(
                        f"• {exercise}"
                    )

                completed = st.checkbox(
                    "Mark day complete",
                    key=(
                        f"workout_{selected_name}_"
                        f"{day['day']}"
                    )
                )

                if completed:
                    completed_count += 1

        st.progress(
            completed_count / 7,
            text=(
                f"Weekly completion: "
                f"{completed_count}/7 days"
            )
        )


def generate_workout(member):

    if groq_client is not None:

        prompt = f"""
Create a safe general 7-day fitness plan.

Person:
{member["name"]}

Goal:
{member["goal"]}

Activity:
{member["activity"]}

Location:
{member["workout_location"]}

Equipment:
{member["equipment"]}

Return ONLY JSON:

{{
    "week": [
        {{
            "day": 1,
            "focus": "Full Body",
            "exercises": [
                "Exercise - 3 sets x 10 reps"
            ]
        }}
    ]
}}

Include rest/recovery days.
Do not provide medical treatment.
"""

        try:

            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Return valid JSON only."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.3,
                max_tokens=2500,
            )

            result = extract_json(
                response.choices[0].message.content
            )

            if (
                isinstance(result, dict)
                and "week" in result
            ):

                return result["week"]

        except Exception:
            pass

    return [
        {
            "day": 1,
            "focus": "Full Body",
            "exercises": [
                "Bodyweight Squats - 3 x 12",
                "Wall or Incline Push-ups - 3 x 10",
                "Brisk Walk - 20 minutes",
            ],
        },
        {
            "day": 2,
            "focus": "Recovery",
            "exercises": [
                "Gentle stretching - 15 minutes",
            ],
        },
        {
            "day": 3,
            "focus": "Lower Body",
            "exercises": [
                "Lunges - 3 x 10 each side",
                "Glute Bridges - 3 x 15",
                "Calf Raises - 3 x 15",
            ],
        },
        {
            "day": 4,
            "focus": "Rest",
            "exercises": [],
        },
        {
            "day": 5,
            "focus": "Upper Body & Core",
            "exercises": [
                "Wall Push-ups - 3 x 12",
                "Bird Dogs - 3 x 10",
                "Plank - 3 x 20 seconds",
            ],
        },
        {
            "day": 6,
            "focus": "Cardio",
            "exercises": [
                "Brisk Walking - 30 minutes",
            ],
        },
        {
            "day": 7,
            "focus": "Recovery",
            "exercises": [
                "Gentle stretching - 15 minutes",
            ],
        },
    ]


# =========================================================
# PROGRESS TRACKER
# =========================================================

def progress_page():

    back_button()

    st.markdown(
        """
        <div class="page-header">

            <h1>📊 Progress Tracker</h1>

            <p>
                Track weight, BMI, calories, protein and
                fitness progress over time.
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
        member["name"]
        for member in st.session_state.family
    ]

    selected_name = st.selectbox(
        "Select Member",
        names
    )

    member = next(
        member
        for member in st.session_state.family
        if member["name"] == selected_name
    )

    st.markdown(
        '<div class="section-title">📝 Log Today\'s Progress</div>',
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
                    member["weight"]
                ),
                step=0.1
            )

        with c2:

            calories = st.number_input(
                "Calories Consumed",
                min_value=0,
                max_value=10000,
                value=0,
                step=50
            )

        with c3:

            protein = st.number_input(
                "Protein Consumed (g)",
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

        bmi = weight / (
            (member["height"] / 100)
            ** 2
        )

        st.session_state.progress_logs.append(
            {
                "date": str(date.today()),
                "member": selected_name,
                "weight": weight,
                "bmi": round(bmi, 1),
                "calories": calories,
                "protein": protein,
            }
        )

        st.success(
            "Progress saved successfully."
        )

    member_logs = [
        log
        for log in st.session_state.progress_logs
        if log["member"] == selected_name
    ]

    if not member_logs:

        st.info(
            "Add your first progress entry to unlock your graphs."
        )

        return

    df = pd.DataFrame(
        member_logs
    )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df = df.sort_values(
        "date"
    )

    latest = df.iloc[-1]

    first_weight = df.iloc[0]["weight"]

    weight_change = (
        latest["weight"]
        - first_weight
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Current Weight",
        f"{latest['weight']:.1f} kg"
    )

    c2.metric(
        "BMI",
        f"{latest['bmi']:.1f}"
    )

    c3.metric(
        "Weight Change",
        f"{weight_change:+.1f} kg"
    )

    c4.metric(
        "Calories",
        f"{latest['calories']:,.0f}"
    )

    c1, c2 = st.columns(2)

    with c1:

        figure = px.line(
            df,
            x="date",
            y="weight",
            markers=True,
            title="Weight Trend"
        )

        figure.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )

    with c2:

        figure = px.line(
            df,
            x="date",
            y="bmi",
            markers=True,
            title="BMI Trend"
        )

        figure.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )

    c1, c2 = st.columns(2)

    with c1:

        figure = px.bar(
            df,
            x="date",
            y="calories",
            title="Calories Consumed"
        )

        figure.add_hline(
            y=member["nutrition"]["Calories"],
            line_dash="dash",
            annotation_text="Target"
        )

        figure.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )

    with c2:

        figure = px.line(
            df,
            x="date",
            y="protein",
            markers=True,
            title="Protein Intake"
        )

        figure.add_hline(
            y=member["nutrition"]["Protein"],
            line_dash="dash",
            annotation_text="Target"
        )

        figure.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            figure,
            use_container_width=True
        )


# =========================================================
# FAVORITES
# =========================================================

def favorites_page():

    back_button()

    st.markdown(
        """
        <div class="page-header">

            <h1>❤️ Favorite Recipes</h1>

            <p>
                Your saved recipes are available here for quick access.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.favorites:

        st.info(
            "No favorites yet. Save recipes from Recipe Explorer."
        )

        return

    if recipes.empty:
        return

    for favorite in st.session_state.favorites:

        matches = recipes[
            recipes["recipe_name"]
            .astype(str)
            .str.lower()
            == favorite.lower()
        ]

        if matches.empty:
            continue

        row = matches.iloc[0]

        with st.expander(
            f"❤️ {favorite}"
        ):

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Calories",
                f"{row['calories']:.0f}"
            )

            c2.metric(
                "Protein",
                f"{row['protein_g']:.0f}g"
            )

            c3.metric(
                "Fat",
                f"{row['fat_g']:.0f}g"
            )

            ingredients = parse_list(
                row["ingredients"]
            )

            if ingredients:

                st.write(
                    "**Ingredients:** "
                    + ", ".join(
                        ingredients
                    )
                )

            if st.button(
                "Remove Favorite",
                key=f"remove_favorite_{favorite}"
            ):

                st.session_state.favorites.remove(
                    favorite
                )

                st.rerun()


# =========================================================
# MAIN ROUTER
# =========================================================

if st.session_state.page == "Dashboard":

    dashboard()

elif st.session_state.page == "Family Profiles":

    family_profiles()

elif st.session_state.page == "Meal Planner":

    meal_planner()

elif st.session_state.page == "Smart Pantry":

    smart_pantry()

elif st.session_state.page == "Recipe Explorer":

    recipe_explorer()

elif st.session_state.page == "Budget & Shopping":

    budget_page()

elif st.session_state.page == "Workout Planner":

    workout_planner()

elif st.session_state.page == "Progress":

    progress_page()

elif st.session_state.page == "Favorites":

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
    padding:1rem;
    color:#758078;
    font-size:.82rem;
">

    🥗 <b>NutriNest</b>
    · Smart Family Nutrition & Wellness

    <br>

    Eat well · Move well · Live well 💚

</div>
""",
    unsafe_allow_html=True
)
