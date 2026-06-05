import pandas as pd
import numpy as np

np.random.seed(24)

lokasi_kampus = ['Gerbang_Utama', 'Gedung_Kuliah_Umum', 'Laboratorium_Teknik', 'Asrama_Mahasiswa', 'Kantin_Pusat', 'Embung_Kampus']
n_titik = len(lokasi_kampus)

matriks_jarak = np.array([
    [0, 300, 500, 800, 600, 900],   
    [300, 0, 200, 600, 400, 700],   
    [500, 200, 0, 500, 300, 600],   
    [800, 600, 500, 0, 400, 400],   
    [600, 400, 300, 400, 0, 300],   
    [900, 700, 600, 400, 300, 0]    
])

status_sensor_iot = {
    'Lokasi': lokasi_kampus,
    'Volume_Sampah (%)': np.random.randint(40, 100, n_titik),
    'Jenis_Dominan': np.random.choice(['Organik', 'Anorganik'], n_titik)
}

df_iot = pd.DataFrame(status_sensor_iot)
df_iot.loc[0, 'Volume_Sampah (%)'] = 0  

print("=== SMART CAMPUS WASTE LOGISTICS ENGINE ===")
print("Berhasil menerima data telemetri sensor IoT Real-Time:\n")
print(df_iot.to_string(index=False))
print("\n" + "-"*50 + "\n")

titik_wajib_angkut = df_iot[df_iot['Volume_Sampah (%)'] >= 70]['Lokasi'].tolist()

if 'Gerbang_Utama' not in titik_wajib_angkut:
    titik_wajib_angkut.insert(0, 'Gerbang_Utama')

print(f"Titik Kritis Terdeteksi (Volume >= 70%): {len(titik_wajib_angkut)-1} Lokasi.")

rute_optimal = ['Gerbang_Utama']
titik_sekarang = 'Gerbang_Utama'
total_jarak_tempuh = 0

Kunjungan = [t for t in titik_wajib_angkut if t != 'Gerbang_Utama']

while Kunjungan:
    idx_sekarang = lokasi_kampus.index(titik_sekarang)
    jarak_terdekat = float('inf')
    titik_terdekat = None
    
    for kandidat in Kunjungan:
        idx_kandidat = lokasi_kampus.index(kandidat)
        jarak = matriks_jarak[idx_sekarang][idx_kandidat]
        if jarak < jarak_terdekat:
            jarak_terdekat = jarak
            titik_terdekat = kandidat
            
    total_jarak_tempuh += jarak_terdekat
    rute_optimal.append(titik_terdekat)
    titik_sekarang = titik_terdekat
    Kunjungan.remove(titik_terdekat)

idx_akhir = lokasi_kampus.index(titik_sekarang)
total_jarak_tempuh += matriks_jarak[idx_akhir][0]
rute_optimal.append('Gerbang_Utama')

print("\n--- RUTE PENGANGKUTAN OPTIMAL HARI INI ---")
for i, lokasi in enumerate(rute_optimal):
    if i == len(rute_optimal) - 1:
        print(f"{lokasi}")
    else:
        print(f"{lokasi} -> ", end="")

print(f"\nTotal Efisiensi Jarak Tempuh: {total_jarak_tempuh} Meter")