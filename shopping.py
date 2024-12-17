import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Wczytaj dane
@st.cache
def load_data():
    return pd.read_csv('shopping_trends.csv')

data = load_data()

# Ustawienia strony
st.title("Shopping Trends Dashboard")
st.sidebar.title("Opcje analizy")

# Filtry
age_filter = st.sidebar.slider("Wiek klienta", int(data["Age"].min()), int(data["Age"].max()), (18, 60))
category_filter = st.sidebar.multiselect("Kategorie produktów", data["Category"].unique(), data["Category"].unique())
location_filter = st.sidebar.multiselect("Lokalizacja", data["Location"].unique(), data["Location"].unique())
shipping_filter = st.sidebar.multiselect("Preferencje wysyłki", data["Shipping Type"].unique(), data["Shipping Type"].unique())

# Filtruj dane
filtered_data = data[(data["Age"] >= age_filter[0]) & 
                     (data["Age"] <= age_filter[1]) & 
                     (data["Category"].isin(category_filter)) &
                     (data["Location"].isin(location_filter)) &
                     (data["Shipping Type"].isin(shipping_filter))]

# Wyświetlanie danych
st.write("### Filtrowane dane", filtered_data)

# Wykresy
st.write("## Analiza wizualna")

# Wykres 1: Zakupy wg kategorii
st.write("### Liczba zakupów wg kategorii")
category_counts = filtered_data["Category"].value_counts()
fig, ax = plt.subplots()
category_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Kategoria")
ax.set_ylabel("Liczba zakupów")
st.pyplot(fig)

# Wykres 2: Średnia kwota zakupów wg sezonu
st.write("### Średnia kwota zakupów wg sezonu")
season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
fig, ax = plt.subplots()
season_mean.plot(kind="bar", ax=ax)
ax.set_xlabel("Sezon")
ax.set_ylabel("Średnia kwota zakupów (USD)")
st.pyplot(fig)

# Wykres 3: Liczba klientów wg wieku
st.write("### Liczba klientów wg wieku")
fig, ax = plt.subplots()
filtered_data["Age"].hist(bins=20, ax=ax)
ax.set_xlabel("Wiek")
ax.set_ylabel("Liczba klientów")
st.pyplot(fig)

# Wykres 4: Średnia kwota zakupów wg rodzaju wysyłki
st.write("### Średnia kwota zakupów wg rodzaju wysyłki")
fig, ax = plt.subplots()
filtered_data["Shipping Type"].hist(bins=20, ax=ax)
ax.set_xlabel("Rodzaj wysyłki")
ax.set_ylabel("Średnia kwota zakupów (USD)")
st.pyplot(fig)

# Wykres 5: Zakupy wg regionu
st.write("### Liczba zakupów wg Lokalizacji")
region_counts = filtered_data["Location"].value_counts()
fig, ax = plt.subplots()
region_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Lokalizacja")
ax.set_ylabel("Liczba zakupów")
plt.xticks(xlabel, [str(i) for i in y], rotation=90)
plt.tick_params(axis='x', which='major', labelsize=5)
st.pyplot(fig)
