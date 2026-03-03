import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Overview | HR Dashboard", layout="wide")
st.markdown("""
<style>
.main{background-color:#F8F9FC;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1A1F36 0%,#2D3561 100%);}
[data-testid="stSidebar"] *{color:#E8EAF6 !important;}
[data-testid="stSidebar"] .stMarkdown h3{color:#7C83FD !important;font-size:13px !important;text-transform:uppercase;letter-spacing:1px;border-bottom:1px solid rgba(124,131,253,0.3);padding-bottom:6px;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}
</style>""", unsafe_allow_html=True)

if 'data_loaded' not in st.session_state:
    st.warning("Jalankan app.py terlebih dahulu.")
    st.stop()

df_raw   = st.session_state['df_raw']
feat_imp = st.session_state['feat_imp']

def ax(text, **kw):
    """Helper: axis dict pakai title=dict"""
    return dict(title=dict(text=text, font=dict(color='#1A1F36')), tickfont=dict(color='#1A1F36'), **kw)

with st.sidebar:
    st.markdown("## 📊 HR Attrition")
    st.caption("Analytics Dashboard")
    st.markdown("---")
    st.markdown("### 🔍 Global Filter")
    st.markdown(" ")
    sel_dept   = st.multiselect("Department", sorted(df_raw['Department'].dropna().unique()), default=[], placeholder="Semua Department", key="d1")
    st.markdown(" ")
    sel_gender = st.multiselect("Gender",     sorted(df_raw['Gender'].dropna().unique()),     default=[], placeholder="Semua Gender",     key="g1")
    st.markdown(" ")
    sel_role   = st.multiselect("Job Role",   sorted(df_raw['JobRole'].dropna().unique()),    default=[], placeholder="Semua Job Role",   key="r1")
    st.markdown("---")
    st.markdown("### 📐 Metric Selector")
    st.markdown(" ")
    metric = st.radio("Tampilkan sebagai:", ["Attrition Rate (%)", "Jumlah Resign"], index=0, key="m1")
    st.markdown("---")
    st.caption("HR Attrition Analytics Dashboard\nPowered by XGBoost")

df = df_raw.copy()
if sel_dept:   df = df[df['Department'].isin(sel_dept)]
if sel_gender: df = df[df['Gender'].isin(sel_gender)]
if sel_role:   df = df[df['JobRole'].isin(sel_role)]

st.markdown("""
<div style='background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);border-radius:16px;padding:28px 32px;margin-bottom:28px;'>
<h1 style='color:white;margin:0;font-size:26px;font-weight:800;'>📋 Overview & Summary</h1>
<p style='color:rgba(255,255,255,0.8);margin:6px 0 0 0;font-size:13px;'>HR Attrition Analytics Dashboard | Powered by XGBoost</p>
</div>""", unsafe_allow_html=True)

if sel_dept or sel_gender or sel_role:
    parts = []
    if sel_dept:   parts.append(f"Dept: {', '.join(sel_dept)}")
    if sel_gender: parts.append(f"Gender: {', '.join(sel_gender)}")
    if sel_role:   parts.append(f"Role: {', '.join(sel_role[:2])}{'...' if len(sel_role)>2 else ''}")
    st.info(f"🔍 Filter aktif: {' | '.join(parts)} — **{len(df):,}** dari {len(df_raw):,} karyawan")

total  = len(df)
resign = int(df['Attrition'].sum())
active = total - resign
rate   = (resign/total*100) if total>0 else 0
base   = df_raw['Attrition'].mean()*100
delta  = rate - base

kpis = [
    ("👥 Total Karyawan", f"{total:,}",   f"Dataset: {len(df_raw):,} total",                             "#667eea","#EEF2FF"),
    ("📉 Attrition Rate", f"{rate:.1f}%", f"{'▲' if delta>0 else '▼'} {abs(delta):.1f}% vs overall {base:.1f}%","#FF6B6B","#FFF5F5"),
    ("🚪 Jumlah Resign",  f"{resign:,}",  f"Dari {total:,} karyawan",                                    "#F093FB","#FDF5FF"),
    ("✅ Jumlah Aktif",   f"{active:,}",  f"{(active/total*100):.1f}% retention rate" if total>0 else "-","#4FACFE","#F0F8FF"),
]
for col,(title,val,dlt,color,bg) in zip(st.columns(4), kpis):
    with col:
        st.markdown(f"""
        <div style='background:{bg};border-radius:16px;padding:22px 20px;
             box-shadow:0 2px 12px rgba(0,0,0,0.06);border-left:5px solid {color};min-height:130px;'>
          <div style='font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;color:#8892A4;margin-bottom:8px;'>{title}</div>
          <div style='font-size:36px;font-weight:800;color:{color};line-height:1.1;margin-bottom:6px;'>{val}</div>
          <div style='font-size:12px;color:#8892A4;'>{dlt}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ── Donut + Dept bar ───────────────────────────────────────────────────────────
st.markdown("### 🥧 Proporsi & Distribusi Attrition")
st.markdown(" ")
c1, c2 = st.columns([1, 1.4])

with c1:
    yes_c = int(df['Attrition'].sum()); no_c = total - yes_c
    fig = go.Figure(go.Pie(
        labels=['Aktif (No)','Resign (Yes)'], values=[no_c,yes_c], hole=0.62,
        marker=dict(colors=['#4361EE','#F72585'], line=dict(color='white',width=3)),
        textinfo='label+percent', textfont=dict(size=13, color='#333'),
        hovertemplate='<b>%{label}</b><br>Jumlah: %{value:,}<br>%{percent}<extra></extra>'
    ))
    fig.update_layout(
        title=dict(text="<b>Proporsi Attrition</b>", font=dict(size=15,color='#1A1F36'), x=0.5),
        template='plotly_white', font=dict(color='#1A1F36'),
        paper_bgcolor='white', plot_bgcolor='white',
        legend=dict(font=dict(color='#333'), orientation='h', y=-0.15, x=0.5, xanchor='center'),
        margin=dict(t=60,b=40,l=20,r=20), height=340,
        annotations=[dict(text=f"<b>{rate:.1f}%</b><br>Attrition", x=0.5,y=0.5, showarrow=False, font=dict(size=18,color='#1A1F36'))]
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    dept = df.groupby('Department').agg(Total=('Attrition','count'),Resign=('Attrition','sum')).reset_index()
    dept['Rate'] = dept['Resign']/dept['Total']*100
    dept = dept.sort_values('Rate', ascending=False)
    if metric=="Attrition Rate (%)":
        yv=dept['Rate']; yl="Attrition Rate (%)"; tf=[f"{v:.1f}%" for v in yv]; ti="<b>Attrition Rate per Department</b>"
    else:
        yv=dept['Resign']; yl="Jumlah Resign"; tf=[f"{int(v):,}" for v in yv]; ti="<b>Jumlah Resign per Department</b>"
    fig2 = go.Figure(go.Bar(
        x=dept['Department'], y=yv,
        marker=dict(color=['#F72585' if v==yv.max() else '#4361EE' for v in yv], line=dict(color='white',width=2)),
        text=tf, textposition='outside', textfont=dict(size=13,color='#1A1F36'),
        customdata=dept[['Total','Resign','Rate']].values,
        hovertemplate='<b>%{x}</b><br>Total: %{customdata[0]:,}<br>Resign: %{customdata[1]:,}<br>Rate: %{customdata[2]:.1f}%<extra></extra>'
    ))
    fig2.update_layout(
        title=dict(text=ti, font=dict(size=15,color='#1A1F36'), x=0.02),
        template='plotly_white', font=dict(color='#1A1F36'),
        xaxis=ax("Department", showgrid=False),
        yaxis=ax(yl, showgrid=True, gridcolor='#F0F2F5', range=[0,yv.max()*1.25]),
        paper_bgcolor='white', plot_bgcolor='white',
        margin=dict(t=60,b=40,l=20,r=20), height=340,
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── Job Role ───────────────────────────────────────────────────────────────────
st.markdown("### 💼 Attrition Rate per Job Role")
st.markdown(" ")

role = df.groupby('JobRole').agg(Total=('Attrition','count'),Resign=('Attrition','sum')).reset_index()
role['Rate'] = role['Resign']/role['Total']*100
if metric=="Attrition Rate (%)":
    role=role.sort_values('Rate',ascending=True); xv=role['Rate']; xl="Attrition Rate (%)"; tf=[f"{v:.1f}%" for v in xv]; ti="<b>Attrition Rate per Job Role</b>"
else:
    role=role.sort_values('Resign',ascending=True); xv=role['Resign']; xl="Jumlah Resign"; tf=[f"{int(v):,}" for v in xv]; ti="<b>Jumlah Resign per Job Role</b>"

norm = xv/xv.max() if xv.max()>0 else xv
fig3 = go.Figure(go.Bar(
    y=role['JobRole'], x=xv, orientation='h',
    marker=dict(color=list(norm), colorscale=[[0,'#4361EE'],[0.5,'#7209B7'],[1,'#F72585']], showscale=False, line=dict(color='white',width=1.5)),
    text=tf, textposition='outside', textfont=dict(size=12,color='#1A1F36'),
    customdata=role[['Total','Resign','Rate']].values,
    hovertemplate='<b>%{y}</b><br>Total: %{customdata[0]:,}<br>Resign: %{customdata[1]:,}<br>Rate: %{customdata[2]:.1f}%<extra></extra>'
))
fig3.update_layout(
    title=dict(text=ti, font=dict(size=15,color='#1A1F36'), x=0.01),
    template='plotly_white', font=dict(color='#1A1F36'),
    xaxis=ax(xl, showgrid=True, gridcolor='#F0F2F5', range=[0,xv.max()*1.25]),
    yaxis=ax("", autorange=True),
    paper_bgcolor='white', plot_bgcolor='white',
    margin=dict(t=60,b=40,l=180,r=80), height=max(380,len(role)*38),
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ── Feature Importance ─────────────────────────────────────────────────────────
st.markdown("### 🏆 Top 10 Feature Importance — XGBoost Model")
st.markdown(" ")

top10 = feat_imp.head(10).sort_values('Importance', ascending=True)
mn,mx = top10['Importance'].min(), top10['Importance'].max()
bar_colors=[]
for v in top10['Importance']:
    n=(v-mn)/(mx-mn) if mx>mn else 0.5
    if n<0.4:   c=(6,214,160)
    elif n<0.7: c=(114,9,183)
    else:       c=(247,37,133)
    bar_colors.append(f'rgb{c}')

fig4 = go.Figure(go.Bar(
    y=top10['Feature'], x=top10['Importance'], orientation='h',
    marker=dict(color=bar_colors, line=dict(color='white',width=1.5)),
    text=[f"{v:.4f}" for v in top10['Importance']],
    textposition='inside', textfont=dict(size=12,color='#1A1F36',family='monospace'),
    hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>'
))
fig4.add_vline(x=0.05, line_dash="dash", line_color="#FF6B6B", line_width=1.5,
               annotation_text="5%", annotation_font=dict(size=10,color="#FF6B6B"))
fig4.add_vline(x=0.02, line_dash="dash", line_color="#4FACFE", line_width=1.5,
               annotation_text="2%", annotation_font=dict(size=10,color="#4FACFE"))
fig4.update_layout(
    title=dict(text="<b>Top 10 Feature Importance</b><br><sub>🟥 >5% Sangat Penting · 🟨 2-5% Cukup · 🟩 Perlu Perhatian</sub>",
               font=dict(size=15,color='#1A1F36'), x=0.01),
    template='plotly_white', font=dict(color='#1A1F36'),
    xaxis=ax("Importance Score", showgrid=True, gridcolor='#F0F2F5'),
    yaxis=ax("", autorange=True),
    paper_bgcolor='white', plot_bgcolor='white',
    margin=dict(t=80,b=50,l=200,r=80), height=440,
)
st.plotly_chart(fig4, use_container_width=True)
st.caption("📌 Feature importance berdasarkan model XGBoost (n_estimators=500, max_depth=3, ROC-AUC=0.805)")

st.markdown("---")