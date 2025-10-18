import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Gunakan backend non-GUI (agar bisa jalan di server tanpa GUI)
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template

# ==================================================
# I. KONFIGURASI FLASK & DATA
# ==================================================
app = Flask(__name__)

DATA_FILE = 'dataset_automobile_cleaned.csv'
IMAGE_DIR = os.path.join('static', 'images')

# Pastikan direktori gambar tersedia
os.makedirs(IMAGE_DIR, exist_ok=True)

# Memuat dataset
try:
    df = pd.read_csv(DATA_FILE)
    print("✅ Data berhasil dimuat!")
except FileNotFoundError:
    print(f"⚠️ ERROR: File '{DATA_FILE}' tidak ditemukan. Pastikan file ada di direktori yang sama.")
    df = None


# ==================================================
# II. FUNGSI VISUALISASI (6 PLOT)
# ==================================================
def create_visualization():
    """Membuat dan menyimpan enam visualisasi ke folder static/images."""
    if df is None:
        print("⚠️ Tidak ada data untuk divisualisasikan.")
        return

    # 1. Bar Chart Rata-rata Harga per Merek
    mean_price_by_make = df.groupby('make')['price'].mean().sort_values(ascending=False)
    plt.figure(figsize=(14, 8))
    sns.barplot(x=mean_price_by_make.index, y=mean_price_by_make.values, palette='viridis')
    plt.title('01. Rata-rata Harga Mobil Berdasarkan Merek (Semua Merek)')
    plt.xlabel('Merek Mobil')
    plt.ylabel('Rata-rata Harga (USD)')
    plt.xticks(rotation=60, ha='right', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '01_avg_price_by_make.png'))
    plt.close()

    # 2. Box Plot Harga vs. Body Style
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='body-style', y='price', data=df)
    plt.title('02. Distribusi Harga Mobil Berdasarkan Tipe Bodi')
    plt.xlabel('Tipe Bodi')
    plt.ylabel('Harga (USD)')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '02_body_style_price_boxplot.png'))
    plt.close()

    # 3. Scatter Plot Harga vs. Horsepower
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='horsepower', y='price', data=df, hue='fuel-type', style='fuel-type', s=100)
    plt.title('03. Hubungan Horsepower dan Harga')
    plt.xlabel('Horsepower')
    plt.ylabel('Harga (USD)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '03_horsepower_price_scatterplot.png'))
    plt.close()

    # 4. Histogram Distribusi Harga
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], kde=True, bins=20, color='red')
    plt.title('04. Distribusi Frekuensi Harga Mobil')
    plt.xlabel('Harga (USD)')
    plt.ylabel('Frekuensi')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '04_price_distribution_histogram.png'))
    plt.close()

    # 5. Distribusi Konsumsi BBM (Highway-mpg)
    plt.figure(figsize=(8, 6))
    sns.histplot(df['highway-mpg'], kde=True, bins=15)
    plt.title('05. Distribusi Konsumsi BBM (Highway MPG)')
    plt.xlabel('Highway MPG')
    plt.ylabel('Frekuensi')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '05_highway_mpg_hist.png'))
    plt.close()

    # 6. Bar Chart Rata-rata Harga Berdasarkan Tipe Mesin
    mean_price_by_engine = df.groupby('engine-type')['price'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=mean_price_by_engine.index, y=mean_price_by_engine.values, palette='Blues_d')
    plt.title('06. Rata-rata Harga Berdasarkan Tipe Mesin')
    plt.xlabel('Tipe Mesin')
    plt.ylabel('Rata-rata Harga (USD)')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, '06_engine_type_mean_price.png'))
    plt.close()

    print("✅ Enam visualisasi berhasil dibuat dan disimpan di folder static/images.")


# ==================================================
# III. ROUTE FLASK
# ==================================================
@app.route('/')
def dashboard():
    """Menampilkan dashboard utama."""
    create_visualization()

    # Metrik utama
    if df is not None:
        key_metrics = [
            {'title': 'Total Data Mobil', 'value': f"{df.shape[0]} Unit", 'color': 'blue'},
            {'title': 'Rata-rata Harga', 'value': f"${df['price'].mean():,.0f}", 'color': 'green'},
            {'title': 'Rata-rata Horsepower', 'value': f"{df['horsepower'].mean():.1f} HP", 'color': 'red'},
            {'title': 'Rata-rata MPG (Highway)', 'value': f"{df['highway-mpg'].mean():.1f} MPG", 'color': 'orange'},
        ]
    else:
        key_metrics = []

    # Daftar plot
    plots = [
        {'title': '1. Rata-rata Harga Mobil Berdasarkan Merek', 'filename': '01_avg_price_by_make.png', 'span': 12},
        {'title': '2. Distribusi Harga Mobil berdasarkan Tipe Bodi', 'filename': '02_body_style_price_boxplot.png', 'span': 6},
        {'title': '3. Hubungan Horsepower dan Harga', 'filename': '03_horsepower_price_scatterplot.png', 'span': 6},
        {'title': '4. Distribusi Frekuensi Harga Mobil', 'filename': '04_price_distribution_histogram.png', 'span': 6},
        {'title': '5. Distribusi Konsumsi BBM (Highway MPG)', 'filename': '05_highway_mpg_hist.png', 'span': 6},
        {'title': '6. Rata-rata Harga Berdasarkan Tipe Mesin', 'filename': '06_engine_type_mean_price.png', 'span': 12},
    ]

    return render_template('index.html', key_metrics=key_metrics, plots=plots)


# ==================================================
# IV. JALANKAN SERVER
# ==================================================
if __name__ == '__main__':
    app.run(debug=True)
