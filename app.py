import streamlit as st
import pandas as pd

st.title("💊 Comparatore di Carrelli: Integratori, Omeopatia e Cosmesi")
st.write("Inserisci i prodotti che ti servono e scopri quale farmacia ti conviene sul totale (con logica spedizioni e suggerimenti smart)!")

# 1. Regole spedizioni per 4 farmacie reali
farmacie_info = {
    "Farmacia Igea": {"spedizione_fissa": 4.90, "soglia_gratis": 49.00},
    "Farmacia Loreto": {"spedizione_fissa": 3.90, "soglia_gratis": 39.90},
    "Farmacie Raven": {"spedizione_fissa": 5.90, "soglia_gratis": 29.90},
    "Dr. Max": {"spedizione_fissa": 4.50, "soglia_gratis": 59.90}
}

# 2. Database REALE mappato su 4 farmacie
database_prezzi = {
    "Prodotto": [
        "Armolipid Plus (Colesterolo) 60 cpr", 
        "Multicentrum Adulti 90 cpr", 
        "Swisse Capelli Pelle Unghie 60 tav", 
        "Arnica Gel Forte 30% 100ml", 
        "Oscillococcinum Omeopatico 30 dosi",
        "Enterogermina Immuno Fermenti 20 cpr",
        "Supradyn Ricarica 60 cpr effervescenti",
        "Magnesio Supremo Polvere 300g",
        "Massigen Magnesio e Potassio 30 buste",
        "Somatoline Snellente 7 Notti 400ml",
        "Bionike Defence Hydra Crema 50ml",
        "Rilastil Crema Smagliature 200ml",
        "Eucerin Sun Fluid Viso 50+",
        "Heel Arnica Comp-Heel Omeopatico 50 tav",
        "Boiron Sedatif PC Ansia/Sonno 90 cpr"
    ],
    "Farmacia Igea": [32.90, 19.80, 16.50, 11.20, 28.40, 14.50, 22.90, 18.50, 11.90, 39.90, 16.20, 26.80, 15.90, 12.50, 13.40],
    "Farmacia Loreto": [31.50, 20.50, 15.90, 12.40, 27.90, 13.90, 21.80, 17.90, 9.90, 38.50, 15.50, 24.90, 14.20, 11.90, 12.80],
    "Farmacie Raven": [33.50, 19.50, 16.90, 10.90, 28.90, 14.20, 23.10, 18.20, 10.50, 39.00, 15.90, 25.50, 15.10, 12.20, 13.10],
    "Dr. Max": [29.90, 18.90, 14.90, 11.95, 26.90, 13.50, 20.90, 16.90, 8.90, 36.90, 14.80, 23.90, 13.90, 11.50, 12.20]
}
df_prezzi = pd.DataFrame(database_prezzi)

# 3. Selezione Prodotti da parte dell'utente
st.subheader("🛒 Componi il tuo carrello reale")
prodotti_selezionati = st.multiselect(
    "Seleziona i prodotti da inserire nel carrello (puoi sceglierne quanti ne vuoi):",
    options=df_prezzi["Prodotto"].tolist(),
    default=["Swisse Capelli Pelle Unghie 60 tav", "Magnesio Supremo Polvere 300g"] # Esempio iniziale sui 33-34€ totali
)

if prodotti_selezionati:
    df_filtrato = df_prezzi[df_prezzi["Prodotto"].isin(prodotti_selezionati)]
    
    st.write("### 🏷️ Prezzi di dettaglio nelle varie farmacie:")
    st.dataframe(df_filtrato.set_index("Prodotto"))

    # Calcoli dinamici del carrello complessivo
    risultati = []
    suggerimenti = []
    
    for nome_farmacia, regole in farmacie_info.items():
        totale_prodotti = float(df_filtrato[nome_farmacia].sum())
        mancante_per_gratis = regole["soglia_gratis"] - totale_prodotti
        
        if mancante_per_gratis <= 0:
            costo_spedizione = 0.0
            testo_spedizione = "0.00 € (Gratis 🎉)"
            testo_mancante = "Raggiunta! ✅"
        else:
            costo_spedizione = regole["spedizione_fissa"]
            testo_spedizione = f"{costo_spedizione:.2f} €"
            testo_mancante = f"Mancano {mancante_per_gratis:.2f} €"
            
            # SUGGERIMENTO SMART: se mancano meno di 15€, avvisa l'utente
            if mancante_per_gratis <= 15.00:
                suggerimenti.append(f"💡 **{nome_farmacia}**: ti mancano appena **{mancante_per_gratis:.2f}€** per sbloccare la spedizione gratuita ed evitare di sprecare {costo_spedizione:.2f}€ di consegna!")
            
        totale_complessivo = totale_prodotti + costo_spedizione
        
        risultati.append({
            "Farmacia": nome_farmacia,
            "Totale Prodotti (€)": round(totale_prodotti, 2),
            "Spedizione (€)": testo_spedizione,
            "Manca a Sped. Gratis": testo_mancante,
            "Soglia Sped. Gratis": f"{regole['soglia_gratis']:.2f} €",
            "TOTALE CARRELLO (€)": round(totale_complessivo, 2)
        })
        
    df_risultati = pd.DataFrame(risultati).sort_values(by="TOTALE CARRELLO (€)")
    
    st.subheader("🏆 Classifica Convenienza Finale (Spedizioni Incluse):")
    st.dataframe(df_risultati.set_index("Farmacia"))
    
    # Vincitore assoluto
    miglior_farmacia = df_risultati.iloc[0]["Farmacia"]
    miglior_prezzo = df_risultati.iloc[0]["TOTALE CARRELLO (€)"]
    
    st.success(f"🥇 Il vincitore è **{miglior_farmacia}**! L'intero carrello ti costa in tutto **{miglior_prezzo:.2f} €**.")
    
    # Mostriamo i consigli se attivi
    if suggerimenti:
        st.subheader("🧠 Strategie d'acquisto intelligenti:")
        for sug in suggerimenti:
            st.info(sug)
else:
    st.info("Seleziona i prodotti dal menu sopra per vedere il confronto dei carrelli.")
