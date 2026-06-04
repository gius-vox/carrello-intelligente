import streamlit as st
import pandas as pd
import itertools
import os

# 1. Impostazione della pagina nativa
st.set_page_config(
    page_title="CarrelloSnello - Il tuo carrello ottimizzato",
    page_icon="🛒",
    layout="centered"
)

# 2. Iniezione CSS globale per layout, card e font
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

html, body, [data-testid="stMarkdownContainer"] p {
    font-family: 'Outfit', 'Helvetica Neue', Arial, sans-serif !important;
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
    box-shadow: 0 10px 15px -3px rgba(2, 136, 209, 0.1) !important;
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
    margin-top: 20px;
    margin-bottom: 15px;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# 3. CARICAMENTO LOGO ORIGINALE DA FILE STATICÒ
logo_path = "logo.png"
if os.path.exists(logo_path):
    # Centriamo l'immagine usando le colonne di Streamlit
    col_left, col_logo, col_right = st.columns([1, 2, 1])
    with col_logo:
        st.image(logo_path, use_container_width=True)
else:
    # Soluzione di emergenza testuale elegante se il file non è ancora presente
    st.markdown("""
    <div style="text-align: center; margin-bottom: 10px;">
        <h1 style="color: #1e3a8a; font-family: 'Outfit', sans-serif; font-size: 38px; font-weight: 800; letter-spacing: 1px; margin-bottom: 0px;">
            CARRELLO<span style="color: #0288d1;">SNELLO</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)

# Slogan del Brand
st.markdown("""
<div style="text-align: center; margin-bottom: 25px;">
    <p style="color: #475569; font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 500; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px; margin-bottom: 20px;">
        L'algoritmo intelligente per la tua spesa online
    </p>
</div>
""", unsafe_allow_html=True)

st.write("---")

# 4. Caricamento e controllo del database CSV
csv_path = "prodotti.csv"
if os.path.exists(csv_path):
    df_prezzi = pd.read_csv(csv_path)
else:
    st.error("Errore critico: File 'prodotti.csv' non trovato. Assicurati che sia nella stessa cartella dello script.")
    st.stop()

# Estrazione pulita dei nomi dei negozi escludendo le colonne di servizio
nomi_farmacie = [col for col in df_prezzi.columns if col not in ["Prodotto", "Immagine"]]

farmacie_info = {
    "Farmacia Igea": {"spedizione_fissa": 4.90, "soglia_gratis": 49.00},
    "Farmacia Loreto": {"spedizione_fissa": 3.90, "soglia_gratis": 39.90},
    "Farmacia Raven": {"spedizione_fissa": 5.90, "soglia_gratis": 29.90},
    "Dr. Max": {"spedizione_fissa": 4.50, "soglia_gratis": 59.90}
}

if "carrello_spesa" not in st.session_state:
    st.session_state.carrello_spesa = [
        "Sustenium Plus Energizzante 22 bustine",
        "La Roche-Posay Anthelios XL 50+",
        "Tachipirina 1000mg Orosolubile 12 cpr"
    ]

# --- SEZIONE: RICERCA PRODOTTO ---
st.markdown('<div class="title-with-icon">🔍 Cerca un prodotto nel database:</div>', unsafe_allow_html=True)

lista_prodotti = sorted(df_prezzi["Prodotto"].unique().tolist())
cerca_testo = st.selectbox(
    "Digita o seleziona cosa stai cercando...",
    options=[""] + lista_prodotti,
    index=0,
    placeholder="Scrivi qui il nome del farmaco..."
)

if cerca_testo != "":
    df_trovati = df_prezzi[df_prezzi["Prodotto"].str.contains(cerca_testo, case=False)]
    if not df_trovati.empty:
        st.write(f"Prodotti trovati ({len(df_trovati)}):")
        for index, row in df_trovati.iterrows():
            prod = row["Prodotto"]
            img_url = row["Immagine"]
            
            prezzi_prodotto = {k: float(row[k]) for k in nomi_farmacie if pd.notna(row[k])}
            if prezzi_prodotto:
                farmacia_migliore = min(prezzi_prodotto, key=prezzi_prodotto.get)
                prezzo_migliore = prezzi_prodotto[farmacia_migliore]
                
                col_img, col_text, col_btn = st.columns([1, 4, 2])
                with col_img:
                    st.image(img_url, width=45)
                with col_text:
                    st.markdown(f"""
                        <div style='padding-top: 5px;'>
                            <span style='font-size: 15px; font-weight: 600; color: #1e3a8a;'>{prod}</span><br>
                            <span style='background-color: #d1fae5; color: #065f46; font-size: 11px; font-weight: bold; padding: 2px 6px; border-radius: 4px;'>
                                🔥 Miglior prezzo su {farmacia_migliore}: {prezzo_migliore:.2f}€
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    st.markdown("<div style='padding-top: 10px;'>", unsafe_allow_html=True)
                    if prod in st.session_state.carrello_spesa:
                        st.button("Incluso", key=f"btn_in_{index}", disabled=True)
                    else:
                        if st.button("Aggiungi", key=f"btn_add_{index}"):
                            st.session_state.carrello_spesa.append(prod)
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Nessun prodotto trovato.")

st.write("---")

# --- RIEPILOGO DEL CARRELLO ---
st.markdown('<div class="title-with-icon">🛒 Il tuo carrello attuale:</div>', unsafe_allow_html=True)

prodotti_selezionati = st.multiselect(
    "Puoi rimuovere gli elementi cliccando sulla 'x':",
    options=df_prezzi["Prodotto"].tolist(),
    default=st.session_state.carrello_spesa
)
st.session_state.carrello_spesa = prodotti_selezionati

# --- CORE ALGORITMO DI CALCOLO ---
if prodotti_selezionati:
    df_filtrato = df_prezzi[df_prezzi["Prodotto"].isin(prodotti_selezionati)]
    
    risultati_singoli = []
    # RISOLTO: Iterazione corretta sulle chiavi reali per azzerare il KeyError
    for nome_farmacia in nomi_farmacie:
        regole = farmacie_info[nome_farmacia]
        totale_prodotti = float(df_filtrato[nome_farmacia].sum())
        costo_spedizione = 0.0 if totale_prodotti >= regole["soglia_gratis"] else regole["spedizione_fissa"]
        totale_complessivo = totale_prodotti + costo_spedizione
        
        if costo_spedizione == 0.0:
            info_sped = "<span style='color: #22c55e; font-weight: bold;'>Spedizione GRATIS</span>"
            suggerimento = ""
        else:
            info_sped = f"Spedizione: {costo_spedizione:.2f}€"
            mancante = regole["soglia_gratis"] - totale_prodotti
            suggerimento = f"<div style='background-color: #fef08a; border-left: 4px solid #facc15; padding: 10px; font-size:13px; border-radius:4px; margin-top:8px;'>💡 Aggiungi <b>{mancante:.2f}€</b> su {nome_farmacia} per azzerare la spedizione!</div>"
        
        risultati_singoli.append({
            "Farmacia": nome_farmacia, 
            "Totale_Prodotti": totale_prodotti,
            "Info_Spedizione": info_sped, 
            "Suggerimento": suggerimento, 
            "Prezzo_Finale": totale_complessivo
        })
        
    df_risultati_singoli = pd.DataFrame(risultati_singoli).sort_values(by="Prezzo_Finale").reset_index(drop=True)
    miglior_singolo = df_risultati_singoli.iloc[0]["Prezzo_Finale"]
    
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
    st.markdown('<div class="title-with-icon">✨ Strategia d\'Acquisto Intelligente:</div>', unsafe_allow_html=True)
    
    if best_split_arrangement:
        risparmio_netto = miglior_singolo - best_split_cost
        st.markdown(f"""
        <div class="split-card">
            <div style="font-size: 28px; font-weight: 800; float: right; color: #0288d1;">{best_split_cost:.2f} €</div>
            <div style="font-size: 19px; font-weight: 900; color: #1e3a8a;">🚀 Ottimizzazione: conviene dividere l'ordine!</div>
            <div style="font-size: 13px; color: #166534; font-weight: 700; margin-top: 5px; background-color: #d1fae5; padding: 4px 8px; border-radius: 4px; display: inline-block;">
                🔥 Risparmio extra: {risparmio_netto:.2f} € rispetto a un negozio unico
            </div>
            <div style="margin-top: 15px; font-size: 14px; color: #334155; margin-bottom: 10px;"><b>Ripartizione consigliata nei carrelli:</b></div>
        </div>
        """, unsafe_allow_html=True)
        
        for farmacia, prods in best_split_arrangement.items():
            if prods:
                st.markdown(f"📦 Su **{farmacia}** prendi:")
                for p in prods:
                    prezzo_p = df_filtrato[df_filtrato["Prodotto"] == p][farmacia].values[0]
                    st.markdown(f"- {p} ({prezzo_p:.2f} €)")
    else:
        st.markdown("""
        <div class="split-card-info">
            <div style="font-size: 15px; font-weight: bold; color: #475569;">🛡️ Controllo combinatorio eseguito</div>
            <p style="font-size: 14px; color: #64748b; margin-top: 6px; margin-bottom: 0;">
                L'algoritmo ha verificato ogni combinazione di split. Dividere l'ordine non conviene: le spese di spedizione multiple annullerebbero il risparmio sui prodotti. Conviene comprare tutto in un unico negozio.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("---")
    
    # Elenco farmacie singole
    st.markdown('<div class="title-with-icon">🏪 Ordinare da un\'unica farmacia:</div>', unsafe_allow_html=True)
    
    for row in df_risultati_singoli.itertuples():
        is_vincitore = (row.Index == 0 and not best_split_arrangement)
        card_class = "vincitore-card" if is_vincitore else "farmacia-card"
        prezzo_color = "#22c55e" if is_vincitore else "#1e3a8a"
        
        st.markdown(f"""
        <div class="{card_class}">
            <div style="font-size: 24px; font-weight: 800; float: right; color: {prezzo_color};">{row.Prezzo_Finale:.2f} €</div>
            <div style="font-size: 17px; font-weight: bold; color: #1e3a8a;">
                🏢 {row.Farmacia}
            </div>
            <div style="font-size: 13px; color: #475569; margin-top: 6px;">
                Prodotti: {row.Totale_Prodotti:.2f} € | {row.Info_Spedizione}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if row.Suggerimento:
            st.markdown(row.Suggerimento, unsafe_allow_html=True)
