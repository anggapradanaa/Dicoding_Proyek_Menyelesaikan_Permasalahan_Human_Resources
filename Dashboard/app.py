import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HR Attrition Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS Styling ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .main { background-color: #F8F9FC; }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1F36 0%, #2D3561 100%);
    }
    [data-testid="stSidebar"] * { color: #E8EAF6 !important; }
    [data-testid="stSidebar"] .stMarkdown h3 { 
        color: #7C83FD !important; 
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 1px solid rgba(124,131,253,0.3);
        padding-bottom: 6px;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 24px 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-left: 5px solid;
        transition: transform 0.2s;
        height: 140px;
    }
    .kpi-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.10); }
    .kpi-title { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; color: #8892A4; margin-bottom: 8px; }
    .kpi-value { font-size: 38px; font-weight: 800; line-height: 1.1; margin-bottom: 6px; }
    .kpi-delta { font-size: 12px; color: #8892A4; }
    .kpi-delta span { font-weight: 600; }
    
    /* Section headers */
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #1A1F36;
        margin: 8px 0 4px 0;
    }
    
    /* Chart containers */
    .chart-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    
    /* Page title */
    .page-title {
        font-size: 28px;
        font-weight: 800;
        color: #1A1F36;
        margin-bottom: 4px;
    }
    .page-subtitle {
        font-size: 14px;
        color: #8892A4;
        margin-bottom: 20px;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Selectbox styling */
    .stMultiSelect [data-baseweb="tag"] { background-color: #7C83FD !important; }
</style>
""", unsafe_allow_html=True)


# ── Data Loading & Caching ─────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    """Load and preprocess dataset from notebook logic"""
    df = pd.read_csv('data/employee_data.csv')
    
    # Drop rows where Attrition is missing
    df_clean = df.dropna(subset=['Attrition']).copy()
    df_clean['Attrition'] = df_clean['Attrition'].astype(int)
    
    return df_clean


@st.cache_resource(show_spinner=False)
def train_model(df):
    """Train XGBoost model identical to notebook Step 5"""
    drop_cols = ['EmployeeId', 'EmployeeCount', 'StandardHours', 'Over18']
    df_model = df.copy()
    df_model.drop(columns=[c for c in drop_cols if c in df_model.columns], inplace=True)
    
    # Encode categorical columns
    cat_cols = df_model.select_dtypes(include='object').columns.tolist()
    le = LabelEncoder()
    label_maps = {}
    for col in cat_cols:
        df_model[col] = le.fit_transform(df_model[col].astype(str))
        label_maps[col] = dict(zip(le.classes_, le.transform(le.classes_)))
    
    X = df_model.drop(columns=['Attrition'])
    y = df_model['Attrition']
    
    # Train-test split stratified
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # XGBoost
    neg = (y_train == 0).sum()
    pos = (y_train == 1).sum()
    scale_pos = neg / pos
    
    model = XGBClassifier(
        n_estimators=500,
        max_depth=3,
        learning_rate=0.01,
        subsample=0.7,
        colsample_bytree=0.6,
        min_child_weight=10,
        gamma=1,
        reg_alpha=0.5,
        reg_lambda=2.0,
        scale_pos_weight=scale_pos,
        random_state=42,
        eval_metric='auc',
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Feature importance DataFrame
    feat_imp = pd.DataFrame({
        'Feature': X_train.columns,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False).reset_index(drop=True)
    
    return model, feat_imp, X_train.columns.tolist()


# ── Load Data & Model ──────────────────────────────────────────────────────────
with st.spinner("Memuat data dan melatih model..."):
    try:
        df_raw = load_data()
        model, feat_imp, feature_names = train_model(df_raw)
        
        # Store in session state for access across pages
        st.session_state['df_raw'] = df_raw
        st.session_state['model'] = model
        st.session_state['feat_imp'] = feat_imp
        st.session_state['feature_names'] = feature_names
        st.session_state['data_loaded'] = True
        
    except FileNotFoundError:
        st.error("File `data/employee_data.csv` tidak ditemukan.")
        st.info("Pastikan file CSV ada di folder `data/` sebelum menjalankan dashboard.")
        st.stop()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 HR Attrition")
    st.caption("Analytics Dashboard")
    st.markdown("---")
    
    # ── Global Filters ─────────────────────────────────────────
    st.markdown("### 🔍 Global Filter")
    st.markdown(" ")
    
    all_departments = sorted(df_raw['Department'].dropna().unique().tolist())
    selected_dept = st.multiselect(
        "Department",
        options=all_departments,
        default=[],
        placeholder="Semua Department"
    )
    
    st.markdown(" ")
    all_genders = sorted(df_raw['Gender'].dropna().unique().tolist())
    selected_gender = st.multiselect(
        "Gender",
        options=all_genders,
        default=[],
        placeholder="Semua Gender"
    )
    
    st.markdown(" ")
    all_jobroles = sorted(df_raw['JobRole'].dropna().unique().tolist())
    selected_jobrole = st.multiselect(
        "Job Role",
        options=all_jobroles,
        default=[],
        placeholder="Semua Job Role"
    )
    
    st.markdown("---")
    
    # ── Metric Selector ────────────────────────────────────────
    st.markdown("### 📐 Metric Selector")
    st.markdown(" ")
    
    metric_mode = st.radio(
        "Tampilkan sebagai:",
        options=["Attrition Rate (%)", "Jumlah Resign"],
        index=0
    )
    
    st.markdown("---")
    
    # ── Info ───────────────────────────────────────────────────
    total_emp = len(df_raw)
    total_resign = int(df_raw['Attrition'].sum())
    rate = df_raw['Attrition'].mean() * 100
    
    st.markdown("### 📌 Info Dataset")
    st.markdown(" ")
    st.markdown(f"**Total Karyawan:** {total_emp:,}")
    st.markdown(f"**Total Resign:** {total_resign:,}")
    st.markdown(f"**Overall Rate:** {rate:.1f}%")
    st.markdown(f"**Model AUC:** 0.805")
    
    st.markdown("---")
    st.caption("HR Attrition Analytics Dashboard\nPowered by XGBoost")


# ── Apply Filters & Store ──────────────────────────────────────────────────────
def apply_filters(df, departments, genders, jobroles):
    filtered = df.copy()
    if departments:
        filtered = filtered[filtered['Department'].isin(departments)]
    if genders:
        filtered = filtered[filtered['Gender'].isin(genders)]
    if jobroles:
        filtered = filtered[filtered['JobRole'].isin(jobroles)]
    return filtered

df_filtered = apply_filters(df_raw, selected_dept, selected_gender, selected_jobrole)

# Store filtered data and metric mode in session state
st.session_state['df_filtered'] = df_filtered
st.session_state['metric_mode'] = metric_mode
st.session_state['selected_dept'] = selected_dept
st.session_state['selected_gender'] = selected_gender
st.session_state['selected_jobrole'] = selected_jobrole


# ── Auto-redirect ke Overview (menyembunyikan tab "app" dari navigasi) ─────────
st.switch_page("pages/1_Overview.py")
