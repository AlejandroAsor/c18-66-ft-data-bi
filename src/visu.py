import streamlit as st

# Menú desplegable
st.sidebar.header("🔧 Top Skills")
options = ["Top Skills", "Skills Trend", "Skills Pay", "Job Salaries", "About", "Health"]
selection = st.sidebar.radio("Select Option", options)

# Filtrar datos (ejemplo)
st.sidebar.header("🔧 Filters")
data_skills = st.sidebar.radio("Data Skills:", ["Top 25", "All"])
timeframe = st.sidebar.radio("Timeframe:", ["All Time", "Last 7 days", "Last 30 days", "YTD (2024)"])

# Título de la página
st.title("🔧 Top Skills for Data Nerds 🤓")

# Contenido principal basado en la selección
if selection == "Top Skills":
    st.subheader("Top Skills")
    st.write("Contenido para Top Skills")
elif selection == "Skills Trend":
    st.subheader("Skills Trend")
    st.write("Contenido para Skills Trend")
elif selection == "Skills Pay":
    st.subheader("Skills Pay")
    st.write("Contenido para Skills Pay")
elif selection == "Job Salaries":
    st.subheader("Job Salaries")
    st.write("Contenido para Job Salaries")
elif selection == "About":
    st.subheader("About")
    st.write("Contenido para About")
elif selection == "Health":
    st.subheader("Health")
    st.write("Contenido para Health")

# Ejemplo de gráfico de barras
import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Skill": ["Python", "SQL", "AWS", "Azure", "Spark", "R", "Tableau", "Java", "Excel", "Power BI"],
    "Percentage": [55.6, 54.4, 24.8, 21.0, 20.0, 17.8, 17.1, 14.9, 13.1, 11.9],
}

df = pd.DataFrame(data)

fig, ax = plt.subplots()
ax.barh(df["Skill"], df["Percentage"], color="#1E90FF")
ax.set_xlabel("Percentage", color=st.session_state.theme["text"])
ax.set_title("Top Skills", color=st.session_state.theme["text"])

st.pyplot(fig)
