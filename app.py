import streamlit as st
import pandas as pd

st.title("💊 Comparatore di Carrelli per Farmacie Online")
st.write("Inserisci i prodotti che ti servono e scopri quale farmacia ti conviene sul totale (incluse spese di spedizione)!")

# 1. Database dei prezzi di esempio per le farmacie (Farmacia A, B, C)
# Ipotizziamo i prezzi per alcuni farmaci comuni
database_prezzi = {
    "Prodotto": ["Tachipirina 500mg", "Oki Task 20 cpr", "Enterogermina 20 fl", "Multicentrum 30 cpr"],
    "Farmacia_Igea": [4.50, 6.20, 12.80, 14.90],
    "Farmacia_Loreto": [3.90, 6.80, 11.50, 15.50],
    "Amica_Farmacia": [4.20, 5.90, 13.10, 13.80]
}
df_prezzi = pd.DataFrame(database_prezzi)

# 2. Regole per le Spese di Spedizione di ogni farmacia
# [Spesa fissa, Soglia per spedizione gratuita]
regole_spedizione = {
    "Farmacia_Igea": {"costo": 4.90, "soglia_gratis": 49.00},
    "Farmacia_Loreto": {"costo": 3.90, "soglia_gratis": 39.90},
    "Amica_Farmacia": {"costo": 5.50, "soglia_gratis": 50.00}
}

# 3. Interfaccia di selezione sul sito
st.subheader("🛒 Crea il tuo carrello")
prodotti_selezionati = st.multiselect(
    "Seleziona i farmaci che vuoi acquistare:",
    options=df_prezzi["Prodotto"].tolist(),
    default=["Tachipirina 500mg", "Oki Task 20 cpr"] # di base ne preselezioniamo due
)

if prodotti_selezionati:
    # Filtriamo il database solo per i prodotti scelti
    df_filtrato = df_prezzi[df_prezzi["Prodotto"].isin(prodotti_selezionati)]
    
    st.write("### Prezzi dei singoli prodotti selezionati:")
    st.dataframe(df_filtrato.set_index("Prodotto"))

    # Calcoliamo i totali per ogni farmacia
    risultati = []
    
    # Le farmacie sono le colonne della tabella (escluse la colonna 'Prodotto')
    farmacie = [col for col in df_prezzi.columns if col != "Prodotto"]
    
    for f in farmacie:
        # Somma dei prodotti scelti in quella farmacia
        totale_prodotti = df_filtrato[f].sum()
        
        # Calcolo spedizione
        regole = regole_spedizione[f]
        if totale_prodotti >= regole["soglia_gratis"]:
            costo_spedizione = 0.0
            info_sped = "Gratis 🎉"
        else:
            costo_spedizione = regole["costo"]
            info_sped = f"{costo_spedizione:.2f} €"
            
        totale_complessivo = totale_prodotti + costo_spedizione
        
        risultati.append({
            "Farmacia": f.replace("_", " "),
            "Totale Prodotti (€)": round(totale_prodotti, 2),
            "Spedizione (€)": info_sped,
            "TOTALE DA PAGARE (€)": round(totale_complessivo, 2)
        })
        
    df_risultati = pd.DataFrame(risultati).sort_values(by="TOTALE DA PAGARE (€)")
    
    st.subheader("🏆 Classifica Convenienza del Carrello:")
    st.dataframe(df_risultati.set_index("Farmacia"))
    
    miglior_farmacia = df_risultati.iloc[0]["Farmacia"]
    miglior_prezzo = df_risultati.iloc[0]["TOTALE DA PAGARE (€)"]
    
    st.success(f"Ti conviene ordinare da **{miglior_farmacia}**! Spenderai in tutto **{miglior_prezzo} €** (prodotti + spedizione).")
else:
    st.info("Seleziona almeno un prodotto per calcolare il totale del carrello.")
