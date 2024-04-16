import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from babel.numbers import format_currency
sns.set_theme(style='dark')

#Membaca semua csv file
all_month = pd.read_csv("all_month.csv")
correlation_df = pd.read_csv("correlation.csv")
jam_df = pd.read_csv("jam.csv")
all_day = pd.read_csv("all_day.csv")
all_day_station = pd.read_csv("all_day_station.csv")
all_year = pd.read_csv("all_year.csv")

# Konversi string 'date_str' menjadi objek datetime
all_day["date"] = pd.to_datetime(all_day["date"])

#Membuat filter datetime
min_date = all_day["date"].min()
max_date = all_day["date"].max()
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("Beijing.jpg")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu Untuk Tren Harian dan Tren Stasiun',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

#bikin main_df yang udah terfilter ceritanya
main_df = all_day[(all_day["date"] >= str(start_date)) & 
                (all_day["date"] <= str(end_date))]


#membuat header
st.header("Analysis of Air Quality Data At Stations In Beijing")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Harian", "Bulanan", "Tahunan", "Jam", "Stasiun", "Korelasi"])

variables = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "WSPM"]
colors = ["#B06286", "#B07562", "#AAB062", "#497F3B", "#7F3B3B", "#3C6F8F", "#CD771A", "#C92E2E", "#487C60"]
PM25_ = " PM2.5 adalah partikel dengan diameter aerodinamis sama atau kurang dari 2,5μm. Menurut WHO, konsentrasi PM2.5 yang baik adalah <= 15μg/m³"
PM10_ = "PM10 adalah partikel dengan diameter aerodinamis sama atau kurang dari 10μm. Menurut WHO, konsentrasi PM10 yang baik adalah <= 45μg/m³"
SO2_ = "Menurut WHO, konsentrasi sulfur dioksida (SO2) yang baik adalah <= 40 µg/m³"
NO2_ = "Menurut WHO, konsentrasi Nitrogen DIoksida adalah <= 100 µg/m³"
CO_ = "Menurut WHO, kosentrasi Karbon Monoksida (CO) adalah <= 4000µg/m³"
O3_ = "Menurut WHO, konsentrasi Ozone (O3) yang baik adalah <= 100μg/m³"
penjelasan = {
    "PM2.5": PM25_,
    "PM10": PM10_,
    "SO2": SO2_,
    "NO2": NO2_,
    "CO": CO_,
    "O3": O3_
}

with tab1:
    st.header("Tren Harian")
    # Definisikan variabel dan warna yang sesuai

    # Loop untuk membuat plot untuk setiap variabel
    for variable, color in zip(variables, colors):
        st.subheader(f"Tren {variable} Harian")
        fig, ax = plt.subplots(figsize=(20, 8))
        ax.plot(
            main_df["date"],
            main_df[variable],
            marker='o', 
            linewidth=2,
            color=color  # Gunakan warna yang sesuai dengan variabel
        )
        ax.tick_params(axis='y', labelsize=20)
        ax.tick_params(axis='x', labelsize=15)
        ax.set_ylabel(f"{variable} (μg/m³)" if variable in ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
                    else f"{variable} dalam °C" if variable == "TEMP"
                    else f"{variable} dalam hPa" if variable == "PRES"
                    else f"{variable} dalam m/s", fontsize=20)
        st.pyplot(fig)
        if variable in ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]:
            with st.expander(f"Penjelasan mengenai {variable}"):
                st.write(penjelasan[variable])

 
with tab2:
    st.header(" Tren Bulanan")
    # Loop untuk membuat plot untuk setiap variabel
    for variable, color in zip(variables, colors):
        st.subheader(f"Tren {variable} Bulanan")
        fig, ax = plt.subplots(figsize=(18, 5))
        ax.plot(
            all_month["time"],
            all_month[variable],
            marker='o', 
            linewidth=2,
            color=color  # Gunakan warna yang sesuai dengan variabel
        )
        ax.tick_params(axis='y', labelsize=20)
        ax.tick_params(axis='x', labelsize=15, rotation=50)
        ax.set_ylabel(f"{variable} (μg/m³)" if variable in ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
                    else f"{variable} dalam °C" if variable == "TEMP"
                    else f"{variable} dalam hPa" if variable == "PRES"
                    else f"{variable} dalam m/s", fontsize=20)
        st.pyplot(fig)
        if variable in ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]:
            with st.expander(f"Penjelasan mengenai {variable}"):
                st.write(penjelasan[variable])

