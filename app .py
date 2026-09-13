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
    page_title="NutriNest | Family Wellness",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# PREMIUM UI
# =========================================================

st.markdown("""
<style>

:root {
    --cream: #FBF8F3;
    --white: #FFFFFF;
    --sage: #E7F0E7;
    --mint: #EEF7F1;
    --peach: #FBE9DD;
    --lavender: #EEEAF7;
    --yellow: #FFF3CF;
    --ink: #25302B;
    --muted: #69756F;
    --green: #587864;
    --green-dark: #395847;
    --border: #E0DED7;
}

.stApp {
    background:
        radial-gradient(circle at 0% 0%, #E8F2E8 0, transparent 25rem),
        radial-gradient(circle at 100% 0%, #FBE9DD 0, transparent 25rem),
        var(--cream);
    color: var(--ink);
}

.block-container {
    max-width: 1280px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E9F1E8, #F8F3EA);
    border-right: 1px solid #DDE5DB;
}

[data-testid="stSidebar"] * {
    color: var(--ink);
}

h1, h2, h3, h4, h5, h6,
p, label, span {
    color: var(--ink);
}

.hero {
    background: linear-gradient(
        120deg,
        #E5F0E5,
        #FBE9DD 55%,
        #EEEAF7
    );
    border: 1px solid rgba(88,120,100,.15);
    border-radius: 30px;
    padding: 2.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 18px 50px rgba(40,60,48,.07);
}

.hero-kicker {
    display: inline-block;
    background: rgba(255,255,255,.75);
    border: 1px solid #D8E4DA;
    border-radius: 999px;
    padding: .35rem .75rem;
    font-size: .75rem;
    font-weight: 800;
    color: var(--green-dark);
}

.hero h1 {
    font-size: clamp(2rem, 4vw, 3.4rem);
    line-height: 1;
    letter-spacing: -.045em;
    margin: .7rem 0 .6rem;
    font-weight: 900;
}

.hero p {
    color: #56645E;
    max-width: 800px;
    font-size: 1.05rem;
}

.section-title {
    font-size: 1.45rem;
    font-weight: 900;
    margin-top: 1.4rem;
    margin-bottom: .25rem;
}

.section-subtitle {
    color: var(--muted);
    margin-bottom: 1rem;
}

.card {
    background: rgba(255,255,255,.92);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.1rem;
    box-shadow: 0 8px 25px rgba(40,50,45,.045);
    margin-bottom: .8rem;
}

.card-sage {
    background: linear-gradient(145deg,#FFFFFF,#F0F8F1);
}

.card-peach {
    background: linear-gradient(145deg,#FFFFFF,#FFF5EF);
}

.card-lavender {
    background: linear-gradient(145deg,#FFFFFF,#F7F4FC);
}

.card-yellow {
    background: linear-gradient(145deg,#FFFFFF,#FFFBF0);
}

.recipe-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.05rem;
    margin: .5rem 0;
    box-shadow: 0 7px 22px rgba(40,50,45,.045);
}

.badge {
    display: inline-block;
    padding: .3rem .65rem;
    border-radius: 999px;
    background: #EFF5EF;
    color: var(--green-dark);
    font-size: .75rem;
    font-weight: 800;
    margin-right: .25rem;
}

.macro {
    display: inline-block;
    padding: .25rem .55rem;
    border-radius: 999px;
    background: #F0F5F1;
    border: 1px solid #DCE6DE;
    font-size: .75rem;
    font-weight: 750;
    margin: .12rem;
}

.info-box {
    background: #EFF7F0;
    border: 1px solid #D9E6DA;
    border-radius: 17px;
    padding: 1rem;
}

.warning-box {
    background: #FFF8E5;
    border: 1px solid #E9DDBD;
    border-radius: 17px;
    padding: 1rem;
}

.pantry-item {
    background: white;
    border: 1px solid #E1DED7;
    border-radius: 13px;
    padding: .6rem .75rem;
    margin: .25rem 0;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 12px;
    min-height: 2.65rem;
    font-weight: 800;
    background: var(--green);
    border: 1px solid var(--green);
    color: white !important;
}

.stButton > button:hover {
    background: var(--green-dark);
    border-color: var(--green-dark);
}

div[data-baseweb="select"] > div,
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border-radius: 12px !important;
    background: white !important;
    border-color: #D8DDD8 !important;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,.9);
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: .8rem 1rem;
}

[data-testid="stMetricValue"] {
    color: #33483D;
    font-weight: 850;
}

.footer {
    margin-top: 2rem;
    padding: .8rem;
    text-align: center;
    border-radius: 14px;
    background: #F2EEE6;
    color: #756E63;
    font-size: .78rem;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATASET
# =========================================================

DATA_FILES = [
    "data/nutrinest_recipes_clean.csv",
    "data/recipes.csv",
    "data/nutrinest_recipes.csv",
    "nutrinest_recipes_clean.csv",
    "recipes.csv",
]


def find_dataset():
    for path in DATA_FILES:
        if os.path.exists(path):
            return path
    return None


@st.cache_data
def load_recipes():

    path = find_dataset()

    if not path:
        return pd.DataFrame(), None

    df = pd.read_csv(path)

    df.columns = [
        str(c).strip().lower()
        for c in df.columns
    ]

    rename_map = {
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

        "meal type": "meal_type",
        "cuisine type": "cuisine",
    }

    df.rename(
        columns={
            k: v
            for k, v in rename_map.items()
            if k in df.columns
        },
        inplace=True
    )

    required = {
        "recipe_name": "Unnamed Recipe",
        "cuisine": "Mixed",
        "meal_type": "Meal",
        "ingredients": "",
        "steps": "",
    }

    for col, default in required.items():
        if col not in df.columns:
            df[col] = default

    for col in [
        "calories",
        "protein_g",
        "carbs_g",
        "fat_g"
    ]:
        if col not in df.columns:
            df[col] = pd.NA

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df, path


recipes, dataset_path = load_recipes()


# =========================================================
# NUTRITION ENGINE
# =========================================================

ACTIVITY = {
    "Sedentary": 1.20,
    "Lightly active": 1.375,
    "Moderately active": 1.55,
    "Very active": 1.725,
    "Extra active": 1.90,
}


GOALS = {
    "Lose weight": "weight_loss",
    "Maintain weight": "maintenance",
    "Gain weight": "weight_gain",
}


def calculate_nutrition(
    age,
    gender,
    height,
    weight,
    activity,
    goal
):

    if gender == "Male":
        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            + 5
        )
    else:
        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            - 161
        )

    tdee = bmr * ACTIVITY[activity]

    if goal == "weight_loss":
        calories = tdee - 400

    elif goal == "weight_gain":
        calories = tdee + 300

    else:
        calories = tdee

    calories = max(calories, 1200)

    bmi = weight / ((height / 100) ** 2)

    return {
        "bmi": round(bmi, 1),
        "bmr": round(bmr),
        "tdee": round(tdee),
        "calories": round(calories),
        "protein": round(calories * .25 / 4),
        "carbs": round(calories * .50 / 4),
        "fat": round(calories * .25 / 9),
        "fiber": 30,
    }


# =========================================================
# HELPERS
# =========================================================

def parse_items(value):

    if value is None:
        return []

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
            r",|;|\||\n",
            text
        )
        if x.strip()
    ]


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


def recipe_text(row):

    return (
        str(row.get("recipe_name", ""))
        + " "
        + str(row.get("ingredients", ""))
        + " "
        + str(row.get("tags", ""))
    ).lower()


def recipe_is_safe(row, family):

    text = recipe_text(row)

    for person in family:

        for allergy in person.get(
            "allergies",
            []
        ):

            if allergy == "None":
                continue

            for word in ALLERGY_WORDS.get(
                allergy,
                [allergy.lower()]
            ):

                if word.lower() in text:
                    return False

    return True


# =========================================================
# PANTRY MATCHING
# =========================================================

def pantry_match(row, pantry):

    ingredients = parse_items(
        row.get("ingredients", "")
    )

    if not ingredients:
        return 0, [], []

    pantry_lower = [
        x.lower()
        for x in pantry
    ]

    have = []
    missing = []

    for ingredient in ingredients:

        ingredient_text = ingredient.lower()

        found = any(
            item in ingredient_text
            or ingredient_text in item
            for item in pantry_lower
        )

        if found:
            have.append(ingredient)
        else:
            missing.append(ingredient)

    percentage = round(
        len(have) / len(ingredients) * 100
    )

    return percentage, have, missing


# =========================================================
# RECIPE SCORING
# =========================================================

def score_recipe(
    row,
    family,
    pantry,
    preferences
):

    if not recipe_is_safe(
        row,
        family
    ):
        return -1000

    score = 0

    # Pantry = highest priority
    pantry_score, _, _ = pantry_match(
        row,
        pantry
    )

    score += pantry_score * 0.40

    # Nutrition
    calories = row.get("calories")

    if pd.notna(calories) and family:

        targets = [
            p["nutrition"]["calories"]
            for p in family
        ]

        target = sum(targets) / len(targets)

        ideal_meal = target / 4

        difference = abs(
            float(calories)
            - ideal_meal
        )

        score += max(
            0,
            20 - difference / 40
        )

    # Protein
    if (
        "High protein" in preferences
        and pd.notna(row.get("protein_g"))
    ):
        score += min(
            15,
            float(row["protein_g"]) / 3
        )

    # Fiber
    if "More fiber" in preferences:

        text = recipe_text(row)

        fiber_foods = [
            "lentil",
            "daal",
            "chickpea",
            "bean",
            "vegetable",
            "oat",
        ]

        if any(
            x in text
            for x in fiber_foods
        ):
            score += 8

    # Quick
    if "Quick to cook" in preferences:

        text = recipe_text(row)

        if any(
            x in text
            for x in [
                "quick",
                "easy",
                "15 min",
                "20 min",
            ]
        ):
            score += 7

    # Budget
    if "Budget friendly" in preferences:
        score += 5

    return score


def ranked_recipes(
    family,
    pantry,
    preferences,
    limit=12
):

    if recipes.empty:
        return pd.DataFrame()

    df = recipes.copy()

    df["_score"] = df.apply(
        lambda row: score_recipe(
            row,
            family,
            pantry,
            preferences
        ),
        axis=1
    )

    df = df[
        df["_score"] > -1000
    ]

    return (
        df.sort_values(
            "_score",
            ascending=False
        )
        .head(limit)
    )


# =========================================================
# PANTRY CATEGORIES
# =========================================================

PANTRY_CATEGORIES = {

    "🥩 Proteins": [
        "Chicken",
        "Beef",
        "Fish",
        "Eggs",
        "Daal",
        "Chickpeas",
        "Beans",
    ],

    "🌾 Grains & Staples": [
        "Rice",
        "Atta",
        "Pasta",
        "Oats",
        "Bread",
        "Flour",
    ],

    "🥬 Vegetables": [
        "Potato",
        "Onion",
        "Tomato",
        "Spinach",
        "Carrot",
        "Capsicum",
        "Cucumber",
    ],

    "🥛 Dairy": [
        "Milk",
        "Yogurt",
        "Cheese",
        "Butter",
        "Paneer",
    ],

    "🌿 Herbs & Spices": [
        "Ginger",
        "Garlic",
        "Green Chilli",
        "Coriander",
        "Cumin",
        "Turmeric",
    ],

    "🍎 Fruits": [
        "Apple",
        "Banana",
        "Orange",
        "Mango",
        "Lemon",
    ],
}


# =========================================================
# SESSION STATE
# =========================================================

defaults = {

    "family": [],

    "pantry": [],

    "budget": {
        "amount": 30000,
        "period": "Monthly",
        "scope": "Household",
    },

    "preferences": [
        "Budget friendly",
        "High protein",
    ],

    "meal_plan": None,

    "shopping": [],

    "logs": [],

    "workouts": {},

}


for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# BUDGET ENGINE
# =========================================================

def monthly_budget(amount, period):

    if period == "Daily":
        return amount * 30

    if period == "Weekly":
        return amount * 4.33

    return amount


def daily_budget():

    b = st.session_state.budget

    return monthly_budget(
        float(b["amount"]),
        b["period"]
    ) / 30


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## 🥗 NutriNest"
    )

    st.caption(
        "Your family's smarter wellness companion"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "👨‍👩‍👧 Family",
            "🍽️ Meal Planner",
            "🧺 Pantry",
            "📖 Recipes",
            "🏃 Fitness",
            "📊 Progress",
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### 👨‍👩‍👧 Household")

    if st.session_state.family:

        for person in st.session_state.family:

            st.markdown(
                f"**{person['name']}**"
            )

            st.caption(
                f"{person['nutrition']['calories']:,} kcal/day"
            )

    else:

        st.caption(
            "Add your family members to begin."
        )

    st.divider()

    st.markdown("### 💰 Food budget")

    st.metric(
        "Daily equivalent",
        f"Rs {daily_budget():,.0f}"
    )

    st.caption(
        f"{st.session_state.budget['period']} · "
        f"{st.session_state.budget['scope']}"
    )


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<span class="hero-kicker">
SMART FAMILY WELLNESS
</span>

<h1>
Healthy planning,<br>
made for real life.
</h1>

<p>
Plan family meals, personalize portions, use what is already
in your kitchen, stay within budget and build healthier routines
without making everyday planning complicated.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# HOME
# =========================================================

if page == "🏠 Home":

    if not st.session_state.family:

        st.markdown(
            '<div class="section-title">'
            '🌱 Welcome to NutriNest'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="card card-sage">

        <h3>Let's build your personalized plan.</h3>

        <p>
        Start by adding your family members, setting your food
        budget and selecting what is already available in your
        kitchen. NutriNest will use these details to create
        smarter suggestions.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.info(
            "Start with 👨‍👩‍👧 Family from the navigation menu."
        )

    else:

        total_calories = sum(
            p["nutrition"]["calories"]
            for p in st.session_state.family
        )

        st.markdown(
            '<div class="section-title">'
            'Today at a glance'
            '</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "👨‍👩‍👧 Members",
            len(st.session_state.family)
        )

        c2.metric(
            "🔥 Family calories",
            f"{total_calories:,}"
        )

        c3.metric(
            "🧺 Pantry items",
            len(st.session_state.pantry)
        )

        c4.metric(
            "💰 Daily budget",
            f"Rs {daily_budget():,.0f}"
        )

        st.markdown(
            '<div class="section-title">'
            'Quick actions'
            '</div>',
            unsafe_allow_html=True
        )

        a, b, c = st.columns(3)

        with a:

            st.markdown("""
            <div class="card card-sage">

            <h3>🍳 What can I cook now?</h3>

            <p>
            Find meals that make the best use of ingredients
            you already have.
            </p>

            </div>
            """, unsafe_allow_html=True)

        with b:

            st.markdown("""
            <div class="card card-peach">

            <h3>✨ Build my meal plan</h3>

            <p>
            Create a personalized plan around your family's
            goals, preferences and budget.
            </p>

            </div>
            """, unsafe_allow_html=True)

        with c:

            st.markdown("""
            <div class="card card-lavender">

            <h3>🛒 Smart shopping</h3>

            <p>
            See exactly what your selected meals still need.
            </p>

            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">'
            '🧺 Best matches from your pantry'
            '</div>',
            unsafe_allow_html=True
        )

        matches = ranked_recipes(
            st.session_state.family,
            st.session_state.pantry,
            st.session_state.preferences,
            6
        )

        if matches.empty:

            st.info(
                "Add a few pantry ingredients to discover meals you can make now."
            )

        else:

            for _, row in matches.iterrows():

                match, have, missing = pantry_match(
                    row,
                    st.session_state.pantry
                )

                st.markdown(
                    f"""
                    <div class="recipe-card">

                    <span class="badge">
                    🟢 {match}% pantry match
                    </span>

                    <h3>
                    {row["recipe_name"]}
                    </h3>

                    <p>
                    {row.get("cuisine","Mixed")}
                    ·
                    {row.get("meal_type","Meal")}
                    </p>

                    <p>
                    <b>You have:</b>
                    {", ".join(have[:7]) or "Nothing yet"}
                    </p>

                    <p>
                    <b>Still needed:</b>
                    {", ".join(missing[:5]) or "Nothing major"}
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# FAMILY
# =========================================================

elif page == "👨‍👩‍👧 Family":

    st.markdown(
        '<div class="section-title">'
        '👨‍👩‍👧 Build your family profile'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="section-subtitle">'
        'These details help NutriNest personalize calories, portions and meal suggestions.'
        '</p>',
        unsafe_allow_html=True
    )

    with st.form("family_form"):

        left, right = st.columns(2)

        with left:

            name = st.text_input(
                "👤 Name",
                placeholder="e.g. Mother"
            )

            age = st.number_input(
                "🎂 Age",
                10,
                100,
                30
            )

            gender = st.selectbox(
                "⚧ Gender",
                ["Female", "Male"]
            )

            height = st.number_input(
                "📏 Height (cm)",
                120,
                220,
                165
            )

            weight = st.number_input(
                "⚖️ Weight (kg)",
                30,
                200,
                65
            )

        with right:

            goal_label = st.selectbox(
                "🎯 Main goal",
                list(GOALS.keys())
            )

            activity = st.selectbox(
                "🏃 Activity level",
                list(ACTIVITY.keys()),
                index=2
            )

            allergies = st.multiselect(
                "⚠️ Food allergies",
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

            workout_location = st.selectbox(
                "🏠 Workout setting",
                ["Home", "Gym"]
            )

            equipment = st.multiselect(
                "🏋️ Available equipment",
                [
                    "None",
                    "Yoga mat",
                    "Dumbbells",
                    "Resistance bands",
                    "Bench",
                    "Full gym",
                ],
                default=["Yoga mat"]
            )

        save = st.form_submit_button(
            "✨ Create / update profile",
            type="primary",
            use_container_width=True
        )

    if save:

        name = name.strip() or "Family Member"

        nutrition = calculate_nutrition(
            age,
            gender,
            height,
            weight,
            activity,
            GOALS[goal_label]
        )

        profile = {

            "name": name,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "goal": GOALS[goal_label],
            "goal_label": goal_label,
            "activity": activity,
            "allergies": allergies,
            "workout_location": workout_location,
            "equipment": equipment,
            "nutrition": nutrition,

        }

        st.session_state.family = [
            p
            for p in st.session_state.family
            if p["name"].lower() != name.lower()
        ]

        st.session_state.family.append(profile)

        st.success(
            f"{name}'s profile has been saved."
        )

    if st.session_state.family:

        st.markdown(
            '<div class="section-title">'
            'Your household'
            '</div>',
            unsafe_allow_html=True
        )

        cols = st.columns(
            min(3, len(st.session_state.family))
        )

        for i, person in enumerate(
            st.session_state.family
        ):

            n = person["nutrition"]

            with cols[i % len(cols)]:

                st.markdown(
                    f"""
                    <div class="card card-sage">

                    <span class="badge">
                    🎯 {person["goal_label"]}
                    </span>

                    <h3>
                    👤 {person["name"]}
                    </h3>

                    <p>
                    BMI {n["bmi"]}
                    ·
                    {person["activity"]}
                    </p>

                    <h2>
                    {n["calories"]:,}
                    <small> kcal/day</small>
                    </h2>

                    <span class="macro">
                    💪 {n["protein"]}g protein
                    </span>

                    <span class="macro">
                    🌾 {n["carbs"]}g carbs
                    </span>

                    <span class="macro">
                    🥑 {n["fat"]}g fat
                    </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "Remove",
                    key=f"remove_{person['name']}"
                ):

                    st.session_state.family = [
                        p
                        for p in st.session_state.family
                        if p["name"] != person["name"]
                    ]

                    st.rerun()


    # -----------------------------------------------------
    # BUDGET
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '💰 Set your food budget'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("budget_form"):

        c1, c2, c3 = st.columns(3)

        with c1:

            period = st.selectbox(
                "Budget period",
                [
                    "Monthly",
                    "Weekly",
                    "Daily"
                ]
            )

        with c2:

            amount = st.number_input(
                "Budget (PKR)",
                300,
                1000000,
                int(
                    st.session_state.budget[
                        "amount"
                    ]
                ),
                step=500
            )

        with c3:

            scope = st.selectbox(
                "Budget applies to",
                [
                    "Household",
                    "Individual"
                ]
            )

        save_budget = st.form_submit_button(
            "Save budget",
            use_container_width=True
        )

    if save_budget:

        st.session_state.budget = {
            "amount": amount,
            "period": period,
            "scope": scope,
        }

        st.success(
            f"Your {period.lower()} budget is Rs {amount:,.0f}."
        )

        st.info(
            f"That's approximately Rs {daily_budget():,.0f} per day."
        )


