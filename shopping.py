import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Wczytaj dane
@st.cache
def load_data():
    return pd.read_csv('shopping_trends_updated.csv')

data = load_data()

# Ustawienia strony
st.title("Shopping Trends Dashboard")
st.sidebar.title("Opcje analizy")

# Filtry
age_filter = st.sidebar.slider("Wiek klienta", int(data["Age"].min()), int(data["Age"].max()), (18, 60))
category_filter = st.sidebar.multiselect("Kategorie produktów", data["Category"].unique(), data["Category"].unique())
region_filter = st.sidebar.multiselect("Region", data["Region"].unique(), data["Region"].unique())
shipping_filter = st.sidebar.multiselect("Preferencje wysyłki", data["Shipping Preference"].unique(), data["Shipping Preference"].unique())

# Filtruj dane
filtered_data = data[(data["Age"] >= age_filter[0]) & 
                     (data["Age"] <= age_filter[1]) & 
                     (data["Category"].isin(category_filter)) &
                     (data["Region"].isin(region_filter)) &
                     (data["Shipping Preference"].isin(shipping_filter))]

# Wyświetlanie danych
st.write("### Filtrowane dane", filtered_data)

# Wykresy
st.write("## Analiza wizualna")

# Wykres 1: Zakupy wg regionu
st.write("### Liczba zakupów wg regionu")
region_counts = filtered_data["Region"].value_counts()
fig, ax = plt.subplots()
region_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Region")
ax.set_ylabel("Liczba zakupów")
st.pyplot(fig)

# Wykres 2: Średnia kwota zakupów wg preferencji wysyłki
st.write("### Średnia kwota zakupów wg preferencji wysyłki")
shipping_mean = filtered_data.groupby("Shipping Preference")["Purchase Amount (USD)"].mean()
fig, ax = plt.subplots()
shipping_mean.plot(kind="bar", ax=ax)
ax.set_xlabel("Preferencje wysyłki")
ax.set_ylabel("Średnia kwota zakupów (USD)")
st.pyplot(fig)

# Wykres 3: Liczba klientów wg wieku
st.write("### Liczba klientów wg wieku")
fig, ax = plt.subplots()
filtered_data["Age"].hist(bins=20, ax=ax)
ax.set_xlabel("Wiek")
ax.set_ylabel("Liczba klientów")
st.pyplot(fig)
