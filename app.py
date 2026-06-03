import streamlit as st
import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import re
import warnings

warnings.filterwarnings("ignore")

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="SPK Pemilihan Mobil Mewah",
    page_icon="",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .stApp { background-color: #0f1117; color: #f0f2f6; }
    [data-testid="stSidebar"] { background-color: #1a1d27 !important; border-right: 2px solid #e94560; }
    [data-testid="stSidebar"] * { color: #f0f2f6 !important; }
    [data-testid="stSidebar"] .stRadio label { color: #f0f2f6 !important; font-size: 0.95rem; }
    [data-testid="stSidebar"] hr { border-color: #3a3f55 !important; }
    .main-title {
        font-size: 2.2rem; font-weight: 800; color: #ffffff;
        text-align: center; padding: 1rem 0 0.3rem 0;
        text-shadow: 0 2px 8px rgba(233,69,96,0.4); letter-spacing: 0.5px;
    }
    .sub-title { font-size: 1.05rem; color: #b0b8d1; text-align: center; margin-bottom: 1.5rem; }
    .section-header {
        font-size: 1.15rem; font-weight: 700; color: #ffffff;
        border-left: 5px solid #e94560; padding-left: 0.7rem;
        margin: 1rem 0 0.7rem 0;
        background: linear-gradient(90deg, rgba(233,69,96,0.12) 0%, transparent 100%);
        padding-top: 0.3rem; padding-bottom: 0.3rem; border-radius: 0 6px 6px 0;
    }
    .card {
        background: #1e2235; border-radius: 10px; padding: 1rem 1.3rem;
        margin-bottom: 1rem; border: 1px solid #3a3f55; color: #e8eaf6;
    }
    .card strong { color: #ffffff; }
    .card small  { color: #b0b8d1; }
    .info-box {
        background: #162032; border-left: 5px solid #3b9edd;
        padding: 0.85rem 1.1rem; border-radius: 0 8px 8px 0;
        margin: 0.6rem 0; color: #c8dff5; font-size: 0.95rem;
    }
    .info-box strong { color: #7ec8f7; }
    .info-box em     { color: #a8d8f5; }
    .podium-gold   { background: linear-gradient(135deg, #3a2e00 0%, #5a4500 100%); border: 2px solid #FFD700; }
    .podium-silver { background: linear-gradient(135deg, #1f1f2e 0%, #2e2e42 100%); border: 2px solid #C0C0C0; }
    .podium-bronze { background: linear-gradient(135deg, #2e1a00 0%, #452800 100%); border: 2px solid #CD7F32; }
    .step-card {
        background: #1e2235; border-radius: 10px; padding: 1rem 0.7rem;
        text-align: center; border: 1px solid #3a3f55; color: #e8eaf6; min-height: 110px;
    }
    .step-card strong { color: #ffffff; font-size: 0.95rem; }
    .step-card small  { color: #9ba4c0; font-size: 0.8rem; }
    [data-testid="stMetric"] { background: #1e2235; border-radius: 10px; padding: 0.8rem 1rem; border: 1px solid #3a3f55; }
    [data-testid="stMetricLabel"] { color: #b0b8d1 !important; font-size: 0.85rem; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 1.6rem; font-weight: 700; }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #e94560 0%, #c0304a 100%) !important;
        color: #ffffff !important; font-weight: 700 !important; font-size: 1rem !important;
        border: none !important; border-radius: 8px !important; padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 14px rgba(233,69,96,0.45) !important; transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important; box-shadow: 0 6px 18px rgba(233,69,96,0.6) !important;
    }
    .stButton > button {
        background: #2a2f45 !important; color: #f0f2f6 !important;
        border: 1px solid #4a5070 !important; border-radius: 8px !important;
    }
    .stSlider label, .stSelectbox label, .stNumberInput label, .stRadio label {
        color: #e0e4f0 !important; font-weight: 600 !important;
    }
    [data-testid="stSlider"] [role="slider"] { background: #e94560 !important; }
    .stSlider [data-baseweb="slider"] div[class*="Track"] { background: #3a3f55 !important; }
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: #1e2235 !important; color: #f0f2f6 !important;
        border: 1px solid #4a5070 !important; border-radius: 6px !important;
    }
    [data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; border: 1px solid #3a3f55 !important; }
    .dataframe thead th { background: #e94560 !important; color: #ffffff !important; font-weight: 700 !important; }
    .dataframe tbody td { background: #1e2235 !important; color: #e8eaf6 !important; }
    .dataframe tbody tr:nth-child(even) td { background: #252a3a !important; }
    [data-testid="stAlert"][data-baseweb="notification"] { border-radius: 8px !important; }
    div[data-testid="stAlert"] p { font-weight: 600; }
    [data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, #e94560, #ff7b93) !important; }
    hr { border-color: #3a3f55 !important; }
    p, li, td, th, span, div { color: #e0e4f0; }
    .profil-table td { padding: 0.5rem 0.6rem; color: #e0e4f0; vertical-align: top; }
    .profil-table td:first-child { color: #b0b8d1; font-weight: 600; width: 36%; }
    .profil-table tr { border-bottom: 1px solid #3a3f55; }
</style>
""", unsafe_allow_html=True)

# FUNGSI BANTU: PARSING DATA
def parse_avg(val):
    """Mengekstrak nilai numerik rata-rata dari string yang mengandung rentang."""
    if pd.isna(val):
        return np.nan
    nums = re.findall(r'\d+(?:\.\d+)?', str(val).replace(',', ''))
    if nums:
        return sum(float(x) for x in nums) / len(nums)
    return np.nan


@st.cache_data
def load_and_clean_data():
    """Memuat dan membersihkan dataset Cars 2025."""
    df = pd.read_csv("Cars_Datasets_2025.csv", encoding="cp1252")
    df['HP_Num']     = df['HorsePower'].apply(parse_avg)
    df['Price_Num']  = df['Cars Prices'].apply(
        lambda v: parse_avg(str(v).replace(',', '')) if not pd.isna(v) else np.nan
    )
    df['Speed_Num']  = df['Total Speed'].apply(parse_avg)
    df['Perf_Num']   = df['Performance(0 - 100 )KM/H'].apply(parse_avg)
    df['Torque_Num'] = df['Torque'].apply(parse_avg)
    df.dropna(subset=['HP_Num', 'Price_Num', 'Speed_Num', 'Perf_Num', 'Torque_Num'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# FUNGSI FUZZY: SISTEM INFERENSI (murni FIS Mamdani)
def build_fuzzy_system():
    """
    Membangun Fuzzy Inference System (FIS) Mamdani untuk penilaian mobil mewah.
    Tidak menggunakan bobot eksternal — skor sepenuhnya dari inferensi fuzzy.

    Variabel Input  : HorsePower, Kecepatan, Akselerasi, Torsi, Harga
    Variabel Output : Skor Kelayakan (0-100)
    """
    # 1. DEFINISI UNIVERSE OF DISCOURSE
    hp_var     = ctrl.Antecedent(np.arange(0, 2500, 1), 'hp')
    speed_var  = ctrl.Antecedent(np.arange(80, 501, 1), 'speed')
    perf_var   = ctrl.Antecedent(np.arange(1, 36, 0.1), 'perf')
    torque_var = ctrl.Antecedent(np.arange(0, 3501, 1), 'torque')
    harga_var  = ctrl.Antecedent(np.arange(0, 18000001, 1000), 'harga')
    skor_var   = ctrl.Consequent(np.arange(0, 101, 1), 'skor')

    # 2. FUNGSI KEANGGOTAAN — INPUT
    # HorsePower: rendah / sedang / tinggi
    hp_var['rendah'] = fuzz.trimf(hp_var.universe, [0, 0, 500])
    hp_var['sedang'] = fuzz.trimf(hp_var.universe, [200, 700, 1200])
    hp_var['tinggi'] = fuzz.trimf(hp_var.universe, [900, 2500, 2500])

    # Kecepatan: lambat / sedang / cepat
    speed_var['lambat'] = fuzz.trimf(speed_var.universe, [80, 80, 200])
    speed_var['sedang'] = fuzz.trimf(speed_var.universe, [150, 250, 350])
    speed_var['cepat']  = fuzz.trimf(speed_var.universe, [300, 501, 501])

    # Akselerasi 0-100 km/h: cepat / sedang / lambat
    # Nilai KECIL = akselerasi CEPAT (lebih baik)
    perf_var['cepat']  = fuzz.trimf(perf_var.universe, [1, 1, 5])
    perf_var['sedang'] = fuzz.trimf(perf_var.universe, [3, 8, 15])
    perf_var['lambat'] = fuzz.trimf(perf_var.universe, [10, 36, 36])

    # Torsi: rendah / sedang / tinggi
    torque_var['rendah'] = fuzz.trimf(torque_var.universe, [0, 0, 500])
    torque_var['sedang'] = fuzz.trimf(torque_var.universe, [300, 800, 1500])
    torque_var['tinggi'] = fuzz.trimf(torque_var.universe, [1000, 3501, 3501])

    # Harga: murah / menengah / mewah
    harga_var['murah']    = fuzz.trimf(harga_var.universe, [0, 0, 300000])
    harga_var['menengah'] = fuzz.trimf(harga_var.universe, [100000, 500000, 1000000])
    harga_var['mewah']    = fuzz.trimf(harga_var.universe, [500000, 18000001, 18000001])

    # 3. FUNGSI KEANGGOTAAN — OUTPUT SKOR
    skor_var['sangat_rendah'] = fuzz.trimf(skor_var.universe, [0, 0, 25])
    skor_var['rendah']        = fuzz.trimf(skor_var.universe, [10, 30, 50])
    skor_var['sedang']        = fuzz.trimf(skor_var.universe, [35, 55, 75])
    skor_var['tinggi']        = fuzz.trimf(skor_var.universe, [60, 80, 95])
    skor_var['sangat_tinggi'] = fuzz.trimf(skor_var.universe, [80, 100, 100])

    # 4. RULE BASE (Dasar Aturan Fuzzy Mamdani)
    rules = [
        # Kombinasi terbaik: semua kriteria unggul
        ctrl.Rule(
            hp_var['tinggi'] & speed_var['cepat'] & perf_var['cepat'] &
            torque_var['tinggi'] & harga_var['mewah'],
            skor_var['sangat_tinggi']
        ),
        # Performa tinggi + harga mewah
        ctrl.Rule(
            hp_var['tinggi'] & speed_var['cepat'] & harga_var['mewah'],
            skor_var['tinggi']
        ),
        ctrl.Rule(
            hp_var['tinggi'] & perf_var['cepat'] & torque_var['tinggi'],
            skor_var['tinggi']
        ),
        ctrl.Rule(
            speed_var['cepat'] & perf_var['cepat'] & harga_var['mewah'],
            skor_var['tinggi']
        ),
        # Performa sedang
        ctrl.Rule(
            hp_var['sedang'] & speed_var['sedang'] & harga_var['mewah'],
            skor_var['sedang']
        ),
        ctrl.Rule(
            hp_var['tinggi'] & speed_var['sedang'] & harga_var['menengah'],
            skor_var['sedang']
        ),
        ctrl.Rule(
            torque_var['tinggi'] & harga_var['mewah'],
            skor_var['sedang']
        ),
        # Performa rendah
        ctrl.Rule(
            hp_var['rendah'] & speed_var['lambat'],
            skor_var['rendah']
        ),
        ctrl.Rule(
            hp_var['sedang'] & speed_var['lambat'] & harga_var['murah'],
            skor_var['rendah']
        ),
        ctrl.Rule(
            hp_var['rendah'] & harga_var['murah'],
            skor_var['sangat_rendah']
        ),
        # Akselerasi lambat
        ctrl.Rule(
            perf_var['lambat'] & speed_var['lambat'],
            skor_var['sangat_rendah']
        ),
        ctrl.Rule(
            perf_var['lambat'] & harga_var['murah'],
            skor_var['rendah']
        ),
        # Torsi rendah + harga murah
        ctrl.Rule(
            torque_var['rendah'] & harga_var['murah'],
            skor_var['sangat_rendah']
        ),
    ]

    tipping_ctrl = ctrl.ControlSystem(rules)
    return tipping_ctrl, hp_var, speed_var, perf_var, torque_var, harga_var, skor_var


def hitung_skor_fuzzy(row, tipping_ctrl):
    """
    Menghitung skor Fuzzy murni dari FIS Mamdani (Centroid defuzzification).
    Tidak ada bobot eksternal — skor sepenuhnya merupakan hasil inferensi fuzzy.
    """
    try:
        sim = ctrl.ControlSystemSimulation(tipping_ctrl)
        sim.input['hp'] = float(np.clip(row['HP_Num'], 0, 2499))
        sim.input['speed'] = float(np.clip(row['Speed_Num'], 80, 500))
        sim.input['perf'] = float(np.clip(row['Perf_Num'], 1, 35.9))
        sim.input['torque'] = float(np.clip(row['Torque_Num'], 0, 3500))
        sim.input['harga'] = float(np.clip(row['Price_Num'], 0, 17999999))
        sim.compute()
        return round(sim.output['skor'], 4)
    except Exception:
        return np.nan

# FUNGSI VISUALISASI KURVA KEANGGOTAAN
def plot_kurva_keanggotaan(hp_var, speed_var, perf_var, torque_var, harga_var, skor_var):
    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    fig.patch.set_facecolor('#0f1117')
    fig.suptitle('Kurva Keanggotaan Variabel Fuzzy',
                 fontsize=14, fontweight='bold', color='white', y=1.01)

    configs = [
        (hp_var,     'HorsePower (hp)',
         ['rendah', 'sedang', 'tinggi'], ['#5bc8f5', '#4dda7e', '#ff6b6b']),
        (speed_var,  'Kecepatan (km/h)',
         ['lambat', 'sedang', 'cepat'], ['#5bc8f5', '#4dda7e', '#ff6b6b']),
        (perf_var,   'Akselerasi 0-100 (detik)',
         ['cepat', 'sedang', 'lambat'], ['#ff6b6b', '#4dda7e', '#5bc8f5']),
        (torque_var, 'Torsi (Nm)',
         ['rendah', 'sedang', 'tinggi'], ['#5bc8f5', '#4dda7e', '#ff6b6b']),
        (harga_var,  'Harga (USD)',
         ['murah', 'menengah', 'mewah'], ['#5bc8f5', '#4dda7e', '#ff6b6b']),
        (skor_var,   'Skor Kelayakan (0-100)',
         ['sangat_rendah', 'rendah', 'sedang', 'tinggi', 'sangat_tinggi'],
         ['#ff4444', '#ff9944', '#ffdd44', '#66dd66', '#44ff99']),
    ]

    for ax, (var, label, terms, colors) in zip(axes.flatten(), configs):
        ax.set_facecolor('#1e2235')
        for term, color in zip(terms, colors):
            ax.plot(var.universe, fuzz.interp_membership(var.universe, var[term].mf, var.universe), label=term, color=color, linewidth=2.5)
        ax.set_title(label, fontsize=10, fontweight='bold', color='white', pad=8)
        ax.set_xlabel('Nilai', color='#b0b8d1', fontsize=9)
        ax.set_ylabel('Derajat Keanggotaan', color='#b0b8d1', fontsize=9)
        leg = ax.legend(fontsize=8, loc='upper right', facecolor='#2a2f45', edgecolor='#4a5070')
        for text in leg.get_texts():
            text.set_color('white')
        ax.grid(True, alpha=0.25, color='#4a5070')
        ax.set_ylim(-0.05, 1.15)
        ax.tick_params(colors='#b0b8d1', labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor('#3a3f55')

    plt.tight_layout()
    return fig

def plot_top_n(df_hasil, n=10):
    top = df_hasil.head(n).copy()
    labels = top['Nama Mobil']
    scores = top['Skor Fuzzy']

    colors = ['#FFD700' if i == 0 else '#C0C0C0' if i == 1 else '#CD7F32' if i == 2
              else '#4a90d9' for i in range(len(top))]

    fig, ax = plt.subplots(figsize=(11, max(6, len(top) * 0.55)))
    fig.patch.set_facecolor('#0f1117')
    ax.set_facecolor('#1e2235')
    bars = ax.barh(range(len(top)), scores, color=colors, edgecolor='#0f1117', height=0.65)
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(labels, fontsize=9, color='white')
    ax.invert_yaxis()
    ax.set_xlabel('Skor Fuzzy', fontsize=10, color='#b0b8d1')
    ax.set_title(f'Top {n} Rekomendasi Mobil Mewah', fontsize=13, fontweight='bold', color='white', pad=12)
    ax.set_xlim(0, 110)
    ax.grid(axis='x', alpha=0.2, color='#4a5070')
    ax.tick_params(colors='#b0b8d1', labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor('#3a3f55')
    for bar, score in zip(bars, scores):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2, f'{score:.2f}', va='center', ha='left', fontsize=9, fontweight='bold', color='white')

    leg = ax.legend(
        handles=[
            mpatches.Patch(color='#FFD700', label='Peringkat 1'),
            mpatches.Patch(color='#C0C0C0', label='Peringkat 2'),
            mpatches.Patch(color='#CD7F32', label='Peringkat 3'),
            mpatches.Patch(color='#4a90d9', label='Lainnya'),
        ],
        loc='lower right', fontsize=8, facecolor='#2a2f45', edgecolor='#4a5070'
    )
    for text in leg.get_texts():
        text.set_color('white')

    plt.tight_layout()
    return fig

# LOAD DATA
df_raw = load_and_clean_data()

# NAVIGASI SIDEBAR
with st.sidebar:
    st.markdown("## SPK Mobil Mewah")
    st.markdown("**Sistem Pendukung Keputusan**  \nPemilihan Mobil Mewah Pertama  \nMenggunakan Metode Fuzzy")
    st.markdown("---")

    halaman = st.radio(
        "Navigasi",
        ["Beranda", "Dataset", "Hitung SPK", "Visualisasi", "Profil Kelompok"],
        index=0
    )

    st.markdown("---")
    st.markdown("**Info Metode**")
    st.markdown("""
Metode: **Fuzzy Inference System (FIS) Mamdani**

Kriteria yang digunakan:
- HorsePower (hp)
- Kecepatan Maksimum (km/h)
- Akselerasi 0-100 km/h (detik)
- Torsi (Nm)
- Harga (USD)
    """)

# HALAMAN: BERANDA
if halaman == "Beranda":
    st.markdown('<div class="main-title">Sistem Pendukung Keputusan</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Rekomendasi Mobil Mewah Pertama untuk Orang Kaya Baru</div>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Data Mobil", f"{len(df_raw):,} unit")
    with col2:
        st.metric("Jumlah Merek", f"{df_raw['Company Names'].nunique()} merek")
    with col3:
        st.metric("Metode SPK", "Fuzzy Logic")

    st.markdown("---")
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<p class="section-header">Tentang Sistem</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        Sistem ini membantu <strong>orang kaya baru</strong> dalam memilih mobil mewah
        pertama mereka secara objektif berdasarkan 5 kriteria utama menggunakan
        <strong>Fuzzy Inference System (FIS) Mamdani</strong>.
        <br><br>
        Fuzzy Logic dipilih karena mampu menangani ketidakpastian dan keambiguan
        dalam penilaian performa kendaraan, serta dapat merepresentasikan
        pengetahuan pakar secara linguistik.
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown('<p class="section-header">Kriteria Penilaian</p>', unsafe_allow_html=True)
        kriteria_data = {
            "Kriteria": ["HorsePower", "Kecepatan Maksimum",
                           "Akselerasi 0-100 km/h", "Torsi", "Harga"],
            "Keterangan": ["Tenaga mesin (hp)", "Kecepatan puncak (km/h)",
                           "Waktu akselerasi (detik)", "Momen puntir mesin (Nm)",
                           "Harga kendaraan (USD)"],
            "Tipe": ["Benefit", "Benefit", "Cost", "Benefit", "Benefit"]
        }
        st.dataframe(pd.DataFrame(kriteria_data), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown('<p class="section-header">Alur Kerja Sistem</p>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    steps = [
        ("1", "Muat Dataset",  "Data 1.218 mobil dari berbagai merek"),
        ("2", "Filter Data",   "Tentukan kriteria dan rentang nilai"),
        ("3", "Fuzzifikasi",   "Nilai numerik ke himpunan fuzzy"),
        ("4", "Inferensi",     "Terapkan rule base Mamdani"),
        ("5", "Defuzzifikasi", "Hasilkan skor dan peringkat akhir"),
    ]
    for col, (icon, judul, desc) in zip([c1, c2, c3, c4, c5], steps):
        col.markdown(f"""
        <div class="step-card">
            <div style="font-size:1.8rem; font-weight:800; color:#e94560; margin-bottom:0.4rem">{icon}</div>
            <strong>{judul}</strong><br>
            <small>{desc}</small>
        </div>
        """, unsafe_allow_html=True)

# HALAMAN: DATASET
elif halaman == "Dataset":
    st.markdown('<div class="main-title">Dataset Mobil 2025</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Cars Dataset 2025 — 1.218 data kendaraan dari berbagai merek dunia</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<p class="section-header">Filter Data</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        merek_list  = ["Semua"] + sorted(df_raw['Company Names'].unique().tolist())
        pilih_merek = st.selectbox("Merek Mobil", merek_list)
    with col2:
        bahan_bakar_list = ["Semua"] + sorted(df_raw['Fuel Types'].unique().tolist())
        pilih_bb         = st.selectbox("Tipe Bahan Bakar", bahan_bakar_list)
    with col3:
        harga_min, harga_max = int(df_raw['Price_Num'].min()), int(df_raw['Price_Num'].max())
        rentang_harga = st.slider("Rentang Harga (USD)", harga_min, harga_max,(harga_min, harga_max), step=10000)

    df_filtered = df_raw.copy()
    if pilih_merek != "Semua":
        df_filtered = df_filtered[df_filtered['Company Names'] == pilih_merek]
    if pilih_bb != "Semua":
        df_filtered = df_filtered[df_filtered['Fuel Types'] == pilih_bb]
    df_filtered = df_filtered[
        (df_filtered['Price_Num'] >= rentang_harga[0]) &
        (df_filtered['Price_Num'] <= rentang_harga[1])
    ]

    st.markdown(f"**Menampilkan {len(df_filtered):,} dari {len(df_raw):,} data**")
    kolom_tampil = ['Company Names', 'Cars Names', 'Engines', 'HorsePower', 'Total Speed', 'Performance(0 - 100 )KM/H', 'Cars Prices', 'Fuel Types', 'Seats', 'Torque']
    st.dataframe(df_filtered[kolom_tampil], use_container_width=True, height=450)

    st.markdown("---")
    st.markdown('<p class="section-header">Statistik Deskriptif (Nilai Numerik)</p>', unsafe_allow_html=True)
    stat_df = df_filtered[['HP_Num', 'Speed_Num', 'Perf_Num', 'Torque_Num', 'Price_Num']].describe().round(2)
    stat_df.index.name = "Statistik"
    stat_df.columns = ['HorsePower (hp)', 'Kecepatan (km/h)', 'Akselerasi (detik)', 'Torsi (Nm)', 'Harga (USD)']
    st.dataframe(stat_df, use_container_width=True)

# HALAMAN: HITUNG SPK
elif halaman == "Hitung SPK":
    st.markdown('<div class="main-title">Hitung SPK — Metode Fuzzy Mamdani</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Atur filter kriteria lalu jalankan perhitungan Fuzzy Inference System</div>', unsafe_allow_html=True)
    st.markdown("---")

    # FILTER KRITERIA
    st.markdown('<p class="section-header">Filter Kriteria Pencarian</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    <strong>Petunjuk:</strong> Atur rentang nilai setiap kriteria untuk menyaring data mobil
    sebelum diproses oleh Fuzzy Inference System. Hanya mobil yang memenuhi semua filter
    yang akan dihitung dan dirangking.
    </div>
    """, unsafe_allow_html=True)

    # Ambil batas aktual dari dataset
    hp_min_data, hp_max_data = int(df_raw['HP_Num'].min()), int(df_raw['HP_Num'].max())
    speed_min_data, speed_max_data = int(df_raw['Speed_Num'].min()), int(df_raw['Speed_Num'].max())
    perf_min_data, perf_max_data = float(df_raw['Perf_Num'].min()), float(df_raw['Perf_Num'].max())
    torque_min_data, torque_max_data = int(df_raw['Torque_Num'].min()), int(df_raw['Torque_Num'].max())
    price_min_data, price_max_data = int(df_raw['Price_Num'].min()),  int(df_raw['Price_Num'].max())

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Tenaga & Performa**")
        filter_hp = st.slider(
            "HorsePower (hp)",
            min_value=hp_min_data, max_value=hp_max_data,
            value=(hp_min_data, hp_max_data), step=50,
            help="Saring berdasarkan rentang tenaga mesin"
        )
        filter_speed = st.slider(
            "Kecepatan Maksimum (km/h)",
            min_value=speed_min_data, max_value=speed_max_data,
            value=(speed_min_data, speed_max_data), step=10,
            help="Saring berdasarkan rentang kecepatan puncak"
        )
        filter_perf = st.slider(
            "Akselerasi 0-100 km/h (detik) — nilai kecil lebih cepat",
            min_value=round(perf_min_data, 1), max_value=round(perf_max_data, 1),
            value=(round(perf_min_data, 1), round(perf_max_data, 1)), step=0.5,
            help="Saring berdasarkan waktu akselerasi (nilai kecil = lebih cepat)"
        )

    with col2:
        st.markdown("**Torsi, Harga & Opsi Lain**")
        filter_torque = st.slider(
            "Torsi (Nm)",
            min_value=torque_min_data, max_value=torque_max_data,
            value=(torque_min_data, torque_max_data), step=50,
            help="Saring berdasarkan rentang torsi/momen puntir"
        )
        filter_harga = st.slider(
            "Harga (USD)",
            min_value=price_min_data, max_value=price_max_data,
            value=(price_min_data, price_max_data), step=50000,
            help="Saring berdasarkan rentang harga kendaraan"
        )
        filter_merek_spk = st.selectbox(
            "Merek Mobil (Opsional)",
            ["Semua"] + sorted(df_raw['Company Names'].unique().tolist())
        )
        filter_bb_spk = st.selectbox(
            "Tipe Bahan Bakar (Opsional)",
            ["Semua"] + sorted(df_raw['Fuel Types'].unique().tolist())
        )

    # Ringkasan filter aktif
    st.markdown(f"""
    <div class="card" style="margin-top:0.5rem;">
    <strong>Ringkasan Filter Aktif:</strong><br><br>
    HP: <strong style="color:#ff6b6b">{filter_hp[0]:,} - {filter_hp[1]:,} hp</strong>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    Speed: <strong style="color:#5bc8f5">{filter_speed[0]:,} - {filter_speed[1]:,} km/h</strong>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    Akselerasi: <strong style="color:#4dda7e">{filter_perf[0]} - {filter_perf[1]} dtk</strong><br><br>
    Torsi: <strong style="color:#ffaa44">{filter_torque[0]:,} - {filter_torque[1]:,} Nm</strong>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    Harga: <strong style="color:#cc88ff">${filter_harga[0]:,} - ${filter_harga[1]:,}</strong>
    &nbsp;&nbsp;|&nbsp;&nbsp;
    Merek: <strong style="color:#e94560">{filter_merek_spk}</strong>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Jumlah top-N
    col_n, col_btn, col_info = st.columns([1, 1, 3])
    with col_n:
        n_hasil = st.number_input(
            "Jumlah Rekomendasi (Top-N)",
            min_value=5, max_value=50, value=10, step=5
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        tombol_hitung = st.button(
            "Jalankan Perhitungan SPK",
            type="primary",
            use_container_width=True
        )
    with col_info:
        st.markdown("""
        <div class="info-box" style="margin-top:0.5rem;">
        Proses perhitungan Fuzzy meliputi:
        <strong>Fuzzifikasi &rarr; Inferensi Rule Base (Mamdani) &rarr; Agregasi &rarr; Defuzzifikasi (Centroid)</strong>.
        Mohon tunggu sejenak.
        </div>
        """, unsafe_allow_html=True)

    # PROSES PERHITUNGAN
    if tombol_hitung:
        df_hitung = df_raw.copy()

        # Terapkan semua filter
        df_hitung = df_hitung[
            (df_hitung['HP_Num'] >= filter_hp[0]) & (df_hitung['HP_Num'] <= filter_hp[1]) &
            (df_hitung['Speed_Num'] >= filter_speed[0]) & (df_hitung['Speed_Num'] <= filter_speed[1]) &
            (df_hitung['Perf_Num'] >= filter_perf[0]) & (df_hitung['Perf_Num'] <= filter_perf[1]) &
            (df_hitung['Torque_Num'] >= filter_torque[0]) & (df_hitung['Torque_Num'] <= filter_torque[1]) &
            (df_hitung['Price_Num'] >= filter_harga[0]) & (df_hitung['Price_Num'] <= filter_harga[1])
        ]
        if filter_merek_spk != "Semua":
            df_hitung = df_hitung[df_hitung['Company Names'] == filter_merek_spk]
        if filter_bb_spk != "Semua":
            df_hitung = df_hitung[df_hitung['Fuel Types'] == filter_bb_spk]

        if len(df_hitung) == 0:
            st.warning("Tidak ada data yang sesuai dengan filter yang dipilih. Coba perlebar rentang filter.")
        else:
            st.info(f"Data setelah filter: **{len(df_hitung):,} mobil** akan dihitung.")

            # Bangun FIS
            with st.spinner("Membangun sistem fuzzy..."):
                tipping_ctrl, hp_var, speed_var, perf_var, torque_var, harga_var, skor_var = \
                    build_fuzzy_system()

            # Hitung skor tiap baris
            progress_bar = st.progress(0, text="Menghitung skor fuzzy...")
            skor_list  = []
            total_rows = len(df_hitung)

            for i, (_, row) in enumerate(df_hitung.iterrows()):
                skor = hitung_skor_fuzzy(row, tipping_ctrl)
                skor_list.append(skor)
                if i % max(1, total_rows // 20) == 0:
                    progress_bar.progress(
                        min(int((i + 1) / total_rows * 100), 100),
                        text=f"Menghitung skor fuzzy... ({i+1}/{total_rows})"
                    )

            progress_bar.progress(100, text="Perhitungan selesai!")

            df_hitung['Skor Fuzzy'] = skor_list
            df_hitung.dropna(subset=['Skor Fuzzy'], inplace=True)
            df_hitung['Nama Mobil'] = df_hitung['Company Names'] + " " + df_hitung['Cars Names']
            df_hitung_sorted = (df_hitung
                                .sort_values('Skor Fuzzy', ascending=False)
                                .reset_index(drop=True))
            df_hitung_sorted['Peringkat'] = range(1, len(df_hitung_sorted) + 1)

            # Simpan ke session state
            st.session_state['hasil_spk']  = df_hitung_sorted
            st.session_state['hp_var']     = hp_var
            st.session_state['speed_var']  = speed_var
            st.session_state['perf_var']   = perf_var
            st.session_state['torque_var'] = torque_var
            st.session_state['harga_var']  = harga_var
            st.session_state['skor_var']   = skor_var
            st.session_state['n_hasil']    = n_hasil

            # TAMPILKAN HASIL
            st.success(f"Berhasil menghitung skor untuk **{len(df_hitung_sorted):,} mobil**!")
            st.markdown("---")

            # Podium Top 3
            st.markdown('<p class="section-header">Podium Top 3 Rekomendasi</p>',
                        unsafe_allow_html=True)
            if len(df_hitung_sorted) >= 3:
                p1, p2, p3 = st.columns(3)
                for col, rank, label, css_class, skor_color in [
                    (p1, 0, "Peringkat 1", "podium-gold",   "#FFD700"),
                    (p2, 1, "Peringkat 2", "podium-silver", "#C0C0C0"),
                    (p3, 2, "Peringkat 3", "podium-bronze", "#CD7F32"),
                ]:
                    row = df_hitung_sorted.iloc[rank]
                    col.markdown(f"""
                    <div class="{css_class}" style="border-radius:12px; padding:1.2rem;
                         text-align:center; margin-bottom:0.5rem;">
                        <div style="font-size:1.1rem; font-weight:700; color:{skor_color};
                             margin-bottom:0.3rem">{label}</div>
                        <div style="font-size:0.95rem; font-weight:700;
                             color:#ffffff; margin-bottom:0.5rem">
                            {row['Nama Mobil']}
                        </div>
                        <div style="font-size:1.5rem; font-weight:800;
                             color:{skor_color}; margin-bottom:0.5rem">
                            {row['Skor Fuzzy']:.2f}
                        </div>
                        <div style="font-size:0.82rem; color:#d0d8f0; line-height:1.6">
                            {row['HP_Num']:.0f} hp &nbsp;|&nbsp;
                            {row['Speed_Num']:.0f} km/h<br>
                            {row['Torque_Num']:.0f} Nm &nbsp;|&nbsp;
                            ${row['Price_Num']:,.0f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")

            # Tabel Hasil Lengkap
            st.markdown(
                f'<p class="section-header">Tabel Hasil Perangkingan (Top {n_hasil})</p>',
                unsafe_allow_html=True
            )
            kolom_hasil = ['Peringkat', 'Nama Mobil', 'Skor Fuzzy', 'HP_Num', 'Speed_Num', 'Perf_Num', 'Torque_Num', 'Price_Num', 'Fuel Types']
            df_tampil = df_hitung_sorted[kolom_hasil].head(n_hasil).copy()
            df_tampil.columns = ['Peringkat', 'Nama Mobil', 'Skor Fuzzy', 'HP (hp)', 'Kec. Maks (km/h)', 'Akselerasi (dtk)', 'Torsi (Nm)', 'Harga (USD)', 'Bahan Bakar']
            df_tampil['Skor Fuzzy']       = df_tampil['Skor Fuzzy'].round(2)
            df_tampil['HP (hp)']          = df_tampil['HP (hp)'].round(0).astype(int)
            df_tampil['Kec. Maks (km/h)'] = df_tampil['Kec. Maks (km/h)'].round(0).astype(int)
            df_tampil['Akselerasi (dtk)'] = df_tampil['Akselerasi (dtk)'].round(1)
            df_tampil['Torsi (Nm)']       = df_tampil['Torsi (Nm)'].round(0).astype(int)
            df_tampil['Harga (USD)']      = df_tampil['Harga (USD)'].apply(lambda x: f"${x:,.0f}")
            st.dataframe(df_tampil, use_container_width=True, hide_index=True)

            # TABEL DEFUZZIFIKASI
            st.markdown("---")
            st.markdown(
                '<p class="section-header">Tabel Defuzzifikasi (Sampel 10 Teratas)</p>',
                unsafe_allow_html=True
            )
            st.markdown("""
            <div class="info-box">
            Tabel berikut menampilkan nilai input yang telah di-<em>fuzzifikasi</em>
            dan skor output hasil <strong>defuzzifikasi (metode Centroid)</strong> untuk
            10 mobil dengan peringkat tertinggi.
            </div>
            """, unsafe_allow_html=True)

            sample_defuzz = df_hitung_sorted.head(10)[
                ['Peringkat', 'Nama Mobil', 'HP_Num', 'Speed_Num', 'Perf_Num', 'Torque_Num', 'Price_Num', 'Skor Fuzzy']
            ].copy()

            def label_hp(v):
                if v < 500: return "Rendah"
                if v < 900: return "Sedang"
                return "Tinggi"
            def label_speed(v):
                if v < 200: return "Lambat"
                if v < 300: return "Sedang"
                return "Cepat"
            def label_perf(v):
                if v < 5: return "Cepat"
                if v < 10: return "Sedang"
                return "Lambat"
            def label_torque(v):
                if v < 500: return "Rendah"
                if v < 1000: return "Sedang"
                return "Tinggi"
            def label_harga(v):
                if v < 300000: return "Murah"
                if v < 1000000: return "Menengah"
                return "Mewah"

            sample_defuzz['Label HP'] = sample_defuzz['HP_Num'].apply(label_hp)
            sample_defuzz['Label Speed'] = sample_defuzz['Speed_Num'].apply(label_speed)
            sample_defuzz['Label Perf'] = sample_defuzz['Perf_Num'].apply(label_perf)
            sample_defuzz['Label Torque'] = sample_defuzz['Torque_Num'].apply(label_torque)
            sample_defuzz['Label Harga'] = sample_defuzz['Price_Num'].apply(label_harga)

            kolom_defuzz = ['Peringkat', 'Nama Mobil',
                            'HP_Num',     'Label HP',
                            'Speed_Num',  'Label Speed',
                            'Perf_Num',   'Label Perf',
                            'Torque_Num', 'Label Torque',
                            'Price_Num',  'Label Harga',
                            'Skor Fuzzy']
            df_defuzz_tampil = sample_defuzz[kolom_defuzz].copy()
            df_defuzz_tampil.columns = [
                'Rank', 'Nama Mobil',
                'HP (hp)',     'HP Fuzzy',
                'Speed (km/h)', 'Speed Fuzzy',
                'Perf (dtk)',  'Perf Fuzzy',
                'Torsi (Nm)',  'Torsi Fuzzy',
                'Harga ($)',   'Harga Fuzzy',
                'Skor Akhir'
            ]
            st.dataframe(df_defuzz_tampil, use_container_width=True, hide_index=True)

            # Grafik Top-N
            st.markdown("---")
            st.markdown(
                '<p class="section-header">Grafik Hasil Perangkingan</p>',
                unsafe_allow_html=True
            )
            fig_bar = plot_top_n(
                df_hitung_sorted[['Nama Mobil', 'Skor Fuzzy']],
                n=min(n_hasil, 15)
            )
            st.pyplot(fig_bar)
            plt.close()

    elif 'hasil_spk' not in st.session_state:
        st.markdown("""
        <div class="card" style="text-align:center; padding:2.5rem;">
            <h3 style="color:#ffffff; margin-bottom:0.5rem">Belum Ada Hasil Perhitungan</h3>
            <p style="color:#b0b8d1">
                Atur filter kriteria di atas, lalu tekan tombol
                <strong style="color:#e94560">Jalankan Perhitungan SPK</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

# HALAMAN: VISUALISASI
elif halaman == "Visualisasi":
    st.markdown('<div class="main-title">Visualisasi Fuzzy</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Kurva keanggotaan dan analisis hasil perhitungan SPK</div>', unsafe_allow_html=True)
    st.markdown("---")

    if 'hasil_spk' not in st.session_state:
        st.warning("Belum ada hasil perhitungan. Silakan jalankan SPK terlebih dahulu di menu **Hitung SPK**.")
    else:
        df_hasil   = st.session_state['hasil_spk']
        hp_var     = st.session_state['hp_var']
        speed_var  = st.session_state['speed_var']
        perf_var   = st.session_state['perf_var']
        torque_var = st.session_state['torque_var']
        harga_var  = st.session_state['harga_var']
        skor_var   = st.session_state['skor_var']
        n_hasil    = st.session_state.get('n_hasil', 10)

        st.markdown(
            '<p class="section-header">Kurva Keanggotaan Variabel Fuzzy</p>',
            unsafe_allow_html=True
        )
        st.markdown("""
        <div class="info-box">
        Grafik berikut menampilkan <strong>fungsi keanggotaan (membership function)</strong>
        dari setiap variabel linguistik yang digunakan dalam Fuzzy Inference System Mamdani.
        </div>
        """, unsafe_allow_html=True)

        fig_mf = plot_kurva_keanggotaan(
            hp_var, speed_var, perf_var, torque_var, harga_var, skor_var
        )
        st.pyplot(fig_mf)
        plt.close()

        st.markdown("---")
        st.markdown(
            f'<p class="section-header">Top {n_hasil} Rekomendasi</p>',
            unsafe_allow_html=True
        )
        fig_bar = plot_top_n(
            df_hasil[['Nama Mobil', 'Skor Fuzzy']],
            n=min(n_hasil, 15)
        )
        st.pyplot(fig_bar)
        plt.close()

# HALAMAN: PROFIL KELOMPOK
elif halaman == "Profil Kelompok":
    st.markdown('<div class="main-title">Profil Kelompok</div>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div class="card" style="text-align:center; padding:2rem;">
            <h3 style="color:#ffffff; margin-bottom:0.3rem">Rafi Dzaka Pratama Putra</h3>
            <p style="color:#b0b8d1; font-size:0.95rem">NIM: 123240104</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="card" style="text-align:center; padding:2rem;">
            <h3 style="color:#ffffff; margin-bottom:0.3rem">Raihan Natawangsa</h3>
            <p style="color:#b0b8d1; font-size:0.95rem">NIM: 123240120</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="section-header">Detail Proyek</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <table class="profil-table" style="width:100%; border-collapse:collapse;">
                <tr><td><strong>Judul Proyek</strong></td>
                    <td style="color:#e0e4f0">Sistem Pendukung Keputusan Pemilihan Mobil Mewah
                    Pertama untuk Orang Kaya Baru</td></tr>
                <tr><td><strong>Mata Kuliah</strong></td>
                    <td style="color:#e0e4f0">Praktikum Sistem Cerdas Pendukung Keputusan (SCPK)</td></tr>
                <tr><td><strong>Tahun Akademik</strong></td>
                    <td style="color:#e0e4f0">2025/2026</td></tr>
                <tr><td><strong>Metode SPK</strong></td>
                    <td style="color:#e0e4f0">Fuzzy Inference System (FIS) Mamdani</td></tr>
                <tr><td><strong>Dataset</strong></td>
                    <td style="color:#e0e4f0">Cars Dataset 2025 (1.218 baris, 11 kolom)</td></tr>
                <tr><td><strong>Sumber Dataset</strong></td>
                    <td style="color:#e0e4f0">Kaggle / Cars Dataset 2025</td></tr>
                <tr><td><strong>Tool / Framework</strong></td>
                    <td style="color:#e0e4f0">Python, Streamlit, scikit-fuzzy, Pandas, Matplotlib</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="section-header">Kriteria & Variabel Fuzzy</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <p style="color:#e0e4f0; font-weight:700; margin-bottom:0.5rem">
                Variabel Input (5 Antecedent):
            </p>
            <ul style="color:#c8d0e8; line-height:2">
                <li><strong style="color:#ff6b6b">HorsePower</strong>
                    &nbsp;-&gt;&nbsp; Rendah / Sedang / Tinggi</li>
                <li><strong style="color:#5bc8f5">Kecepatan Maksimum</strong>
                    &nbsp;-&gt;&nbsp; Lambat / Sedang / Cepat</li>
                <li><strong style="color:#4dda7e">Akselerasi 0-100 km/h</strong>
                    &nbsp;-&gt;&nbsp; Cepat / Sedang / Lambat <em style="color:#9ba4c0">(Cost)</em></li>
                <li><strong style="color:#ffaa44">Torsi</strong>
                    &nbsp;-&gt;&nbsp; Rendah / Sedang / Tinggi</li>
                <li><strong style="color:#cc88ff">Harga</strong>
                    &nbsp;-&gt;&nbsp; Murah / Menengah / Mewah</li>
            </ul>
            <p style="color:#e0e4f0; font-weight:700; margin: 0.7rem 0 0.5rem 0">
                Variabel Output (1 Consequent):
            </p>
            <ul style="color:#c8d0e8; line-height:2">
                <li><strong style="color:#ffffff">Skor Kelayakan</strong>
                    &nbsp;-&gt;&nbsp; Sangat Rendah / Rendah / Sedang / Tinggi / Sangat Tinggi</li>
            </ul>
            <p style="color:#b0b8d1; margin-top:0.5rem">
                <strong style="color:#e0e4f0">Metode Defuzzifikasi:</strong>
                Centroid (Center of Gravity)
            </p>
        </div>
        """, unsafe_allow_html=True)