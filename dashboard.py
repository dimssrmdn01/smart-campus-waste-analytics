import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Smart Campus Waste Logistics Pro", layout="wide", page_icon="♻️")

np.random.seed(24)

# 1. Setup Data Spasial Dasar Kampus
lokasi_kampus = ['Gerbang_Utama', 'Gedung_Kuliah_Umum', 'Laboratorium_Teknik', 'Asrama_Mahasiswa', 'Kantin_Pusat', 'Embung_Kampus']
koordinat_lat = [-5.3562, -5.3578, -5.3592, -5.3610, -5.3585, -5.3625]
koordinat_lon = [105.3112, 105.3144, 105.3128, 105.3155, 105.3160, 105.3105]
n_titik = len(lokasi_kampus)

# Menghitung matriks jarak antar koordinat (skala meter)
matriks_jarak = np.zeros((n_titik, n_titik))
for i in range(n_titik):
    for j in range(n_titik):
        if i != j:
            matriks_jarak[i][j] = np.sqrt((koordinat_lat[i] - koordinat_lat[j])**2 + (koordinat_lon[i] - koordinat_lon[j])**2) * 111000

st.title("♻️ Smart Campus Waste Analytics - PRO Version")
st.subheader("Sistem Optimasi Spasial, Prediksi Presisi, & Kalkulator Emisi Karbon")
st.write("---")

# 2. Sidebar Panel Kontrol
st.sidebar.header("🎛️ Panel Kontrol Sensor & Predictive Engine")
threshold = st.sidebar.slider("Ambang Batas Kritis Ketinggian (%)", min_value=50, max_value=90, value=70)

volumes = []
jenis_list = []
laju_isi = [] 

for lokasi in lokasi_kampus:
    if lokasi == 'Gerbang_Utama':
        volumes.append(0)
        jenis_list.append('Pool Utama')
        laju_isi.append(0.0)
    else:
        vol = st.sidebar.slider(f"Volume {lokasi} (%)", 0, 100, int(np.random.randint(40, 95)))
        volumes.append(vol)
        # Sektor padat (Kantin/Asrama) memiliki laju akumulasi sampah organik yang lebih tinggi
        if lokasi in ['Kantin_Pusat', 'Asrama_Mahasiswa', 'Gedung_Kuliah_Umum']:
            jenis = 'Organik'
            rate = np.random.uniform(7.0, 14.0) 
        else:
            jenis = 'Anorganik'
            rate = np.random.uniform(3.0, 6.5) 
        jenis_list.append(jenis)
        laju_isi.append(round(rate, 1))

# Konstruksi DataFrame IoT Terintegrasi
df_iot = pd.DataFrame({
    'Lokasi': lokasi_kampus,
    'Latitude': koordinat_lat,
    'Longitude': koordinat_lon,
    'Volume (%)': volumes,
    'Kategori': jenis_list,
    'Laju (%/Jam)': laju_isi
})

# 3. Engine Prediksi Waktu Penuh (Predictive Analytics)
jam_sisa = []
for idx, row in df_iot.iterrows():
    if row['Lokasi'] == 'Gerbang_Utama':
        jam_sisa.append("-")
    elif row['Volume (%)'] >= 100:
        jam_sisa.append("Penuh! 🚨")
    else:
        sisa_waktu = (100 - row['Volume (%)']) / row['Laju (%/Jam)']
        jam_sisa.append(f"{round(sisa_waktu, 1)} Jam")
df_iot['Estimasi Penuh'] = jam_sisa

# 4. Engine Optimasi Rute Logistik (Greedy TSP Algorithm)
titik_wajib_angkut = df_iot[df_iot['Volume (%)'] >= threshold]['Lokasi'].tolist()
if 'Gerbang_Utama' not in titik_wajib_angkut:
    titik_wajib_angkut.insert(0, 'Gerbang_Utama')

rute_optimal = ['Gerbang_Utama']
titik_sekarang = 'Gerbang_Utama'
total_jarak_tempuh = 0
kunjungan = [t for t in titik_wajib_angkut if t != 'Gerbang_Utama']

while kunjungan:
    idx_sekarang = lokasi_kampus.index(titik_sekarang)
    jarak_terdekat = float('inf')
    titik_terdekat = None
    for kandidat in kunjungan:
        idx_kandidat = lokasi_kampus.index(kandidat)
        jarak = matriks_jarak[idx_sekarang][idx_kandidat]
        if jarak < jarak_terdekat:
            jarak_terdekat = jarak
            titik_terdekat = kandidat
    total_jarak_tempuh += jarak_terdekat
    rute_optimal.append(titik_terdekat)
    titik_sekarang = titik_terdekat
    kunjungan.remove(titik_terdekat)

idx_akhir = lokasi_kampus.index(titik_sekarang)
total_jarak_tempuh += matriks_jarak[idx_akhir][0]
rute_optimal.append('Gerbang_Utama')

# 5. Engine ESG & Kalkulator Efisiensi Karbon
jarak_konvensional = 0
for i in range(n_titik):
    jarak_konvensional += matriks_jarak[i][(i+1)%n_titik]

jarak_dihemat = max(0.0, jarak_konvensional - total_jarak_tempuh)
efisiensi_persen = (jarak_dihemat / jarak_konvensional) * 100 if jarak_konvensional > 0 else 0
co2_dihemat = (jarak_dihemat / 1000) * 268.5  # Standar emisi truk sampah ringan: 268.5g CO2/km

# 6. Tata Letak Dashboard Visual (KPI Metrics)
m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label="🛣️ Jarak Operasional Dipangkas", value=f"{round(jarak_dihemat, 1)} Meter", delta=f"{round(efisiensi_persen, 1)}% Lebih Hemat")
with m2:
    st.metric(label="🌱 Emisi Karbon Dicegah", value=f"{round(co2_dihemat, 1)} Gram CO₂", delta="Dampak ESG Positif", delta_color="normal")
with m3:
    st.metric(label="🚨 Titik Kritis Pengangkutan", value=f"{len(titik_wajib_angkut)-1} / {n_titik-1} Lokasi", delta="Status Real-Time")

st.write("---")

# Layout Utama Grid Konten
col1, col2 = st.columns([1.2, 1.8])

with col1:
    st.markdown("### 📊 Telemetri Sensor & Inteligensi Prediktif")
    st.dataframe(df_iot[['Lokasi', 'Volume (%)', 'Kategori', 'Laju (%/Jam)', 'Estimasi Penuh']], use_container_width=True)
    st.info(f"📋 **Urutan Rute Tugas Pengemudi:**  \n{' ➔ '.join(rute_optimal)}")

with col2:
    st.markdown("### 🗺️ Visualisasi Jalur Spasial Truk Sampah")
    df_rute = pd.DataFrame([df_iot[df_iot['Lokasi'] == loc].iloc[0] for loc in rute_optimal])
    
    fig = px.scatter_mapbox(df_iot, lat="Latitude", lon="Longitude", text="Lokasi",
                            color="Volume (%)", size="Volume (%)",
                            color_continuous_scale=px.colors.sequential.YlOrRd, size_max=16, zoom=14.3)
    
    fig.add_trace(px.line_mapbox(df_rute, lat="Latitude", lon="Longitude").data[0])
    fig.update_traces(line=dict(color="#00FFCC", width=4))
    fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}, height=450)
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"ℹ️ Jarak rute efisien saat ini: {round(total_jarak_tempuh, 1)}m vs Jarak jika memutari seluruh titik: {round(jarak_konvensional, 1)}m.")