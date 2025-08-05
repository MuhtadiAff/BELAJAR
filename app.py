import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- API Key ---
API_KEY = "fcc307d141d54bc257328c6a486adcbd"  # Ganti dengan milikmu

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Aplikasi Cuaca Lengkap", layout="centered")
st.title("🌦️ Aplikasi Cuaca Real-Time dan Prakiraan")
st.markdown("Masukkan nama kota atau klik di peta untuk melihat cuaca dan grafik prakiraan.")

# --- Pilih Metode Lokasi ---
option = st.radio("Pilih metode lokasi:", ["Ketik Nama Kota", "Klik Peta"])

lat, lon, lokasi_label = None, None, ""

# --- Input Manual Nama Kota ---
if option == "Ketik Nama Kota":
    city_name = st.text_input("Masukkan nama kota", value="Jakarta")
    if city_name:
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
        geo_res = requests.get(geo_url).json()
        if geo_res:
            lat = geo_res[0]['lat']
            lon = geo_res[0]['lon']
            lokasi_label = f"{geo_res[0]['name']}, {geo_res[0]['country']}"
        else:
            st.error("Kota tidak ditemukan.")

# --- Klik Peta ---
elif option == "Klik Peta":
    st.markdown("Klik di peta untuk memilih lokasi.")
    default_location = [-6.2, 106.8]
    m = folium.Map(location=default_location, zoom_start=5)
    m.add_child(folium.LatLngPopup())
    output = st_folium(m, height=450, width=700)
    if output.get("last_clicked"):
        lat = output["last_clicked"]["lat"]
        lon = output["last_clicked"]["lng"]
        lokasi_label = f"Koordinat: ({lat:.4f}, {lon:.4f})"

# --- Ambil & Tampilkan Data Cuaca ---
if lat is not None and lon is not None:
    st.subheader("📍 Lokasi")
    st.markdown(f"**{lokasi_label}**")

    # --- Cuaca Saat Ini ---
    st.subheader("☁️ Cuaca Saat Ini")
    current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=id&appid={API_KEY}"
    try:
        res = requests.get(current_url)
        data = res.json()
        if res.status_code == 200:
            st.markdown(f"**Suhu:** {data['main']['temp']} °C")
            st.markdown(f"**Kelembapan:** {data['main']['humidity']}%")
            st.markdown(f"**Angin:** {data['wind']['speed']} m/s")
            st.markdown(f"**Kondisi:** {data['weather'][0]['description'].title()}")
        else:
            st.error(data.get("message", "Gagal mengambil data cuaca"))
    except Exception as e:
        st.error(f"Error: {e}")

    # --- Prakiraan Cuaca 5 Hari / 3 Jam ---
    st.subheader("📅 Prakiraan Cuaca 5 Hari (tiap 3 jam)")
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&lang=id&appid={API_KEY}"
    try:
        res = requests.get(forecast_url)
        forecast_data = res.json()
        if res.status_code == 200:
            # Konversi ke DataFrame
            df = pd.DataFrame(forecast_data['list'])
            df['waktu'] = pd.to_datetime(df['dt'], unit='s')
            df['suhu'] = df['main'].apply(lambda x: x['temp'])
            df['hujan'] = df['rain'].apply(lambda x: x.get('3h', 0) if isinstance(x, dict) else 0)

            # Pilih tanggal
            tanggal_uni_
