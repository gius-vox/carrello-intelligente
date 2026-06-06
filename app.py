import streamlit as st
import pandas as pd
import os

# 1. Impostazione della pagina nativa
st.set_page_config(
    page_title="CarrelloSnello - Il tuo carrello ottimizzato",
    page_icon="🛒",
    layout="centered"
)

# 2. Iniezione CSS globale coordinata con i colori del brand
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght=400;600;800&display=swap');

html, body, [data-testid="stMarkdownContainer"] p {
    font-family: 'Outfit', 'Helvetica Neue', Arial, sans-serif !important;
}
/* Card standard */
.farmacia-card {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    padding: 18px 20px !important;
    border-radius: 14px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
}
/* Card del negozio singolo più conveniente */
.vincitore-card {
    background-color: #fff5f5 !important;
    border: 2px solid #b91c1c !important;
    border-left: 6px solid #b91c1c !important;
    padding: 18px 20px !important;
    border-radius: 14px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 10px 15px -3px rgba(185, 28, 28, 0.08) !important;
}
/* Card della strategia split (ordine diviso) */
.split-card {
    background-color: #f0f9ff !important;
    border: 2px solid #00a8cc !important;
    padding: 20px !important;
    border-radius: 14px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 10px 15px -3px rgba(0, 168, 204, 0.1) !important;
}
.title-with-icon {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #b91c1c;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 15px;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# 3. Gestione Intestazione: PRIMA IL LOGO E POI IL TITOLO sempre visibili
nomi_possibili_logo = ["logo carrellosnello.png", "Logo carrellosnello.png", "logo.png", "Logo.png"]
logo_trovato = None

for nome in nomi_possibili_logo:
    if os.path.exists(nome):
        logo_trovato = nome
        break

if logo_trovato:
    col_left, col_logo, col_right = st.columns([1, 2, 1])
    with col_logo:
        st.image(logo_trovato, use_container_width=True)

st.markdown("""
<div style="text-align: center; margin-top: 15px; margin-bottom: 5px;">
    <h1 style="color: #b91c1c; font-family: 'Outfit', sans-serif; font-size: 42px; font-weight: 800; letter-spacing: 1px; margin-bottom: 0px;">
        CARRELLO<span style="color: #00a8cc;">SNELLO</span>
    </h1>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 25px;">
    <p style="color: #475569; font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 500; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px; margin-bottom: 20px;">
        L'algoritmo intelligente per la tua spesa online
    </p>
</div>
""", unsafe_allow_html=True)

st.write("---")

# 4. Configurazione delle regole delle farmacie supportate
farmacie_info = {
    "Farmacia Igea": {"spedizione_fissa": 4.90, "soglia_gratis": 49.00},
    "Farmacia Loreto": {"spedizione_fissa": 3.90, "soglia_gratis": 39.90},
    "Farmacia Raven": {"spedizione_fissa": 5.90, "soglia_gratis": 29.90},
    "Dr. Max": {"spedizione_fissa": 4.50, "soglia_gratis": 59.90}
}

# 5. Caricamento database prodotti
csv_path = "prodotti.csv"
if os.path.exists(csv_path):
    df_prezzi = pd.read_csv(csv_path)
else:
    st.error("Errore: File 'prodotti.csv' non trovato.")
    st.stop()

nomi_farmacie = [col for col in df_prezzi.columns if col in farmacie_info]

if "carrello_spesa" not in st.session_state:
    st.session_state.carrello_spesa = []

# --- RICERCA PRODOTTO ---
st.markdown("""<div class="title-with-icon">🔍 Cerca un prodotto nel database:</div>""", unsafe_allow_html=True)

lista_prodotti = sorted(df_prezzi["Prodotto"].unique().tolist())
cerca_testo = st.selectbox(
    "Seleziona un farmaco da aggiungere:",
    options=[""] + lista_prodotti,
    index=0
)

if cerca_testo != "":
    df_trovati = df_prezzi[df_prezzi["Prodotto"] == cerca_testo]
    if not df_trovati.empty:
        prod = df_trovati.iloc[0]["Prodotto"]
        if prod not in st.session_state.carrello_spesa:
            st.session_state.carrello_spesa.append(prod)
            st.rerun()

# --- IL TUO CARRELLO ---
st.markdown("""<div class="title-with-icon">🛒 Il tuo carrello attuale:</div>""", unsafe_allow_html=True)

prodotti_selezionati = st.multiselect(
    "Prodotti inseriti nel carrello:",
    options=df_prezzi["Prodotto"].tolist(),
    default=st.session_state.carrello_spesa
)
st.session_state.carrello_spesa = prodotti_selezionati

# --- CALCOLO CONVENIENZA OTTIMIZZATO ---
if prodotti_selezionati:
    df_filtrato = df_prezzi[df_prezzi["Prodotto"].isin(prodotti_selezionati)]
    
    # A. Calcolo dei risultati per i negozi singoli
    risultati_singoli = []
    for nome_farmacia in nomi_farmacie:
        regole = farmacie_info[nome_farmacia]
        totale_prodotti = float(df_filtrato[nome_farmacia].sum())
        costo_spedizione = 0.0 if totale_prodotti >= regole["soglia_gratis"] else regole["spedizione_fissa"]
        totale_complessivo = totale_prodotti + costo_spedizione
        
        if costo_spedizione == 0.0:
            info_sped = "<span style='color: #16a34a; font-weight: bold;'>Spedizione GRATIS</span>"
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
    miglior_negozio_singolo = df_risultati_singoli.iloc[0]["Prezzo_Finale"]

    # B. Calcolo Ottimizzato dello Split Sicuro (Utilizza .iterrows() per mantenere intatti i nomi delle colonne)
    carrelli_split = {f: [] for f in nomi_farmacie}
    
    for _, row in df_filtrato.iterrows():
        # Creiamo il dizionario estraendo i valori direttamente dalle chiavi stringa del dizionario della riga
        prezzi_prodotto = {f: float(row[f]) for f in nomi_farmacie if f in row and pd.notna(row[f])}
        
        if prezzi_prodotto:
            miglior_farmacia_prodotto = min(prezzi_prodotto, key=prezzi_prodotto.get)
            carrelli_split[miglior_farmacia_prodotto].append(row["Prodotto"])

    costo_totale_split = 0.0
    dettagli_assegnazione = {}
    
    for farm, prods_in_farm in carrelli_split.items():
        if prods_in_farm:
            sotto_df = df_filtrato[df_filtrato["Prodotto"].isin(prods_in_farm)]
            prezzo_prodotti = float(sotto_df[farm].sum())
            regole = farmacie_info[farm]
            spedizione = 0.0 if prezzo_prodotti >= regole["soglia_gratis"] else regole["spedizione_fissa"]
            costo_totale_split += (prezzo_prodotti + spedizione)
            dettagli_assegnazione[farm] = {
                "prodotti": prods_in_farm,
                "prezzo_prodotti": prezzo_prodotti,
                "spedizione": spedizione
            }

    st.write("---")
    st.markdown("""<div class="title-with-icon">🏪 Risultati del confronto delle Farmacie:</div>""", unsafe_allow_html=True)
    
    # Mostriamo lo split solo se genera un risparmio effettivo rispetto al negozio singolo
    if costo_totale_split < miglior_negozio_singolo - 0.05:
        risparmio_generato = miglior_negozio_singolo - costo_totale_split
        st.markdown(f"""
        <div class="split-card">
            <div style="font-size: 24px; font-weight: 800; float: right; color: #00a8cc;">{costo_totale_split:.2f} €</div>
            <div style="font-size: 18px; font-weight: bold; color: #0c4a6e;">
                💡 Strategia Split Consigliata!
            </div>
            <div style="font-size: 14px; color: #0284c7; font-weight: 600; margin-top: 2px; margin-bottom: 12px;">
                Dividendo l'ordine risparmi ancora {risparmio_generato:.2f} € rispetto al negozio singolo più economico!
            </div>
            <div style="font-size: 13px; color: #334155;">
        """, unsafe_allow_html=True)
        
        for f_nome, dati in dettagli_assegnazione.items():
            elenco_p = ", ".join([f"<b>{p}</b>" for p in dati["prodotti"]])
            info_s = "Spedizione Gratis" if dati["spedizione"] == 0.0 else f"Spedizione {dati['spedizione']:.2f}€"
            st.markdown(f"• Compra su **{f_nome}** ({info_s}): {elenco_p} → *Prodotti: {dati['prezzo_prodotti']:.2f}€*", unsafe_allow_html=True)
            
        st.markdown("</div></div>", unsafe_allow_html=True)

    # Elenco classico dei negozi singoli ordinati dal più conveniente
    for row in df_risultati_singoli.itertuples():
        card_class = "vincitore-card" if row.Index == 0 else "farmacia-card"
        prezzo_color = "#b91c1c" if row.Index == 0 else "#1e293b"
        prefisso = "🏆 Più conveniente (ordine unico): " if row.Index == 0 else ""
        
        st.markdown(f"""
        <div class="{card_class}">
            <div style="font-size: 24px; font-weight: 800; float: right; color: {prezzo_color};">{row.Prezzo_Finale:.2f} €</div>
            <div style="font-size: 17px; font-weight: bold; color: #0f172a;">
                {prefisso}{row.Farmacia}
            </div>
            <div style="font-size: 13px; color: #475569; margin-top: 6px;">
                Prodotti: {row.Totale_Prodotti:.2f} € | {row.Info_Spedizione}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if row.Suggerimento:
            st.markdown(row.Suggerimento, unsafe_allow_html=True)
else:
    st.info("Il carrello è vuoto. Cerca e seleziona un farmaco in alto per vedere il confronto dei prezzi in tempo reale.")
