import ast
import json
import os
import re
import random
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

try:
    from groq import Groq
except Exception:
    Groq = None

st.set_page_config(page_title="NutriNest", page_icon="🥗", layout="wide", initial_sidebar_state="collapsed")

# ============================================================
# DESIGN — IMPORTANT: every HTML block is inside st.markdown
# with unsafe_allow_html=True, so HTML will render instead of
# appearing as raw text in the Streamlit page.
# ============================================================
st.markdown("""
<style>
:root {
  --ink:#26342d; --muted:#68756e; --cream:#fbf8f3; --white:#ffffff;
  --sage:#e7f1e7; --mint:#edf7f0; --peach:#fbe9dd; --lav:#eeeaf7;
  --butter:#fff4cf; --accent:#587864; --accent-dark:#3f5d4a; --line:#e2ded5;
}
.stApp { background: radial-gradient(circle at 5% 0%,rgba(231,241,231,.85),transparent 28rem), radial-gradient(circle at 95% 4%,rgba(251,233,221,.8),transparent 28rem), var(--cream); color:var(--ink); }
.block-container { max-width:1380px; padding-top:1.35rem; padding-bottom:4rem; }
h1,h2,h3,h4,h5,h6 { color:var(--ink)!important; }
[data-testid="stMetric"] { background:rgba(255,255,255,.94); border:1px solid var(--line); border-radius:18px; padding:.85rem; box-shadow:0 6px 20px rgba(40,60,48,.05); }
[data-testid="stMetricValue"] { color:var(--accent)!important; font-weight:900; }
.stButton > button { border-radius:13px; font-weight:800; min-height:2.55rem; }
.stButton > button[kind="primary"] { background:var(--accent); border-color:var(--accent); color:#fff; }
.stButton > button:hover { border-color:var(--accent-dark); }
.stTextInput input,.stNumberInput input,.stTextArea textarea { border-radius:12px!important; }
div[data-baseweb="select"] > div { border-radius:12px!important; }
.hero { padding:2.15rem 2.3rem; border-radius:30px; background:linear-gradient(120deg,#e6f0e6,#fbe9dd,#eeeaf7); border:1px solid #dfe5dd; box-shadow:0 16px 42px rgba(45,65,53,.08); margin-bottom:1rem; }
.hero-badge { display:inline-block; padding:.4rem .8rem; border-radius:999px; background:rgba(255,255,255,.8); color:#4c6957!important; font-size:.76rem; font-weight:900; letter-spacing:.08em; }
.hero-title { font-size:3rem; line-height:1.05; font-weight:950; letter-spacing:-.045em; margin-top:.7rem; }
.hero-subtitle { max-width:900px; color:#5f6d65!important; font-size:1.03rem; line-height:1.6; margin-top:.55rem; }
.quote-card { padding:1.15rem 1.45rem; border-radius:22px; background:linear-gradient(135deg,#fffdf7,#eef7f0); border:1px solid #dfe6de; box-shadow:0 8px 24px rgba(40,60,48,.06); margin:1rem 0 1.3rem; }
.quote { font-size:1.18rem; font-weight:850; color:#3d5948!important; }
.quote-category { margin-top:.35rem; color:#78847d!important; font-size:.8rem; }
.slideshow { position:relative; height:205px; overflow:hidden; border-radius:26px; margin:1rem 0 1.3rem; }
.slide { position:absolute; inset:0; padding:2rem; display:flex; flex-direction:column; justify-content:center; opacity:0; animation:slideFade 25s infinite both; }
.slide:nth-child(1){background:linear-gradient(120deg,#e6f0e6,#f5f9f4);animation-delay:0s;}
.slide:nth-child(2){background:linear-gradient(120deg,#fbe8dc,#fff5ed);animation-delay:5s;}
.slide:nth-child(3){background:linear-gradient(120deg,#eeeaf7,#f8f6fc);animation-delay:10s;}
.slide:nth-child(4){background:linear-gradient(120deg,#fff1c9,#fff9e8);animation-delay:15s;}
.slide:nth-child(5){background:linear-gradient(120deg,#e8f3f6,#f6fbfc);animation-delay:20s;}
.slide h2{font-size:1.8rem;margin:0 0 .35rem;font-weight:950;}
.slide p{max-width:780px;color:#68756e!important;margin:0;}
@keyframes slideFade{0%{opacity:0}5%{opacity:1}23%{opacity:1}28%{opacity:0}100%{opacity:0}}
.section-title { font-size:1.45rem; font-weight:950; margin:1.25rem 0 .8rem; }
.feature-card { min-height:175px; padding:1.2rem; border-radius:22px; background:rgba(255,255,255,.94); border:1px solid var(--line); box-shadow:0 8px 26px rgba(45,60,50,.06); margin-bottom:.65rem; }
.feature-icon { font-size:2.2rem; }
.feature-title { font-size:1.06rem; font-weight:900; margin-top:.4rem; }
.feature-description { color:#6b7770!important; font-size:.84rem; line-height:1.45; margin-top:.25rem; }
.page-header { padding:1.25rem 1.45rem; border-radius:22px; background:linear-gradient(120deg,#eaf2e9,#fff9f2); border:1px solid var(--line); margin-bottom:1.2rem; }
.page-header h1{margin:0;font-size:2rem;font-weight:950}.page-header p{margin:.35rem 0 0;color:#6b7770!important;}
.soft-card,.recipe-card,.member-card,.plate-card { padding:1.05rem 1.15rem; border-radius:20px; background:rgba(255,255,255,.94); border:1px solid var(--line); box-shadow:0 7px 22px rgba(45,60,50,.05); margin-bottom:.8rem; }
.recipe-card{background:linear-gradient(145deg,#fff,#fff9ef)}
.member-card{background:linear-gradient(145deg,#fff,#f0f7f0)}
.plate-card{background:linear-gradient(145deg,#fff,#f4f8f3)}
.pill,.macro-chip { display:inline-block; padding:.27rem .62rem; margin:.13rem; border-radius:999px; font-size:.74rem; font-weight:800; }
.pill{background:#f1eee6;color:#655d4d!important}.macro-chip{background:#edf5ef;color:#496352!important}
.quick-card { padding:1rem; border-radius:18px; background:#fff; border:1px solid var(--line); }
.footer-note{text-align:center;color:#7a857f!important;font-size:.8rem;padding:1.5rem 0;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATHS = [
    os.path.join(BASE_DIR, "data", "nutrinest_recipes_clean.csv"),
    os.path.join(BASE_DIR, "data", "nutrinest_recipes_clean.xlsx"),
    os.path.join(BASE_DIR, "data", "nutrinest_recipes_clean.xls"),
    os.path.join(BASE_DIR, "data", "recipes.csv"),
    os.path.join(BASE_DIR, "data", "recipes.xlsx"),
    os.path.join(BASE_DIR, "data", "recipes.xls"),
    os.path.join(BASE_DIR, "nutrinest_recipes_clean.csv"),
    os.path.join(BASE_DIR, "recipes.csv"),
]


def find_dataset():
    for p in DATA_PATHS:
        if os.path.exists(p):
            return p
    return None


@st.cache_data

def load_recipes():
    path = find_dataset()
    if not path:
        return pd.DataFrame(), None
    try:
        if path.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)
    except Exception:
        return pd.DataFrame(), path
    df.columns = [str(c).strip().lower() for c in df.columns]
    aliases = {
        "name":"recipe_name", "recipe name":"recipe_name", "dish name":"recipe_name",
        "calories_per_serving":"calories", "calories per serving":"calories",
        "protein":"protein_g", "protein(g)":"protein_g", "protein per serving":"protein_g",
        "carbs":"carbs_g", "carbohydrates":"carbs_g", "carbs(g)":"carbs_g",
        "fat":"fat_g", "fat(g)":"fat_g", "cuisine_type":"cuisine", "cuisine type":"cuisine",
        "meal type":"meal_type",
    }
    for old,new in aliases.items():
        if old in df.columns and new not in df.columns:
            df = df.rename(columns={old:new})
    defaults = {
        "recipe_name":"Recipe", "meal_type":"Main", "cuisine":"Mixed", "ingredients":"",
        "steps":"", "allergens":"", "tags":"", "calories":0, "protein_g":0, "carbs_g":0,
        "fat_g":0, "fiber_g":0, "servings":1, "serving_size":"1 serving",
    }
    for c,d in defaults.items():
        if c not in df.columns:
            df[c] = d
    for c in ["calories","protein_g","carbs_g","fat_g","fiber_g","servings"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    return df, path


recipes_df, recipe_source = load_recipes()

# ============================================================
# SESSION
# ============================================================
def init_state():
    defaults = {
        "page":"Dashboard", "nav_history":[], "family":[], "pantry":[], "favorites":[], "shopping_list":[],
        "meal_plan":None, "workouts":{}, "logs":[],
        "budget_period":"Monthly", "budget_amount":30000,
        "budget_spent":0.0, "allocations":{}, "budget_entry_mode":"Household Total",
        "workout_done":{},
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


def go(page, remember=True):
    current = st.session_state.get("page", "Dashboard")
    if page == current:
        return
    if remember and current != "Dashboard":
        history = st.session_state.setdefault("nav_history", [])
        if not history or history[-1] != current:
            history.append(current)
        # Keep the in-app history compact and predictable.
        st.session_state.nav_history = history[-12:]
    st.session_state.page = page
    st.rerun()


def go_back():
    history = st.session_state.get("nav_history", [])
    if history:
        previous = history.pop()
        st.session_state.nav_history = history
        st.session_state.page = previous
    else:
        st.session_state.page = "Dashboard"
    st.rerun()


def go_dashboard():
    st.session_state.nav_history = []
    st.session_state.page = "Dashboard"
    st.rerun()


def parse_listish(value):
    if value is None:
        return []
    try:
        if pd.isna(value):
            return []
    except Exception:
        pass
    if isinstance(value,list):
        return [str(x).strip() for x in value if str(x).strip()]
    text = str(value).strip()
    if not text:
        return []
    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed,list):
            return [str(x).strip() for x in parsed if str(x).strip()]
    except Exception:
        pass
    return [x.strip() for x in re.split(r"[,;|\n]",text) if x.strip()]


def norm(text):
    return re.sub(r"[^a-z0-9 ]"," ",str(text).lower()).strip()


ALLERGY_TERMS = {
    "nuts":["nut","almond","peanut","cashew","walnut","pistachio"],
    "dairy":["milk","cheese","yogurt","yoghurt","cream","butter","paneer"],
    "gluten":["wheat","flour","bread","roti","chapati","pasta","barley"],
    "egg":["egg","eggs"],
    "seafood":["fish","prawn","shrimp","seafood","tuna","salmon"],
}


def safe_for_family(row):
    allergies=[]
    for m in st.session_state.family:
        allergies += [str(a).lower() for a in m.get("allergies",[]) if str(a).lower() not in ("none","")]
    if not allergies:
        return True
    text = " ".join([
        str(row.get("recipe_name","")),str(row.get("ingredients","")),str(row.get("allergens","")),str(row.get("tags",""))
    ]).lower()
    for a in allergies:
        for term in ALLERGY_TERMS.get(a,[a]):
            if term in text:
                return False
    return True


def pantry_match(row):
    ingredients=parse_listish(row.get("ingredients",""))
    if not ingredients:
        return 0,[],[]
    pantry=[norm(x) for x in st.session_state.pantry]
    matched=[]; missing=[]
    for ingredient in ingredients:
        ni=norm(ingredient)
        if any(pi in ni or ni in pi for pi in pantry if pi):
            matched.append(ingredient)
        else:
            missing.append(ingredient)
    pct=round(100*len(matched)/max(1,len(ingredients)))
    return pct,matched,missing

# ============================================================
# NUTRITION + AI
# ============================================================
def nutrition(age, sex, height, weight, activity, goal):
    bmr = 10*weight + 6.25*height - 5*age + (5 if sex=="Male" else -161)
    factors={"Sedentary":1.2,"Light":1.375,"Moderate":1.55,"Active":1.725,"Very Active":1.9}
    tdee=bmr*factors.get(activity,1.55)
    if goal=="Weight Loss": target=tdee-400
    elif goal=="Weight Gain": target=tdee+300
    else: target=tdee
    target=max(1200,round(target))
    return {
        "BMI":round(weight/((height/100)**2),1),"BMR":round(bmr),"TDEE":round(tdee),"Target":target,
        "Protein":round(target*.25/4),"Carbs":round(target*.50/4),"Fat":round(target*.25/9),"Fiber":30,
    }


def get_secret(name):
    try:
        value=st.secrets.get(name)
        if value: return value
    except Exception:
        pass
    return os.getenv(name)


def get_client():
    if Groq is None: return None
    key=get_secret("GROQ_API_KEY")
    if not key: return None
    try: return Groq(api_key=key)
    except Exception: return None


client=get_client()
AI_MODEL="openai/gpt-oss-120b"


def extract_json(text):
    if not text: return None
    text=str(text).strip()
    if "```" in text:
        parts=text.split("```")
        text=max(parts,key=len).strip()
        if text.lower().startswith("json"):
            text=text[4:].strip()
    start=text.find("{"); end=text.rfind("}")
    if start<0 or end<0: return None
    try: return json.loads(text[start:end+1])
    except Exception: return None

# ============================================================
# QUOTES
# ============================================================
QUOTES=[
("Healthy habits become easier when the whole family joins in.","Family Health 🏡"),
("Small healthy choices today create a stronger tomorrow.","Healthy Living 🌱"),
("Consistency is more powerful than perfection.","Motivation 💚"),
("Eat well, move often, rest deeply.","Wellness 🌿"),
("Your health is one of your greatest investments.","Health ❤️"),
("Every workout is a vote for the person you want to become.","Fitness 💪"),
("Nourish your body with food that helps you thrive.","Nutrition 🥗"),
("Progress may be slow, but it is still progress.","Motivation 🔥"),
("A healthy family grows through healthy habits together.","Family Wellness 👨‍👩‍👧‍👦"),
("You do not need to be perfect. Just keep moving forward.","Mindset ✨"),
("Balanced meals support balanced days.","Nutrition 🍽️"),
("Movement is a daily gift to your future self.","Fitness 🚶"),
("Good nutrition is built one practical meal at a time.","Nutrition 🌾"),
("Strong routines are made from small repeatable actions.","Habits 🌱"),
("Rest is part of progress, not a break from it.","Recovery 😴"),
("A little preparation can make healthy choices much easier.","Meal Planning 🥣"),
("Your pantry can be the starting point for smarter meals.","Smart Cooking 🧺"),
("Family wellness grows when healthy choices feel doable.","Family Wellness 💚"),
("Hydrate, nourish, move, recover, repeat.","Wellness 💧"),
("Healthy progress is measured over weeks, not moments.","Progress 📈"),
("A nourishing plate can be simple, colorful and satisfying.","Nutrition 🥦"),
("Plan for the life you actually live, not a perfect one.","Sustainable Health 🌿"),
("The best routine is one your family can keep.","Family Habits 🏡"),
("Small improvements repeated consistently create big change.","Motivation ✨"),
("Food is fuel, culture, comfort and connection.","Family Nutrition ❤️"),
("Fitness does not need to be complicated to be effective.","Fitness 💪"),
("Use your goals as direction, not pressure.","Mindset 🧭"),
("Prepare what you can today to make tomorrow easier.","Planning 🗓️"),
("Celebrate the habits that move you forward.","Progress 🎉"),
("Healthy living works best when it fits your family.","Family Health 🌼"),
]


def show_quote():
    text,cat=random.choice(QUOTES)
    st.markdown(f"""
    <div class="quote-card"><div class="quote">“{text}”</div><div class="quote-category">{cat}</div></div>
    """,unsafe_allow_html=True)

# ============================================================
# PANTRY CHECKBOX CATEGORIES
# ============================================================
PANTRY_CATEGORIES={
"🥩 Proteins":["Chicken","Beef","Mutton","Fish","Eggs","Lentils","Chickpeas","Beans","Tofu"],
"🌾 Grains & Staples":["Rice","Brown Rice","Flour","Whole Wheat Flour","Oats","Bread","Pasta","Noodles"],
"🥬 Vegetables":["Tomato","Onion","Potato","Spinach","Carrot","Cucumber","Capsicum","Cauliflower","Peas","Garlic","Ginger"],
"🍎 Fruits":["Apple","Banana","Orange","Mango","Guava","Dates","Lemon"],
"🥛 Dairy":["Milk","Yogurt","Cheese","Paneer","Butter"],
"🌿 Herbs & Spices":["Coriander","Mint","Cumin","Turmeric","Chilli","Black Pepper","Garam Masala"],
"🫙 Oils & Sauces":["Cooking Oil","Olive Oil","Soy Sauce","Tomato Sauce","Chilli Sauce"],
}

# ============================================================
# DASHBOARD
# ============================================================
def dashboard():
    st.markdown("""
    <div class="hero">
      <span class="hero-badge">SMART FAMILY WELLNESS</span>
      <div class="hero-title">Welcome to NutriNest 🥗</div>
      <div class="hero-subtitle">Your family's nutrition, meal planning, pantry, fitness and progress companion — beautifully organized in one place.</div>
    </div>
    """,unsafe_allow_html=True)

    st.markdown("""
    <div class="slideshow">
      <div class="slide"><h2>🥗 Personalized Nutrition</h2><p>Understand calories, protein, carbohydrates, fats and personal nutrition targets.</p></div>
      <div class="slide"><h2>🍛 Smart Family Meal Planning</h2><p>Create practical shared meals while keeping individual portions and nutrition targets in mind.</p></div>
      <div class="slide"><h2>🧺 Cook From Your Pantry</h2><p>Select what you already have and discover recipes you can make now with pantry-match scoring.</p></div>
      <div class="slide"><h2>💪 Fitness Made Simple</h2><p>Build a 7-day routine, mark completed workouts and follow your progress.</p></div>
      <div class="slide"><h2>📈 Track Your Progress</h2><p>See weight, BMI, nutrition, meal-adherence and workout trends in one clear dashboard.</p></div>
    </div>
    """,unsafe_allow_html=True)
    show_quote()

    total_cal=sum(m["nutrition"]["Target"] for m in st.session_state.family)
    period=st.session_state.budget_period; amount=st.session_state.budget_amount
    daily=amount if period=="Daily" else amount/7 if period=="Weekly" else amount/30
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Family Members",len(st.session_state.family))
    c2.metric("Daily Calories",f"{total_cal:,}")
    c3.metric("Pantry Items",len(st.session_state.pantry))
    c4.metric("Daily Budget",f"Rs {daily:,.0f}")

    st.markdown('<div class="section-title">Your NutriNest modules 💚</div>',unsafe_allow_html=True)
    modules=[
      ("👨‍👩‍👧‍👦","Family Profiles","Members, goals, allergies and nutrition targets.","Family Profiles"),
      ("🍽️","Meal Planner","Shared 7-day family meals with portions.","Meal Planner"),
      ("🧺","Smart Pantry","Checkbox pantry and cook-now recommendations.","Smart Pantry"),
      ("🍛","Recipe Explorer","Search, filter, nutrition and pantry matching.","Recipe Explorer"),
      ("💰","Budget & Shopping","Daily/weekly/monthly household budget and allocations.","Budget & Shopping"),
      ("💪","Workout Planner","Goal-based 7-day fitness schedule and completion.","Workout Planner"),
      ("📊","Progress Tracker","Weight, BMI, calories, protein and workout trends.","Progress"),
      ("❤️","Favorites","Save and revisit your favorite recipes.","Favorites"),
    ]
    for start in range(0,len(modules),4):
        cols=st.columns(4)
        for col,(icon,title,desc,page) in zip(cols,modules[start:start+4]):
            with col:
                st.markdown(f"""
                <div class="feature-card"><div class="feature-icon">{icon}</div><div class="feature-title">{title}</div><div class="feature-description">{desc}</div></div>
                """,unsafe_allow_html=True)
                if st.button(f"Open {title} →",key=f"dash_{title}",use_container_width=True): go(page)

    # Quick actions
    st.markdown('<div class="section-title">Quick actions ⚡</div>',unsafe_allow_html=True)
    q=st.columns(4)
    actions=[("➕ Add Family Member","Family Profiles"),("🍽️ Create Meal Plan","Meal Planner"),("🧺 Update Pantry","Smart Pantry"),("📝 Log Progress","Progress")]
    for col,(label,page) in zip(q,actions):
        with col:
            if st.button(label,key=f"quick_{page}",use_container_width=True): go(page)

    # Dynamic graphs
    budget_amount=float(st.session_state.budget_amount)
    budget_spent=float(st.session_state.budget_spent)
    if budget_amount>0:
        st.markdown('<div class="section-title">Budget snapshot 💰</div>',unsafe_allow_html=True)
        used=min(budget_spent,budget_amount)
        remaining=max(0.0,budget_amount-budget_spent)
        bdf=pd.DataFrame({"Status":["Used","Remaining"],"PKR":[used,remaining]})
        fig=px.pie(bdf,names="Status",values="PKR",hole=.62,title=f"{st.session_state.budget_period} Budget")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig,use_container_width=True)

    if st.session_state.family:
        st.markdown('<div class="section-title">Family nutrition overview 📊</div>',unsafe_allow_html=True)
        rows=[]
        for m in st.session_state.family:
            n=m["nutrition"]; rows.append({"Member":m["name"],"Calories":n["Target"],"Protein":n["Protein"],"Carbs":n["Carbs"],"Fat":n["Fat"]})
        ndf=pd.DataFrame(rows)
        a,b=st.columns(2)
        with a:
            fig=px.bar(ndf,x="Member",y=["Protein","Carbs","Fat"],barmode="group",title="Daily Macronutrient Targets")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig,use_container_width=True)
        with b:
            fig=px.bar(ndf,x="Member",y="Calories",title="Daily Calorie Targets")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig,use_container_width=True)

    if st.session_state.workout_done:
        done_count=sum(1 for v in st.session_state.workout_done.values() if v)
        total_count=len(st.session_state.workout_done)
        st.markdown('<div class="section-title">Workout completion 💪</div>',unsafe_allow_html=True)
        st.progress(done_count/max(1,total_count),text=f"Completed {done_count} of {total_count} planned workout days")

    if st.session_state.logs:
        logs=pd.DataFrame(st.session_state.logs)
        st.markdown('<div class="section-title">Activity & progress overview 📈</div>',unsafe_allow_html=True)
        a,b=st.columns(2)
        with a:
            health=logs[logs["type"]=="health"].copy()
            if not health.empty:
                health["date"]=pd.to_datetime(health["date"])
                health=health.sort_values("date")
                latest=health.groupby("member",as_index=False).tail(1).copy()
                targets={m["name"]:m["nutrition"]["Target"] for m in st.session_state.family}
                latest["target"]=latest["member"].map(targets).fillna(0)
                melted=latest.melt(id_vars="member",value_vars=["calories","target"],var_name="Metric",value_name="kcal")
                fig=px.bar(melted,x="member",y="kcal",color="Metric",barmode="group",title="Daily Calories vs Target")
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.info("Calories-vs-target graph will appear after a health log.")
        with b:
            health=logs[logs["type"]=="health"].copy()
            if not health.empty:
                health["date"]=pd.to_datetime(health["date"])
                fig=px.line(health.sort_values("date"),x="date",y="weight",color="member",markers=True,title="Weight Trend")
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.info("Weight/BMI trend will appear after health logs.")

        a,b=st.columns(2)
        with a:
            w=logs[logs["type"]=="workout"]
            if not w.empty:
                g=w.groupby("member",as_index=False)["minutes"].sum()
                fig=px.bar(g,x="member",y="minutes",title="Workout Minutes")
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.info("Workout graph will appear after logging workouts.")
        with b:
            m=logs[logs["type"]=="meal"]
            if not m.empty:
                meal_names=m.get("item",pd.Series(dtype=str)).fillna("Meal").astype(str)
                g=meal_names.value_counts().reset_index()
                g.columns=["Meal","Count"]
                fig=px.pie(g,names="Meal",values="Count",hole=.55,title="Meal-Type Distribution")
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.info("Meal distribution will appear after logging meals.")

# ============================================================
# IN-APP PAGE NAVIGATION
# ============================================================
def page_nav():
    page = st.session_state.get("page", "Dashboard")
    if page == "Dashboard":
        return
    st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)
    left, middle, right = st.columns([1, 1.2, 4.8])
    with left:
        if st.button("← Back", key=f"back_{page}", use_container_width=True):
            go_back()
    with middle:
        if st.button("⌂ Dashboard", key=f"home_{page}", use_container_width=True):
            go_dashboard()
    with right:
        trail = ["Dashboard"] + st.session_state.get("nav_history", []) + [page]
        # Show only the last few labels so the navigation never becomes crowded.
        trail = trail[-4:]
        st.caption("  ›  ".join(trail))


# ============================================================
# FAMILY
# ============================================================
def family_page():
    page_nav()
    st.markdown('<div class="page-header"><h1>👨‍👩‍👧‍👦 Family Profiles</h1><p>Personalize nutrition, allergies, goals, portions and workouts for each member.</p></div>',unsafe_allow_html=True)
    with st.form("family_form",clear_on_submit=True):
        a,b=st.columns(2)
        with a:
            name=st.text_input("Name",placeholder="Father")
            age=st.number_input("Age",10,100,35)
            sex=st.selectbox("Sex",["Male","Female"])
            height=st.number_input("Height (cm)",120,230,170)
            weight=st.number_input("Weight (kg)",25.0,250.0,70.0,step=.5)
        with b:
            goal=st.selectbox("Goal",["Weight Loss","Maintenance","Weight Gain"])
            activity=st.selectbox("Activity Level",["Sedentary","Light","Moderate","Active","Very Active"],index=2)
            allergies=st.multiselect("Food Allergies",["None","Nuts","Dairy","Gluten","Egg","Seafood"],default=["None"])
            conditions=st.multiselect("Health Considerations",["None","Diabetes","Hypertension","Thyroid","PCOS"],default=["None"])
            location=st.selectbox("Workout Location",["Home","Gym"])
            equipment=st.multiselect("Available Equipment",["None","Yoga Mat","Dumbbells","Resistance Bands","Bench","Full Gym"],default=["Yoga Mat"])
        save=st.form_submit_button("Save Family Member",use_container_width=True)
    if save:
        if not name.strip(): st.error("Please enter a name.")
        else:
            member={"name":name.strip(),"age":int(age),"sex":sex,"height_cm":float(height),"weight_kg":float(weight),"goal":goal,"activity_level":activity,"allergies":allergies,"medical":conditions,"workout_location":location,"equipment":equipment,"nutrition":nutrition(age,sex,height,weight,activity,goal)}
            st.session_state.family=[m for m in st.session_state.family if m["name"].casefold()!=member["name"].casefold()]
            st.session_state.family.append(member); st.success(f"{member['name']} saved successfully."); st.rerun()
    if st.session_state.family:
        st.markdown('<div class="section-title">Family overview</div>',unsafe_allow_html=True)
        cols=st.columns(min(3,len(st.session_state.family)))
        for i,m in enumerate(st.session_state.family):
            n=m["nutrition"]
            with cols[i%len(cols)]:
                st.markdown(f"""
                <div class="member-card"><span class="pill">{m['goal']}</span><h3>👤 {m['name']}</h3><p>BMI {n['BMI']} · {m['activity_level']}</p><div style="font-size:1.65rem;font-weight:900;color:#587864">{n['Target']} kcal/day</div><span class="macro-chip">Protein {n['Protein']}g</span><span class="macro-chip">Carbs {n['Carbs']}g</span><span class="macro-chip">Fat {n['Fat']}g</span><span class="macro-chip">Fiber {n['Fiber']}g</span></div>
                """,unsafe_allow_html=True)
                if st.button(f"Remove {m['name']}",key=f"rm_{i}",use_container_width=True):
                    st.session_state.family.pop(i); st.rerun()

# ============================================================
# PANTRY
# ============================================================
def pantry_page():
    page_nav()
    st.markdown('<div class="page-header"><h1>🧺 Smart Pantry</h1><p>Select what you already have. NutriNest will prioritize recipes with the highest pantry match.</p></div>',unsafe_allow_html=True)
    selected=[]
    for category,items in PANTRY_CATEGORIES.items():
        with st.expander(category,expanded=True):
            cols=st.columns(4)
            for i,item in enumerate(items):
                with cols[i%4]:
                    if st.checkbox(item,value=item in st.session_state.pantry,key=f"chk_{category}_{item}"):
                        selected.append(item)
    st.session_state.pantry=selected
    if selected: st.success("Pantry: " + " · ".join(selected))
    else: st.info("Select ingredients above to build your pantry.")
    if recipes_df.empty or not selected: return
    st.markdown('<div class="section-title">✨ What can I cook now?</div>',unsafe_allow_html=True)
    safe=recipes_df[recipes_df.apply(safe_for_family,axis=1)].copy()
    results=[]
    for _,row in safe.iterrows():
        pct,matched,missing=pantry_match(row); results.append((pct,matched,missing,row))
    results.sort(key=lambda x:x[0],reverse=True)
    for i,(pct,matched,missing,row) in enumerate(results[:20]):
        st.markdown(f"<div class='recipe-card'><h3>🍛 {row['recipe_name']}</h3><span class='pill'>🟢 {pct}% pantry match</span><span class='pill'>🔥 {float(row['calories']):.0f} kcal</span><span class='pill'>💪 {float(row['protein_g']):.0f}g protein</span></div>",unsafe_allow_html=True)
        a,b=st.columns(2)
        with a: st.write("**Available:** " + (", ".join(matched[:12]) if matched else "None"))
        with b:
            st.write("**Missing:** " + (", ".join(missing[:12]) if missing else "Nothing 🎉"))
            if missing and st.button("🛒 Add missing",key=f"addmiss_{i}"):
                for x in missing:
                    if x not in st.session_state.shopping_list: st.session_state.shopping_list.append(x)
                st.success("Missing ingredients added to shopping list.")

# ============================================================
# RECIPES
# ============================================================
def recipes_page():
    page_nav()
    st.markdown('<div class="page-header"><h1>🍛 Recipe Explorer</h1><p>Search by recipe, meal type, cuisine, nutrition and pantry availability.</p></div>',unsafe_allow_html=True)
    if recipes_df.empty:
        st.error("Recipe dataset not found. Put it at data/nutrinest_recipes_clean.csv or data/recipes.csv.")
        return
    a,b,c=st.columns(3)
    with a: search=st.text_input("🔎 Search",placeholder="Chicken, rice, chana...")
    with b:
        meal_options=["All"]+sorted(recipes_df["meal_type"].astype(str).dropna().unique().tolist())
        meal=st.selectbox("Meal Type",meal_options)
    with c:
        cuisine_options=["All"]+sorted(recipes_df["cuisine"].astype(str).dropna().unique().tolist())
        cuisine=st.selectbox("Cuisine",cuisine_options)
    a,b,c,d=st.columns(4)
    with a: max_cal=st.slider("Max calories",100,1500,800,25)
    with b: min_protein=st.slider("Min protein (g)",0,100,0)
    with c: filters=st.multiselect("Nutrition tags",["High Protein","High Fiber","Vegetarian","Budget Friendly"])
    with d: pantry_first=st.checkbox("Prioritize pantry match",value=True)
    data=recipes_df[recipes_df.apply(safe_for_family,axis=1)].copy()
    if search.strip():
        hay=(data["recipe_name"].fillna("").astype(str)+" "+data["ingredients"].fillna("").astype(str)+" "+data["tags"].fillna("").astype(str)).str.lower()
        data=data[hay.str.contains(re.escape(search.lower()),na=False)]
    if meal!="All": data=data[data["meal_type"].astype(str).str.casefold().str.contains(meal.casefold(),na=False)]
    if cuisine!="All": data=data[data["cuisine"].astype(str).str.casefold()==cuisine.casefold()]
    data=data[data["calories"]<=max_cal]; data=data[data["protein_g"]>=min_protein]
    if filters:
        tagtext=data["tags"].fillna("").astype(str).str.lower()+" "+data["ingredients"].fillna("").astype(str).str.lower()
        if "High Protein" in filters: data=data[data["protein_g"]>=25]
        if "High Fiber" in filters: data=data[data["fiber_g"]>=6]
        if "Vegetarian" in filters: data=data[~tagtext.str.contains("chicken|beef|mutton|fish|prawn|shrimp|meat",na=False)]
        if "Budget Friendly" in filters: data=data[data["calories"]<=600]
    if pantry_first and st.session_state.pantry:
        data["pantry_match"]=data.apply(lambda r:pantry_match(r)[0],axis=1); data=data.sort_values("pantry_match",ascending=False)
    st.caption(f"{len(data)} recipes found")
    for i,(_,row) in enumerate(data.head(50).iterrows()):
        name=str(row["recipe_name"]); pct=pantry_match(row)[0] if st.session_state.pantry else None
        with st.expander(f"{'❤️' if name in st.session_state.favorites else '🍽️'} {name}"):
            a,b,c,d=st.columns(4); a.metric("Calories",f"{row['calories']:.0f}"); b.metric("Protein",f"{row['protein_g']:.0f}g"); c.metric("Carbs",f"{row['carbs_g']:.0f}g"); d.metric("Fat",f"{row['fat_g']:.0f}g")
            st.write(f"**Cuisine:** {row['cuisine']} · **Meal:** {row['meal_type']}")
            if pct is not None: st.progress(pct/100,text=f"Pantry Match: {pct}%")
            ing=parse_listish(row["ingredients"])
            if ing: st.write("**Ingredients:** " + " · ".join(ing))
            if str(row.get("steps","")).strip(): st.write("**Method:** " + str(row["steps"]))
            if name not in st.session_state.favorites:
                if st.button("⭐ Add Favorite",key=f"fav_{i}"): st.session_state.favorites.append(name); st.rerun()
            else:
                if st.button("☆ Remove Favorite",key=f"unfav_{i}"): st.session_state.favorites.remove(name); st.rerun()

# ============================================================
# BUDGET
# ============================================================
def budget_page():
    page_nav()
    st.markdown('<div class="page-header"><h1>💰 Budget & Shopping</h1><p>Manage daily, weekly or monthly household spending, optional member allocations and your shopping list.</p></div>',unsafe_allow_html=True)

    period=st.selectbox(
        "Budget Period",
        ["Daily","Weekly","Monthly"],
        index=["Daily","Weekly","Monthly"].index(st.session_state.budget_period),
    )
    st.session_state.budget_period=period

    mode=st.radio(
        "How do you want to set the budget?",
        ["Household Total","Individual Allocations"],
        horizontal=True,
        index=0 if st.session_state.budget_entry_mode=="Household Total" else 1,
    )
    st.session_state.budget_entry_mode=mode

    if mode=="Household Total" or not st.session_state.family:
        amount=st.number_input(
            f"Household {period.lower()} budget (PKR)",
            min_value=0.0,
            max_value=10000000.0,
            value=float(st.session_state.budget_amount),
            step=500.0,
        )
        st.session_state.budget_amount=float(amount)
        if st.session_state.family:
            st.caption("Optional: switch to Individual Allocations if you want member-wise amounts to calculate the household total automatically.")
    else:
        st.markdown('<div class="section-title">Individual allocations</div>',unsafe_allow_html=True)
        total=0.0
        for m in st.session_state.family:
            current=float(st.session_state.allocations.get(m["name"],0.0))
            value=st.number_input(
                f"{m['name']} — {period.lower()} allocation (PKR)",
                min_value=0.0,
                max_value=10000000.0,
                value=current,
                step=500.0,
                key=f"alloc_{period}_{m['name']}",
            )
            st.session_state.allocations[m["name"]]=float(value)
            total+=float(value)
        st.session_state.budget_amount=total
        amount=total
        st.success(f"Household {period.lower()} total calculated automatically: Rs {amount:,.0f}")

    daily=amount if period=="Daily" else amount/7 if period=="Weekly" else amount/30
    weekly=daily*7
    monthly=daily*30
    a,b,c=st.columns(3)
    a.metric("Daily",f"Rs {daily:,.0f}")
    b.metric("Weekly",f"Rs {weekly:,.0f}")
    c.metric("Monthly",f"Rs {monthly:,.0f}")

    st.markdown('<div class="section-title">Household spending</div>',unsafe_allow_html=True)
    spent=st.number_input(
        f"Amount spent in this {period.lower()} period (PKR)",
        min_value=0.0,
        max_value=10000000.0,
        value=float(max(0,st.session_state.budget_spent)),
        step=500.0,
    )
    st.session_state.budget_spent=float(spent)
    remaining=max(0.0,amount-spent)
    ratio=0.0 if amount<=0 else min(1.0,spent/amount)
    st.progress(ratio,text=f"Used Rs {spent:,.0f} · Remaining Rs {remaining:,.0f}")
    if amount>0 and spent>amount:
        st.warning(f"You are Rs {spent-amount:,.0f} over this {period.lower()} budget.")

    st.markdown('<div class="section-title">🛒 Shopping list</div>',unsafe_allow_html=True)
    a,b=st.columns([5,1])
    with a:
        item=st.text_input("Add shopping item",placeholder="Tomatoes, chicken, oats...")
    with b:
        st.write("")
        add=st.button("Add",use_container_width=True)
    if add and item.strip():
        clean=item.strip()
        if clean.casefold() not in [x.casefold() for x in st.session_state.shopping_list]:
            st.session_state.shopping_list.append(clean)
        st.rerun()

    if st.session_state.shopping_list:
        for i,x in enumerate(st.session_state.shopping_list):
            a,b=st.columns([8,1])
            a.markdown(f"<div class='soft-card'>🛒 <b>{x}</b></div>",unsafe_allow_html=True)
            if b.button("×",key=f"shoprm_{i}"):
                st.session_state.shopping_list.pop(i)
                st.rerun()
        if st.button("Clear Shopping List"):
            st.session_state.shopping_list=[]
            st.rerun()
    else:
        st.info("Shopping list is empty.")

# ============================================================
# MEAL PLANNER
# ============================================================
def generate_ai_meal_plan(cuisines,preferences):
    if not client:
        raise RuntimeError("Groq AI is not connected. Add GROQ_API_KEY in Streamlit → Settings → Secrets.")
    family=[{"name":m["name"],"goal":m["goal"],"target":m["nutrition"]["Target"],"protein":m["nutrition"]["Protein"],"allergies":m["allergies"]} for m in st.session_state.family]
    pool=[]
    if not recipes_df.empty:
        safe=recipes_df[recipes_df.apply(safe_for_family,axis=1)]
        for _,r in safe.head(60).iterrows(): pool.append({"name":r["recipe_name"],"meal_type":r["meal_type"],"calories":r["calories"],"protein":r["protein_g"],"ingredients":r["ingredients"]})
    prompt=f"""
Create a realistic 7-day shared family meal plan.
Family: {json.dumps(family)}
Cuisines: {json.dumps(cuisines)}
Preferences: {json.dumps(preferences)}
Pantry: {json.dumps(st.session_state.pantry)}
Budget: PKR {st.session_state.budget_amount} per {st.session_state.budget_period.lower()}
Recipes: {json.dumps(pool)}
Rules: respect allergies; prefer pantry ingredients; use one shared dish per meal with individual portions; include Breakfast, Lunch, Snack and Dinner every day; do not provide medical treatment advice.
Return ONLY JSON: {{"days":[{{"day":1,"meals":[{{"meal":"Breakfast","main":"Recipe","calories":400,"protein":20,"carbs":40,"fat":15,"portions":{{"Member":"1 serving"}},"description":"short","ingredients":["ingredient 1","ingredient 2"]}}]}}]}}
"""
    try:
        r=client.chat.completions.create(model=AI_MODEL,messages=[{"role":"system","content":"Return valid JSON only."},{"role":"user","content":prompt}],temperature=.25,max_tokens=6000)
        obj=extract_json(r.choices[0].message.content)
        if isinstance(obj,dict) and isinstance(obj.get("days"),list) and len(obj["days"])>=7:
            return obj["days"][:7]
        raise RuntimeError("Groq returned an invalid meal-plan response. Please try again.")
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"Groq meal-plan generation failed: {e}")


def meal_page():
    page_nav()
    st.markdown('<div class="page-header"><h1>🍽️ Smart Family Meal Planner</h1><p>Plan shared meals around goals, allergies, pantry ingredients, cuisine, preferences and budget.</p></div>',unsafe_allow_html=True)
    if not st.session_state.family:
        st.warning("Add at least one family member first."); return
    a,b=st.columns(2)
    with a: cuisines=st.multiselect("Preferred cuisines",["Desi / Pakistani","Indian","Chinese","Italian","Continental","Mixed"],["Desi / Pakistani"])
    with b: preferences=st.multiselect("Preferences",["High Protein","High Fiber","Less Oil","Budget Friendly","Quick Meals","Vegetarian","Pantry First"],["High Protein","Less Oil"])
    if st.session_state.pantry: st.success(f"🧺 Pantry-aware planning: {len(st.session_state.pantry)} ingredients selected.")
    if st.button("✨ Generate 7-Day Family Meal Plan",type="primary",use_container_width=True):
        with st.spinner("Creating your family plan with Groq AI..."):
            try:
                st.session_state.meal_plan=generate_ai_meal_plan(cuisines,preferences)
                st.success("7-day AI meal plan generated 🎉")
            except Exception as e:
                st.session_state.meal_plan=[]
                st.error(str(e))
    plan=st.session_state.meal_plan
    if not plan: return
    st.success("7-day meal plan ready 🎉")
    for day in plan:
        with st.expander(f"Day {day.get('day','')} ",expanded=day.get('day')==1):
            for meal in day.get("meals",[]):
                st.markdown(f"<div class='plate-card'><span class='pill'>{meal.get('meal','Meal')}</span><h3>{meal.get('main','Meal')}</h3><p>{meal.get('description','')}</p></div>",unsafe_allow_html=True)
                a,b,c,d=st.columns(4); a.metric("Calories",f"{meal.get('calories','—')} kcal"); b.metric("Protein",f"{meal.get('protein','—')} g"); c.metric("Carbs",f"{meal.get('carbs','—')} g"); d.metric("Fat",f"{meal.get('fat','—')} g")
                portions=meal.get("portions",{})
                ingredients=parse_listish(meal.get("ingredients",[]))
                if ingredients:
                    st.caption("Ingredients: " + " · ".join(ingredients))
                if portions:
                    cols=st.columns(min(4,len(portions)))
                    for i,(person,portion) in enumerate(portions.items()):
                        cols[i%len(cols)].info(f"**{person}**\n\n{portion}")

    plan_ingredients=[]
    for day in plan:
        for meal in day.get("meals",[]):
            plan_ingredients.extend(parse_listish(meal.get("ingredients",[])))
    pantry_norm=[norm(x) for x in st.session_state.pantry]
    missing=[]
    for ingredient in plan_ingredients:
        ni=norm(ingredient)
        if ni and not any(pi in ni or ni in pi for pi in pantry_norm if pi):
            if ingredient.casefold() not in [x.casefold() for x in missing]:
                missing.append(ingredient)
    if missing:
        st.markdown('<div class="section-title">🛒 Meal-plan shopping support</div>',unsafe_allow_html=True)
        st.write("Missing from pantry: " + " · ".join(missing[:40]))
        if st.button("Add meal-plan missing ingredients to Shopping List",use_container_width=True):
            existing=[x.casefold() for x in st.session_state.shopping_list]
            for ingredient in missing:
                if ingredient.casefold() not in existing:
                    st.session_state.shopping_list.append(ingredient)
                    existing.append(ingredient.casefold())
            st.success("Missing meal-plan ingredients added to the shopping list.")

# ============================================================
# WORKOUT
# ============================================================
def generate_ai_workout(member):
    if not client:
        raise RuntimeError("Groq AI is not connected. Add GROQ_API_KEY in Streamlit → Settings → Secrets.")
    prompt=f"Create a safe general 7-day workout plan for {member['name']}. Goal={member['goal']}, activity={member['activity_level']}, location={member['workout_location']}, equipment={member['equipment']}. Include rest/recovery. Return ONLY JSON with member and week list, each day having day, focus and exercises with name plus sets/reps or duration. Do not give medical treatment advice."
    try:
        r=client.chat.completions.create(model=AI_MODEL,messages=[{"role":"system","content":"Return valid JSON only."},{"role":"user","content":prompt}],temperature=.3,max_tokens=3000)
        obj=extract_json(r.choices[0].message.content)
        if isinstance(obj,dict) and isinstance(obj.get("week"),list) and len(obj["week"])>=7:
            return obj
        raise RuntimeError("Groq returned an invalid workout response. Please try again.")
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"Groq workout generation failed: {e}")


def workout_page():
    page_nav()
    st.markdown('<div class="page-header"><h1>💪 Workout Planner</h1><p>Personalized 7-day routines based on goals, activity, location and equipment.</p></div>',unsafe_allow_html=True)
    if not st.session_state.family: st.warning("Add a family member first."); return
    selected=st.selectbox("Select Member",[m["name"] for m in st.session_state.family])
    member=next(m for m in st.session_state.family if m["name"]==selected)
    st.markdown(f"<div class='soft-card'><span class='pill'>{member['goal']}</span><span class='pill'>{member['workout_location']}</span><p><b>Equipment:</b> {', '.join(member['equipment'])}</p></div>",unsafe_allow_html=True)
    if st.button("🏃 Generate 7-Day Workout",type="primary",use_container_width=True):
        with st.spinner("Creating your workout with Groq AI..."):
            try:
                st.session_state.workouts[selected]=generate_ai_workout(member)
                st.success("7-day AI workout generated 🎉")
            except Exception as e:
                st.session_state.workouts.pop(selected,None)
                st.error(str(e))
    plan=st.session_state.workouts.get(selected)
    if not plan:return
    completed=0
    for day in plan.get("week",[]):
        d=day.get("day"); key=f"done_{selected}_{d}"
        with st.expander(f"Day {d} · {day.get('focus','Workout')}",expanded=d==1):
            exs=day.get("exercises",[])
            if not exs: st.write("🌙 Rest / recovery day")
            for ex in exs:
                if ex.get("duration"): st.write(f"• **{ex.get('name','Exercise')}** — {ex['duration']}")
                else: st.write(f"• **{ex.get('name','Exercise')}** — {ex.get('sets','')} × {ex.get('reps','')}")
            done_key=f"{selected}|{d}"
            current=bool(st.session_state.workout_done.get(done_key,False))
            done=st.checkbox("Mark day complete",value=current,key=key)
            st.session_state.workout_done[done_key]=done
            if done: completed+=1
    st.progress(completed/7,text=f"Weekly completion: {completed}/7 days")

# ============================================================
# PROGRESS
# ============================================================
def progress_page():
    page_nav()
    st.markdown('<div class="page-header"><h1>📊 Progress Tracker</h1><p>Track weight, BMI, calories, protein, meals and workout completion.</p></div>',unsafe_allow_html=True)
    if not st.session_state.family: st.warning("Add a family member first."); return
    selected=st.selectbox("Select Member",[m["name"] for m in st.session_state.family])
    member=next(m for m in st.session_state.family if m["name"]==selected)
    a,b=st.columns(2)
    with a:
        st.markdown("### ⚖️ Daily health log")
        with st.form("health_log"):
            w=st.number_input("Weight (kg)",25.0,250.0,float(member["weight_kg"]),.1)
            cal=st.number_input("Calories consumed",0,10000,0,50)
            pro=st.number_input("Protein consumed (g)",0,500,0,5)
            save=st.form_submit_button("Save health log",use_container_width=True)
        if save:
            bmi=w/((member["height_cm"]/100)**2)
            st.session_state.logs.append({"date":str(date.today()),"member":selected,"type":"health","weight":w,"bmi":round(bmi,1),"calories":cal,"protein":pro,"status":"logged","minutes":0})
            st.success("Health progress saved.")
    with b:
        st.markdown("### 🏃 Workout log")
        with st.form("workout_log"):
            status=st.selectbox("Status",["completed","skipped","rest"])
            minutes=st.number_input("Minutes",0,300,30,5)
            savew=st.form_submit_button("Save workout",use_container_width=True)
        if savew:
            st.session_state.logs.append({"date":str(date.today()),"member":selected,"type":"workout","status":status,"minutes":int(minutes) if status=="completed" else 0,"weight":None,"bmi":None,"calories":None,"protein":None})
            st.success("Workout saved.")
    st.markdown("### 🍽 Meal log")
    with st.form("meal_log"):
        meal=st.text_input("Meal name", "Breakfast")
        status=st.selectbox("Meal status",["followed","different","skipped"])
        savem=st.form_submit_button("Log meal",use_container_width=True)
    if savem:
        st.session_state.logs.append({"date":str(date.today()),"member":selected,"type":"meal","item":meal,"status":status,"minutes":0,"weight":None,"bmi":None,"calories":None,"protein":None}); st.success("Meal logged.")
    rows=[x for x in st.session_state.logs if x.get("member")==selected]
    if not rows: st.info("Add progress entries to unlock graphs."); return
    df=pd.DataFrame(rows); df["date"]=pd.to_datetime(df["date"]); df=df.sort_values("date")
    health=df[df["type"]=="health"]
    workouts=df[df["type"]=="workout"]
    meals=df[df["type"]=="meal"]
    if not health.empty:
        latest=health.iloc[-1]
        change=float(latest["weight"])-float(health.iloc[0]["weight"])
        a,b,c,d=st.columns(4); a.metric("Current Weight",f"{latest['weight']:.1f} kg"); b.metric("BMI",f"{latest['bmi']:.1f}"); c.metric("Weight Change",f"{change:+.1f} kg"); d.metric("Calories",f"{latest['calories']:,.0f}")
        a,b=st.columns(2)
        with a:
            fig=px.line(health,x="date",y="weight",markers=True,title="Weight Trend"); st.plotly_chart(fig,use_container_width=True)
        with b:
            fig=px.line(health,x="date",y="bmi",markers=True,title="BMI Trend"); st.plotly_chart(fig,use_container_width=True)
        a,b=st.columns(2)
        with a:
            fig=px.bar(health,x="date",y="calories",title="Calories vs Target"); fig.add_hline(y=member["nutrition"]["Target"],line_dash="dash",annotation_text="Target"); st.plotly_chart(fig,use_container_width=True)
        with b:
            fig=px.line(health,x="date",y="protein",markers=True,title="Protein vs Target"); fig.add_hline(y=member["nutrition"]["Protein"],line_dash="dash",annotation_text="Target"); st.plotly_chart(fig,use_container_width=True)
    a,b=st.columns(2)
    with a:
        if not workouts.empty:
            g=workouts.groupby("date",as_index=False)["minutes"].sum(); fig=px.bar(g,x="date",y="minutes",title="Workout Minutes"); st.plotly_chart(fig,use_container_width=True)
    with b:
        if not meals.empty:
            followed=int((meals["status"]=="followed").sum()); total=len(meals); st.metric("Meal adherence",f"{followed}/{total}",f"{(100*followed/max(1,total)):.0f}%")
    st.markdown("### 📅 Weekly / monthly summary")
    today=pd.Timestamp(date.today()); week= df[df["date"]>=today-pd.Timedelta(days=6)]; month=df[df["date"]>=today-pd.Timedelta(days=29)]
    a,b=st.columns(2); a.metric("Last 7 days logs",len(week)); b.metric("Last 30 days logs",len(month))
    st.dataframe(df,use_container_width=True,hide_index=True)
    st.download_button("Download progress CSV",df.to_csv(index=False).encode(),"nutrinest_progress.csv","text/csv")
    if st.button("Clear all progress logs for this member"):
        st.session_state.logs=[x for x in st.session_state.logs if x.get("member")!=selected]; st.rerun()

# ============================================================
# FAVORITES
# ============================================================
def favorites_page():
    page_nav()
    st.markdown('<div class="page-header"><h1>❤️ Favorites</h1><p>Your saved recipes in one place.</p></div>',unsafe_allow_html=True)
    if not st.session_state.favorites: st.info("No favorites yet. Save recipes from Recipe Explorer."); return
    if recipes_df.empty:return
    for i,name in enumerate(st.session_state.favorites):
        matches=recipes_df[recipes_df["recipe_name"].astype(str).str.casefold()==name.casefold()]
        if matches.empty: continue
        row=matches.iloc[0]
        with st.expander(f"❤️ {name}"):
            a,b,c,d=st.columns(4); a.metric("Calories",f"{row['calories']:.0f}"); b.metric("Protein",f"{row['protein_g']:.0f}g"); c.metric("Carbs",f"{row['carbs_g']:.0f}g"); d.metric("Fat",f"{row['fat_g']:.0f}g")
            st.write("**Ingredients:** " + ", ".join(parse_listish(row["ingredients"])))
            if st.button("Remove Favorite",key=f"favremove_{i}"): st.session_state.favorites.remove(name); st.rerun()

# ============================================================
# ROUTER + NAVIGATION
# ============================================================
page = st.session_state.get("page", "Dashboard")

with st.sidebar:
    st.markdown("## 🥗 NutriNest")
    st.caption("Family Nutrition & Wellness")
    st.divider()

    if page == "Dashboard":
        st.success("🏠 Dashboard active")
    else:
        if st.button("🏠 Dashboard", key="sidebar_dashboard", use_container_width=True):
            go_dashboard()
        if st.button("← Back to previous page", key="sidebar_back", use_container_width=True):
            go_back()

    st.divider()
    st.caption(f"Current page: {page}")
    st.caption("Use the cards on Dashboard and the Back / Dashboard buttons inside each module.")

    st.markdown("### System status")
    st.write("AI: " + ("🟢 Connected" if client else "🔴 Not connected"))
    st.write("Recipes: " + (f"🟢 Loaded ({len(recipes_df):,})" if not recipes_df.empty else "🔴 Dataset missing"))
    st.write(f"Family: {len(st.session_state.family)} member(s)")
    st.write(f"Pantry: {len(st.session_state.pantry)} item(s)")
    st.caption("Groq uses Streamlit Secrets. Keep secrets.toml out of GitHub.")

if page == "Dashboard":
    dashboard()
elif page == "Family Profiles":
    family_page()
elif page == "Smart Pantry":
    pantry_page()
elif page == "Recipe Explorer":
    recipes_page()
elif page == "Budget & Shopping":
    budget_page()
elif page == "Meal Planner":
    meal_page()
elif page == "Workout Planner":
    workout_page()
elif page == "Progress":
    progress_page()
elif page == "Favorites":
    favorites_page()
else:
    st.session_state.page = "Dashboard"
    st.session_state.nav_history = []
    st.rerun()

st.markdown("""
<div class="footer-note">🥗 <b>NutriNest</b> · Smart Family Nutrition & Wellness<br>Eat well · Move well · Live well 💚<br><br>NutriNest provides general wellness planning and is not a substitute for medical diagnosis or clinical treatment.</div>
""",unsafe_allow_html=True)
