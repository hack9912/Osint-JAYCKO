import streamlit as st
import requests
import hashlib
import re

# =====================
# CONFIG APP
# =====================
st.set_page_config(
    page_title="OSINT FREE – Jaycko",
    layout="centered"
)

st.title("🕵️ OSINT FREE – Jaycko 🇫🇷")
st.caption("OSINT légal • Gratuit • Sources ouvertes")

st.markdown("---")

# =====================
# UTILS
# =====================
def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# ---- Password breach check (FREE)
def password_pwned_check(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    if r.status_code != 200:
        return None

    for line in r.text.splitlines():
        h, count = line.split(":")
        if h == suffix:
            return int(count)
    return 0

# ---- IP OSINT (FREE)
def ip_lookup(ip):
    r = requests.get(f"http://ip-api.com/json/{ip}")
    return r.json() if r.status_code == 200 else {}

# ---- Gravatar check (FREE)
def gravatar_check(email):
    email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
    r = requests.get(url)
    return r.status_code == 200, url

# ---- GitHub username check
def github_lookup(username):
    r = requests.get(f"https://api.github.com/users/{username}")
    return r.json() if r.status_code == 200 else None

# =====================
# MENU
# =====================
module = st.selectbox(
    "Module OSINT",
    [
        "🔑 Mot de passe compromis",
        "📧 Présence email publique",
        "🌍 Analyse IP",
        "👤 Username OSINT",
        "🧬 Synthèse OSINT"
    ]
)

# =====================
# 🔑 PASSWORD CHECK
# =====================
if module == "🔑 Mot de passe compromis":
    st.subheader("Vérification mot de passe")
    st.caption("🔒 Aucun mot de passe envoyé en clair")

    password = st.text_input("Mot de passe", type="password")

    if st.button("Vérifier"):
        with st.spinner("Analyse…"):
            count = password_pwned_check(password)

        if count is None:
            st.error("Erreur de vérification")
        elif count > 0:
            st.error(f"⚠️ Compromis {count} fois dans des fuites")
        else:
            st.success("✅ Mot de passe jamais vu dans des fuites connues")

# =====================
# 📧 EMAIL PRESENCE
# =====================
elif module == "📧 Présence email publique":
    st.subheader("Présence publique de l’email")
    email = st.text_input("Email")

    if st.button("Analyser"):
        if not valid_email(email):
            st.error("Email invalide")
        else:
            found, avatar = gravatar_check(email)
            if found:
                st.success("✅ Gravatar détecté")
                st.image(avatar)
            else:
                st.warning("❌ Aucun Gravatar public")

            st.info("ℹ️ Présence basée sur sources ouvertes uniquement")

# =====================
# 🌍 IP OSINT
# =====================
elif module == "🌍 Analyse IP":
    st.subheader("Analyse IP")
    ip = st.text_input("Adresse IP")

    if st.button("Analyser"):
        with st.spinner("Analyse IP…"):
            data = ip_lookup(ip)

        if data:
            st.write("🌍 Pays :", data.get("country"))
            st.write("🏙️ Ville :", data.get("city"))
            st.write("📡 ISP :", data.get("isp"))
            st.write("🧬 ASN :", data.get("as"))
            st.write("🔐 VPN/Proxy :", data.get("proxy"))
        else:
            st.error("Impossible d’analyser l’IP")

# =====================
# 👤 USERNAME OSINT
# =====================
elif module == "👤 Username OSINT":
    st.subheader("Recherche par pseudo")
    username = st.text_input("Pseudo")

    if st.button("Rechercher"):
        gh = github_lookup(username)
        if gh:
            st.success("Profil GitHub trouvé")
            st.write("Nom :", gh.get("name"))
            st.write("Repos publics :", gh.get("public_repos"))
            st.write("Bio :", gh.get("bio"))
            st.write("URL :", gh.get("html_url"))
        else:
            st.warning("Aucun GitHub public trouvé")

# =====================
# 🧬 SYNTHÈSE
# =====================
elif module == "🧬 Synthèse OSINT":
    st.markdown("""
### Capacités FREE
✔️ Mot de passe compromis  
✔️ Présence email publique (Gravatar)  
✔️ IP OSINT  
✔️ Username GitHub  

### Limites
❌ Pas de détail des fuites email  
❌ Pas d’API payante  

👉 100 % gratuit • 100 % légal
""")

st.markdown("---")
st.caption("OSINT responsable • FREE Edition • Jaycko 🇫🇷")
