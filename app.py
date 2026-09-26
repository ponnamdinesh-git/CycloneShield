import streamlit as st
import pandas as pd
import plotly.express as px
from risk_engine import calculate_risk

st.set_page_config(page_title="CycloneShield AI", page_icon="🌀", layout="wide")
st.title("🌀 CycloneShield AI")
st.caption("Anticipatory cyclone-risk intelligence for coastal authorities")

@st.cache_data
def load_assets():
    return pd.read_csv("data/infrastructure.csv")

assets = load_assets()

st.sidebar.header("Cyclone Scenario")
location = st.sidebar.selectbox("Location", ["Visakhapatnam","Kakinada","Machilipatnam","Nellore","Chennai"])
wind = st.sidebar.slider("Wind speed (km/h)", 60, 240, 150, 5)
rain = st.sidebar.slider("Rainfall / 24h (mm)", 20, 600, 300, 10)
surge = st.sidebar.slider("Storm surge (m)", 0.2, 6.0, 3.2, 0.1)
lead_time = st.sidebar.slider("Lead time (hours)", 6, 72, 18, 1)

risk = calculate_risk(wind, rain, surge, lead_time)

if st.sidebar.button("Run Risk Assessment", type="primary"):
    st.rerun()

st.subheader(f"Risk Assessment — {location}")
c1,c2,c3,c4 = st.columns(4)
c1.metric("Overall Risk", f"{risk['overall_score']}/100")
c2.metric("Wind", f"{risk['wind_score']}/100")
c3.metric("Rainfall", f"{risk['rain_score']}/100")
c4.metric("Storm Surge", f"{risk['surge_score']}/100")
st.progress(risk["overall_score"]/100)

st.markdown("### Priority Actions")
for action in risk["actions"]:
    st.write("• " + action)

m = assets.copy()
m["Risk"] = m.apply(lambda r: min(100, risk["overall_score"] + int(r["exposure_multiplier"]*20) + (10 if r["critical"] else 0)), axis=1)

st.markdown("### Infrastructure Exposure")
fig = px.scatter_map(m, lat="latitude", lon="longitude", color="Risk", size="importance",
                     hover_name="name", hover_data=["type","critical","Risk"],
                     zoom=7, height=520)
fig.update_layout(map_style="open-street-map", margin=dict(l=0,r=0,t=0,b=0))
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Asset-level priorities")
st.dataframe(m[["name","type","critical","importance","Risk"]].sort_values("Risk", ascending=False),
             use_container_width=True, hide_index=True)

st.info("Prototype only: not an operational emergency-warning system.")
