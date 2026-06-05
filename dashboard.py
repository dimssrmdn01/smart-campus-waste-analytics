import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Smart Campus Waste Logistics", layout="wide", page_icon="♻️")

np.random.seed(24)

lokasi_kampus = ['Gerbang_Utama', 'Gedung_Kuliah_Umum', 'Laboratorium_Teknik', 'Asrama_Mahasiswa', 'Kantin_Pusat', 'Embung_Kampus']
koordinat_lat = [-5.3562, -5.3578, -5.3592, -5.3610, -5.3585, -5.3625]
koordinat_lon = [105.3112, 105.3144, 105.3128, 105.3155, 105.3160, 105.3105]
n_titik = len(lokasi_kampus)

matriks_jarak = np.zeros((n_titik, n_titik))
for i in range(n_titik):
    for j in range(n_titik):
        if i != j:
            matriks_jarak[i][j] = np.sqrt((koordinat_lat[i] - koordinat_lat[j])**2 + (koordinat_lon[i] - koordinat_lon[j])**2) * 111000

st.title("♻️ Smart Campus Waste Analytics Dashboard")
st.subheader("Sistem Optimasi Logistik & Monitoring IoT Real-Time (Sektor Kampus ITERA)")
st.write("---")

st.sidebar.header("🎛️ Panel Kontrol Simulasi Sensor")
threshold = st.sidebar.slider("Ambang Batas Kritis Ketinggian (%)", min_value=50, max_value=90, value=70)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📊 Status Kapasitas Tempat Sampah")
    
    volumes = []
    jenis_list = []
    for i, lokasi in enumerate(lokasi_kampus):
        if lokasi == 'Gerbang_Utama':
            volumes.append(0)
            jenis_list.append('Pool Utama')
        else:
            vol = st.sidebar.slider(f"Volume {lokasi} (%)", 0, 100, int(np.random.randint(40, 100)))
            volumes.append(vol)
            jenis_list.append(np.random.choice(['Organik', 'Anorganik']))
            
    df_iot = pd.DataFrame({
        'Lokasi': lokasi_kampus,
        'Latitude': koordinat_lat,
        'Longitude': koordinat_lon,
        'Volume_Sampah (%)': volumes,
        'Jenis_Dominan': jenis_list
    })
    
    st.dataframe(df_iot, use_container_width=True)
    
    titik_wajib_angkut = df_iot[df_iot['Volume_Sampah (%)'] >= threshold]['Lokasi'].tolist()
    if 'Gerbang_Utama' not in titik_wajib_angkut:
        titik_wajib_angkut.insert(0, 'Gerbang_Utama')
        
    st.metric(label="🚨 Jumlah Titik Kritis Pengangkutan", value=f"{len(titik_wajib_angkut)-1} / {n_titik-1}")

with col2:
    st.markdown("### 🗺️ Peta Panduan Rute Operasional Truk")
    
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
    
    df_rute = pd.DataFrame([df_iot[df_iot['Lokasi'] == loc].iloc[0] for loc in rute_optimal])
    
    fig = px.scatter_mapbox(df_iot, lat="Latitude", lon="Longitude", text="Lokasi",
                            color="Volume_Sampah (%)", size="Volume_Sampah (%)",
                            color_continuous_scale=px.colors.sequential.OrRd, size_max=15, zoom=14.5)
    
    fig.add_trace(px.line_mapbox(df_rute, lat="Latitude", lon="Longitude").data[0])
    fig.update_traces(line=dict(color="cyan", width=4))
    
    fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}, height=450)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info(f"🛣️ **Urutan Rute Pengumpulan:** {' ➔ '.join(rute_optimal)}")
    st.success(f"⛽ **Total Estimasi Jarak Tempuh Efisien:** {round(total_jarak_tempuh, 2)} Meter")