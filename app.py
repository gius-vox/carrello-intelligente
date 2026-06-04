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
    margin-bottom: 15px;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# 3. LOGO VETTORIALE IDENTICO AL MOCKUP (image_5b208f.png)
st.components.v1.html("""
<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 5px;">
<svg width="220" height="120" viewBox="0 0 220 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="98" cy="95" rx="5" ry="8" fill="#1E3A8A" transform="rotate(-5 98 95)"/>
  <ellipse cx="136" cy="95" rx="5" ry="8" fill="#1E3A8A" transform="rotate(-5 136 95)"/>
  
  <path d="M86 85H144" stroke="#1E3A8A" stroke-width="5" stroke-linecap="round"/>
  <path d="M89 85L95 44M139 85L145 52" stroke="#1E3A8A" stroke-width="4.5" stroke-linecap="round"/>
  
  <path d="M144 48H152L154 39" stroke="#1E3A8A" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

  <path d="M84 41H141L137 47C146 44.5 158.5 40 171.5 30C161 38.5 154.5 43 162.5 44.5C175 46.5 186.5 41.5 192.5 37C179 49.5 166.5 50.5 157.5 51.5C170 55 180 54 184.5 51.5C170 61.5 154 59.5 141.5 59.5L131 73H93L84 41Z" fill="#0288d1" stroke="#0288d1" stroke-width="0.5" stroke-linejoin="round"/>
  
  <path d="M139 48.5C150.5 48.5 161.5 45 168.5 40.5" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M141 54.5C151.5 54.5 159.5 52 165 48.5" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>

  <path d="M116 49.5C113.5 47.5 109.5 47.5 107.5 50C104.5 53.5 104.5 59 107.5 62.5C109.5 65 113.5 65 116 63" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
</svg>
</div>
""", height=125)

# 4. Intestazione Brand con Doppio Colore Ripristinato (Blu Notte e Azzurro)
st.markdown("""
<div style="text-align: center; margin-bottom: 25px;">
    <h1 style="color: #1e3a8a; font-family: 'Outfit', sans-serif; font-size: 40px; font-weight: 800; letter-spacing: 1px; margin-bottom: 0px;">
        CARRELLO<span style="color: #0288d1;">SNELLO</span>
    </h1>
    <p style="color: #475569; font-family: 'Outfit', sans-serif; font-size: 14px; font-weight: 500; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px; margin-bottom: 20px;">
        L'algoritmo intelligente per la tua spesa online
    </p>
</div>
""", unsafe_allow_html=True)

st.write("---")

# 5. Caricamento Sicuro del Database CSV
csv_path = "prodotti.csv"
if os.path.exists(csv_path):
    df_prezzi = pd.read_csv(csv_path)
else:
    st.error("Errore critico: File 'prodotti.csv' non trovato nel repository.")
    st.stop()

# Estrazione dinamica delle colonne per bypassare i KeyError delle farmacie
nomi_farmacie = [col for col in df_prezzi.columns if col not in ["Prodotto", "Immagine"]]

regole_config = {
    "Farmacia Igea": {"spedizione_fissa": 4.90, "soglia_gratis": 49.00},
    "Farmacia Loreto": {"spedizione_fissa": 3.90, "soglia_gratis": 39.90},
    "Farmacia Raven": {"spedizione_fissa": 5.90, "soglia_gratis": 29.90},
    "Dr. Max": {"spedizione_fissa": 4.50, "soglia_gratis": 59.90}
}

# Associazione intelligente per evitare disallineamenti di stringa tra dizionario e CSV
farmacie_info = {}
for col in nomi_farmacie:
    match_trovato = None
    for k, v in regole_config.items():
        if k.lower() in col.lower() or col.lower() in k.lower():
            match_trovato = v
            break
    if match_trovato:
        farmacie_info[col] = match_trovato
    else:
        farmacie_info[col] = {"spedizione_fissa": 4.50, "soglia_gratis": 49.00}

# Stato iniziale della spesa
if "carrello_spesa" not in st.session_state:
    st.session_state.carrello_spesa = [
        "Sustenium Plus Energizzante 22 bustine",
        "La Roche-Posay Anthelios XL 50+",
        "Tachipirina 1000mg Orosolubile 12 cpr"
    ]

# --- SEZIONE: RICERCA PRODOTTO ---
st.markdown("""<div class="title-with-icon">🔍 Cerca un prodotto nel database:</div>""", unsafe_allow_html=True)

lista_prodotti = sorted(df_prezzi["Prodotto"].unique().tolist())
cerca_testo = st.selectbox(
    "Digita o seleziona cosa stai cercando...",
    options=[""] + lista_prodotti,
    index=0,
    placeholder="Scrivi qui il nome del farmaco (es. Tachipirina...)"
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
        st.warning("Nessun prodotto trovato. Prova con parole chiave differenti.")

st.write("---")

# --- RIEPILOGO DEL CARRELLO ---
st.markdown("""<div class="title-with-icon">🛒 Il tuo carrello attuale:</div>""", unsafe_allow_html=True)

prodotti_selezionati = st.multiselect(
    "Puoi rimuovere gli elementi cliccando sulla 'x':",
    options=df_prezzi["Prodotto"].tolist(),
    default=st.session_state.carrello_spesa
)
st.session_state.carrello_spesa = prodotti_selezionati

# --- CORE ALGORITMO DI SPLIT ---
if prodotti_selezionati:
    df_filtrato = df_prezzi[df_prezzi["Prodotto"].isin(prodotti_selezionati)]
    
    risultati_singoli = []
    for nome_farmacia in nomi_farmacie:
        regole = farmacie_info[nome_farmacia]
        totale_prodotti = float(df_filtrato[nome_farmacia].sum())
        costo_spedizione = 0.0 if totale_prodotti >= regole["soglia_gratis"] else regole["spedizione_fissa"]
        totale_complessivo = totale_prodotti + costo_spedizione
        
        info_sped = "<span style='color: #22c55e; font-weight: bold;'>Spedizione GRATIS</span>" if costo_spedizione == 0.0 else f"Spedizione: {costo_spedizione:.2f}€"
        mancante = regole["soglia_gratis"] - totale_prodotti
        suggerimento = f"<div style='background-color: #fef08a; border-left: 4px solid #facc15; padding: 10px; font-size:13px; border-radius:4px; margin-top:8px;'>💡 Aggiungi <b>{mancante:.2f}€</b> per azzerare la spedizione!</div>" if costo_spedizione > 0.0 else ""
        
        risultati_singoli.append({
            "Farmacia": nome_farmacia, "Totale_Prodotti": totale_prodotti,
            "Info_Spedizione": info_sped, "Suggerimento": suggerimento, "Prezzo_Finale": totale_complessivo
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
    st.markdown("""<div class="title-with-icon">✨ Strategia d'Acquisto Intelligente:</div>""", unsafe_allow_html=True)
    
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
        """, unsafe_allow_html=True)
        
        for farmacia, prods in best_split_arrangement.items():
            if prods:
                st.markdown(f"📦 Su **{farmacia}** prendi:")
                for p in prods:
                    prezzo_p = df_filtrato[df_filtrato["Prodotto"] == p][farmacia].values[0]
                    st.markdown(f"- {p} ({prezzo_p:.2
