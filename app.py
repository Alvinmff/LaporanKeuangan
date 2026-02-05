import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Laporan Keuangan", layout="wide")

st.title("📊 Dashboard Laporan Keuangan")

# Upload file
uploaded_file = st.file_uploader("Upload File CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Konversi tipe data
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    df['jumlah'] = pd.to_numeric(df['jumlah'])

    # Filter tanggal
    st.sidebar.header("Filter Tanggal")
    start_date = st.sidebar.date_input("Dari Tanggal", df['tanggal'].min())
    end_date = st.sidebar.date_input("Sampai Tanggal", df['tanggal'].max())

    mask = (df['tanggal'] >= pd.to_datetime(start_date)) & (df['tanggal'] <= pd.to_datetime(end_date))
    filtered_df = df.loc[mask]

    # Hitung total
    total_pemasukan = filtered_df[filtered_df['tipe'] == 'pemasukan']['jumlah'].sum()
    total_pengeluaran = filtered_df[filtered_df['tipe'] == 'pengeluaran']['jumlah'].sum()
    saldo = total_pemasukan - total_pengeluaran

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pemasukan", f"Rp {total_pemasukan:,.0f}")
    col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
    col3.metric("Saldo", f"Rp {saldo:,.0f}")

    st.subheader("📋 Data Transaksi")
    st.dataframe(filtered_df)

    # Grafik
    st.subheader("📈 Grafik Pemasukan & Pengeluaran")

    summary = filtered_df.groupby(['tanggal', 'tipe'])['jumlah'].sum().unstack().fillna(0)

    fig, ax = plt.subplots()
    summary.plot(kind='bar', ax=ax)
    plt.xticks(rotation=45)
    plt.ylabel("Jumlah (Rp)")
    st.pyplot(fig)

    # Rekap kategori
    st.subheader("📊 Rekap per Kategori")
    kategori_summary = filtered_df.groupby('kategori')['jumlah'].sum().sort_values(ascending=False)
    st.bar_chart(kategori_summary)

else:
    st.info("Silakan upload file CSV untuk melihat laporan keuangan.")
