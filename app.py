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
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght=400;600;800&display=swap');

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

# 3. LOGO VETTORIALE RACCORDATO (image_5b208f.png)
st.components.v1.html("""
<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 5px;">
<svg width="200" height="130" viewBox="0 0 200 130" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="88" cy="102" rx="5.5" ry="9" fill="#1E3A8A" transform="rotate(-15 88 102)"/>
  <ellipse cx="128" cy="102" rx="5.5" ry="9" fill="#1E3A8A" transform="rotate(-15 128 102)"/>
  
  <path d="M74 91H138" stroke="#1E3A8A" stroke-width="5" stroke-linecap="round"/>
  <path d="M80 91L85 53M123 91L131 59" stroke="#1E3A8A" stroke-width="4.5" stroke-linecap="round"/>
  
  <path d="M130 54H139L142 43" stroke="#1E3A8A" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

  <path d="M73 44H131L126 50.5C136 48.5 149 43.5 163 33C152 42 145 46.5 153.5 48C167 50 179 45 185 40C171 53 158 54 148.5 55C161.5 59 172 58 176.5 55.5C161.5 66 145 64 132 64L121 78H83L73 44Z" fill="#0288d1"/>
  
  <path d="M128 52.5C140 52.5 151.5 49 159 44" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M130 58.5C141 58.5 149.5 56 155 52.5" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>

  <path d="M106 52.5C103.5 50.5 99.5 50.5 97.5 53C94.5 56.5 94.5 62 97.5 65.5C99.5 68 103.5 68 106 66" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
</svg>
</div>
""", height=135)

# 4. Intestazione Brand con Doppio Colore Ripristinato (Blu Notte e Azzurro)
st.markdown("""
<div style="text-align: center; margin-bottom: 25px;">
    <h1 style="color: #1e3a8a; font-family: 'Outfit', sans-serif; font-size: 38px; font-weight: 800; letter-spacing: 1px; margin-bottom: 0px;">
        CARRELLO<span style="color: #0288d1;">SNELLO</span>
    </h1>
    <p style="color: #475569; font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 500; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px; margin-bottom: 20px;">
        L'algoritmo intelligente per la tua spesa online
    </p>
</div>
""", unsafe_allow_html=True)

st.write("---")

# 5. Caricamento database CSV
csv_path = "prodotti.csv"
if os.path.exists(csv_path):
    df_prezzi = pd.read_csv(csv_path)
else:
    st.error("Errore critico: File 'prodotti.csv' non trovato.")
    st.stop()

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
st.markdown("""<div class="title-with-icon">🔍 Cerca un prodotto nel database:</div>""", unsafe_allow_html=True)

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

# ---
