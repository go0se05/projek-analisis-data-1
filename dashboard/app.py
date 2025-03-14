import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
day_df = pd.read_csv("dashboard/days_processed.csv")
hour_df = pd.read_csv("dashboard/hours_processed.csv")

st.title("Bike Sharing Data Exploration Dashboard")

# Filtering options
st.sidebar.header("Filter Data")
selected_date = st.sidebar.date_input("Select Date Range", [])
selected_season = st.sidebar.multiselect("Select Season", day_df["season"].unique())
selected_weather = st.sidebar.multiselect("Select weather Condition", day_df["weather_condition"].unique())

# Apply filters
if selected_date:
    day_df = day_df[pd.to_datetime(day_df['dteday']).isin(selected_date)]
if selected_season:
    day_df = day_df[day_df["season"].isin(selected_season)]
if selected_weather:
    day_df = day_df[day_df["weather_condition"].isin(selected_weather)]

# 1. Perbedaan jumlah peminjaman pada hari kerja vs. akhir pekan
st.header("Perbedaan Jumlah Peminjaman pada Hari Kerja vs. Akhir Pekan")

st.subheader("Rata-rata Penyewaan")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(ax=ax1, x=["Weekend", "Weekday"], 
            y=day_df.groupby("workingday")["total_rentals"].mean().values, 
            palette='pastel')
ax1.set_xlabel("Day Type")
ax1.set_ylabel("Average Total Rentals")
ax1.set_title("Average Bike Rentals")
ax1.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig1)

st.subheader("Total Penyewaan")
fig2, ax2 = plt.subplots(figsize=(11, 7))
workday_totals = day_df.groupby("workingday")["total_rentals"].sum()
sns.barplot(ax=ax2, y=['Weekend', 'Weekday'], x=workday_totals.values, palette='pastel')
ax2.set_ylabel("Day Type")
ax2.set_xlabel("Total Rentals")
ax2.set_title("Total Bike Rentals: Weekday vs Weekend")
ax2.grid(axis="x", linestyle="--", alpha=0.7)
st.pyplot(fig2)
st.write("\n**Rata-rata Penyewaan**")
st.write("\n**Insight:**")
st.write("- Rata-rata peminjaman sepeda lebih tinggi pada hari kerja dibanding akhir pekan.")
st.write("- Ini menunjukkan bahwa mayoritas pengguna sepeda adalah pekerja atau mahasiswa yang menggunakannya untuk keperluan mobilitas harian.")

st.write("\n**Total Penyewaan:**")
st.write("\n**Insight:**")
st.write("- Total penyewaan sepeda di hari kerja jauh lebih tinggi dibandingkan akhir pekan.")
st.write("- Hal ini mengindikasikan bahwa pengguna sepeda dalam jumlah besar lebih aktif pada hari kerja, kemungkinan besar sebagai alternatif transportasi utama di perkotaan.")

st.markdown("---")

# 2. Pengaruh kondisi cuaca terhadap jumlah peminjaman
import matplotlib.ticker as mticker
st.header("Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman")

st.subheader("Penyewaan Sepeda Berdasarkan Cuaca")
fig3, ax3 = plt.subplots(figsize=(10, 6))
total_rentals = day_df.groupby("weather_condition")["totals_rentals"].sum().astype(int)
sns.lineplot(x=total_rentals.index.astype(int), y=total_rentals.values, marker='o')
ax3.set_xlabel("Weather Condition")
ax3.set_ylabel("Total Rentals")
ax3.set_title("Bike Rentals by Weather Condition")
ax3.set_xticks(cnt.index.astype(int))
ax3.grid(axis="y", linestyle="--", alpha=0.7)
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig3)

st.subheader("Rata-rata Penyewaan Perkondisi Cuaca")
fig4, ax4 = plt.subplots(figsize=(10, 6)) 
weather_avg = day_df.groupby("weather_condition")["total_rentals"].mean()
sns.barplot(ax=ax4, x=weather_avg.index, y=weather_avg.values, palette='pastel')
ax4.set_xlabel("Weather Condition")
ax4.set_ylabel("Average Rentals")
ax4.set_title("Average Bike Rentals per Weather Condition")
ax4.grid(axis="y", linestyle="--", alpha=0.7)
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig4)
st.write("\n**Penyewaan Berdasarkan Cuaca**")
st.write("\n**Insight:**")
st.write("- Dari boxplot, terlihat bahwa jumlah peminjaman sepeda paling tinggi terjadi saat cuaca cerah atau sedikit berawan (kategori 1).")
st.write("- Saat cuaca berkabut (kategori 2), jumlah peminjaman mulai menurun, meskipun masih dalam jumlah yang cukup signifikan.")
st.write("- Pada cuaca hujan (kategori 3), menunjukkan distribusi yang lebih rendah, dengan beberapa pencilan yang mengindikasikan peminjaman tetap terjadi meskipun jumlahnya lebih sedikit.")

