"""
Halaman 3 — Faktor Lanjutan
EnvironmentSatisfaction, JobInvolvement, RelationshipSatisfaction, Distribusi Usia
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Faktor Lanjutan | HR Dashboard", layout="wide")
st.markdown("""
<style>
.main{background-color:#F8F9FC;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1A1F36 0%,#2D3561 100%);}
[data-testid="stSidebar"] *{color:#E8EAF6 !important;}
[data-testid="stSidebar"] .stMarkdown h3{color:#7C83FD !important;font-size:13px !important;text-transform:uppercase;letter-spacing:1px;border-bottom:1px solid rgba(124,131,253,0.3);padding-bottom:6px;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}
</style>""", unsafe_allow_html=True)

if 'data_loaded' not in st.session_state:
    st.warning("⚠️ Silakan jalankan app.py terlebih dahulu.")
    st.stop()

df_raw = st.session_state['df_raw']

def ax(text, **kw):
    return dict(title=dict(text=text, font=dict(color='#1A1F36')), tickfont=dict(color='#1A1F36'), **kw)

with st.sidebar:
    st.markdown("## 📊 HR Attrition")
    st.caption("Analytics Dashboard")
    st.markdown("---")
    st.markdown("### 🔍 Global Filter")
    st.markdown(" ")
    sel_dept   = st.multiselect("Department", sorted(df_raw['Department'].dropna().unique()), default=[], placeholder="Semua Department", key="d3")
    st.markdown(" ")
    sel_gender = st.multiselect("Gender",     sorted(df_raw['Gender'].dropna().unique()),     default=[], placeholder="Semua Gender",     key="g3")
    st.markdown(" ")
    sel_role   = st.multiselect("Job Role",   sorted(df_raw['JobRole'].dropna().unique()),    default=[], placeholder="Semua Job Role",   key="r3")
    st.markdown("---")
    st.markdown("### 📐 Metric Selector")
    st.markdown(" ")
    metric = st.radio("Tampilkan sebagai:", ["Attrition Rate (%)", "Jumlah Resign"], index=0, key="m3")
    st.markdown("---")
    st.caption("HR Attrition Analytics Dashboard\nPowered by XGBoost")

df = df_raw.copy()
if sel_dept:   df = df[df['Department'].isin(sel_dept)]
if sel_gender: df = df[df['Gender'].isin(sel_gender)]
if sel_role:   df = df[df['JobRole'].isin(sel_role)]

st.markdown("""
<div style='background:linear-gradient(135deg,#4facfe 0%,#00f2fe 100%);border-radius:16px;padding:28px 32px;margin-bottom:28px;'>
<h1 style='color:white;margin:0;font-size:26px;font-weight:800;'>🔬 Faktor Lanjutan</h1>
<p style='color:rgba(255,255,255,0.85);margin:6px 0 0 0;font-size:13px;'>Analisis Faktor Lanjutan Penyebab Attrition | HR Attrition Analytics Dashboard</p>
</div>""", unsafe_allow_html=True)

if sel_dept or sel_gender or sel_role:
    parts=[]
    if sel_dept:   parts.append(f"Dept: {', '.join(sel_dept)}")
    if sel_gender: parts.append(f"Gender: {', '.join(sel_gender)}")
    if sel_role:   parts.append(f"Role: {', '.join(sel_role[:2])}{'...' if len(sel_role)>2 else ''}")
    st.info(f"🔍 Filter aktif: {' | '.join(parts)} — **{len(df):,}** dari {len(df_raw):,} karyawan")

def yl():
    return "Attrition Rate (%)" if metric=="Attrition Rate (%)" else "Jumlah Resign"

def get_metric(x):
    return x['Attrition'].mean()*100 if metric=="Attrition Rate (%)" else x['Attrition'].sum()

def fmt(vals):
    return [f"{v:.1f}%" if metric=="Attrition Rate (%)" else f"{int(v):,}" for v in vals]

def make_satisfaction_chart(col, title, subtitle, xlabel, label_map):
    g = df.groupby(col).apply(lambda x: pd.Series({
        'metric': get_metric(x), 'total': len(x),
        'resign': int(x['Attrition'].sum()), 'rate': x['Attrition'].mean()*100
    })).reset_index().sort_values(col)
    g['label'] = g[col].map(label_map)
    fig = go.Figure(go.Bar(
        x=g['label'], y=g['metric'],
        marker=dict(
            color=g['metric'].tolist(),
            colorscale=[[0,'#06D6A0'],[0.5,'#4361EE'],[1,'#F72585']],
            reversescale=True, showscale=False,
            line=dict(color='white', width=2)
        ),
        text=fmt(g['metric']), textposition='outside', textfont=dict(size=12,color='#1A1F36'),
        customdata=g[['total','resign','rate']].values,
        hovertemplate=f'<b>%{{x}}</b><br>Total: %{{customdata[0]:,}}<br>Resign: %{{customdata[1]:,}}<br>Rate: %{{customdata[2]:.1f}}%<extra></extra>'
    ))
    fig.update_layout(
        title=dict(text=f"<b>{title}</b><br><sub>{subtitle}</sub>", font=dict(size=14,color='#1A1F36'), x=0.01),
        template='plotly_white', font=dict(color='#1A1F36'),
        xaxis=ax(xlabel, showgrid=False),
        yaxis=ax(yl(), showgrid=True, gridcolor='#F0F2F5', range=[0,g['metric'].max()*1.3]),
        paper_bgcolor='white', plot_bgcolor='white',
        margin=dict(t=70,b=40,l=20,r=20), height=320,
    )
    return fig

SAT_MAP = {1:'1-Low',2:'2-Medium',3:'3-High',4:'4-Very High'}

# ── Row 1: EnvironmentSatisfaction + JobInvolvement ───────────────────────────
st.markdown("### 😊 Kepuasan Lingkungan & Keterlibatan Kerja")
st.markdown(" ")
c1,c2 = st.columns(2)

with c1:
    st.plotly_chart(make_satisfaction_chart(
        'EnvironmentSatisfaction',
        'EnvironmentSatisfaction vs Attrition',
        'Feature Importance #7 (0.037)',
        'Environment Satisfaction Level', SAT_MAP
    ), use_container_width=True)

with c2:
    g = df.groupby('JobInvolvement').apply(lambda x: pd.Series({
        'metric': get_metric(x), 'total': len(x),
        'resign': int(x['Attrition'].sum()), 'rate': x['Attrition'].mean()*100
    })).reset_index().sort_values('JobInvolvement')
    g['label'] = g['JobInvolvement'].map(SAT_MAP)
    fig = go.Figure(go.Bar(
        x=g['label'], y=g['metric'],
        marker=dict(
            color=g['metric'].tolist(),
            colorscale=[[0,'#4CC9F0'],[0.5,'#7209B7'],[1,'#F72585']],
            reversescale=True, showscale=False,
            line=dict(color='white', width=2)
        ),
        text=fmt(g['metric']), textposition='outside', textfont=dict(size=12,color='#1A1F36'),
        customdata=g[['total','resign','rate']].values,
        hovertemplate='<b>%{x}</b><br>Total: %{customdata[0]:,}<br>Resign: %{customdata[1]:,}<br>Rate: %{customdata[2]:.1f}%<extra></extra>'
    ))
    fig.update_layout(
        title=dict(text="<b>JobInvolvement vs Attrition</b><br><sub>Feature Importance #8 (0.035)</sub>", font=dict(size=14,color='#1A1F36'), x=0.01),
        template='plotly_white', font=dict(color='#1A1F36'),
        xaxis=ax("Job Involvement Level", showgrid=False),
        yaxis=ax(yl(), showgrid=True, gridcolor='#F0F2F5', range=[0,g['metric'].max()*1.3]),
        paper_bgcolor='white', plot_bgcolor='white',
        margin=dict(t=70,b=40,l=20,r=20), height=320,
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Row 2: RelationshipSatisfaction + Histogram Usia ──────────────────────────
st.markdown("### 💬 Hubungan Kerja & Distribusi Usia")
st.markdown(" ")
c3,c4 = st.columns(2)

with c3:
    st.plotly_chart(make_satisfaction_chart(
        'RelationshipSatisfaction',
        'RelationshipSatisfaction vs Attrition',
        'Feature Importance #9 (0.034)',
        'Relationship Satisfaction Level', SAT_MAP
    ), use_container_width=True)

with c4:
    age_no  = df[df['Attrition']==0]['Age']
    age_yes = df[df['Attrition']==1]['Age']
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=age_no,  name='Aktif (No)',    nbinsx=20, opacity=0.65,
                               marker=dict(color='#4361EE', line=dict(color='white',width=0.8)),
                               hovertemplate='<b>Aktif</b><br>Usia: %{x}<br>Jumlah: %{y}<extra></extra>'))
    fig.add_trace(go.Histogram(x=age_yes, name='Resign (Yes)',  nbinsx=20, opacity=0.65,
                               marker=dict(color='#F72585', line=dict(color='white',width=0.8)),
                               hovertemplate='<b>Resign</b><br>Usia: %{x}<br>Jumlah: %{y}<extra></extra>'))
    fig.update_layout(
        title=dict(text="<b>Distribusi Usia per Status Attrition</b><br><sub>Histogram overlay — Yes vs No Attrition</sub>", font=dict(size=14,color='#1A1F36'), x=0.01),
        barmode='overlay',
        template='plotly_white', font=dict(color='#1A1F36'),
        xaxis=ax("Usia (Tahun)", showgrid=True, gridcolor='#F0F2F5'),
        yaxis=ax("Jumlah Karyawan", showgrid=True, gridcolor='#F0F2F5'),
        legend=dict(font=dict(color='#333'), orientation='h', yanchor='top', y=0.98, xanchor='right', x=1,
                    bgcolor='rgba(255,255,255,0.8)', bordercolor='#E0E4ED', borderwidth=1),
        paper_bgcolor='white', plot_bgcolor='white',
        margin=dict(t=70,b=40,l=20,r=20), height=340,
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")