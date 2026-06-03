import streamlit as st
import pandas as pd

# 1. Impostazione della pagina
st.set_page_config(
    page_title="FiutaCarrello - Il fiuto intelligente per la tua spesa", 
    page_icon="🛒", 
    layout="centered"
)

# 2. Iniezione CSS globale per sovrascrivere il tema di default di Streamlit
st.markdown("""
    <style>
    /* Sovrascrive i font e i colori nativi di Streamlit a livello globale */
    html, body, [data-testid="stMarkdownContainer"] p {
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
    }
    
    /* Forza il colore Blu Notte sul titolo principale */
    h1 {
        color: #1a237e !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        text-align: center !important;
    }
    
    /* Colore del sottotitolo */
    h3 {
        color: #5c6bc0 !important;
        font-weight: 400 !important;
        text-align: center !important;
        font-size: 1.2em !important;
    }

    /* CARD RISULTATI RIPULITE ED ELEGANTI */
    .farmacia-card {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        padding: 15px 20px !important;
        border-radius: 12px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    
    .vincitore-card {
        background-color: #f4fbf7 !important;
        border: 2px solid #00c853 !important;
        padding: 18px 20px !important;
        border-radius: 12px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(0,200,83,0.08) !important;
    }
    
    .prezzo-tag {
        font-size: 1.5em !important;
        font-weight: bold !important;
        float: right !important;
        color: #1a237e !important;
    }
    
    .prezzo-tag-vincitore {
        font-size: 1.6em !important;
        font-weight: bold !important;
        float: right !important;
        color: #00c853 !important;
    }
    
    .sped-gratis { color: #00c853 !important; font-weight: bold !important; font-size: 0.9em !important; }
    .sped-pagamento { color: #d32f2f !important; font-weight: bold !important; font-size: 0.9em !important; }
    
    .suggerimento-testo {
        background-color: #fffde7 !important;
        border-left: 4px solid #fdd835 !important;
        padding: 8px 12px !important;
        font-size: 0.85em !important;
        border-radius: 4px !important;
        margin-top: 8px !important;
        margin-bottom: 8px !important;
        color: #4e342e !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Intestazione visiva mista (Nativa + HTML) per evitare blocchi
st.markdown("<div style='text-align: center; font-size: 50px;'>🐕 🔍 🛒</div>", unsafe_allow_html=True)

# Usiamo l'HTML diretto per il titolo combinato bi-colore
st.markdown("<h1>Fiuta<span style='color: #0288d1;'>Carrello</span></h1>", unsafe_allow_html=True)
st.markdown("<h3>L'algoritmo intelligente che scova la combinazione più economica e azzera le spese di spedizione</h3>", unsafe_allow_html=True)

st.write("---")

# Data (Il nostro primo mercato di test)
farmacie_info = {
    "Farmacia Igea": {"spedizione_fissa": 4.90, "soglia_gratis": 49.00},
    "Farmacia Loreto": {"spedizione_fissa": 3.90, "soglia_gratis": 39.90},
    "Farmacie Raven": {"spedizione_fissa": 5.90, "soglia_gratis": 29.90},
    "Dr. Max": {"spedizione_fissa": 4.50, "soglia_gratis": 59.90}
}

database_prezzi = {
    "Prodotto": [
        "❤️ Armolipid Plus (Colesterolo) 60 cpr", 
        "🧪 Multicentrum Adulti 90 cpr", 
        "💅 Swisse Capelli Pelle Unghie 60 tav", 
        "🌿 Arnica Gel Forte 30% 100ml", 
        "❄️ Oscillococcinum Omeopatico 30 dosi",
        "🦠 Enterogermina Immuno Fermenti 20 cpr",
        "⚡ Supradyn Ricarica 60 cpr effervescenti",
        "🥄 Magnesio Supremo Polvere 300g",
        "🍊 Massigen Magnesio e Potassio 30 buste",
        "🧴 Somatoline Snellente 7 Notti 400ml",
        "💧 Bionike Defence Hydra Crema 50ml",
        "✨ Rilastil Crema Smagliature 200ml",
        "☀️ Eucerin Sun Fluid Viso 50+",
        "🌼 Heel Arnica Comp-Heel Omeopatico 50 tav",
        "🧠 Boiron Sedatif PC Ansia/Sonno 90 cpr"
    ],
    "Farmacia Igea": [32.90, 19.80, 16.50, 11.20, 28.40, 14.50, 22.90, 18.50, 11.90, 39.90, 16.20, 26.80, 15.90, 12.50, 13.40],
    "Farmacia Loreto": [31.50, 20.50, 15.90, 12.40, 27.90, 13.90, 21.80, 17.90, 9.90, 38.50, 15.50, 24.90, 14.20, 11.90, 12.80],
    "Farmacie Raven": [33.50, 19.50, 16.90, 10.90, 28.90, 14.20, 23.10, 18.20, 10.50, 39.00, 15.90, 25.50, 15.10, 12.20, 13.10],
    "Dr. Max": [29.90, 18.90, 14.90, 11.95, 26.90, 13.50, 20.90, 16.90, 8.90, 36.90, 14.80, 23.90, 13.90, 11.50, 12.20]
}
df_prezzi = pd.DataFrame(database_prezzi)

# Selezione prodotti
st.markdown("### 🛍️ Componi il tuo carrello:")
prodotti_selezionati = st.multiselect(
    "Aggiungi o rimuovi elementi dal tuo carrello:",
    options=df_prezzi["Prodotto"].tolist(),
    default=["💅 Swisse Capelli Pelle Unghie 60 tav", "🥄 Magnesio Supremo Polvere 300g"],
    label_visibility="collapsed"
)

if prodotti_selezionati:
    df_filtrato = df_prezzi[df_prezzi["Prodotto"].isin(prodotti_selezionati)]
    
    # Calcoli
    risultati = []
    for nome_farmacia, regole in farmacie_info.items():
        totale_prodotti = float(df_filtrato[nome_farmacia].sum())
        mancante_per_gratis = regole["soglia_gratis"] - totale_prodotti
        
        if mancante_per_gratis <= 0:
            costo_spedizione = 0.0
            info_spedizione = "<span class='sped-gratis'>Spedizione GRATIS 🎉</span>"
            suggerimento = ""
        else:
            costo_spedizione = regole["spedizione_fissa"]
            info_spedizione = f"<span class='sped-pagamento'>Spedizione: +{costo_spedizione:.2f} €</span> (soglia gratis a {regole['soglia_gratis']:.0f} €)"
            if mancante_per_gratis <= 15.00:
                suggerimento = f"🎯 <b>Il consiglio di FiutaCarrello:</b> Ti mancano solo <b>{mancante_per_gratis:.2f}€</b> per azzerare la spedizione su questo sito. Ti conviene aggiungere un piccolo prodotto per non sprecare soldi nella consegna!"
            else:
                suggerimento = ""
                
        totale_complessivo = totale_prodotti + costo_spedizione
        
        risultati.append({
            "Farmacia": nome_farmacia,
            "Totale_Prodotti": totale_prodotti,
            "Info_Spedizione": info_spedizione,
            "Suggerimento": suggerimento,
            "Prezzo_Finale": totale_complessivo
        })
        
    df_risultati = pd.DataFrame(risultati).sort_values(by="Prezzo_Finale")
    
    st.write("")
    st.markdown("### 📊 Risultati dell'analisi:")
    
    # Generazione dei riquadri
    for i, row in enumerate(df_risultati.itertuples()):
        is_vincitore = (i == 0)
        
        if i == 0: badge = "👑"
        elif i == 1: badge = "🥈"
        elif i == 2: badge = "🥉"
        else: badge = "📋"
        
        card_class = "vincitore-card" if is_vincitore else "farmacia-card"
        prezzo_class = "prezzo-tag-vincitore" if is_vincitore else "prezzo-tag"
        suggerimento_html = f"<div class='suggerimento-testo'>{row.Suggerimento}</div>" if row.Suggerimento else ""
        
        st.markdown(f"""
            <div class="{card_class}">
                <div class="{prezzo_class}">{row.Prezzo_Finale:.2f} €</div>
                <div style="font-size: 1.1em; font-weight: bold; color: #1a237e;">{badge} {row.Farmacia}</div>
                <div style="font-size: 0.9em; color: #555; margin-top: 4px;">
                    Prodotti: {row.Totale_Prodotti:.2f} € | {row.Info_Spedizione}
                </div>
                {suggerimento_html}
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"📄 Controlla la trasparenza dei singoli prezzi per {row.Farmacia}"):
            df_singolo = df_filtrato[["Prodotto", row.Farmacia]].copy()
            df_singolo.columns = ["Prodotto Selezionato", "Prezzo Singolo"]
            df_singolo["Prezzo Singolo"] = df_singolo["Prezzo Singolo"].map('{:.2f} €'.format)
            st.dataframe(df_singolo.set_index("Prodotto Selezionato"), use_container_width=True)
            
else:
    st.info("Aggiungi i prodotti in alto per attivare il fiuto del sistema.")
