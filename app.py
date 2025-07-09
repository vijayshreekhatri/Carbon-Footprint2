# 1️ Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# 2️ Page setup
st.set_page_config(page_title="Vehicle CO₂ Emissions Dashboard", layout="wide")
st.title(" Vehicle CO₂ Emissions Dashboard")
st.markdown("Explore and compare fuel economy and carbon footprint of various vehicle models.")

# 3️ Load CSV
df = pd.read_csv("C:/Users/ASTHA/Desktop/carbon_dashboard/CO2 Data (1).csv")
df.columns = df.columns.str.strip()  

# 4️ Rename columns to avoid errors
df.rename(columns={
    "Fuel Consumption Comb (L/100 km)": "Fuel_Comb_L",
    "Fuel Consumption Comb (mpg)": "Fuel_Comb_mpg",
    "CO2 Emissions(g/km)": "CO2_g_per_km",
    "Vehicle Class": "Vehicle_Class"
}, inplace=True)

# 5️ Emission category logic
def classify_emission(co2):
    if co2 < 100:
        return "Ultra Low"
    elif co2 < 150:
        return "Low"
    elif co2 < 200:
        return "Moderate"
    else:
        return "High"

df["Emission_Category"] = df["CO2_g_per_km"].apply(classify_emission)

# 6️ Sidebar filters
st.sidebar.header(" Filter Options")
selected_makes = st.sidebar.multiselect("Choose Make(s):", options=df["Make"].unique(), default=df["Make"].unique())
selected_category = st.sidebar.multiselect("Choose Emission Category:", options=df["Emission_Category"].unique(), default=df["Emission_Category"].unique())

# 7️ Apply filters
df_filtered = df[df["Make"].isin(selected_makes) & df["Emission_Category"].isin(selected_category)]

# 8️ Show filtered data
st.subheader(" Filtered Vehicle Data")
st.dataframe(df_filtered)

# 9️ Emission Category Histogram
st.subheader(" Emission Category Distribution")
fig1 = px.histogram(df_filtered, x="Emission_Category", color="Emission_Category", title="Distribution of Emission Categories")
st.plotly_chart(fig1)

# Emissions by Model (Scatter Plot)
st.subheader(" Emissions by Vehicle Model")
fig2 = px.scatter(
    df_filtered,
    x="Model",
    y="CO2_g_per_km",
    color="Make",
    size="CO2_g_per_km",
    hover_name="Model",
    title="Emissions by Vehicle Model"
)
st.plotly_chart(fig2)

#  AI-Powered Summary
st.subheader(" AI Insight Summary")

if not df_filtered.empty:
    best = df_filtered.sort_values(by="CO2_g_per_km").iloc[0]
    avg = df_filtered["CO2_g_per_km"].mean()

    st.success(f" **Lowest Emission Vehicle**: `{best['Make']} {best['Model']}` → **{best['CO2_g_per_km']} g/km**")
    st.info(f" **Average CO₂ Emissions** in selection: **{avg:.2f} g/km**")

    st.markdown(f"""
    ###  Smart Suggestion
    - This vehicle is a **{best['Vehicle_Class']}**, with a fuel efficiency of **{best['Fuel_Comb_L']} L/100 km**.
    - It uses fuel type **{best['Fuel Type']}**, making it suitable for eco-conscious driving.
    - For fleet decarbonization, prioritize models in the **{best['Vehicle_Class']}** class with CO₂ emissions below **{avg:.0f} g/km**.
    """)
else:
    st.warning("No results match your filters. Please adjust the sidebar selections.")
    