# =========================================================
# PANTRY
# =========================================================

elif page == "🧺 Pantry":

    st.markdown(
        '<div class="section-title">'
        '🧺 What is already in your kitchen?'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="section-subtitle">'
        'Tick what you already have. NutriNest will prioritize recipes that use these ingredients.'
        '</p>',
        unsafe_allow_html=True
    )

    pantry = set(
        x.lower()
        for x in st.session_state.pantry
    )

    for category, items in PANTRY_CATEGORIES.items():

        st.markdown(
            f"### {category}"
        )

        cols = st.columns(4)

        for i, item in enumerate(items):

            key = (
                "pantry_"
                + category
                + "_"
                + item
            )

            checked = cols[i % 4].checkbox(
                item,
                value=item.lower() in pantry,
                key=key
            )

            if checked:
                pantry.add(item.lower())
            else:
                pantry.discard(item.lower())

    st.markdown("### ➕ Something else?")

    custom = st.text_input(
        "Add another ingredient",
        placeholder="e.g. mince, frozen peas, vermicelli"
    )

    if st.button("Add ingredient"):

        if custom.strip():

            pantry.add(
                custom.strip().lower()
            )

    st.session_state.pantry = sorted(
        pantry
    )

    st.markdown(
        '<div class="section-title">'
        'Your pantry'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.pantry:

        cols = st.columns(4)

        for i, item in enumerate(
            st.session_state.pantry
        ):

            cols[i % 4].markdown(
                f"""
                <div class="pantry-item">
                ✓ {item.title()}
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("Clear pantry"):

            st.session_state.pantry = []

            st.rerun()

    else:

        st.info(
            "Your pantry is empty. Select some ingredients above."
        )


# =========================================================
# MEAL PLANNER
# =========================================================

elif page == "🍽️ Meal Planner":

    st.markdown(
        '<div class="section-title">'
        '🍽️ Build your family meal plan'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="section-subtitle">'
        'NutriNest combines nutrition goals, allergies, pantry availability and preferences before recommending meals.'
        '</p>',
        unsafe_allow_html=True
    )

    if not st.session_state.family:

        st.warning(
            "Please create at least one family profile first."
        )

    elif recipes.empty:

        st.error(
            "Recipe dataset not found. Put your CSV inside the data folder."
        )

    else:

        with st.form("meal_plan_form"):

            c1, c2 = st.columns(2)

            with c1:

                selected_people = st.multiselect(
                    "👨‍👩‍👧 Who are we planning for?",
                    [
                        p["name"]
                        for p in st.session_state.family
                    ],
                    default=[
                        p["name"]
                        for p in st.session_state.family
                    ]
                )

                days = st.selectbox(
                    "📅 Plan length",
                    [1, 3, 7],
                    index=2,
                    format_func=lambda x:
                        f"{x} day"
                        if x == 1
                        else f"{x} days"
                )

                cuisines = st.multiselect(
                    "🍜 Food style",
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
                    "✨ What matters most?",
                    [
                        "Budget friendly",
                        "High protein",
                        "More fiber",
                        "Quick to cook",
                        "Less oil",
                    ],
                    default=st.session_state.preferences
                )

                prioritize_pantry = st.toggle(
                    "🧺 Prioritize pantry ingredients",
                    value=True
                )

            build = st.form_submit_button(
                "✨ Build my plan",
                type="primary",
                use_container_width=True
            )

        if build:

            family = [
                p
                for p in st.session_state.family
                if p["name"] in selected_people
            ]

            if not family:
                family = st.session_state.family

            ranked = ranked_recipes(
                family,
                st.session_state.pantry,
                preferences,
                80
            )

            if ranked.empty:

                st.error(
                    "No suitable recipes were found. Try broadening your preferences."
                )

            else:

                meal_plan = []

                used = set()

                meal_types = [
                    ("Breakfast", "breakfast"),
                    ("Lunch", "lunch"),
                    ("Dinner", "dinner"),
                ]

                for day_number in range(
                    1,
                    days + 1
                ):

                    for label, hint in meal_types:

                        pool = ranked[
                            ~ranked.index.isin(used)
                        ]

                        if pool.empty:
                            pool = ranked

                        if prioritize_pantry:

                            pool = pool.copy()

                            pool["_pantry"] = pool.apply(
                                lambda r:
                                pantry_match(
                                    r,
                                    st.session_state.pantry
                                )[0],
                                axis=1
                            )

                            pool = pool.sort_values(
                                [
                                    "_pantry",
                                    "_score"
                                ],
                                ascending=False
                            )

                        matching_type = pool[
                            pool["meal_type"]
                            .astype(str)
                            .str.lower()
                            .str.contains(
                                hint,
                                na=False
                            )
                        ]

                        if not matching_type.empty:
                            pool = matching_type

                        recipe = pool.iloc[0]

                        used.add(recipe.name)

                        match, have, missing = pantry_match(
                            recipe,
                            st.session_state.pantry
                        )

                        meal_plan.append({

                            "day": day_number,
                            "meal": label,
                            "recipe": recipe.to_dict(),
                            "pantry": match,
                            "have": have,
                            "missing": missing,

                        })

                st.session_state.meal_plan = meal_plan

                missing_all = []

                for meal in meal_plan:

                    missing_all.extend(
                        meal["missing"]
                    )

                unique_missing = []

                for ingredient in missing_all:

                    if not ingredient:
                        continue

                    if not any(
                        ingredient.lower()
                        == x.lower()
                        for x in unique_missing
                    ):
                        unique_missing.append(
                            ingredient
                        )

                st.session_state.shopping = (
                    unique_missing
                )

                st.session_state.preferences = (
                    preferences
                )

                st.success(
                    "Your personalized meal plan is ready."
                )

        # -------------------------------------------------
        # DISPLAY PLAN
        # -------------------------------------------------

        if st.session_state.meal_plan:

            st.markdown(
                '<div class="section-title">'
                '✨ Your personalized plan'
                '</div>',
                unsafe_allow_html=True
            )

            max_day = max(
                x["day"]
                for x in st.session_state.meal_plan
            )

            for day_number in range(
                1,
                max_day + 1
            ):

                st.markdown(
                    f"### 📅 Day {day_number}"
                )

                day_meals = [
                    x
                    for x in st.session_state.meal_plan
                    if x["day"] == day_number
                ]

                for meal in day_meals:

                    recipe = meal["recipe"]

                    calories = recipe.get(
                        "calories"
                    )

                    protein = recipe.get(
                        "protein_g"
                    )

                    calories_text = (
                        "—"
                        if pd.isna(calories)
                        else f"{float(calories):.0f} kcal"
                    )

                    protein_text = (
                        "—"
                        if pd.isna(protein)
                        else f"{float(protein):.0f}g protein"
                    )

                    st.markdown(
                        f"""
                        <div class="recipe-card">

                        <span class="badge">
                        🍽️ {meal["meal"]}
                        </span>

                        <span class="badge">
                        🧺 {meal["pantry"]}% pantry match
                        </span>

                        <h3>
                        {recipe["recipe_name"]}
                        </h3>

                        <p>
                        {recipe.get("cuisine","Mixed")}
                        ·
                        {calories_text}
                        ·
                        {protein_text}
                        </p>

                        <p>
                        <b>Already have:</b>
                        {", ".join(meal["have"][:7]) or "—"}
                        </p>

                        <p>
                        <b>Shopping:</b>
                        {", ".join(meal["missing"][:6]) or "Nothing major"}
                        </p>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # -------------------------------------------------
            # SHOPPING
            # -------------------------------------------------

            if st.session_state.shopping:

                st.markdown(
                    '<div class="section-title">'
                    '🛒 Smart shopping list'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<p class="section-subtitle">'
                    'Only the ingredients missing from your pantry are listed here.'
                    '</p>',
                    unsafe_allow_html=True
                )

                shopping_text = []

                for i, item in enumerate(
                    st.session_state.shopping
                ):

                    checked = st.checkbox(
                        item,
                        key=f"shopping_{i}"
                    )

                    shopping_text.append(
                        f"[{'x' if checked else ' '}] {item}"
                    )

                st.download_button(
                    "⬇️ Download shopping list",
                    "\n".join(shopping_text),
                    "NutriNest_Shopping_List.txt"
                )


# =========================================================
# RECIPES
# =========================================================

elif page == "📖 Recipes":

    st.markdown(
        '<div class="section-title">'
        '📖 Explore recipes'
        '</div>',
        unsafe_allow_html=True
    )

    if recipes.empty:

        st.error(
            "Recipe dataset not found."
        )

    else:

        c1, c2, c3 = st.columns(
            [1.5, 1, 1]
        )

        with c1:

            search = st.text_input(
                "🔎 Search recipes",
                placeholder="chicken, rice, daal..."
            )

        with c2:

            cuisine = st.selectbox(
                "🍜 Cuisine",
                [
                    "All"
                ]
                + sorted(
                    recipes["cuisine"]
                    .astype(str)
                    .unique()
                    .tolist()
                )
            )

        with c3:

            max_calories = st.slider(
                "🔥 Maximum calories",
                100,
                1500,
                800,
                25
            )

        safe_only = st.toggle(
            "🛡️ Show family-safe recipes",
            value=True
        )

        df = recipes.copy()

        if safe_only:

            df = df[
                df.apply(
                    lambda row:
                    recipe_is_safe(
                        row,
                        st.session_state.family
                    ),
                    axis=1
                )
            ]

        df = df[
            df["calories"].isna()
            |
            df["calories"].le(
                max_calories
            )
        ]

        if cuisine != "All":

            df = df[
                df["cuisine"]
                .astype(str)
                .str.casefold()
                ==
                cuisine.casefold()
            ]

        if search.strip():

            query = search.lower()

            df = df[
                (
                    df["recipe_name"]
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        query,
                        na=False
                    )
                )
                |
                (
                    df["ingredients"]
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        query,
                        na=False
                    )
                )
            ]

        st.caption(
            f"{len(df)} recipes found"
        )

        for _, row in df.head(60).iterrows():

            match, have, missing = pantry_match(
                row,
                st.session_state.pantry
            )

            with st.expander(
                f"🍽️ {row['recipe_name']} · {match}% pantry match"
            ):

                st.markdown(
                    f"""
                    <span class="badge">
                    {row.get("cuisine","Mixed")}
                    </span>

                    <span class="badge">
                    {row.get("meal_type","Meal")}
                    </span>
                    """,
                    unsafe_allow_html=True
                )

                c1, c2, c3, c4 = st.columns(4)

                c1.metric(
                    "🔥 Calories",
                    "—"
                    if pd.isna(row["calories"])
                    else f"{float(row['calories']):.0f}"
                )

                c2.metric(
                    "💪 Protein",
                    "—"
                    if pd.isna(row["protein_g"])
                    else f"{float(row['protein_g']):.0f}g"
                )

                c3.metric(
                    "🌾 Carbs",
                    "—"
                    if pd.isna(row["carbs_g"])
                    else f"{float(row['carbs_g']):.0f}g"
                )

                c4.metric(
                    "🥑 Fat",
                    "—"
                    if pd.isna(row["fat_g"])
                    else f"{float(row['fat_g']):.0f}g"
                )

                st.markdown("### 🧺 Pantry")

                st.write(
                    "Already available: "
                    + (
                        ", ".join(have)
                        if have
                        else "None"
                    )
                )

                st.write(
                    "Still needed: "
                    + (
                        ", ".join(missing)
                        if missing
                        else "Nothing major"
                    )
                )

                ingredients = parse_items(
                    row.get(
                        "ingredients",
                        ""
                    )
                )

                if ingredients:

                    st.markdown(
                        "### 🥕 Ingredients"
                    )

                    st.write(
                        " · ".join(
                            ingredients
                        )
                    )

                if str(
                    row.get("steps","")
                ).strip():

                    st.markdown(
                        "### 👩‍🍳 Method"
                    )

                    st.write(
                        str(
                            row["steps"]
                        )
                    )


