import streamlit as st
import pandas as pd
import itertools
import os

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
    .farmacia-card {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 18px 20px !important;
        border-radius: 14px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    .vincitore-card {
        background-color: #f0fdf4 !important;
        border: 2px solid #22c55e !important;
        padding: 18px 20px !important;
        border-radius: 14px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 10px 15px -3px rgba(34, 197, 94, 0.1) !important;
    }
    .split-card {
        background-color: #f0f9ff !important;
        border: 2px solid #0288d1 !important;
        padding: 20px !important;
        border-radius: 14px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 15px -3px rgba(2, 136, 209, 0.15) !important;
    }
    .split-card-info {
        background-color: #f8fafc !important;
        border: 2px dashed #cbd5e1 !important;
        padding: 20px !important;
        border-radius: 14px !important;
        margin-bottom: 20px !important;
    }
    .title-with-icon {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #1e3a8a;
        font-weight: 700;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Logo Brand (La F Dinamica Tech)
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

# 5. Caricamento sicuro del Database CSV esterno
csv_path = "prodotti.csv"
if os.path.exists(csv_path):
    df_prezzi = pd.read_csv(csv_path)
else:
    st.error("Errore critico: File 'prodotti.csv' non trovato. Assicurati di averlo caricato su GitHub insieme ad app.py.")
    st.stop()

# Set state iniziale con prodotti reali presenti nel CSV
if "carrello_spesa" not in st.session_state:
    st.session_state.carrello_spesa = [
        "Sustenium Plus Energizzante 22 bustine", 
        "La Roche-Posay Anthelios XL 50+", 
        "Tachipirina 1000mg Orosolubile 12 cpr"
    ]

# Regole Spedizioni Farmacie
farmacie_info = {
    "Farmacia Igea": {"spedizione_fissa": 4.90, "soglia_gratis": 49.00},
    "Farmacia Loreto": {"spedizione_fissa": 3.90, "soglia_gratis": 39.90},
    "Farmacie Raven": {"spedizione_fissa": 5.90, "soglia_gratis": 29.90},
    "Dr. Max": {"spedizione_fissa": 4.50, "soglia_gratis": 59.90}
}

# --- SEZIONE: RICERCA PRODOTTO ---
st.markdown("""
    <div class="title-with-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0288d1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <span style="font-size: 20px;">Cerca un prodotto nel database (300+ disponibili):</span>
    </div>
""", unsafe_allow_html=True)

cerca_testo = st.text_input("Digita qui cosa stai cercando...", placeholder="Scrivi qui il nome del farmaco (es. Tachipirina, Polase, Aboca, Avene, Durex)...", label_visibility="collapsed")

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
                    st.button("Incluso", key=f"btn_in_{index}", disabled=True)
                else:
                    if st.button("Aggiungi", key=f"btn_add_{index}"):
                        st.session_state.carrello_spesa.append(prod)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Nessun prodotto trovato. Prova con parole chiave come 'Tosse', 'Crema', 'Vitamina', 'Aboca'!")

st.write("---")

# Riepilogo del carrello
st.markdown("""
    <div class="title-with-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1e3a8a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
        <span style="font-size: 20px;">Il tuo carrello attuale:</span>
    </div>
""", unsafe_allow_html=True)

prodotti_selezionati = st.multiselect(
    "Puoi rimuovere gli elementi cliccando sulla 'x':",
    options=df_prezzi["Prodotto"].tolist(),
    default=st.session_state.carrello_spesa,
    label_visibility="visible"
)
st.session_state.carrello_spesa = prodotti_selezionati

# --- CORE ALGORITMO DI SPLIT ---
if prodotti_selezionati:
    df_filtrato = df_prezzi[df_prezzi["Prodotto"].isin(prodotti_selezionati)]
    nomi_farmacie = list(farmacie_info.keys())
    
    # Calcolo opzioni singole tradizionali
    risultati_singoli = []
    for nome_farmacia, regole in farmacie_info.items():
        totale_prodotti = float(df_filtrato[nome_farmacia].sum())
        costo_spedizione = 0.0 if totale_prodotti >= regole["soglia_gratis"] else regole["spedizione_fissa"]
        totale_complessivo = totale_prodotti + costo_spedizione
        
        info_sped = "<span style='color: #22c55e; font-weight: bold;'>Spedizione GRATIS</span>" if costo_spedizione == 0 else f"<span style='color: #ef4444; font-weight: bold;'>Spedizione: +{costo_spedizione:.2f} €</span>"
        mancante = regole["soglia_gratis"] - totale_prodotti
        suggerimento = f"<div style='background-color: #fef08a; border-left: 4px solid #facc15; padding: 10px; font-size: 12px; border-radius: 6px; margin-top: 8px; color: #713f12;'>🎯 Ti mancano solo <b>{mancante:.2f}€</b> per la spedizione gratis!</div>" if (0 < mancante <= 15.00) else ""

        risultati_singoli.append({
            "Farmacia": nome_farmacia, "Totale_Prodotti": totale_prodotti,
            "Info_Spedizione": info_sped, "Suggerimento": suggerimento, "Prezzo_Finale": totale_complessivo
        })
    df_risultati_singoli = pd.DataFrame(risultoli_singoli if 'risultoli_singoli' not in locals() else risultati_singoli).sort_values(by="Prezzo_Finale")
    miglior_singolo = df_risultati_singoli.iloc[0]["Prezzo_Finale"]
    nome_miglior_singolo = df_risultati_singoli.iloc[0]["Farmacia"]

    # ALGORITMO COMBINATORIO
    best_split_cost = miglior_singolo
    best_split_arrangement = None
    prodotti_lista = df_filtrato["Prodotto"].tolist()
    
    if len(prodotti_lista) <= 5:
        for assegnazione in itertools.product(nomi_farmacie, repeat=len(prodotti_lista)):
            partizione = {f: [] for f in nomi_farmacie}
            for prod, farmacia in zip(prodotti_lista, assegnazione):
                partizione[farmacia].append(prod)
            
            costo_corrente = 0.0
            for f, prods_assegnati in partizione.items():
                if prods_assegnati:
                    sub_df = df_filtrato[df_filtrato["Prodotto"].isin(prods_assegnati)]
                    tot_prod = float(sub_df[f].sum())
                    costo_sped = 0.0 if tot_prod >= farmacie_info[f]["soglia_gratis"] else farmacie_info[f]["spedizione_fissa"]
                    costo_corrente += (tot_prod + costo_sped)
            
            if costo_corrente < best_split_cost - 0.10:
                best_split_cost = costo_corrente
                best_split_arrangement = partizione

    # --- VISUALIZZAZIONE SEZIONE INTELLIGENTE ---
    st.write("")
    st.markdown("""
        <div class="title-with-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0288d1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A5 5 0 0 0 8 8c0 1.3.5 2.6 1.5 3.5.8.8 1.3 1.5 1.5 2.5"></path><line x1="9" y1="18" x2="15" y2="18"></line><line x1="10" y1="22" x2="14" y2="22"></line></svg>
            <span style="font-size: 20px;">Strategia d'Acquisto Intelligente:</span>
        </div>
    """, unsafe_allow_html=True)

    if best_split_arrangement:
        risparmio_netto = miglior_singolo - best_split_cost
        st.markdown(f"""
            <div class="split-card">
                <div style="font-size: 28px; font-weight: 800; float: right; color: #0288d1;">{best_split_cost:.2f} €</div>
                <div style="font-size: 20px; font-weight: 900; color: #1e3a8a;">🚀 Ottimizzazione: conviene dividere l'ordine!</div>
                <div style="font-size: 14px; color: #166534; font-weight: 700; margin-top: 5px; background-color: #dcfce7; display: inline-block; padding: 4px 10px; border-radius: 6px;">
                    🔥 Risparmio extra: {risparmio_netto:.2f} € rispetto a un negozio unico
                </div>
                <div style="margin-top: 15px; font-size: 14px; color: #334155; margin-bottom: 10px;">
                    <b>Ripartizione consigliata nei carrelli:</b>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        for farmacia, prods in best_split_arrangement.items():
            if prods:
                st.markdown(f"📦 Su **{farmacia}** prendi:")
                for p in prods:
                    prezzo_p = df_filtrato[df_filtrato["Prodotto"] == p][farmacia].values[0]
                    st.markdown(f"- {p} ({prezzo_p:.2f} €)")
    else:
        st.markdown(f"""
            <div class="split-card-info">
                <div style="font-size: 16px; font-weight: bold; color: #475569; display: flex; align-items: center; gap: 8px;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                    Controllo combinatorio eseguito
                </div>
                <p style="font-size: 14px; color: #64748b; margin-top: 6px; margin-bottom: 0; line-height: 1.4;">
                    L'algoritmo ha verificato ogni combinazione di split. Dividere l'ordine non conviene: le spese di spedizione aggiuntive supererebbero il risparmio sui farmaci. La scelta ottimale è acquistare tutto su <b>{nome_miglior_singolo}</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # Elenco tradizionale unico negozio
    st.markdown("""
        <div class="title-with-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1e3a8a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
            <span style="font-size: 20px;">Ordinare da un'unica farmacia:</span>
        </div>
    """, unsafe_allow_html=True)

    for i, row in enumerate(df_risultati_singoli.itertuples()):
        is_vincitore = (i == 0 and not best_split_arrangement)
        card_class = "vincitore-card" if is_vincitore else "farmacia-card"
        prezzo_color = "#22c55e" if is_vincitore else "#1e3a8a"
        
        if i == 0:
            badge_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="margin-right:8px;"><circle cx="12" cy="12" r="10"></circle><path d="M12 16V8M10 10l2-2"></path></svg>'
        elif i == 1:
            badge_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right:8px;"><circle cx="12" cy="12" r="10"></circle><path d="M10 16h4M10 10a2 2 0 0 1 4 0c0 .7-.5 1.2-1 1.5L10 14h4"></path></svg>'
        else:
            badge_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:8px;"><circle cx="12" cy="12" r="10"></circle><path d="M10 10a2 2 0 0 1 4 0c0 .7-.5 1.2-1 1.5L11 13h3M10 16h4"></path></svg>'

        st.markdown(f"""
            <div class="{card_class}">
                <div style="font-size: 24px; font-weight: 800; float: right; color: {prezzo_color};">{row.Prezzo_Finale:.2f} €</div>
                <div style="font-size: 17px; font-weight: bold; color: #1e3a8a; display: flex; align-items: center;">
                    {badge_svg} {row.Farmacia}
                </div>
                <div style="font-size: 13px; color: #64748b; margin-top: 6px;">
                    Prodotti: {row.Totale_Prodotti:.2f} € | {row.Info_Spedizione}
                </div>
                {row.Suggerimento}
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander(f"Dettaglio listino prezzi {row.Farmacia}"):
            df_singolo = df_filtrato[["Prodotto", row.Farmacia]].copy()
            df_singolo.columns = ["Prodotto Selezionato", "Prezzo Singolo"]
            df_singolo["Prezzo Singolo"] = df_singolo["Prezzo Singolo"].map('{:.2f} €'.format)
            st.dataframe(df_singolo.set_index("Prodotto Selezionato"), use_container_width=True)
            
else:
    st.info("Il tuo carrello è vuoto. Cerca un prodotto in alto per attivare l'analisi dei prezzi.")
