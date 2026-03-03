# 📊 HR Attrition Analytics Dashboard

### End-to-End Data Science & Machine Learning Project

## 📌 Project Overview

Proyek ini merupakan implementasi **end-to-end data science workflow** untuk menganalisis dan memprediksi attrition karyawan menggunakan pendekatan:

* Exploratory Data Analysis (EDA)
* Feature Engineering & Encoding
* Machine Learning (XGBoost Classifier)
* Interactive Dashboard menggunakan Streamlit

Tujuan utama proyek ini adalah:

1. Mengidentifikasi faktor utama penyebab attrition
2. Membangun model prediksi risiko resign
3. Menyediakan dashboard interaktif sebagai decision-support system bagi HR

---

## 📂 Dataset

Dataset yang digunakan: https://github.com/dicodingacademy/dicoding_dataset/tree/main/employee

Setelah preprocessing:

* Total data modeling: **1.058 karyawan**
* Attrition rate: **16.9%**
* Jumlah fitur: 30+ variabel HR (usia, job level, overtime, satisfaction, dll.)

Tahapan data preparation meliputi:

* Drop missing target (Attrition NaN)
* Drop kolom konstan (EmployeeCount, StandardHours, Over18, EmployeeId)
* Label Encoding untuk variabel kategorikal
* Stratified Train-Test Split (80:20)

---

## 🤖 Machine Learning Model

Model yang digunakan: **XGBoost Classifier**

Konfigurasi utama:

* 500 trees
* max_depth = 3
* learning_rate = 0.01
* scale_pos_weight untuk menangani class imbalance
* Evaluasi menggunakan ROC-AUC

Model menghasilkan performa:

* ROC-AUC ≈ **0.80**
* Threshold prediksi: **0.4**
* Output: Probability + Risk Level (Low / Medium / High)

Model dapat digunakan sebagai **early warning system** untuk mendeteksi karyawan berisiko resign.

---

## 📊 Dashboard Architecture

Dashboard dibangun menggunakan **Streamlit (Multipage App)** dengan struktur:

```
PROYEK1/
│
├── Dashboard/
│   ├── .streamlit/
│   │   └── config.toml
│   │
│   ├── data/
│   │   └── employee_data.csv
│   │
│   ├── pages/
│   │   ├── 1_Overview.py
│   │   ├── 2_Faktor_Utama.py
│   │   └── 3_Faktor_Lanjutan.py
│   │
│   ├── app.py
│   └── requirements.txt
│
├── data/
│   └── employee_data.csv
│
├── model/
│   ├── model.pkl
│   ├── feature_names.pkl
│   └── label_maps.pkl
│
├── notebook.ipynb
├── prediction.py
├── README.md
└── requirements.txt
```

---

### Fitur Utama Dashboard

* Global filter (Department, Gender, Job Role)
* KPI Summary (Total, Attrition Rate, Resign, Aktif)
* Distribusi attrition (Donut + Bar Chart)
* Analisis faktor utama:

  * OverTime
  * StockOptionLevel
  * JobLevel
  * Age Group
  * Total Working Years
  * Marital Status
* Analisis faktor lanjutan:

  * Environment Satisfaction
  * Job Involvement
  * Relationship Satisfaction
* Visualisasi interaktif berbasis Plotly

---

# 🚀 Installation & Usage Guide

## 1️⃣ Clone Repository

```bash
git clone <repository-url>
cd PROYEK1
```

---

## 2️⃣ Install Dependencies

Jika ingin menjalankan **seluruh project (notebook + model + dashboard)**:

```bash
pip install -r requirements.txt
```

Jika hanya ingin menjalankan dashboard saja:

```bash
cd Dashboard
pip install -r requirements.txt
```

---

# ▶️ Menjalankan Notebook (EDA & Training Model)

Jalankan dengan:

```bash
jupyter notebook
```

Lalu buka file:

```
notebook.ipynb
```

---

# 🤖 Menjalankan Script Prediksi Individual

File: `prediction.py`

Jalankan dengan:

```bash
python prediction.py
```

---

# 📊 Menjalankan Dashboard

Masuk ke folder Dashboard:

```bash
cd Dashboard
streamlit run app.py
```

---

## 🎯 Project Scope

Proyek ini mencakup:

* Business understanding
* Data exploration
* Modeling
* Evaluation
* Deployment ke dashboard interaktif

Pendekatan ini memungkinkan HR berpindah dari analisis deskriptif menjadi analisis prediktif berbasis data.

---

## 📊 Konteks Bisnis

Perusahaan saat ini memiliki **1.058 karyawan**, dengan **attrition rate sebesar 16,9%** (179 karyawan resign).

Artinya, hampir **1 dari setiap 6 karyawan meninggalkan perusahaan**, yang berpotensi berdampak pada:

* Biaya rekrutmen
* Biaya onboarding dan pelatihan
* Penurunan produktivitas tim
* Gangguan stabilitas organisasi

