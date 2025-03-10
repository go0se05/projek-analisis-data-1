import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
days_df = pd.read_csv("dashboard/days_processed.csv")
hours_df = pd.read_csv("dashboard/hours_processed.csv")

# Streamlit UI
st.title("📊 Analisis Peminjaman Sepeda")
st.sidebar.header("Filter Data")

# Filter untuk jenis hari
# Filter bulan
month_dict = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
    7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}
selected_month = st.sidebar.selectbox("Pilih Bulan", list(month_dict.keys()), format_func=lambda x: month_dict[x])

# Filter data berdasarkan bulan yang dipilih
filtered_df = days_df[days_df["month"] == selected_month]

day_type = st.sidebar.selectbox("Pilih Jenis Hari", ["Semua", "Hari Kerja", "Akhir Pekan"])
if day_type == "Hari Kerja":
    days_df = days_df[days_df['workingday'] == 1]
elif day_type == "Akhir Pekan":
    days_df = days_df[days_df['workingday'] == 0]

# Filter untuk kondisi cuaca
weather_options = {1: "Cerah", 2: "Mendung", 3: "Hujan", 4: "Salju"}
weather_choice = st.sidebar.multiselect("Pilih Kondisi Cuaca", options=list(weather_options.keys()), format_func=lambda x: weather_options[x])
if weather_choice:
    days_df = days_df[days_df['weather_condition'].isin(weather_choice)]

# Visualisasi 1: Perbedaan jumlah peminjaman pada hari kerja vs akhir pekan

fig, ax = plt.subplots(figsize=(6, 4))
rental_means = days_df.groupby("workingday")["total_rentals"].mean()
custom_palette = {"Hari Kerja": "#F39E60", "Akhir Pekan": "#89A8B2"}

if day_type == "Semua":
    labels = ["Akhir Pekan", "Hari Kerja"]
    sns.barplot(x=labels, y=rental_means, hue=labels, legend=False, palette=custom_palette, ax=ax)
else:
    label = "Hari Kerja" if day_type == "Hari Kerja" else "Akhir Pekan"

    if rental_means.empty:
        mean_value = 0
    else:
        mean_value = rental_means.values[0]

    sns.barplot(x=[label], y=[mean_value], hue=[label], legend=False, palette=custom_palette, ax=ax)


ax.set_ylabel("Rata-rata Peminjaman")
ax.set_xlabel("Jenis Hari")
ax.set_title("Peminjaman Sepeda: Hari Kerja vs Akhir Pekan")
st.pyplot(fig)

st.write("\n**Insight:**")
st.write("- Peminjaman sepeda lebih tinggi pada hari kerja dibanding akhir pekan.")
st.write("- Ini menunjukkan bahwa mayoritas pengguna sepeda adalah pekerja atau mahasiswa yang menggunakannya untuk keperluan mobilitas harian.")

# Visualisasi 2: Pengaruh cuaca terhadap jumlah peminjaman
st.subheader("🌦️ Pengaruh Kondisi Cuaca terhadap jumlah Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(
    x=days_df["weather_condition"], 
    y=days_df["total_rentals"], 
    hue=days_df["weather_condition"], 
    legend=False, 
    palette="coolwarm", 
    ax=ax
    )
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Peminjaman")
ax.set_title("Pengaruh Cuaca terhadap Peminjaman Sepeda")
st.pyplot(fig)

st.write("\n**Insight:**")
st.write("- Peminjaman sepeda lebih rendah saat cuaca buruk (hujan/salju), dibandingkan saat cerah.")
st.write("- Ini bisa menjadi faktor penting dalam mengelola stok sepeda di musim hujan.")

# Visualisasi 3: Tren peminjaman berdasarkan jam (hour_df)
st.subheader("⏰ Jam Puncak Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(8, 4))
sns.lineplot(
    x=hours_df.groupby("hour")["total_rentals"].mean().index,
    y=hours_df.groupby("hour")["total_rentals"].mean().values,
    marker="o", color="royalblue", ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Peminjaman")
ax.set_title("Tren Peminjaman Sepeda per Jam")
st.pyplot(fig, clear_figure=True)

st.write ("- Puncak peminjaman terjadi pada jam sibuk: pagi (07:00 - 09:00) dan sore (17:00 - 19:00).")
st.write ("- Ini menunjukkan bahwa banyak pengguna memakai sepeda sebagai moda transportasi untuk bekerja/sekolah.")
st.write ("- Ada kemungkinan perbedaan pola peminjaman antara pekerja kantoran dan mahasiswa.")
st.write ("- Bisa jadi layanan rental sepeda bisa lebih optimal jika ada harga dinamis berdasarkan jam sibuk dan jam sepi.")

# Visualisasi 4: Pengaruh cuaca terhadap peminjaman di berbagai jam
st.subheader("☁️ Pengaruh cuaca terhadap peminjaman di berbagai jam")
fig = sns.displot(
    data=hours_df,
    x="total_rentals",
    hue="weather_condition",
    kind="kde",
    multiple="stack",
    palette="viridis",
    alpha=0.7,
    height=6,
    aspect=1.5
).figure  # Ambil figure dari seaborn
st.pyplot(fig, clear_figure=True)
st.write("\n**Insight:**")
st.write("- Cuaca buruk berdampak signifikan pada penurunan jumlah penyewaan di semua jam.")
st.write("- Namun, jam sibuk tetap menunjukkan peminjaman lebih tinggi meskipun cuaca kurang baik.")
st.write("- Mungkin ada pengguna yang tetap menggunakan sepeda meskipun hujan, kemungkinan besar mereka yang tidak memiliki alternatif transportasi lain.")
st.write("- Bisa jadi implementasi fitur seperti penyewaan mantel hujan atau jalur sepeda yang lebih terlindungi dari hujan dapat meningkatkan kenyamanan pengguna.")

st.markdown("---")  # Garis horizontal sebagai pemisah

st.subheader("\n📌**Kesimpulan:**")
st.write("- Hari kerja memiliki jumlah peminjaman lebih tinggi dibanding akhir pekan.")
st.write("- Peminjaman sepeda menurun saat kondisi cuaca buruk.")
st.write("- Puncak peminjaman terjadi pada jam 07:00–09:00 dan 17:00–19:00 pada hari kerja.")
st.write("- Pada akhir pekan, peminjaman lebih stabil antara jam 10:00–16:00.")
