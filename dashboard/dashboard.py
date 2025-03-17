import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Load dataset
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])  # Convert to datetime
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")
year_filter = st.sidebar.multiselect("Pilih Tahun:", df['yr'].unique(), default=df['yr'].unique())
month_filter = st.sidebar.multiselect("Pilih Bulan:", df['mnth'].unique(), default=df['mnth'].unique())
season_filter = st.sidebar.multiselect("Pilih Musim:", df['season'].unique(), default=df['season'].unique())

df_filtered = df[(df['yr'].isin(year_filter)) & (df['mnth'].isin(month_filter)) & (df['season'].isin(season_filter))]

# About Section in Sidebar
st.sidebar.markdown("## About")
st.sidebar.markdown("Developed by [M. Fakhrizal Nur A](https://github.com/MFakhrizalNA)  ")
st.sidebar.markdown("Connect on [LinkedIn](https://www.linkedin.com/in/m-fakhrizal-nur-athoilah/)")

# Visualisasi Jumlah Penyewa
st.title("📊Visualisasi Bike Sharing🚴‍♂️")
fig = px.line(df_filtered, x='dteday', y='cnt', title='Tren Penyewaan Sepeda', labels={'cnt': 'Jumlah Penyewa'})
st.plotly_chart(fig)

# Visualisasi Pengaruh Musim dan Kondisi Cuaca terhadap Penyewaan Sepeda
season_weather = df_filtered.groupby(["season", "weathersit"])['cnt'].mean().reset_index()
fig2 = px.bar(season_weather, x="season", y="cnt", color="weathersit", 
              title="Pengaruh Musim dan Kondisi Cuaca terhadap Penyewaan Sepeda",
              labels={"cnt": "Rata-rata Penyewaan Sepeda", "season": "Musim", "weathersit": "Kondisi Cuaca"},
              barmode='group', color_discrete_sequence=px.colors.qualitative.Set1)
st.plotly_chart(fig2)

# Visualisasi Pola Penggunaan Sepeda Berdasarkan Jam dan Hari dalam Seminggu
hour_weekday = df_filtered.pivot_table(values='cnt', index='hr', columns='weekday', aggfunc=np.mean)
fig3 = px.imshow(hour_weekday, aspect='auto', color_continuous_scale='rdylbu',
                 title="Pola Penggunaan Sepeda Berdasarkan Jam dan Hari dalam Seminggu", 
                 labels={'x': 'Hari dalam Seminggu', 'y': 'Jam', 'color': 'Jumlah Penyewa'})
fig3.update_xaxes(tickmode='array', tickvals=list(range(7)), ticktext=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"])
st.plotly_chart(fig3)

# Visualisasi Tren Penyewaan Sepeda Berdasarkan Hari dalam Satu Tahun
daily_trend = df_filtered.groupby("dteday")["cnt"].sum().reset_index()
daily_trend["rolling_avg"] = daily_trend["cnt"].rolling(window=7).mean()

fig4 = px.line(daily_trend, x="dteday", y="rolling_avg", title="Tren Penyewaan Sepeda Berdasarkan Hari dalam Satu Tahun",
               labels={"rolling_avg": "Total Penyewaan Sepeda", "dteday": "Tanggal"},
               line_shape='linear', color_discrete_sequence=["navy"])
fig4.update_xaxes(tickangle=30, tickformat="%Y-%m")
st.plotly_chart(fig4)

# Visualisasi Persentase Penyewaan Sepeda: Hari Kerja vs. Hari Libur
workday_trend = df_filtered.groupby("workingday")["cnt"].sum().reset_index()
labels = ["Hari Libur", "Hari Kerja"]
fig5 = px.pie(workday_trend, values="cnt", names=labels, title="Persentase Penyewaan Sepeda: Hari Kerja vs. Hari Libur",
              color_discrete_sequence=["#ff9999", "#66b3ff"])
st.plotly_chart(fig5)

# Footer
st.markdown("---")
st.markdown("© 2025 M. Fakhrizal Nur Athoilah . All Rights Reserved.")