Melalui model machine learning XGBoost (ROC-AUC: 0.805), faktor-faktor utama penyebab attrition berhasil diidentifikasi dan diterjemahkan menjadi rencana aksi strategis.

---

# 🔥 Prioritas 1 — Kendalikan Beban Kerja & Lembur (Dampak Cepat)

### 📊 Insight Utama

* Tanpa lembur → 10,8% attrition
* Dengan lembur → 31,9% attrition
* Faktor paling berpengaruh dalam model

### 🎯 Aksi Strategis

* Menerapkan kebijakan batas maksimal lembur
* Melakukan rebalancing tenaga kerja pada divisi bertekanan tinggi (misalnya Sales)
* Monitoring workload secara rutin melalui dashboard
* Otomatisasi pekerjaan repetitif jika memungkinkan

### 💼 Dampak yang Diharapkan

Mengurangi burnout dan meningkatkan work-life balance, sehingga menurunkan risiko resign secara signifikan.

---

# 💰 Prioritas 2 — Perkuat Strategi Kompensasi Jangka Panjang

### 📊 Insight Utama

* Tanpa stock option → 25,7% attrition
* Level stock option lebih tinggi → ~7,3% attrition

### 🎯 Aksi Strategis

* Memperluas cakupan program stock option
* Memberikan retention bonus bagi karyawan berperforma tinggi
* Menyusun skema insentif jangka panjang berbasis masa kerja

### 💼 Dampak yang Diharapkan

Meningkatkan rasa kepemilikan terhadap perusahaan dan memperkuat loyalitas karyawan.

---

# 👶 Prioritas 3 — Lindungi Karyawan di Fase Awal Karier

Attrition terkonsentrasi pada karyawan tahap awal.

### 📊 Insight Pendukung

* Usia 18–25 tahun → 37,2% attrition
* Pengalaman kerja 0–2 tahun → 42,7% attrition
* Job Level 1 → 27,4% attrition

### 🎯 Aksi Strategis

* Program retensi 6 bulan pertama
* Check-in engagement pada hari ke-30, 60, dan 90
* Sistem mentoring & buddy system
* Jalur percepatan karier yang jelas

### 💼 Dampak yang Diharapkan

Mengurangi lonjakan attrition pada 2 tahun pertama masa kerja.

---

# 💍 Prioritas 4 — Segmentasi Tenaga Kerja Secara Strategis

### 📊 Insight

* Single → 26,7% attrition
* Married → 13,4%
* Divorced → 9,5%

Karyawan yang belum menikah menunjukkan mobilitas karier yang lebih tinggi.

### 🎯 Aksi Strategis

* Program mobilitas karier internal
* Rotasi jabatan internal
* Dukungan pengembangan diri dan pelatihan

### 💼 Dampak yang Diharapkan

Mengubah karyawan dengan mobilitas tinggi menjadi talenta internal yang berkembang dalam perusahaan.

---

# 🌿 Prioritas 5 — Tingkatkan Lingkungan Kerja & Engagement

### 📊 Temuan Utama

* Environment Satisfaction rendah → 27,3% attrition
* Job Involvement rendah → 40% attrition
* Relationship Satisfaction rendah → 22,9% attrition

### 🎯 Aksi Strategis

* Pengembangan kemampuan leadership bagi manajer
* Survey kepuasan karyawan secara rutin
* Evaluasi performa manajer dikaitkan dengan retensi tim
* Program psychological safety dan team building

### 💼 Dampak yang Diharapkan

Meningkatkan keterikatan emosional karyawan terhadap organisasi.

---

# 🤖 Sistem Prediksi Retensi (Transformasi HR Berbasis Data)

Model XGBoost yang telah dibangun memungkinkan:

* Skoring risiko resign per individu
* Early warning system untuk HR
* Intervensi proaktif sebelum resign terjadi

### Rencana Implementasi

* Integrasi model ke dashboard HR
* Monitoring risiko resign secara bulanan
* Laporan otomatis untuk karyawan berisiko tinggi

Pendekatan ini mengubah strategi HR dari reaktif menjadi proaktif.

---

# 📈 Proyeksi Dampak Bisnis

Jika attrition berhasil diturunkan dari **16,9% menjadi 12%**, perusahaan dapat mencegah sekitar:

≈ 50 resign per tahun

Manfaat potensial:

* Pengurangan biaya rekrutmen
* Penghematan biaya onboarding dan pelatihan
* Stabilitas tim yang lebih baik
* Peningkatan produktivitas jangka panjang

---

# 🚀 Kesimpulan Strategis

Attrition bukan disebabkan oleh satu faktor tunggal, melainkan kombinasi dari:

* Beban kerja
* Sistem kompensasi
* Tahap karier
* Profil demografis
* Pengalaman dan lingkungan kerja

Dengan menggabungkan perbaikan operasional dan sistem prediktif berbasis data, perusahaan dapat secara sistematis menurunkan attrition dan meningkatkan keberlanjutan tenaga kerja.

---