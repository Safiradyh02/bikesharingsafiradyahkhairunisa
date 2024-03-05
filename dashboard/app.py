import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# mendefinisikan pertanyaan 1
def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit_hourly").cnt_hourly.sum().reset_index()
    byweather_df.weathersit_hourly.replace(1, "Clear", inplace=True)
    byweather_df.weathersit_hourly.replace(2, "Cloudy", inplace=True)
    byweather_df.weathersit_hourly.replace(3, "Light rain", inplace=True)
    byweather_df.weathersit_hourly.replace(4, "Heavy rain", inplace=True)

    byweather_df.rename(columns={
    "weathersit_hourly": "Weather",
    "cnt_hourly": "Total_user"
    }, inplace=True)

    return byweather_df

# mendefinisikan pertanyaan 2
def create_monthly_sharing_df(df):
    monthly_sharing_df = df.resample(rule='M', on='dteday').agg({
    "casual_hourly": "sum",
    "registered_hourly": "sum",
    "cnt_hourly": "sum"
    })

    monthly_sharing_df.index = monthly_sharing_df.index.strftime('%Y-%m')
    monthly_sharing_df = monthly_sharing_df.reset_index()

    monthly_sharing_df.rename(columns={
        "dteday": "date_sharing",
        "casual_hourly": "casual_user",
        "registered_hourly": "registered_user",
        "cnt_hourly": "total_user"
    }, inplace=True)

    return monthly_sharing_df

#loading all data pada bike_df.csv
bike_df = pd.read_csv("bike_df.csv")

datetime_columns = ["dteday"]
 
for column in datetime_columns:
    bike_df[column] = pd.to_datetime(bike_df[column])

min_date = bike_df["dteday"].min()
max_date = bike_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("/content/rental bike logo.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bike_df[(bike_df["dteday"] >= str(start_date)) & 
                (bike_df["dteday"] <= str(end_date))]

byweather_df = create_byweather_df(main_df)
monthly_sharing_df = create_monthly_sharing_df(main_df)

#Membuat Header Bagian 1 (Bike Rental by Month)

st.subheader('Total Bike Rental by Month')

col1, col2 = st.columns(2)
 
with col1:
    casual = main_df.casual_hourly.sum()
    st.metric("Total Casual User", value=casual)
 
with col2:
    registered = main_df.registered_hourly.sum() 
    st.metric("Total Registered User", value=registered)

fig, ax = plt.subplots(figsize=(28, 8))
ax.plot(monthly_sharing_df["date_sharing"], monthly_sharing_df["casual_user"], marker='o', linewidth=2, color="#77BBAA", label="casual user")
ax.plot(monthly_sharing_df["date_sharing"], monthly_sharing_df["registered_user"], marker='o', linewidth=2, color="#3366BB", label="registered user")
ax.plot(monthly_sharing_df["date_sharing"], monthly_sharing_df["total_user"], marker='o', linewidth=2, color="#FF6633", label="total user")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xlabel("Date")
ax.set_ylabel("Amount User")
ax.legend()
st.pyplot(fig)

#Membuat Sub-Header (Bike Rental Performance by Weather)
st.subheader("Bike Rental Performance by Weather")

fig, ax = plt.subplots(figsize=(18, 10))

sns.barplot(
    y="Total_user", 
    x="Weather",
    data=byweather_df.sort_values(by="Total_user", ascending=False),
    ax=ax
    )
ax.set_title("Bike Rental Performance ", loc="center", fontsize=50)
ax.set_ylabel("Total sharing")
ax.set_xlabel("Weather")
st.pyplot(fig)

st.caption('Safira Dyah Khairunisa')
