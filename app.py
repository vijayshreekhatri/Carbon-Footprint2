# 1️ Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# 2️ Set up the page
st.set_page_config(page_title=" Vehicle Emissions Dashboard", layout="wide")
st.title(" Vehicle CO₂ Emissions Dashboard")
st.markdown("Explore your data and learn which vehicles are the cleanest ")

# 3️ Load CSV file
df = pd.read_csv("C:/Users/ASTHA/Downloads/CO2 Data (1).csv")  # <-- update path here
df.columns = [col.strip() for col in df.columns]  # clean column names

# 4️ Emissions category column
def classify_emission(co2):
    if co2 < 100:
        return "Ultra Low"
    elif co2 < 150:
        return "Low"
    elif co2 < 200:
        return "Moderate"
    else:
        return "High"

df["Emission Category"] = df["CO2 Emissions(g/km)"].apply(classify_emission)

# 5️ Filters in the sidebar
st.sidebar.header(" Filter Options")
selected_makes = st.sidebar.multiselect("Choose Make(s):", options=df["Make"].unique(), default=df["Make"].unique())
selected_category = st.sidebar.multiselect("Choose Emission Category:", options=df["Emission Category"].unique(), default=df["Emission Category"].unique())

# Filter the data based on selections
df_filtered = df[df["Make"].isin(selected_makes) & df["Emission Category"].isin(selected_category)]

# 6️ Showing data
st.subheader(" Filtered Vehicle Data")
st.dataframe(df_filtered)

# 7️ Histogram of emission categories
st.subheader(" Emission Category Distribution")
fig1 = px.histogram(df_filtered, x="Emission Category", color="Emission Category")
st.plotly_chart(fig1)

# 8️ Scatter plot by model
st.subheader(" Emissions by Vehicle Model")
fig2 = px.scatter(df_filtered, x="Model", y="CO2 Emissions(g/km)", color="Make", size="CO2 Emissions(g/km)", hover_name="Model")
st.plotly_chart(fig2)

# 9️ Summary box
st.subheader(" Summary")
best = df_filtered.sort_values(by="CO2 Emissions(g/km)").iloc[0]
avg = df_filtered["CO2 Emissions(g/km)"].mean()

st.success(f" Lowest Emission Vehicle: {best['Model']} → {best['CO2 Emissions(g/km)']} g/km")
st.info(f" Average CO₂ Emissions: {avg:.2f} g/km")
