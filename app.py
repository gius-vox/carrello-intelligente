import streamlit as st
import pandas as pd

st.title("🛒 Carrello Intelligente")
st.write("Benvenuto nel tuo comparatore di prezzi personale!")

# Creiamo una tabella di esempio per i prodotti
dati = {
    "Prodotto": ["Pane", "Latte", "Caffè", "Pasta"],
    "Supermercato A (€)": [1.50, 1.20, 2.50, 0.85],
    "Supermercato B (€)": [1.40, 1.30, 2.40, 0.90]
}
df = pd.DataFrame(dati)

# Mostriamo la tabella sul sito
st.subheader("Confronto Prezzi:")
st.dataframe(df)

# Un piccolo selettore interattivo
prodotto_scelto = st.selectbox("Seleziona un prodotto per vedere dove costa meno:", df["Prodotto"])
prezzo_a = df[df["Prodotto"] == prodotto_scelto]["Supermercato A (€)"].values[0]
prezzo_b = df[df["Prodotto"] == prodotto_scelto]["Supermercato B (€)"].values[0]

if prezzo_a < prezzo_b:
    st.success(f"Conviene comprare il/la {prodotto_scelto} al Supermercato A! Risparmi {round(prezzo_b - prezzo_a, 2)}€")
else:
    st.success(f"Conviene comprare il/la {prodotto_scelto} al Supermercato B! Risparmi {round(prezzo_a - prezzo_b, 2)}€")
