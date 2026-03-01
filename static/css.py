import streamlit as st

def load_css():
    st.markdown("""
    <style>
        /* Importation d'une police */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Application de la police à toute l'application */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* En-têtes (h1, h2, h3...) */
        h1, h2, h3, h4, h5, h6 {
            color: #000000 !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        /* Style des boutons */
        div.stButton > button {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #000000 !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1.5rem !important;
            transition: all 0.2s ease-in-out !important;
        }
        
        div.stButton > button:hover {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #000000 !important;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1) !important;
        }

        /* Customisation de la Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #fcfcfc !important;
            border-right: 1px solid #eeeeee !important;
        }

        /* Les cartes (boîtes de sélections, champs de texte) */
        div[data-baseweb="select"] > div {
            border: 1px solid #e0e0e0 !important;
            border-radius: 6px !important;
            background-color: #ffffff !important;
        }

        div[data-baseweb="select"] > div:hover {
            border-color: #000000 !important;
        }
        
    </style>
    """, unsafe_allow_html=True)