st.write("\n**Rata-rata Penyewaan per-Kondisi Cuaca**")
st.write("\n**Insight:**")
st.write("- Rata-rata penyewaan tertinggi terjadi saat cuaca cerah atau sedikit berawan (kategori 1), yang jauh lebih tinggi dibandingkan kondisi cuaca lainnya.")
st.write("- Cuaca berkabut atau mendung (kategori 2) masih memungkinkan jumlah peminjaman yang cukup besar, meskipun ada penurunan dibandingkan cuaca cerah.")
st.write("- Saat hujan dan salju (kategori 3), jumlah penyewaan menurun drastis, menunjukkan bahwa faktor cuaca sangat memengaruhi keputusan pengguna dalam menyewa sepeda.")

st.markdown("---")

# 3. Jam puncak penyewaan sepeda
st.header("Jam Puncak Penyewaan Sepeda")

st.subheader("Total Penyewaan Per Jam")
fig5, ax5 = plt.subplots(figsize=(10, 5))
sns.lineplot(ax=ax5, x=hour_df["hour"], y=hour_df.groupby("hour")["total_rentals"].mean(), marker='o')
ax5.set_xlabel("Hour")
ax5.set_ylabel("Average Rentals")
ax5.set_title("Peak Bike Rental Hours")
ax5.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig5)

st.subheader("Perbandingan Jam Sibuk vs Non-Sibuk")
rush_hours = hour_df[(hour_df["hour"] >= 7) & (hour_df["hour"] <= 9) | (hour_df["hour"] >= 17) & (hour_df["hour"] <= 19)]
non_rush_hours = hour_df[~hour_df["hour"].isin(rush_hours["hour"])]

rush_avg = rush_hours["cnt"].mean()
non_rush_avg = non_rush_hours["cnt"].mean()

fig6, ax6 = plt.subplots(figsize=(8, 5))
sns.barplot(ax=ax6, x=["Rush Hours", "Non-Rush Hours"], y=[rush_avg, non_rush_avg], palette='pastel')
ax6.set_xlabel("Time Period")
ax6.set_ylabel("Average Rentals")
ax6.set_title("Comparison of Bike Rentals During Rush & Non-Rush Hours")
ax6.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig6)
st.write("\n**Total penyewaan per-jam**")
st.write("\n**Insight:**")
st.write("- Puncak penyewaan terjadi pada pagi hari sekitar pukul 8 dan sore hari sekitar pukul 17-18.")
st.write("- Ini menunjukkan bahwa mayoritas pengguna sepeda kemungkinan besar  adalah pekerja atau pelajar yang menggunakan sepeda untuk perjalanan ke dan dari tempat kerja/sekolah.")

st.write("\n**Perbandingan Jam Sibuk vs Non-Sibuk**")
st.write("\n**Insight:**")
st.write("- Rata-rata penyewaan pada jam sibuk (pagi dan sore) lebih tinggi dibandingkan dengan jam non-sibuk.")
st.write("- Hal ini semakin memperkuat dugaan bahwa penyewaan sepeda sangat dipengaruhi oleh pola aktivitas harian masyarakat.")

st.markdown("---")

# 4. Pengaruh cuaca terhadap jumlah peminjaman di berbagai jam
st.header("Pengaruh Cuaca terhadap Jumlah Peminjaman di Berbagai Jam")

st.subheader("Rata-rata Penyewaan Per Jam Berdasarkan Cuaca")
fig7, ax7 = plt.subplots(figsize=(10, 6))
sns.lineplot(x=hours_df["hour"], y=hours_df.groupby(["hour", "weather_condition"])["total_rentals"].mean().reset_index().sort_values("hour")["total_rentals"], hue=hours_df["weather_condition"].astype(str))
ax7.set_xlabel("Hour")
ax7.set_ylabel("Average Rentals")
ax7.set_title("Hourly Bike Rentals Based on Weather Condition")
ax7.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig7)

st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Cuaca")
fig8 = sns.displot(
    data=hour_df,
    x="cnt",
    hue="weathersit",
    kind="kde",
    multiple="stack",
    palette="viridis",
    alpha=0.7,
    height=6,
    aspect=1.5
)
st.pyplot(fig8)
st.write("\n**Penyewaan Per Jam Berdasarkan Cuaca**")
st.write("\n**Insight:**")
st.write("- Jumlah penyewaan sepeda cenderung lebih rendah saat cuaca buruk (kode cuaca lebih tinggi.")
st.write("- Tren penyewaan tetap mengikuti pola harian, dengan puncak di pagi dan sore hari, tetapi intensitasnya lebih rendah saat cuaca tidak mendukung.")

st.write("\n**Dsitribusi Penyewaan Sepeda Berdasarkan Cuaca**")
st.write("\n**Insight:**")
st.write("- Jumlah penyewaan sepeda cenderung lebih rendah saat cuaca buruk (kode cuaca lebih tinggi")
st.write("- Tren penyewaan tetap mengikuti pola harian, dengan puncak di pagi dan sore hari, tetapi intensitasnya lebih rendah saat cuaca tidak mendukung.")

