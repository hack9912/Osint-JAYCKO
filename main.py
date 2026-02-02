import streamlit as st

st.set_page_config(page_title="OSINT Jaycko", layout="centered")

st.title("🔍 Outil OSINT – Jaycko 🇫🇷")

key = st.text_input("Clé d'accès", type="password")

if key != "JAYCKO2025":
    st.warning("Entre la clé pour continuer")
    st.stop()

st.success("Accès autorisé")

st.subheader("Recherche d'identité (démo)")
email = st.text_input("Email")
pseudo = st.text_input("Pseudo")

if st.button("Rechercher"):
    st.write("Résultats simulés :")
    st.write("- Aucun leak critique")
    st.write("- Profil GitHub trouvé")