# =========================================================
# FITNESS
# =========================================================

elif page == "🏃 Fitness":

    st.markdown(
        '<div class="section-title">'
        '🏃 Weekly movement plan'
        '</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.family:

        st.warning(
            "Create a family profile first."
        )

    else:

        names = [
            p["name"]
            for p in st.session_state.family
        ]

        selected = st.selectbox(
            "👤 Choose a family member",
            names
        )

        person = next(
            p
            for p in st.session_state.family
            if p["name"] == selected
        )

        st.markdown(
            f"""
            <div class="card card-lavender">

            <span class="badge">
            🎯 {person["goal_label"]}
            </span>

            <span class="badge">
            🏠 {person["workout_location"]}
            </span>

            <h3>
            {person["name"]}
            </h3>

            <p>
            Equipment:
            {", ".join(person["equipment"])}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "🏃 Build my 7-day routine",
            type="primary",
            use_container_width=True
        ):

            workout = {

                "member": selected,

                "week": [

                    {
                        "day": 1,
                        "focus": "Full Body",
                        "exercises": [
                            "Bodyweight Squats — 3 × 12",
                            "Incline Push-ups — 3 × 10",
                            "Brisk Walk — 20 min",
                        ],
                    },

                    {
                        "day": 2,
                        "focus": "Recovery",
                        "exercises": [
                            "Gentle stretching — 15 min"
                        ],
                    },

                    {
                        "day": 3,
                        "focus": "Lower Body",
                        "exercises": [
                            "Lunges — 3 × 10 each",
                            "Glute Bridges — 3 × 15",
                        ],
                    },

                    {
                        "day": 4,
                        "focus": "Rest",
                        "exercises": [],
                    },

                    {
                        "day": 5,
                        "focus": "Upper Body + Core",
                        "exercises": [
                            "Wall Push-ups — 3 × 12",
                            "Plank — 3 × 30 sec",
                        ],
                    },

                    {
                        "day": 6,
                        "focus": "Cardio",
                        "exercises": [
                            "Brisk Walk — 30 min"
                        ],
                    },

                    {
                        "day": 7,
                        "focus": "Recovery",
                        "exercises": [
                            "Gentle stretching — 15 min"
                        ],
                    },

                ]
            }

            st.session_state.workouts[
                selected
            ] = workout

        workout = st.session_state.workouts.get(
            selected
        )

        if workout:

            for day in workout["week"]:

                with st.expander(
                    f"Day {day['day']} · {day['focus']}"
                ):

                    if not day["exercises"]:

                        st.info(
                            "🌙 Rest and recovery day."
                        )

                    else:

                        for exercise in day[
                            "exercises"
                        ]:

                            st.markdown(
                                f"**{exercise}**"
                            )


# =========================================================
# PROGRESS
# =========================================================

elif page == "📊 Progress":

    st.markdown(
        '<div class="section-title">'
        '📊 Track your progress'
        '</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.family:

        st.warning(
            "Create a family profile first."
        )

    else:

        names = [
            p["name"]
            for p in st.session_state.family
        ]

        left, right = st.columns(2)

        with left:

            st.markdown(
                """
                <div class="card card-sage">
                <h3>🍽️ Log a meal</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.form("meal_log"):

                member = st.selectbox(
                    "Family member",
                    names
                )

                meal = st.text_input(
                    "Meal",
                    "Breakfast"
                )

                status = st.selectbox(
                    "How did it go?",
                    [
                        "Followed plan",
                        "Different meal",
                        "Skipped",
                    ]
                )

                save = st.form_submit_button(
                    "Log meal",
                    use_container_width=True
                )

            if save:

                st.session_state.logs.append({

                    "date": str(date.today()),
                    "member": member,
                    "type": "meal",
                    "item": meal,
                    "status": status,
                    "minutes": 0,

                })

                st.success(
                    "Meal logged."
                )

        with right:

            st.markdown(
                """
                <div class="card card-lavender">
                <h3>🏃 Log a workout</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.form("workout_log"):

                member = st.selectbox(
                    "Family member",
                    names,
                    key="workout_member"
                )

                status = st.selectbox(
                    "Workout status",
                    [
                        "Completed",
                        "Skipped",
                        "Rest",
                    ]
                )

                minutes = st.number_input(
                    "Minutes",
                    0,
                    300,
                    30
                )

                save = st.form_submit_button(
                    "Log workout",
                    use_container_width=True
                )

            if save:

                st.session_state.logs.append({

                    "date": str(date.today()),
                    "member": member,
                    "type": "workout",
                    "item": "Workout",
                    "status": status,
                    "minutes":
                        int(minutes)
                        if status == "Completed"
                        else 0,

                })

                st.success(
                    "Workout logged."
                )

        if st.session_state.logs:

            logs = pd.DataFrame(
                st.session_state.logs
            )

            st.markdown(
                '<div class="section-title">'
                'Your progress overview'
                '</div>',
                unsafe_allow_html=True
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "📝 Entries",
                len(logs)
            )

            c2.metric(
                "🍽️ Meals logged",
                int(
                    (
                        logs["type"]
                        == "meal"
                    ).sum()
                )
            )

            c3.metric(
                "🏃 Workout minutes",
                int(
                    logs["minutes"]
                    .sum()
                )
            )

            if "workout" in logs["type"].values:

                workout_data = (
                    logs[
                        logs["type"]
                        == "workout"
                    ]
                    .groupby("member")
                    ["minutes"]
                    .sum()
                    .reset_index()
                )

                fig = px.bar(
                    workout_data,
                    x="member",
                    y="minutes",
                    title="Workout minutes"
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            st.dataframe(
                logs,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "⬇️ Download progress CSV",
                logs.to_csv(
                    index=False
                ).encode(),
                "NutriNest_Progress.csv",
                mime="text/csv"
            )

            if st.button(
                "Clear progress history"
            ):

                st.session_state.logs = []

                st.rerun()

        else:

            st.info(
                "Your progress history will appear here as you log meals and workouts."
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
    🥗 NutriNest · Family nutrition and wellness planning
    <br>
    General wellness guidance only — not a substitute for professional medical advice.
    </div>
    """,
    unsafe_allow_html=True
)
