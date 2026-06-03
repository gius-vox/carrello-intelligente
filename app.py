import streamlit as st
import pandas as pd

# 1. Impostazione della pagina nativa
st.set_page_config(
    page_title="FiutaCarrello - Il fiuto intelligente per la tua spesa", 
    page_icon="🛒", 
    layout="centered"
)

# 2. Iniezione CSS globale per layout e card
st.markdown("""
    <style>
    /* Forza il font moderno su tutta la pagina */
    html, body, [data-testid="stMarkdownContainer"] p {
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
    }
    
    /* CARD STANDARD */
    .farmacia-card {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 18px 20px !important;
        border-radius: 14px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
    }
    
    /* CARD VINCITORE */
    .vincitore-card {
        background-color: #f0fdf4 !important;
        border: 2px solid #22c55e !important;
        padding: 18px 20px !important;
        border-radius: 14px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 10px 15px -3px rgba(34, 197, 94, 0.1), 0 4px 6px -4px rgba(34, 197, 94, 0.1) !important;
    }
    
    /* Contenitore logo centrato */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Logo Definitivo (La F Dinamica Tech)
st.markdown("""
<div class="logo-container">
<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- Cerchio di sfondo tech morbido -->
    <circle cx="50" cy="50" r="42" fill="#f1f5f9"/>
    <!-- Lettera F fusa con scia dinamica -->
    <path d="M35 72V28H68M35 48H60" stroke="#1e3a8a" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Simbolo del carrello minimale che taglia la F -->
    <path d="M52 65H68L74 48" stroke="#0288d1" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="56" cy="74" r="3" fill="#0288d1"/>
    <circle cx="66" cy="74" r="3" fill="#0288d1"/>
</svg>
</div>
""", unsafe_allow_html=True)

# 4. Intestazione Brand
st.html("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h1 style="color: #1e3a8a; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 46px; font-weight: 800; margin: 0;">
            Fiuta<span style="color: #0288d1;">Carrello</span>
        </h1>
        <p style="color: #475569; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 16px; font-weight: 400; margin-top: 12px; line-height: 1.5; max-width: 600px; margin-left: auto; margin-right: auto;">
            L'algoritmo intelligente che scova la combinazione più economica e azzera le spese di spedizione
        </p>
    </div>
""")

st.write("---")

# Gestione dello stato del carrello per evitare che si svuoti al click dei bottoni
if "carrello_spesa" not in st.session_state:
    st.session_state.carrello_spesa = ["💅 Swisse Capelli Pelle Unghie 60 tav", "🥄 Magnesio Supremo Polvere 300g"]

# Data (Il nostro database)
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

# --- NUOVA SEZIONE: CERCA E COMPONI IL CARRELLO ---
st.markdown("### 🔍 Cerca un prodotto da aggiungere:")
cerca_testo = st.text_input("Digita qui cosa stai cercando (es. Magnesio, Crema, Swisse...)", placeholder="🔎 Scrivi qui il nome del farmaco o integratore...", label_visibility="collapsed")

if cerca_testo:
    # Filtra il database in base a cosa scrive l'utente (senza fare distinzione tra maiuscole e minuscole)
    prodotti_trovati = df_prezzi[df_prezzi["Prodotto"].str.contains(cerca_testo, case=False)]["Prodotto"].tolist()
    
    if prodotti_trovati:
        st.write(f"Prodotti trovati ({len(prodotti_trovati)}):")
        for prod in prodotti_trovati:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{prod}**")
            with col2:
                # Se il prodotto è già nel carrello mostra un feedback, altrimenti mostra il bottone per aggiungerlo
                if prod in st.session_state.carrello_spesa:
                    st.button("✅ Nel Carrello", key=f"btn_in_{prod}", disabled=True)
                else:
                    if st.button("🛒 Aggiungi", key=f"btn_add_{prod}"):
                        st.session_state.carrello_spesa.append(prod)
                        st.rerun()
    else:
        st.warning("Nessun prodotto trovato nel database con questo nome. Prova a scrivere un'altra parola chiave!")

st.write("---")

# Visualizzazione e riepilogo del carrello corrente
st.markdown("### 🛍️ Il tuo carrello attuale:")
prodotti_selezionati = st.multiselect(
    "Puoi rimuovere gli elementi cliccando sulla 'x':",
    options=df_prezzi["Prodotto"].tolist(),
    default=st.session_state.carrello_spesa,
    label_visibility="visible"
)

# Sincronizza lo stato globale se l'utente rimuove prodotti dalla lista multiselect
st.session_state.carrello_spesa = prodotti_selezionati

# --- CALCOLO RISULTATI ---
if prodotti_selezionati:
    df_filtrato = df_prezzi[df_prezzi["Prodotto"].isin(prodotti_selezionati)]
    
    risultati = []
    for nome_farmacia, regole in farmacie_info.items():
        totale_prodotti = float(df_filtrato[nome_farmacia].sum())
        mancante_per_gratis = regole["soglia_gratis"] - totale_prodotti
        
        if mancante_per_gratis <= 0:
            costo_spedizione = 0.0
            info_spedizione = "<span style='color: #22c55e; font-weight: bold;'>Spedizione GRATIS 🎉</span>"
            suggerimento = ""
        else:
            costo_spedizione = regole["spedizione_fissa"]
            info_spedizione = f"<span style='color: #ef4444; font-weight: bold;'>Spedizione: +{costo_spedizione:.2f} €</span> (soglia gratis a {regole['soglia_gratis']:.0f} €)"
            if mancante_per_gratis <= 15.00:
                suggerimento = f"<div style='background-color: #fef08a; border-left: 4px solid #facc15; padding: 10px 14px; font-size: 13px; border-radius: 6px; margin-top: 10px; color: #713f12;'>🎯 <b>Il consiglio di FiutaCarrello:</b> Ti mancano solo <b>{mancante_per_gratis:.2f}€</b> per azzerare la spedizione su questo sito! Conviene aggiungere un piccolo prodotto.</div>"
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
    
    for i, row in enumerate(df_risultati.itertuples()):
        is_vincitore = (i == 0)
        
        if i == 0: badge = "👑"
        elif i == 1: badge = "🥈"
        elif i == 2: badge = "🥉"
        else: badge = "📋"
        
        if is_vincitore:
            card_class = "vincitore-card"
            prezzo_color = "#22c55e"
        else:
            card_class = "farmacia-card"
            prezzo_color = "#1e3a8a"
        
        st.markdown(f"""
            <div class="{card_class}">
                <div style="font-size: 26px; font-weight: 800; float: right; color: {prezzo_color};">{row.Prezzo_Finale:.2f} €</div>
                <div style="font-size: 18px; font-weight: bold; color: #1e3a8a;">{badge} {row.Farmacia}</div>
                <div style="font-size: 14px; color: #64748b; margin-top: 6px;">
                    Prodotti: {row.Totale_Prodotti:.2f} € | {row.Info_Spedizione}
                </div>
                {row.Suggerimento}
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"📄 Controlla la trasparenza dei singoli prezzi per {row.Farmacia}"):
            df_singolo = df_filtrato[["Prodotto", row.Farmacia]].copy()
            df_singolo.columns = ["Prodotto Selezionato", "Prezzo Singolo"]
            df_singolo["Prezzo Singolo"] = df_singolo["Prezzo Singolo"].map('{:.2f} €'.format)
            st.dataframe(df_singolo.set_index("Prodotto Selezionato"), use_container_width=True)
            
else:
    st.info("Il tuo carrello è vuoto. Cerca un prodotto in alto e clicca su 'Aggiungi' per attivare l'analisi dei prezzi.")
