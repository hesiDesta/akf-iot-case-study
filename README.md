# Studi Kasus: Pipeline IoT Smart Farming di ASEAN-Korea HPC Facility (AKF)

> Catatan: materi rapat AKF berisi kebijakan penggunaan fasilitas HPC, bukan konten IoT.
> Studi kasus ini adalah **skenario penerapan** yang menyesuaikan pipeline IoT dengan aturan AKF.

## 1. Skenario
Jaringan sensor (ESP32 + DHT22 + soil moisture) memantau kebun. Data dikirim ke gateway,
dianonimisasi, lalu dilatih model deteksi anomali di HPC AKF sebagai job batch.

## 2. Pemetaan Aturan AKF -> Desain

| Ketentuan AKF | Penerapan di proyek |
|---|---|
| Penelitian damai / non-komersial / inovasi terapan | Riset smart farming, termasuk inovasi terapan |
| Kredensial tidak boleh dibagikan | Satu akun per anggota, tidak ada akun bersama di slurm script |
| Wajib batch scheduler | `slurm/train.slurm`, tanpa menjalankan job berat di login node |
| Software legal | Hanya library open source (lihat `requirements.txt`) |
| Data pribadi wajib anonimisasi (UU PDP) | `src/anonymize.py`: hash node ID, buang lokasi/pemilik |
| Data dihapus 90 hari setelah proyek | Simpan salinan di storage sendiri; rencanakan backup sebelum hari ke-90 |
| Timeline proyek wajib saat daftar | Lihat bagian 5 |
| Acknowledgement di output | Lihat bagian 6 |
| PI harus warga/afiliasi institusi ASEAN | Syarat pengusul proposal di ELSA AKF |

## 3. Arsitektur
```
[ESP32 sensor] -> [Gateway lokal] -> data/sensors.csv
      -> anonymize.py -> [HPC AKF: sbatch train.slurm] -> models/isoforest.joblib
      -> (unduh model) -> inferensi di gateway/edge
```

## 4. Cara Menjalankan (lokal)
```bash
pip install -r requirements.txt
python src/simulate_sensors.py --nodes 5 --days 60
python src/anonymize.py data/sensors.csv data/sensors_anon.csv
python src/train_anomaly.py
```
Di HPC (setelah akun aktif via ELSA AKF): `sbatch slurm/train.slurm`

## 5. Timeline Contoh (untuk proposal)
| Minggu | Kegiatan |
|---|---|
| 1-2 | Pemasangan sensor, pengumpulan data |
| 3 | Anonimisasi & validasi data |
| 4-6 | Training/tuning di HPC |
| 7 | Evaluasi & pelaporan |
| 8-20 | Backup data/model (batas 90 hari setelah proyek selesai) |

## 6. Acknowledgement (contoh)
"This work was supported by the ASEAN-Korea HPC Facility in Indonesia."

## 7. Ide Pengembangan
- Ganti IsolationForest dengan LSTM/Autoencoder (butuh GPU)
- MQTT broker + dashboard Grafana
- Edge inference di ESP32 (TinyML)
