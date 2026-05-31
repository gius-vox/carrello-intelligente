import streamlit as st
import pandas as pd

st.title("💊 Comparatore di Carrelli per Farmacie Online")
st.write("Inserisci i prodotti che ti servono e scopri quale farmacia ti conviene sul totale (incluse spese di spedizione)!")

# 1. Definizione chiara dei dati e delle soglie di spedizione gratis
farmacie_info = {
    "Farmacia Igea": {"spedizione_fissa": 4.90, "soglia_gratis": 49.00},
    "Farmacia Loreto": {"spedizione_fissa": 3.90, "soglia_gratis": 39.90},
    "Amica Farmacia": {"spedizione_fissa": 5.50, "soglia_gratis": 50.00}
}

database_prezzi = {
    "Prodotto": ["Tachipirina 500mg", "Oki Task 20 cpr", "Enterogermina 20 fl", "Multicentrum 30 cpr", "Solfac Gel Scarafaggi", "Ananase 40 cpr"],
    "Farmacia Igea": [4.50, 6.20, 12.80, 14.90, 19.50, 11.20],
    "Farmacia Loreto": [3.90, 6.80, 11.50, 15.50, 18.90, 11.90],
    "Amica Farmacia": [4.20, 5.90, 13.10, 13.80, 20.10, 10.50]
}
df_prezzi = pd.DataFrame(database_prezzi)

# 2. Interfaccia di selezione sul sito
st.subheader("🛒 Crea il tuo carrello")
prodotti_selezionati = st.multiselect(
    "Seleziona i farmaci che vuoi acquistare:",
    options=df_prezzi["Prodotto"].tolist(),
    default=["Tachipirina 500mg", "Oki Task 20 cpr"]
)

if prodotti_selezionati:
    # Filtriamo i prodotti scelti
    df_filtrato = df_prezzi[df_prezzi["Prodotto"].isin(prodotti_selezionati)]
    
    st.write("### Prezzi dei singoli prodotti selezionati:")
    st.dataframe(df_filtrato.set_index("Prodotto"))

    # 3. Calcolo dinamico con indicazione di quanto manca alla spedizione gratuita
    risultati = []
    
    for nome_farmacia, regole in farmacie_info.items():
        totale_prodotti = float(df_filtrato[nome_farmacia].sum())
        
        # Calcolo della differenza per la spedizione gratuita
        mancante_per_gratis = regole["soglia_gratis"] - totale_prodotti
        
        if mancante_per_gratis <= 0:
            costo_spedizione = 0.0
            testo_spedizione = "0.00 € (Gratis 🎉)"
            testo_mancante = "Raggiunta! ✅"
        else:
            costo_spedizione = regole["spedizione_fissa"]
            testo_spedizione = f"{costo_spedizione:.2f} €"
            testo_mancante = f"Mancano {mancante_per_gratis:.2f} €"
            
        totale_complessivo = totale_prodotti + costo_spedizione
        
        risultati.append({
            "Farmacia": nome_farmacia,
            "Totale Prodotti (€)": round(totale_prodotti, 2),
            "Spedizione (€)": testo_spedizione,
            "Manca a Sped. Gratis": testo_mancante,
            "Soglia Gratis Sped.": f"{regole['soglia_gratis']:.2f} €",
            "TOTALE DA PAGARE (€)": round(totale_complessivo, 2)
        })
        
    # Ordiniamo la classifica dal più economico al più caro
    df_risultati = pd.DataFrame(risultati).sort_values(by="TOTALE DA PAGARE (€)")
    
    st.subheader("🏆 Classifica Convenienza del Carrello:")
    st.dataframe(df_risultati.set_index("Farmacia"))
    
    miglior_farmacia = df_risultati.iloc[0]["Farmacia"]
    miglior_prezzo = df_risultati.iloc[0]["TOTALE DA PAGARE (€)"]
    
    st.success(f"Ti conviene ordinare da **{miglior_farmacia}**! Spenderai in tutto **{miglior_prezzo:.2f} €** (prodotti + spedizione).")
else:
    st.info("Seleziona almeno un prodotto per calcolare il totale del carrello.")
