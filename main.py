import streamlit as st
import requests

st.set_page_config(page_title="OSINT Jaycko", layout="centered")

st.title("🔍 Outil OSINT – Jaycko 🇫🇷")

# 🔐 Sécurité
key = st.text_input("Clé d'accès", type="password")
if key != "JAYCKO2025":
    st.warning("Clé incorrecte")
    st.stop()

st.success("Accès autorisé")

st.markdown("---")

# 📌 Menu
module = st.selectbox(
    "Choisis un module",
    [
        "Recherche identité",
        "Analyse email",
        "Analyse IP",
        "Profils sociaux",
    ]
)

# 🔎 Recherche identité
if module == "Recherche identité":
    st.subheader("Recherche d'identité")
    email = st.text_input("Email")
    pseudo = st.text_input("Pseudo")

    if st.button("Lancer la recherche"):
        st.info("Résultats OSINT")
        if email:
            st.write(f"- Email analysé : {email}")
            st.write("- Aucun leak critique détecté (démo)")
        if pseudo:
            st.write(f"- Pseudo analysé : {pseudo}")
            st.write("- Profil GitHub possible")
            st.write("- Profil Twitter possible")

# 📧 Analyse email
elif module == "Analyse email":
    st.subheader("Analyse Email")
    email = st.text_input("Email à analyser")

    if st.button("Analyser"):
        st.write(f"Analyse de : {email}")
        st.write("- Format valide")
        st.write("- Domaine existant")
        st.write("- Vérification leaks : OK (démo)")

# 🌍 Analyse IP
elif module == "Analyse IP":
    st.subheader("Analyse IP")
    ip = st.text_input("Adresse IP")

    if st.button("Analyser IP"):
        st.write(f"IP : {ip}")
        st.write("- Pays : France (exemple)")
        st.write("- Fournisseur : OVH")
        st.write("- VPN détecté : Non")

# 👤 Profils sociaux
elif module == "Profils sociaux":
    st.subheader("Recherche de profils sociaux")
    pseudo = st.text_input("Pseudo")

    if st.button("Rechercher profils"):
        st.write(f"Résultats pour : {pseudo}")
        st.write("- GitHub : trouvé")
        st.write("- Twitter : possible")
        st.write("- Instagram : inconnu")

st.markdown("---")
st.caption("Créé par Jaycko 🇫🇷")
