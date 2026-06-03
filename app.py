import streamlit as st
import pandas as pd
import itertools

# 1. Impostazione della pagina nativa
st.set_page_config(
    page_title="FiutaCarrello - Il fiuto intelligente per la tua spesa", 
    page_icon="🛒", 
    layout="centered"
)

# 2. Iniezione CSS globale per layout e card
st.markdown("""
    <style>
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
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* CARD VINCITORE SINGOLO */
    .vincitore-card {
        background-color: #f0fdf4 !important;
        border: 2px solid #22c55e !important;
        padding: 18px 20px !important;
        border-radius: 14px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 10px 15px -3px rgba(34, 197, 94, 0.1) !important;
    }

    /* CARD SPLIT KILLER FUNCTION */
    .split-card {
        background-color: #f0f9ff !important;
        border: 2px solid #0288d1 !important;
        padding: 20px !important;
        border-radius: 14px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 15px -3px rgba(2, 136, 209, 0.15) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Logo Definitivo (La F Dinamica Tech)
st.components.v1.html("""
<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px;">
<svg width="90" height="90" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="42" fill="#f1f5f9"/>
    <path d="M35 72V28H68M35 48H60" stroke="#1e3a8a" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M52 65H68L74 48" stroke="#0288d1" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="56" cy="74" r="3" fill="#0288d1"/>
    <circle cx="66" cy="74" r="3" fill="#0288d1"/>
</svg>
</div>
""", height=100)

# 4. Intestazione Brand
st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h1 style="color: #1e3a8a; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 44px; font-weight: 800; margin: 0;">
            Fiuta<span style="color: #0288d1;">Carrello</span>
        </h1>
        <p style="color: #475569; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 16px; font-weight: 400; margin-top: 10px; line-height: 1.5; max-width: 600px; margin-left: auto; margin-right: auto;">
            L'algoritmo intelligente che scova la combinazione più economica e azzera le spese di spedizione
        </p>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# Session state per preservare il carrello
if "carrello_spesa" not in st.session_state:
    st.session_state.carrello_spesa = ["❤️ Armolipid Plus (Colesterolo) 60 cpr", "⚡ Supradyn Ricarica 60 cpr effervescenti", "🧴 Somatoline Snellente 7 Notti 400ml"]

# Regole Spedizioni Farmacie
farmacie_info = {
    "Farmacia Igea": {"spedizione_fissa": 4.90, "soglia_gratis": 49.00},
    "Farmacia Loreto": {"spedizione_fissa": 3.90, "soglia_gratis": 39.90},
    "Farmacie Raven": {"spedizione_fissa": 5.90, "soglia_gratis": 29.90},
    "Dr. Max": {"spedizione_fissa": 4.50, "soglia_gratis": 59.90}
}

# Database con immagini stabili
database_prezzi = {
    "Prodotto": [
        "❤️ Armolipid Plus (Colesterolo) 60 cpr", "🧪 Multicentrum Adulti 90 cpr", "💅 Swisse Capelli Pelle Unghie 60 tav", 
        "🌿 Arnica Gel Forte 30% 100ml", "❄️ Oscillococcinum Omeopatico 30 dosi", "🦠 Enterogermina Immuno Fermenti 20 cpr",
        "⚡ Supradyn Ricarica 60 cpr effervescenti", "🥄 Magnesio Supremo Polvere 300g", "🍊 Massigen Magnesio e Potassio 30 buste",
        "🧴 Somatoline Snellente 7 Notti 400ml", "💧 Bionike Defence Hydra Crema 50ml", "✨ Rilastil Crema Smagliature 200ml",
        "☀️ Eucerin Sun Fluid Viso 50+", "🌼 Heel Arnica Comp-Heel Omeopatico 50 tav", "🧠 Boiron Sedatif PC Ansia/Sonno 90 cpr"
    ],
    "Immagine": [
        "https://cdn-icons-png.flaticon.com/512/3024/3024613.png", "https://cdn-icons-png.flaticon.com/512/4341/4341147.png",
        "https://cdn-icons-png.flaticon.com/512/822/822143.png", "https://cdn-icons-png.flaticon.com/512/3004/3004613.png",
        "https://cdn-icons-png.flaticon.com/512/2966/2966426.png", "https://cdn-icons-png.flaticon.com/512/865/865805.png",
        "https://cdn-icons-png.flaticon.com/512/2864/2864274.png", "https://cdn-icons-png.flaticon.com/512/5061/5061214.png",
        "https://cdn-icons-png.flaticon.com/512/6122/6122393.png", "https://cdn-icons-png.flaticon.com/512/3063/3063822.png",
        "https://cdn-icons-png.flaticon.com/512/481/481116.png", "https://cdn-icons-png.flaticon.com/512/3144/3144360.png",
        "https://cdn-icons-png.flaticon.com/512/2917/2917633.png", "https://cdn-icons-png.flaticon.com/512/4341/4341071.png",
        "https://cdn-icons-png.flaticon.com/512/1047/1047683.png"
    ],
    "Farmacia Igea": [32.90, 19.80, 16.50, 11.20, 28.40, 14.50, 22.90, 18.50, 11.90, 39.90, 16.20, 26.80, 15.90, 12.50, 13.40],
    "Farmacia Loreto": [31.50, 20.50, 15.90, 12.40, 27.90, 13.90, 21.80, 17.90, 9.90, 38.50, 15.50, 24.90, 14.20, 11.90, 12.80],
    "Farmacie Raven": [33.50, 19.50, 16.90, 10.90, 28.90, 14.20, 23.10, 18.20, 10.50, 39.00, 15.90, 25.50, 15.10, 12.20, 13.10],
    "Dr. Max": [29.90, 18.90, 14.90, 11.95, 26.90, 13.50, 20.90, 16.90, 8.90, 36.90, 14.80, 23.90, 13.90, 11.50, 12.20]
}
df_prezzi = pd.DataFrame(database_prezzi)

# --- SEZIONE: RICERCA PRODOTTO ---
st.markdown("### 🔍 Cerca un prodotto da aggiungere:")
cerca_testo = st.text_input("Digita qui cosa stai cercando...", placeholder="🔎 Scrivi qui il nome del farmaco (es. Arnica, Swisse, Magnesio)...", label_visibility="collapsed")

if cerca_testo:
    df_trovati = df_prezzi[df_prezzi["Prodotto"].str.contains(cerca_testo, case=False)]
    if not df_trovati.empty:
        st.write(f"Prodotti trovati ({len(df_trovati)}):")
        for index, row in df_trovati.iterrows():
            prod = row["Prodotto"]
            img_url = row["Immagine"]
            col_img, col_text, col_btn = st.columns([1, 4, 2])
            with col_img:
                st.image(img_url, width=45)
            with col_text:
                st.markdown(f"<div style='padding-top: 10px; font-size: 15px; font-weight: 600; color: #1e3a8a;'>{prod}</div>", unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='padding-top: 4px;'>", unsafe_allow_html=True)
                if prod in st.session_state.carrello_spesa:
                    st.button("✅ Incluso", key=f"btn_in_{index}", disabled=True)
                else:
                    if st.button("🛒 Aggiungi", key=f"btn_add_{index}"):
                        st.session_state.carrello_spesa.append(prod)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Nessun prodotto trovato.")

st.write("---")

# Riepilogo del carrello attuale
st.markdown("### 🛍️ Il tuo carrello attuale:")
prodotti_selezionati = st.multiselect(
    "Puoi rimuovere gli elementi cliccando sulla 'x':",
    options=df_prezzi["Prodotto"].tolist(),
    default=st.session_state.carrello_spesa,
    label_visibility="visible"
)
st.session_state.carrello_spesa = prodotti_selezionati

# --- CORE ALGORITMO DI SPLIT & ANALISI ---
if prodotti_selezionati:
    df_filtrato = df_prezzi[df_prezzi["Prodotto"].isin(prodotti_selezionati)]
    nomi_farmacie = list(farmacie_info.keys())
    
    # 1. Calcolo opzioni singole tradizionali
    risultati_singoli = []
    for nome_farmacia, regole in farmacie_info.items():
        totale_prodotti = float(df_filtrato[nome_farmacia].sum())
        costo_spedizione = 0.0 if totale_prodotti >= regole["soglia_gratis"] else regole["spedizione_fissa"]
        totale_complessivo = totale_prodotti + costo_spedizione
        
        info_sped = "<span style='color: #22c55e; font-weight: bold;'>Spedizione GRATIS 🎉</span>" if costo_spedizione == 0 else f"<span style='color: #ef4444; font-weight: bold;'>Spedizione: +{costo_spedizione:.2f} €</span>"
        mancante = regole["soglia_gratis"] - totale_prodotti
        suggerimento = f"<div style='background-color: #fef08a; border-left: 4px solid #facc15; padding: 10px; font-size: 12px; border-radius: 6px; margin-top: 8px; color: #713f12;'>🎯 Ti mancano solo <b>{mancante:.2f}€</b> per la spedizione gratis!</div>" if (0 < mancante <= 15.00) else ""

        risultati_singoli.append({
            "Farmacia": nome_farmacia, "Totale_Prodotti": totale_prodotti,
            "Info_Spedizione": info_sped, "Suggerimento": suggerimento, "Prezzo_Finale": totale_complessivo
        })
    df_risultati_singoli = pd.DataFrame(risultati_singoli).sort_values(by="Prezzo_Finale")
    miglior_singolo = df_risultati_singoli.iloc[0]["Prezzo_Finale"]

    # 2. ALGORITMO DI SPLIT (Ricerca combinatoria su tutte le farmacie)
    best_split_cost = miglior_singolo
    best_split_arrangement = None  # Conterrà la divisione ideale dei prodotti

    # Genera tutte le possibili assegnazioni dei prodotti selezionati alle farmacie disponibili
    # Esempio: se ho 3 prodotti, cerco tutte le combinazioni possibili di ripartizione
    prodotti_lista = df_filtrato["Prodotto"].tolist()
    
    # Per evitare calcoli infiniti in modalità prototipo, limitiamo l'analisi combinatoria a massimo 5 prodotti
    if len(prodotti_lista) <= 5:
        for assegnazione in itertools.product(nomi_farmacie, repeat=len(prodotti_lista)):
            partizione = {f: [] for f in nomi_farmacie}
            for prod, farmacia in zip(prodotti_lista, assegnazione):
                partizione[farmacia].append(prod)
            
            # Calcola il costo di questa specifica partizione
            costo_corrente = 0.0
            for f, prods_assegnati in partizione.items():
                if prods_assegnati:
                    sub_df = df_filtrato[df_filtrato["Prodotto"].isin(prods_assegnati)]
                    tot_prod = float(sub_df[f].sum())
                    costo_sped = 0.0 if tot_prod >= farmacie_info[f]["soglia_gratis"] else farmacie_info[f]["spedizione_fissa"]
                    costo_corrente += (tot_prod + costo_sped)
            
            # Se lo split corrente costa MENO del miglior negozio singolo, lo memorizziamo
            if costo_corrente < best_split_cost - 0.05:  # Tolleranza di 5 centesimi per rendere significativo il risparmio
                best_split_cost = costo_corrente
                best_split_arrangement = partizione

    # --- VISUALIZZAZIONE RISULTATI ---
    st.markdown("### 📊 Risultati dell'analisi intelligente:")

    # Se lo split fa risparmiare, mostra la CARD SPECIAL KILLER FEATURE in cima
    if best_split_arrangement:
        risparmio_netto = miglior_singolo - best_split_cost
        st.markdown(f"""
            <div class="split-card">
                <div style="font-size: 28px; font-weight: 800; float: right; color: #0288d1;">{best_split_cost:.2f} €</div>
                <div style="font-size: 20px; font-weight: 900; color: #1e3a8a;">🚀 Super Fiuto: Conviene Dividere il Carrello!</div>
                <div style="font-size: 15px; color: #166534; font-weight: 700; margin-top: 5px; background-color: #dcfce7; display: inline-block; padding: 3px 8px; border-radius: 4px;">
                    🔥 Risparmi extra {risparmio_netto:.2f} € rispetto a comprare tutto su un unico sito!
                </div>
                <div style="margin-top: 15px; font-size: 14px; color: #334155;">
                    <b>Ecco come devi dividere i prodotti:</b>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Mostra la ripartizione dei prodotti all'interno della card dello split
        for farmacia, prods in best_split_arrangement.items():
            if prods:
                st.markdown(f"📦 Su **{farmacia}** acquista:")
                for p in prods:
                    prezzo_p = df_filtrato[df_filtrato["Prodotto"] == p][farmacia].values[0]
                    st.markdown(f"- {p} (`{prezzo_p:.2f} €`)")
        st.write("---")

    # Mostra l'elenco tradizionale del "Tutto in un unico negozio"
    st.markdown("#### 📋 Comprare tutto da un'unica farmacia:")
    for i, row in enumerate(df_risultati_singoli.itertuples()):
        is_vincitore = (i == 0 and not best_split_arrangement)
        card_class = "vincitore-card" if is_vincitore else "farmacia-card"
        prezzo_color = "#22c55e" if is_vincitore else "#1e3a8a"
        badge = "👑" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "📋"
        
        st.markdown(f"""
            <div class="{card_class}">
                <div style="font-size: 24px; font-weight: 800; float: right; color: {prezzo_color};">{row.Prezzo_Finale:.2f} €</div>
                <div style="font-size: 17px; font-weight: bold; color: #1e3a8a;">{badge} {row.Farmacia}</div>
                <div style="font-size: 13px; color: #64748b; margin-top: 4px;">
                    Prodotti: {row.Totale_Prodotti:.2f} € | {row.Info_Spedizione}
                </div>
                {row.Suggerimento}
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"📄 Vedi i singoli prezzi di {row.Farmacia}"):
            df_singolo = df_filtrato[["Prodotto", row.Farmacia]].copy()
            df_singolo.columns = ["Prodotto Selezionato", "Prezzo Singolo"]
            df_singolo["Prezzo Singolo"] = df_singolo["Prezzo Singolo"].map('{:.2f} €'.format)
            st.dataframe(df_singolo.set_index("Prodotto Selezionato"), use_container_width=True)
            
else:
    st.info("Il tuo carrello è vuoto. Cerca un prodotto in alto e clicca su 'Aggiungi' per attivare l'analisi dei prezzi.")
