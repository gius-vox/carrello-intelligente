import streamlit as st
import pandas as pd

# 1. Impostazione della pagina nativa
st.set_page_config(
    page_title="FiutaCarrello - Il fiuto intelligente per la tua spesa", 
    page_icon="🛒", 
    layout="centered"
)

# 2. Iniezione CSS globale corretta e potenziata
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
    /* Contenitore per centrare i loghi SVG */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# PANNELLO DI SCELTA LOGO (Temporaneo, per farti decidere visivamente)
# ------------------------------------------------------------------
st.sidebar.header("🎨 Laboratorio Creativo Logo")
opzione_logo = st.sidebar.radio(
    "Scegli quale concetto visualizzare in cima:",
    ("Opzione 1: Il Cane-Carrello (Geometrico)", 
     "Opzione 2: Il Segugio Detective (Iconico)", 
     "Opzione 3: La F Dinamica (Tech-Minimal)",
     "Nessuno, lascia solo il testo pulito")
)
st.sidebar.info("💡 Guarda come cambia la cima della pagina e scegli quello che ti trasmette più fiducia e professionalità!")

# Definizione dei 3 loghi in SVG grafico puro
logo_1_svg = """
<div class="logo-container">
<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- Corpo Carrello/Cane -->
    <path d="M25 40H75V55H35L30 40" stroke="#1e3a8a" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M32 45H70" stroke="#1e3a8a" stroke-width="2"/>
    <path d="M34 50H65" stroke="#1e3a8a" stroke-width="2"/>
    <!-- Collo e Testa da segugio integrata davanti -->
    <path d="M75 40L82 28H92L90 38L82 42" fill="#0288d1" stroke="#1e3a8a" stroke-width="3" stroke-linejoin="round"/>
    <!-- Orecchio penzolante -->
    <path d="M80 28C78 34 82 38 82 38" stroke="#1e3a8a" stroke-width="3" stroke-linecap="round"/>
    <!-- Coda dinamica dietro -->
    <path d="M25 40C20 35 18 25 22 22" stroke="#0288d1" stroke-width="4" stroke-linecap="round"/>
    <!-- Ruote / Zampe -->
    <circle cx="38" cy="68" r="7" stroke="#1e3a8a" stroke-width="3" fill="#ffffff"/>
    <circle cx="38" cy="68" r="2" fill="#1e3a8a"/>
    <circle cx="68" cy="68" r="7" stroke="#1e3a8a" stroke-width="3" fill="#ffffff"/>
    <circle cx="68" cy="68" r="2" fill="#1e3a8a"/>
</svg>
</div>
"""

logo_2_svg = """
<div class="logo-container">
<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- Faccia Cane Stilizzata -->
    <path d="M25 65C25 45 40 35 55 35H75V55C75 62 65 68 55 68H45" stroke="#1e3a8a" stroke-width="4" stroke-linecap="round" fill="#ffffff"/>
    <!-- Orecchia Lunga Cadente (Tratto distintivo del fiuto) -->
    <path d="M38 38C28 42 26 58 32 68C35 72 40 68 38 55" fill="#0288d1" stroke="#1e3a8a" stroke-width="3"/>
    <!-- Occhio Sveglio -->
    <circle cx="60" cy="46" r="3" fill="#1e3a8a"/>
    <!-- Cappello da Detective / Lente sopra -->
    <path d="M48 35L58 22H78L75 35H48" fill="#1e3a8a"/>
    <path d="M78 32H86" stroke="#1e3a8a" stroke-width="3" stroke-linecap="round"/>
    <!-- Tartufo/Naso Nero che fiuta -->
    <circle cx="75" cy="55" r="4.5" fill="#000000"/>
</svg>
</div>
"""

logo_3_svg = """
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
"""

# Mostra il logo selezionato dall'utente nel pannello laterale
if "Opzione 1" in opzione_logo:
    st.markdown(logo_1_svg, unsafe_allow_html=True)
elif "Opzione 2" in opzione_logo:
    st.markdown(logo_2_svg, unsafe_allow_html=True)
elif "Opzione 3" in opzione_logo:
    st.markdown(logo_3_svg, unsafe_allow_html=True)
else:
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------

# Titolo bicolore e sottotitolo coordinato
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
    st.info("Aggiungi i prodotti in alto per attivare il fiuto del sistema.")