with tab3:
    variables = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    colors = ["#B06286", "#B07562", "#AAB062", "#497F3B", "#7F3B3B", "#3C6F8F"]
    for variable in variables:
        st.subheader(f"Rata-rata {variable} Tahunan")
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x=all_year["year"], y=all_year[variable], hue=all_year["year"], palette="viridis", legend=False)
        ax.set_ylabel(f"Rata-rata {variable} (μg/m³)" if variable in ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
                        else f"Rata-rata {variable} dalam °C" if variable == "TEMP"
                        else f"Rata-rata {variable} dalam hPa" if variable == "PRES"
                        else f"Rata-rata {variable} dalam m/s", fontsize=18)
        ax.set_xlabel("Tahun", fontsize=18)
        ax.tick_params(axis='y', labelsize=15)
        ax.tick_params(axis='x', labelsize=15)
        st.pyplot(fig)
        if variable in ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]:
            with st.expander(f"Penjelasan mengenai {variable}"):
                st.write(penjelasan[variable])

with tab5:
    # Konversi string 'date_str' menjadi objek datetime
    all_day_station["date"] = pd.to_datetime(all_day_station["date"])

    #bikin stations_df yang udah terfilter ceritanya
    stations_df = all_day_station[(all_day_station["date"] >= str(start_date)) & 
                    (all_day_station["date"] <= str(end_date))]

    # Menghitung rata-rata setiap variabel di setiap stasiun
    station_avg = stations_df.groupby('station')[variables].mean()

    # Membuat plot grafik bar untuk setiap variabel
    for variable in variables:
        st.subheader(f"Rata-rata {variable} di Setiap Stasiun")
        fig, ax = plt.subplots(figsize=(15, 5))
        sns.barplot(x=station_avg.index, y=station_avg[variable], hue=station_avg.index, palette="viridis", legend=False)
        ax.set_ylabel(f"Rata-rata {variable} (μg/m³)" if variable in ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
                        else f"Rata-rata {variable} dalam °C" if variable == "TEMP"
                        else f"Rata-rata {variable} dalam hPa" if variable == "PRES"
                        else f"Rata-rata {variable} dalam m/s", fontsize=15)
        ax.set_xlabel("Stasiun", fontsize=15)
        ax.tick_params(axis='y', labelsize=15)
        ax.tick_params(axis='x', labelsize=15, rotation=45)
        st.pyplot(fig)
        if variable in ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]:
            with st.expander(f"Penjelasan mengenai {variable}"):
                st.write(penjelasan[variable])

with tab4:
    variables = ["PM2.5", "PM10"]
    colors = ["#B06286", "#B07562"]
    penjelasan = {
        "PM2.5": PM25_,
        "PM10": PM10_,
    }
    # Loop untuk membuat plot untuk setiap variabel
    for variable, color in zip(variables, colors):
        st.subheader(f"Tren Polutan {variable} Per-Jam")
        fig, ax = plt.subplots(figsize=(18, 5))
        ax.plot(
            jam_df["hour_str"],
            jam_df[variable],
            marker='o', 
            linewidth=2,
            color=color  # Gunakan warna yang sesuai dengan variabel
        )
        ax.tick_params(axis='y', labelsize=20)
        ax.tick_params(axis='x', labelsize=15, rotation=50)
        ax.set_ylabel("{variable} (μg/m³)", fontsize=20)
        st.pyplot(fig)
        with st.expander(f"Penjelasan mengenai {variable}"):
            st.write(penjelasan[variable])


with tab6:
    st.subheader("Korelasi antara polutan dan variabel meteorologi")
    korelasi = correlation_df.corr(method = "pearson")
    # menampilkan grafik korelasi heatmap
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.heatmap(korelasi, vmax = 1, vmin = -1, center = 0, cmap = "plasma")
    ax.tick_params(labelsize = 15)
    st.pyplot(fig)