import streamlit as st
import pandas as pd
import plotly.express as px

# --- STYLE & BACKGROUND ---
st.set_page_config(page_title="Morph.AI Dashboard Kinerja", layout="wide")
st.markdown(
    """
    <style>
    .morph-header {
        width: 100vw;
        min-height: 120px;
        padding-top: 32px;
        padding-bottom: 24px;
        margin-left: -3vw;
        margin-top: -3.5rem;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%);
        border-radius: 0 0 40px 40px;
        box-shadow: 0 4px 24px 0 rgba(60,60,100,0.09);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .morph-title {
        font-family: 'Segoe UI', 'Montserrat', 'Arial', sans-serif;
        font-weight: 900;
        font-size: 2.7rem;
        letter-spacing: 2px;
        color: white;
        margin-bottom: 0.2rem;
        text-shadow: 0 2px 12px rgba(80,80,120,0.10);
    }
    .morph-subtitle {
        font-family: 'Segoe UI', 'Montserrat', 'Arial', sans-serif;
        font-weight: 400;
        font-size: 1.18rem;
        color: #e0e7ef;
        margin-bottom: 0.2rem;
        text-shadow: 0 1px 6px rgba(80,80,120,0.08);
    }
    .badge-karyawan {
        display: inline-block;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 60%, #EC4899 100%);
        color: white;
        font-weight: 600;
        padding: 7px 18px;
        border-radius: 999px;
        margin: 4px 8px 4px 0;
        font-size: 1.06rem;
        box-shadow: 0 2px 8px 0 rgba(139,92,246,0.09);
        letter-spacing: 0.5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- HEADER (GRADIENT, TITLE) ---
st.markdown(
    """
    <div class="morph-header">
        <div class="morph-title">Morph.AI</div>
        <div class="morph-subtitle">Dashboard Kinerja Karyawan & Survei Bulanan</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# --- UPLOAD DATA ---
st.sidebar.header("Upload Data")
kpi_file = st.sidebar.file_uploader("Upload file KPI (.csv)", type="csv")
survey_file = st.sidebar.file_uploader("Upload file Survey Bulanan (.csv)", type="csv")

if kpi_file and survey_file:
    # --- LOAD DATA ---
    kpi_data = pd.read_csv(kpi_file)
    survey_data = pd.read_csv(survey_file)

    # --- NORMALISASI NAMA KOLOM ---
    kpi_data = kpi_data.rename(columns={
        'Employee Name': 'Karyawan',
        'Employee ID': 'ID',
        'Productivity: Number of tasks completed': 'Jumlah Tugas Selesai',
        'Productivity: Time to complete tasks (hours/task)': 'Waktu Penyelesaian Rata-rata (jam)',
        'Quality of Work: Error rate (%)': 'Tingkat Kesalahan (%)',
        'Quality of Work: Customer satisfaction rate (%)': 'Tingkat Kepuasan Pelanggan (%)',
        'Presence and Punctuality: Attendance rate (%)': 'Tingkat Kehadiran (%)',
        'Presence and Punctuality: Punctuality rate (%)': 'Tingkat Ketepatan Waktu (%)',
        'Goals and Objectives: Individual goal achievement (%)': 'Pencapaian Sasaran Individu (%)',
        'Goals and Objectives: Team goal achievement (%)': 'Pencapaian Sasaran Tim (%)',
        'Goals and Objectives: Contribution to company vision (1-5)': 'Kontribusi Terhadap Visi Perusahaan',
        'Collaboration and Teamwork: Communication skills (1-5)': 'Skor Komunikasi',
        'Collaboration and Teamwork: Ability to work in a team (1-5)': 'Skor Kerja Tim'
    })
    survey_data = survey_data.rename(columns={
        'Employee Name': 'Karyawan',
        'Employee ID': 'ID'
    })

    # --- FILTER KARYAWAN ---
    selected_karyawan = st.sidebar.multiselect(
        "Pilih Karyawan:",
        options=kpi_data['Karyawan'].unique(),
        default=kpi_data['Karyawan'].unique()
    )
    filtered_kpi = kpi_data[kpi_data['Karyawan'].isin(selected_karyawan)]
    filtered_survey = survey_data[survey_data['Karyawan'].isin(selected_karyawan)]

    # --- KPI METRICS (GRID, TETAP SEPERTI SEMULA) ---
    st.markdown("### 📊 Ringkasan KPI")
    cols = st.columns(min(4, len(filtered_kpi)))
    for i, (_, row) in enumerate(filtered_kpi.iterrows()):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color:#8B5CF6; margin-bottom:6px;">{row['Karyawan']}</h3>
                <p style="font-size:1.1rem; margin:0;">Tugas Selesai</p>
                <h2 style="color:#3B82F6; margin:0;">{int(row['Jumlah Tugas Selesai'])}</h2>
                <p style="margin:0;">Waktu Rata-rata: {row['Waktu Penyelesaian Rata-rata (jam)']:.2f} jam</p>
                <p style="margin:0;">Kesalahan: {row['Tingkat Kesalahan (%)']}%</p>
                <p style="margin:0;">Kepuasan: {row['Tingkat Kepuasan Pelanggan (%)']}%</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- GRAFIK KPI ---
    st.markdown("### 📈 Jumlah Tugas Selesai per Karyawan")
    fig1 = px.bar(
        filtered_kpi,
        x='Karyawan',
        y='Jumlah Tugas Selesai',
        text='Jumlah Tugas Selesai',
        color='Jumlah Tugas Selesai',
        color_continuous_scale=['#3B82F6', '#8B5CF6', '#EC4899'],
        range_y=[0, max(filtered_kpi['Jumlah Tugas Selesai'].max(), 40)]
    )
    fig1.add_shape(
        type="line",
        x0=-0.5, x1=len(filtered_kpi['Karyawan'])-0.5,
        y0=30, y1=30,
        line=dict(color="#EF4444", width=3, dash="dashdot"),
        xref='x', yref='y'
    )
    fig1.add_annotation(
        x=len(filtered_kpi['Karyawan'])-1,
        y=31,
        text="Target ≥ 30 tugas",
        showarrow=False,
        font=dict(color="#EF4444", size=14)
    )
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        yaxis_title="Jumlah Tugas Selesai",
        xaxis_title="Karyawan",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- GRAFIK KOLABORASI & MENTAL ---
    st.markdown("### 🧠 Skor Kolaborasi & Kesehatan Mental")
    if 'Skor Komunikasi' in filtered_kpi.columns and 'Skor Kerja Tim' in filtered_kpi.columns:
        fig2 = px.bar(
            filtered_kpi.melt(id_vars=['Karyawan'], value_vars=['Skor Komunikasi', 'Skor Kerja Tim']),
            x='Karyawan',
            y='value',
            color='variable',
            barmode='group',
            labels={'value': 'Skor', 'variable': 'Kategori'},
            color_discrete_map={
                'Skor Komunikasi': '#3B82F6',
                'Skor Kerja Tim': '#F97316'
            }
        )
        fig2.update_traces(texttemplate='%{y}', textposition='outside')
        fig2.update_layout(
            yaxis=dict(range=[0, 5]),
            xaxis_title="Karyawan",
            yaxis_title="Skor",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- VISUALISASI INTERAKTIF SURVEY BULANAN ---
    st.markdown("### 📊 Visualisasi Hasil Survey Bulanan")
    survey_cols = [col for col in survey_data.columns if col not in ['Karyawan', 'ID', 'Employee Name', 'Employee ID']]
    selected_survey_col = st.selectbox("Pilih Kolom Survey untuk Visualisasi:", survey_cols)

    # Tampilkan distribusi jawaban (top 10)
    jawaban_counts = survey_data[selected_survey_col].value_counts().reset_index()
    jawaban_counts.columns = ['Jawaban', 'Jumlah']

    fig_survey = px.bar(
        jawaban_counts.head(10),
        x='Jumlah',
        y='Jawaban',
        orientation='h',
        color='Jawaban',
        color_discrete_sequence=['#3B82F6', '#6366F1', '#8B5CF6', '#EC4899', '#F97316', '#EF4444'],
        title=f"Distribusi Jawaban: {selected_survey_col}"
    )
    fig_survey.update_layout(
        yaxis={'categoryorder':'total ascending'},
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#222'
    )
    st.plotly_chart(fig_survey, use_container_width=True)

    # --- TAMPILKAN KARYAWAN UNTUK SETIAP VALUE (NAMA, BUKAN ID) ---
    st.markdown("#### 👥 Karyawan yang Memilih Jawaban Tertentu")
    value_selected = st.selectbox(
        f"Pilih jawaban pada '{selected_survey_col}' untuk melihat siapa saja yang memilihnya:",
        jawaban_counts['Jawaban']
    )
    karyawan_list = survey_data[survey_data[selected_survey_col] == value_selected]['Karyawan'].tolist()
    if karyawan_list:
        st.markdown(
            "".join([f"<span class='badge-karyawan'>{nama}</span>" for nama in karyawan_list]),
            unsafe_allow_html=True
        )
    else:
        st.info("Tidak ada karyawan yang memilih jawaban ini.")

else:
    st.info("Silakan upload file KPI dan Survey Bulanan (format CSV) melalui sidebar untuk mulai menampilkan dashboard.")