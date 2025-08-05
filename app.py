import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# --- API Key OpenWeatherMap ---
API_KEY = "fcc307d141d54bc257328c6a486adcbd"  # Ganti dengan API key kamu

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Cuaca Berdasarkan Kota atau Titik Peta", layout="centered")
st.title("🌦️ Aplikasi Cuaca Real-Time")
st.markdown("Masukkan nama kota atau klik titik pada peta untuk melihat cuaca saat ini.")

# --- Opsi input ---
option = st.radio("Pilih metode pencarian:", ["Ketik Nama Kota", "Klik Titik di Peta"])

lat, lon, lokasi_label = None, None, ""

# --- Input nama kota ---
if option == "Ketik Nama Kota":
    city_name = st.text_input("Masukkan nama kota", value="Jakarta")

    if city_name:
        # Ambil koordinat kota dari OpenWeatherMap Geocoding API
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
        geo_res = requests.get(geo_url).json()
        if geo_res:
            lat = geo_res[0]['lat']
            lon = geo_res[0]['lon']
            lokasi_label = f"{geo_res[0]['name']}, {geo_res[0]['country']}"
        else:
            st.error("Kota tidak ditemukan.")

# --- Klik titik pada peta ---
elif option == "Klik Titik di Peta":
    st.markdown("Klik di peta untuk memilih lokasi.")
    default_location = [-6.2, 106.8]  # Jakarta
    m = folium.Map(location=default_location, zoom_start=5)

    # Tambahkan fitur klik
    m.add_child(folium.LatLngPopup())
    output = st_folium(m, height=450, width=700)

    # Ambil lat/lon dari hasil klik
    if output.get("last_clicked"):
        lat = output["last_clicked"]["lat"]
        lon = output["last_clicked"]["lng"]
        lokasi_label = f"Koordinat: ({lat:.4f}, {lon:.4f})"

# --- Tampilkan cuaca jika ada lat/lon ---
if lat is not None and lon is not None:
    st.subheader("🌤️ Informasi Cuaca")
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&units=metric&lang=id&appid={API_KEY}"
    )
    try:
        response = requests.get(weather_url)
        data = response.json()

        if response.status_code == 200:
            st.markdown(f"**Lokasi**: {lokasi_label}")
            st.markdown(f"**Suhu**: {data['main']['temp']} °C")
            st.markdown(f"**Kelembapan**: {data['main']['humidity']}%")
            st.markdown(f"**Angin**: {data['wind']['speed']} m/s")
            st.markdown(f"**Awan**: {data['clouds']['all']}%")
            rain = data.get("rain", {}).get("1h", 0)
            st.markdown(f"**Curah Hujan (1 jam)**: {rain} mm")
            st.markdown(f"**Kondisi**: {data['weather'][0]['description'].title()}")
        else:
            st.error(f"Gagal mengambil data cuaca: {data.get('message', 'Tidak diketahui')}")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
