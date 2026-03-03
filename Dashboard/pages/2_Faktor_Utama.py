"""
Halaman 2 — Faktor Utama Penyebab Attrition
Top 6 Feature Importance dari XGBoost
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Faktor Utama | HR Dashboard", layout="wide")
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
    sel_dept   = st.multiselect("Department", sorted(df_raw['Department'].dropna().unique()), default=[], placeholder="Semua Department", key="d2")
    st.markdown(" ")
    sel_gender = st.multiselect("Gender",     sorted(df_raw['Gender'].dropna().unique()),     default=[], placeholder="Semua Gender",     key="g2")
    st.markdown(" ")
    sel_role   = st.multiselect("Job Role",   sorted(df_raw['JobRole'].dropna().unique()),    default=[], placeholder="Semua Job Role",   key="r2")
    st.markdown("---")
    st.markdown("### 📐 Metric Selector")
    st.markdown(" ")
    metric = st.radio("Tampilkan sebagai:", ["Attrition Rate (%)", "Jumlah Resign"], index=0, key="m2")
    st.markdown("---")
    st.caption("HR Attrition Analytics Dashboard\nPowered by XGBoost")

df = df_raw.copy()
if sel_dept:   df = df[df['Department'].isin(sel_dept)]
if sel_gender: df = df[df['Gender'].isin(sel_gender)]
if sel_role:   df = df[df['JobRole'].isin(sel_role)]

st.markdown("""
<div style='background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);border-radius:16px;padding:28px 32px;margin-bottom:28px;'>
<h1 style='color:white;margin:0;font-size:26px;font-weight:800;'>⭐ Faktor Utama Penyebab Attrition</h1>
<p style='color:rgba(255,255,255,0.85);margin:6px 0 0 0;font-size:13px;'>Analisis Top 6 Feature Importance XGBoost | HR Attrition Analytics Dashboard</p>
</div>""", unsafe_allow_html=True)

if sel_dept or sel_gender or sel_role:
    parts=[]
    if sel_dept:   parts.append(f"Dept: {', '.join(sel_dept)}")
    if sel_gender: parts.append(f"Gender: {', '.join(sel_gender)}")
    if sel_role:   parts.append(f"Role: {', '.join(sel_role[:2])}{'...' if len(sel_role)>2 else ''}")
    st.info(f"🔍 Filter aktif: {' | '.join(parts)} — **{len(df):,}** dari {len(df_raw):,} karyawan")

def get_grp(col, df):
    g = df.groupby(col).apply(lambda x: pd.Series({
        'metric': x['Attrition'].mean()*100 if metric=="Attrition Rate (%)" else x['Attrition'].sum(),
        'total': len(x), 'resign': int(x['Attrition'].sum()), 'rate': x['Attrition'].mean()*100
    })).reset_index()
    return g

def fmt(vals):
    return [f"{v:.1f}%" if metric=="Attrition Rate (%)" else f"{int(v):,}" for v in vals]

def yl():
    return "Attrition Rate (%)" if metric=="Attrition Rate (%)" else "Jumlah Resign"

def make_bar(g, col, colors, title, subtitle, xlabel):
    fig = go.Figure(go.Bar(
        x=g[col].astype(str), y=g['metric'],
        marker=dict(color=colors, line=dict(color='white',width=2)),
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

# ── Row 1: OverTime + StockOptionLevel ────────────────────────────────────────
st.markdown("### 🔥 Faktor #1 & #2 — Lembur & Kompensasi Saham")
st.markdown(" ")
c1,c2 = st.columns(2)

with c1:
    g = get_grp('OverTime', df).sort_values('OverTime')
    colors = ['#4361EE' if str(v)=='No' else '#F72585' for v in g['OverTime']]
    st.plotly_chart(make_bar(g,'OverTime',colors,"OverTime vs Attrition","Feature Importance #1 (0.077)","OverTime Status"), use_container_width=True)

with c2:
    g = get_grp('StockOptionLevel', df).sort_values('StockOptionLevel')
    colors = ['#4361EE','#7209B7','#F72585','#FB8500'][:len(g)]
    st.plotly_chart(make_bar(g,'StockOptionLevel',colors,"StockOptionLevel vs Attrition","Feature Importance #2 (0.066) · 0=Tidak Ada, 3=Tinggi","Stock Option Level"), use_container_width=True)

st.markdown("---")

# ── Row 2: JobLevel + AgeGroup ─────────────────────────────────────────────────
st.markdown("### 🏢 Faktor #3 & #4 — Jenjang Karir & Usia")
st.markdown(" ")
c3,c4 = st.columns(2)

with c3:
    g = get_grp('JobLevel', df).sort_values('JobLevel')
    colors = ['#F72585','#7209B7','#4361EE','#4CC9F0','#06D6A0'][:len(g)]
    st.plotly_chart(make_bar(g,'JobLevel',colors,"JobLevel vs Attrition","Feature Importance #3 (0.058) · 1=Junior, 5=Senior","Job Level"), use_container_width=True)

with c4:
    age_bins  = [18,25,30,35,40,45,61]
    age_lbls  = ['18-25','26-30','31-35','36-40','41-45','46+']
    df2 = df.copy()
    df2['AgeBin'] = pd.cut(df2['Age'], bins=age_bins, labels=age_lbls, right=True)
    g = df2.groupby('AgeBin', observed=True).apply(lambda x: pd.Series({
        'metric': x['Attrition'].mean()*100 if metric=="Attrition Rate (%)" else x['Attrition'].sum(),
        'total': len(x), 'resign': int(x['Attrition'].sum()), 'rate': x['Attrition'].mean()*100
    })).reset_index()
    mx = g['metric'].max()
    colors = []
    for v in g['metric']:
        n = v/mx if mx>0 else 0
        colors.append(f'rgb({int(247*n+67*(1-n))},{int(37*n+214*(1-n))},{int(133*n+160*(1-n))})')
    fig = go.Figure(go.Bar(
        x=g['AgeBin'].astype(str), y=g['metric'],
        marker=dict(color=colors, line=dict(color='white',width=2)),
        text=fmt(g['metric']), textposition='outside', textfont=dict(size=12,color='#1A1F36'),
        customdata=g[['total','resign','rate']].values,
        hovertemplate='<b>Usia %{x}</b><br>Total: %{customdata[0]:,}<br>Resign: %{customdata[1]:,}<br>Rate: %{customdata[2]:.1f}%<extra></extra>'
    ))
    fig.update_layout(
        title=dict(text="<b>Age Group vs Attrition</b><br><sub>Feature Importance #4 (0.043) · Binning otomatis</sub>", font=dict(size=14,color='#1A1F36'), x=0.01),
        template='plotly_white', font=dict(color='#1A1F36'),
        xaxis=ax("Kelompok Usia", showgrid=False),
        yaxis=ax(yl(), showgrid=True, gridcolor='#F0F2F5', range=[0,g['metric'].max()*1.3]),
        paper_bgcolor='white', plot_bgcolor='white',
        margin=dict(t=70,b=40,l=20,r=20), height=320,
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Row 3: TotalWorkingYears + MaritalStatus ───────────────────────────────────
st.markdown("### 📅 Faktor #5 & #6 — Pengalaman Kerja & Status Pernikahan")
st.markdown(" ")
c5,c6 = st.columns(2)

with c5:
    tw_bins = [0,2,5,10,20,40]; tw_lbls=['0-2 thn','3-5 thn','6-10 thn','11-20 thn','>20 thn']
    df3 = df.copy()
    df3['TWBin'] = pd.cut(df3['TotalWorkingYears'], bins=tw_bins, labels=tw_lbls, right=True)
    g = df3.groupby('TWBin', observed=True).apply(lambda x: pd.Series({
        'metric': x['Attrition'].mean()*100 if metric=="Attrition Rate (%)" else x['Attrition'].sum(),
        'total': len(x), 'resign': int(x['Attrition'].sum()), 'rate': x['Attrition'].mean()*100
    })).reset_index()
    colors = ['#F72585','#7209B7','#4361EE','#4CC9F0','#06D6A0'][:len(g)]
    fig = go.Figure(go.Bar(
        x=g['TWBin'].astype(str), y=g['metric'],
        marker=dict(color=colors, line=dict(color='white',width=2)),
        text=fmt(g['metric']), textposition='outside', textfont=dict(size=12,color='#1A1F36'),
        customdata=g[['total','resign','rate']].values,
        hovertemplate='<b>%{x}</b><br>Total: %{customdata[0]:,}<br>Resign: %{customdata[1]:,}<br>Rate: %{customdata[2]:.1f}%<extra></extra>'
    ))
    fig.update_layout(
        title=dict(text="<b>TotalWorkingYears vs Attrition</b><br><sub>Feature Importance #5 (0.040)</sub>", font=dict(size=14,color='#1A1F36'), x=0.01),
        template='plotly_white', font=dict(color='#1A1F36'),
        xaxis=ax("Total Working Years", showgrid=False),
        yaxis=ax(yl(), showgrid=True, gridcolor='#F0F2F5', range=[0,g['metric'].max()*1.3]),
        paper_bgcolor='white', plot_bgcolor='white',
        margin=dict(t=70,b=40,l=20,r=20), height=320,
    )
    st.plotly_chart(fig, use_container_width=True)

with c6:
    g = get_grp('MaritalStatus', df).sort_values('metric', ascending=False)
    mx_v = g['metric'].max(); mn_v = g['metric'].min()
    colors = ['#F72585' if v==mx_v else '#06D6A0' if v==mn_v else '#7209B7' for v in g['metric']]
    st.plotly_chart(make_bar(g,'MaritalStatus',colors,"MaritalStatus vs Attrition","Feature Importance #6 (0.039)","Marital Status"), use_container_width=True)

st.markdown("---")