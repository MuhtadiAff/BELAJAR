import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Aplikasi Berita Cuaca", layout="centered")

st.title("🌤️ Aplikasi Berita Cuaca Real-Time")
st.markdown("Dapatkan informasi cuaca terkini berdasarkan lokasi Anda.")

# --- API Key OpenWeatherMap ---
API_KEY = "fcc307d141d54bc257328c6a486adcbd"  # Ganti dengan API key milikmu

# --- Input Lokasi ---
st.subheader("📍 Lokasi")
use_auto = st.checkbox("Gunakan lokasi otomatis (berdasarkan IP)")

if use_auto:
    try:
        ip_info = requests.get("https://ipinfo.io").json()
        coords = ip_info["loc"].split(",")
        lat, lon = float(coords[0]), float(coords[1])
        lokasi_kota = ip_info.get("city", "Tidak diketahui")
        st.success(f"Lokasi terdeteksi: {lokasi_kota}")
    except:
        st.error("Gagal mendapatkan lokasi otomatis. Gunakan input manual.")
        lat = st.number_input("Latitude", value=-6.2, format="%.6f")
        lon = st.number_input("Longitude", value=106.8, format="%.6f")
else:
    lat = st.number_input("Latitude", value=-6.2, format="%.6f")
    lon = st.number_input("Longitude", value=106.8, format="%.6f")

# --- Tampilkan Peta dengan Folium ---
st.subheader("🗺️ Lokasi pada Peta")
map = folium.Map(location=[lat, lon], zoom_start=10)
folium.Marker([lat, lon], tooltip="Lokasi Anda").add_to(map)
st_folium(map, width=700)

# --- Ambil Data Cuaca ---
st.subheader("🌦️ Informasi Cuaca")

weather_url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?lat={lat}&lon={lon}&units=metric&lang=id&appid={API_KEY}"
)

try:
    response = requests.get(weather_url)
    data = response.json()

    if response.status_code == 200:
        st.markdown(f"**Kota**: {data['name']}")
        st.markdown(f"**Suhu**: {data['main']['temp']} °C")
        st.markdown(f"**Kelembapan**: {data['main']['humidity']}%")
        st.markdown(f"**Angin**: {data['wind']['speed']} m/s")
        st.markdown(f"**Awan**: {data['clouds']['all']}%")
        rain = data.get("rain", {}).get("1h", 0)
        st.markdown(f"**Curah Hujan (1 jam)**: {rain} mm")
        st.markdown(f"**Kondisi Umum**: {data['weather'][0]['description'].title()}")
    else:
        st.error(f"Gagal mengambil data cuaca: {data.get('message', 'Tidak diketahui')}")

except Exception as e:
    st.error(f"Terjadi kesalahan saat mengambil data cuaca: {e}")
