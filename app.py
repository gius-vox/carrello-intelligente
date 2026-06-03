import streamlit as st
import pandas as pd

# 1. Impostazione della pagina nativa
st.set_page_config(
    page_title="FiutaCarrello - Il fiuto intelligente per la tua spesa", 
    page_icon="🛒", 
    layout="centered"
)

# 2. Iniezione CSS globale per bloccare layout, loghi e card
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
    
    /* Contenitore logo centrato fisso */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        margin-bottom: 10px;
        width: 100%;
    }

    /* Immagini dei prodotti quadrate e pulite */
    .prod-img {
        max-width: 55px;
        max-height: 55px;
        object-fit: contain;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Logo Definitivo (La F Dinamica Tech) inserito con st.components per massima stabilità
st.components.v1.html("""
<div style="display: flex; justify-content: center; align-items: center;">
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
st.html("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h1 style="color: #1e3a8a; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 44px; font-weight:
